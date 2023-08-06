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

import backports.zoneinfo
import datetime
from cruscoplanets import location
import abc
from swisseph import julday
import re


class InvalidFormatError(Exception):

	def __init__(self, message):
		super().__init__()
		self.message = message
	
	def __str__(self):
		return self.message
	

class EventBuilder:
	"""
	Builder of Event instances. This class doesn't need to be initialized, since it has only a class method (*buildEvent*) and a static method (*now*).

	"""

	@classmethod
	def buildEvent(cls, dateandtimestr: str, thelocation: location.Location):
		"""Parses date and time from a string in a given format and returns an :class:`Event` instance.
		The format for date and time must is the following: [L|U]YYYY-MM-DD[-hh-mm-ss|![hh-mm-ss]]. In other words:
		
		 - it may start by a character, which is U if the time is to be considered local, L if it is to be considered UTC time (parsing is case insensitive). If omitted, time will be considered local by default
		 - date indication is formatted as YYYY-MM-DD. It must be inserted.
		 - time indication, if available, is inserted as -hh-mm-ss (hours count up to 24)
		 - in all the numeric fields, values must always be inserted with two digits
		 - if the time of the event is unknown, after the date an exclamation mark is placed; the planetary positions will be calculated by the time 12:00 UTC of the given date.
		 - it is actually possible to specify a time even in events with unknown hour, placing it in the same hh-mm-ss format after the exclamation mark; that time will be used for calculating the planetary positions, but the chart will in any case have no domification.
		
		Args:
			dateandtimestring(str): the string representing the date and time to parse.
			
		Raises:
			InvalidFormatError
		
		Returns:
			parsed_date_and_time: a tuple of int representing the year, month, day, and hour, minute, second if time is known.
		"""

		#checking if the string is simply 'now':
		mystr = dateandtimestr.lower()
		if mystr == 'now':
			return cls.now(thelocation)

		if mystr[0] != 'u' and mystr[-1] == '!':
			raise InvalidFormatError("It is a nonsense to specify a local time if you don't insert time!")

		#parsing the regular expression:
		regex = re.compile('^(?P<timemod>[ul])?(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)(?P<unknown_flag>(?P<known_time>-(?!$))?(?P<unknown_time>(?(known_time)|!)))(?P<time>(?P<hour>\d\d)-(?P<minute>\d\d)-(?P<second>\d\d))?$')
		match_object = regex.fullmatch(mystr)
		if match_object == None:
			raise InvalidFormatError("String '%s' has not a valid format"%dateandtimestr)

		#getting year, month and day values as int
		year, month, day = int(match_object.group('year')), int(match_object.group('month')), int(match_object.group('day'))
		if month > 12 or month < 1:
			raise InvalidFormatError("Months must be integer between 1 and 12")
		
		#getting a boolean value True if time is local
		is_time_local = True
		if match_object.group('timemod') == 'u':
			is_time_local = False
		
		#getting a boolean value True if time is known:
		is_time_known = True
		if match_object.group('unknown_flag') == '!':
			is_time_known = False
		
		#parsing time:
		hour, minute, second = None, None, None
		if match_object.group('hour') != None:
			hour = int(match_object.group('hour'))
		if match_object.group('minute') != None:
			minute = int(match_object.group('minute'))
		if match_object.group('second') != None:
			second = int(match_object.group('second'))
		
		event_args = (year, month, day, hour, minute, second, thelocation)
		
		if is_time_known:
			if is_time_local:
				event = TimeZonedEvent(*event_args)
			else:
				event = UTCEvent(*event_args)
		else:
			if is_time_local:
				event = UnknownTimeEvent.fromLocalTime(*event_args)
			else:
				event = UnknownTimeEvent(*event_args)
		return event
		
	@staticmethod
	def now(thelocation: location.Location = None):
		"""Returns a :class:`TimeZonedEvent` instance representing the current moment in a given location
		
		Args:
			thelocation (:class:`location.Location`): the location from which the event set to the current moment must be initialized

		Returns: 
			event (:class:`location.TimeZonedEvent`): the event representing the current moment at thelocation.
		"""
		if thelocation == None:
			thelocation = location.Location.default()
		timezone = backports.zoneinfo.ZoneInfo(thelocation.timezone)
		now = datetime.datetime.now(tz=timezone)
		return TimeZonedEvent(now.year, now.month, now.day, now.hour, now.minute, now.second, thelocation)
		

