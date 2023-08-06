#    This file is part of Cruscoplanets.
#
#    Cruscoplanets is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Cruscoplanets is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Cruscoplanets.  If not, see <http://www.gnu.org/licenses/>.

import time, timezonefinder
from cruscoplanets import angles
from cruscoplanets import utils
import sqlite3
import os
from cruscoplanets import utils


class LocationConfiguration(metaclass=utils.Singleton):
	"""Handles all the settings regarding locations. This class is a Singleton, therefore any call will always return the same instance.
	The instance of this class is programmed to behave like a dictionary where keys are the settings and the items their values. The settings can be got, set and listed with the same methods of
	*dict* objects. Moreover, they are also accessible through the normal access operator '.'.
	The values of the settings are provided as *float* objects if numeric, strings if not.
	"""

	LOCATION_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "location.txt")
	
	def __init__(self):
		config_tuple = utils.parseBanalConfig(self.__class__.LOCATION_CONFIG_PATH)
		for pair in config_tuple:
			if pair[1] != None:
				self.__dict__[pair[0]] = int(pair[1])
			else:
				self.__dict__[pair[0]] = pair[1]
		
	def __getitem__(self, key):
		return self.__dict__[key]
	
	def __setitem__(self, key, value):
		self.__dict__[key] == value

	def saveChanges(self):
		"""Saves the changes made in configuration in the config files, in order to keep them in future accesses"""
		config_tuple = tuple(sorted(self.__dict__.items(), key = lambda pair: pair[0]))#sorts the elements of self.__dict__ by the alphabetical order of the keys and creates a tuple with them
		new_config = utils.buildBanalConfig(config_tuple)
		with open(self.__class__.LOCATION_CONFIG_PATH, 'w') as config_file:
			config_file.write(new_config)


class LocationError(Exception):

	def __init__(self, message):
		self.message = message
	
	def __str__(self):
		return self.message


class MissingDefaultLocationError(LocationError):

	def __init__(self):
		super().__init__("Default location has not yet been set.")


class Location:
	"""Represents a location and provides geodetic data.
	
	Args:
		location_name (str): the name of the location
		latitude (float): the latitude of the location
		longitude (float): the longitude of the location
		timezone (str): the timezone of the location. If None, the timezone will be inferred by the location's coordinates.
	
	Attributes:
		name (str): the name of the location
		latitude (float): the latitude of the location
		longitude (float): the longitude of the location
		timezone (str): the timezone of the location. If None, the timezone will be inferred by the location's coordinates.
	"""
	timezone_finder = timezonefinder.TimezoneFinder()
	GEONAMES_DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases","geonames.sql")
	LOCATIONS_LIST = None
	
	
	def __init__(self, location_name, latitude: float, longitude: float, timezone: str = None):
		self.name = location_name
		self.latitude = angles.Angle(latitude)
		self.longitude = angles.Angle(longitude)
		if timezone == None:
			self.__timezone = self.__class__.timezone_finder.timezone_at(lat=self.latitude.decvalue, lng=self.longitude.decvalue)
		else:
			self.__timezone = timezone
	
	@property
	def timezone(self):
		return self.__timezone
		
	@classmethod
	def fromCoordinates(cls, lat: float, lon: float):
		"""Returns an anonym location with given coordinates
		
		Args:
			lat (float): the latitude of the location
			lon (float): the longitude of the location
		"""
		return cls(None, lat, lon)
		
	@classmethod
	def listLocations(cls):
		"""Returns a tuple of tuples containing basic information about all the locations in the database. Each tuple contains the name of a location, the Alpha-2 code of its country and its 
		database id. This function can be useful when creating selection menus for locations. Please notice that a location can have multiple names, and therefore more tuples in this collection can 
		have the same id.
		"""
		
		#the first time this function is called, its returned value is stored in the class attribute LOCATIONS_LIST. In this way, a second call will prevent from repeating the database reading.
		if cls.LOCATIONS_LIST == None:
			with sqlite3.connect(cls.GEONAMES_DATABASE_PATH) as connection:
				connection.row_factory = sqlite3.Row
				cursor = connection.cursor()
				cursor.execute("SELECT id, name, asciiname, alternatenames, country FROM geonames")
				retcollection = []
				
				for row in cursor.fetchall():
					allnames = [row['name'], row['asciiname']]
					for altname in row['alternatenames'].split(','):
						allnames.append(altname)
					allnames = tuple(set(allnames))#to remove duplicates
					for name in allnames:				
						retcollection.append((name, row['country'], row['id']))
				cls.LOCATIONS_LIST = tuple(retcollection)
		return cls.LOCATIONS_LIST
		
	@classmethod
	def searchLocationFromGeonamesDatabase(cls, location_id: int):
		"""Returns an instance of Location getting its data from the geonames database, passing the location_id as argument. If location_id is equal to -1, it will return the default location.
		
		Args:
			location_id (id): the id of the location in the Geonames database.
		
		Returns:
			thelocation (:class:`cruscoplanets.location.Location`): the location looked for.
		"""
		
		if location_id == -1:
			return cls.default()
			
		with sqlite3.connect(cls.GEONAMES_DATABASE_PATH) as connection:
			connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM geonames WHERE id = ?", (location_id,))
			results = cursor.fetchone()
			if results == None:
				raise LocationError("Invalid location id")
			results = dict(results)
			return cls(results['name'], results['latitude'], results['longitude'], results['timezone'])
		
	
	@classmethod
	def fromCityName(cls, locname: str):
		"""Searches a location in the Geonames database by its name and returns a list of possible values.
		
			Args:
				locname (str): the name of the location
				
			Returns:
				values (list): a list of dictionaries representing the localities fetched from the geonames databases
		"""
		with sqlite3.connect(cls.GEONAMES_DATABASE_PATH) as connection:
			connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			cursor.execute(
				"SELECT * FROM geonames WHERE name = ? OR asciiname = ? or alternatenames LIKE ? or alternatenames LIKE ? or alternatenames LIKE ?", 
				(locname, locname, "%%,%s,%%"%locname, "%s,%%"%locname, "%%,%s"%locname)
			)
			results = cursor.fetchall()
			return [dict(row) for row in results]
		
	@classmethod
	def default(cls):
		"""Returns default location in case no location is provided for an event"""
		config = LocationConfiguration()
		default_id = config.DEFAULT_LOCATION_ID
		if default_id == None:
			raise MissingDefaultLocationError
		return cls.searchLocationFromGeonamesDatabase(default_id)
	
	@classmethod
	def setDefault(cls, location_id):
		"""Sets a new location as default.
		
		Args:
			location_id (int): the integer id of the location (retrievable, for example, with the py:classmethod:`Location.fromCityName` class method).
		"""
		
		#here we prevent to insert -1 as integer. -1 is already the integer value for default location
		if location_id == -1:
			raise LocationError("Default location can not be set to -1")

		#here we check if the new id value actually corresponds to an id contained in the database
		try:
			newdefault = cls.searchLocationFromGeonamesDatabase(location_id)
		except LocationError:
			raise
		config = LocationConfiguration()
		config.DEFAULT_LOCATION_ID = int(location_id)
		config.saveChanges()
	
	def __repr__(self):
		return "%s, %s - %s (%s)"%(self.name, self.latitude.reprAsLatitude(), self.longitude.reprAsLongitude(), self.timezone)