class Event(abc.ABC):
	"""Abstract class for handling date and time of events."""

	@abc.abstractproperty
	def utcdatetime(self) -> datetime.datetime:
		"""A :class:`datetime.datetime` instance of the date and time of the event in UTC time"""
		pass

	@abc.abstractproperty
	def localdatetime(self) -> datetime.datetime:
		"""A :class:`datetime.datetime` instance of the date and time of the event in local time"""
		pass
		
	@abc.abstractproperty
	def julianDay(self) -> float:
		"""The Julian Day corresponding to the date and time of the event."""
		pass
	
	@abc.abstractproperty
	def isTimeUnknown(self) -> bool:
		"""True if the time of the event is unknown, False otherwise."""
		pass
		
	@abc.abstractproperty
	def dateAndTime(self) -> str:
		"""A string representing the date and time of the event in a readable format."""
		pass


class TimeZonedEvent(Event):
	"""
	Concrete implementation of :class:`Event` employed with events defined by a local time and a given location.
	
	Args:
		year (int): year of the event's date (in Gregorian calendar)
		month (int): month of the event's date (in Gregorian calendar, from 1 to 12)
		day (int): day of the event's date (in Gregorian calendar)
		hour (int): hour of the event's time (from 0 to 24)
		minute (int): minute of the event's time
		second (int): second of the event time
		location (:class:`location.Location`): location of the event
	
	Attributes:
		location (:class:`location.Location`): location of the event
		timezone (:class:`backports.zoneinfo.ZoneInfo`): time zone of the event's time)
	"""
	def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int, location: location.Location):
		self.location = location
		self.timezone = backports.zoneinfo.ZoneInfo(self.location.timezone)
		self.__localdatetime = datetime.datetime(year, month, day, hour, minute, second, 0, self.timezone)#0 refers to microseconds
		self.__utcdatetime = self.__localdatetime.astimezone(backports.zoneinfo.ZoneInfo('GMT'))
		dec_hour = self.__utcdatetime.hour + self.__utcdatetime.minute/60 + self.__utcdatetime.second/3600
		self.__julday = julday(self.__utcdatetime.year, self.__utcdatetime.month, self.__utcdatetime.day, dec_hour)
	
	@property
	def dateAndTime(self):
		return self.localdatetime.strftime("%d/%m/%Y %X")
		
	@property
	def julianDay(self):
		return self.__julday
	
	@property	
	def utcdatetime(self):
		return self.__utcdatetime

	@property
	def localdatetime(self):
		return self.__localdatetime
	
	@property
	def isTimeUnknown(self):
		return False
		
	def __repr__(self):
		return "Location: %s. %s UTC: %s Julian Day: %f"%(self.location, self.__localdatetime.strftime("%d/%m/%Y %X"), self.__utcdatetime.strftime("%d/%m/%Y %X"), self.julianDay)


class UTCEvent(Event):
	"""Concrete implementation of Event employed with certain UTC time and certain location, and where local date time is inferred by the location's longitude.
	
	Args:
		year (int): year of the event's date (in Gregorian calendar)
		month (int): month of the event's date (in Gregorian calendar, from 1 to 12)
		day (int): day of the event's date (in Gregorian calendar)
		hour (int): hour of the event's time (from 0 to 24)
		minute (int): minute of the event's time
		second (int): second of the event time
		location (:class:`location.Location`): location of the event
	
	Attributes:
		location (:class:`location.Location`): location of the event
		timezone (:class:`backports.zoneinfo.ZoneInfo`): time zone of the event's time)
	"""

	def __init__(self, utcyear: int, utcmonth: int, utcday: int, utchour: int, utcminute: int, utcsecond: int, location: location.Location):
		timeformat = "%04d-%02d-%02dT%02d:%02d:%02d.%09d"%(utcyear, utcmonth, utcday, utchour, utcminute, utcsecond, 0)
		self.__utcdatetime = datetime.datetime(utcyear, utcmonth, utcday, utchour, utcminute, utcsecond, 0, backports.zoneinfo.ZoneInfo('GMT'))
		self.location = location
		self.timeOffset = datetime.timedelta(hours=self.location.longitude.hoursvalue)
		self.__localdatetime = self.__utcdatetime + self.timeOffset
		dec_hour = utchour + utcminute/60 + utcsecond/3600
		self.__julday = julday(utcyear, utcmonth, utcday, dec_hour)
		print(self)
	
	@property
	def dateAndTime(self):
		return self.utcdatetime.strftime("%d/%m/%Y %X") + ' (UTC)'
	
	@property
	def isTimeUnknown(self):
		return False
		
	@property
	def julianDay(self):
		return self.__julday
		
	
	@property
	def utcdatetime(self):
		return self.__utcdatetime

	@property
	def localdatetime(self):
		return self.__localdatetime
		
	def __repr__(self):
		return "Location: %s. %s UTC: %s. Longitude: %s. TimeOffset: %s Julian Day: %f"%(
			self.location, 
			self.__localdatetime.strftime("%d/%m/%Y %X"), 
			self.__utcdatetime.strftime("%d/%m/%Y %X"), 
			self.location.longitude, 
			self.timeOffset, 
			self.julianDay
		)


class UnknownTimeEvent(Event):
	"""Class for events whose time is unknown. Time can actually be set (default is noon in UTC) for calculating planetary positions, but in any case the chart printed from this event will have no domification.
	
	Args:
		year (int): year of the event's date (in Gregorian calendar)
		month (int): month of the event's date (in Gregorian calendar, from 1 to 12)
		day (int): day of the event's date (in Gregorian calendar)
		hour (int): hour of the event's time (from 0 to 24)
		minute (int): minute of the event's time
		second (int): second of the event time
		location (:class:`location.Location`): location of the event
	
	Attributes:
		location (:class:`location.Location`): location of the event
		timezone (:class:`backports.zoneinfo.ZoneInfo`): time zone of the event's time)
	"""
	DEFAULT_HOUR, DEFAULT_MINUTE, DEFAULT_SECOND = 12, 0, 0

	def __init__(self, utcyear: int, utcmonth: int, utcday: int, utchour: int, utcminute: int, utcsecond: int, location: location.Location):
		if utchour == None:
			utchour = self.__class__.DEFAULT_HOUR
		if utcminute == None:
			utcminute = self.__class__.DEFAULT_MINUTE
		if utcsecond == None:
			utcsecond = self.__class__.DEFAULT_SECOND
		self.__utcdatetime = datetime.datetime(utcyear, utcmonth, utcday, utchour, utcminute, utcsecond, 0, backports.zoneinfo.ZoneInfo('GMT'))
		self.location = location
		self.timeOffset = datetime.timedelta(hours=self.location.longitude.hoursvalue)
		self.__localdatetime = self.__utcdatetime + self.timeOffset
		dec_hour = utchour + utcminute/60 + utcsecond/3600
		self.__julday = julday(utcyear, utcmonth, utcday, dec_hour)
	
	@classmethod
	def fromLocalTime(cls, year: int, month: int, day: int, hour: int, minute: int, second: int, location: location.Location):
		if hour == None:
			hour = cls.DEFAULT_HOUR
		if minute == None:
			minute = cls.DEFAULT_MINUTE
		if second == None:
			second = cls.DEFAULT_SECOND
		timezone = backports.zoneinfo.ZoneInfo(location.timezone)
		localdatetime = datetime.datetime(year, month, day, hour, minute, second, 0, timezone)#0 refers to microseconds
		utcdatetime = localdatetime.astimezone(backports.zoneinfo.ZoneInfo('GMT'))
		new_instance = cls(utcdatetime.year, utcdatetime.month, utcdatetime.day, utcdatetime.hour, utcdatetime.minute, utcdatetime.second, location)
		new_instance.__localdatetime = localdatetime
		return new_instance
	
	@property
	def dateAndTime(self):
		return self.utcdatetime.strftime("%d/%m/%Y %X")
	
	@property
	def isTimeUnknown(self):
		return True
		
	@property
	def julianDay(self):
		return self.__julday
	
	@property
	def utcdatetime(self):
		return self.__utcdatetime

	@property
	def localdatetime(self):
		return self.__localdatetime
	
	def __repr__(self):
		return "Location: %s. %s UTC: %s. (Unknown time. Set to UTC noon). Julian Day: %f"%(
			self.location, 
			self.__localdatetime.strftime("%d/%m/%Y %X"), 
			self.__utcdatetime.strftime("%d/%m/%Y %X"), 
			self.julianDay
		)
			
		
if __name__ == '__main__':
	rome = location.Location("Rome", 41.9027835, 12.4963655)
	datetime1 = TimeZonedEvent(1992, 12, 22, 19, 15, 00, rome)
	nairobi = location.Location("Nairobi", -1.2833300, 36.8166700)
	datetime2 = UTCEvent(1993, 8, 9, 12, 00, 00, nairobi)
	nardo = location.Location("Nardò", 40.1795300, 18.0317400)
	datetime3 = UnknownTimeEvent(1322, 4, 5, nardo)
	datetime4 = EventBuilder.now()
	print()
	print(datetime1)
	print()
	print(datetime2)
	print()
	print(datetime3)
	print()
	print(datetime4)

