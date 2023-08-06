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

import swisseph as swe
from cruscoplanets import dates
from cruscoplanets import angles
import os


class House:
	"""Represents one of the twelve houses of Placidus' domification employed in Morpurgo's astrology.
	
	Args:
		house_index (int): the number of the house. While astrological houses are generally counted from one to twelve, these indexes range from 0 (first house) to 11 (twelveth house)
		position (float): the ecliptic longitude of the house border.

	Attributes:
		house_index (int): the number of the house. While astrological houses are generally counted from one to twelve, these indexes range from 0 (first house) to 11 (twelveth house)
		position (:class:`cruscoplanets.angles.Angle`): the ecliptic longitude of the house border.
	"""
	SYMBOLS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")

	def __init__(self, house_index, position: float):
		self.index = house_index
		self.position = angles.Angle(position)
		
	@property
	def symbol(self):
		return self.__class__.SYMBOLS[self.index]
		
	def __repr__(self):
		return "house %4s %s"%(self.symbol, self.position.asZodiacPoint)


class Planet:
	"""Represents a planet of the Zodiac chart. Morpurgo's astrological school recognizes twelve planets; the twelveth, Y-Aeolus, must still be individuated, whereas for the eleventh, X-Proserpine,
	seems to correspond to Eris.
	This class is thought only to build the Zodiac charts and should not be implemented directly by the user.

	Args:
		bodyInt (int): an integer from 0 to 11 representing the planet. In order: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Eris.
		lngposition (float): the ecliptic longitude of the planet that will be represented on the chart
		lngspeed (float): the ecliptic longitudinal speed of the planet. Necessary to check if the planet is retrograde.
	
	Attributes:
		bodyInt (int): an integer from 0 to 11 representing the planet. In order: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Eris.
		eclipticLongitude (:class:`cruscoplanets.angles.Angle`): the ecliptic longitude of the planet that will be represented on the chart. The pointers relative to the planet will always be placed at this angle.
		figurePosition (:class:`cruscoplanets.angles.Angle`): the position (expressed as an angle) where the planet's symbol will appear in the chart. By default it corresponds to eclipticLongitude, but it can be changed of some degrees to prevent close figures from overlapping
	"""

	SYMBOLS = "☉☽☿♀♂♃♄♅♆♇⯱"
	NAMES= ('sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'eris')

	def __init__(self, bodyInt: int, lngposition: float, lngspeed: float):
		self.bodyInt = bodyInt
		self.eclipticLongitude = angles.Angle(lngposition) #actual angular position of the planet. The pointer of the planet will always be placed at this angle.
		self.figurePosition = angles.Angle(lngposition) #angular position where the figure of the planet. It is by default equal to self.eclipticLongitude, but can be changed to prevent overlapping
		if lngspeed >= 0:
			self.isRetrograde = False
		else:
			self.isRetrograde = True
			
	@property
	def name(self):
		"""Returns the name of the planet in lowercase."""
		return self.__class__.NAMES[self.bodyInt]
	
	@property
	def symbol(self):
		"""Returns the Unicode character representing the planet."""
		return self.__class__.SYMBOLS[self.bodyInt]
		
	def __sub__(self, other) -> angles.Angle:
		"""Returns the lesser angular distance between the two planets. This method is useful in calculating planetary aspects.
		
		Args:
			other (:class:`cruscoplanets.ephemeris.Planet`): the planet from which the angular distance must be calculated
		
		Returns:
			difference (:class:`cruscoplanets.angles.Angle`): the angular distance between the two planets.
		"""
		if self.eclipticLongitude < other.eclipticLongitude:
			min_angle, max_angle = self.eclipticLongitude, other.eclipticLongitude
		else:
			max_angle, min_angle = self.eclipticLongitude, other.eclipticLongitude
		difference = max_angle - min_angle
		#now one must check if the difference obtained is the minimum angular distance between the two planets. Up to this point if one uses this method with two planets,
		#whose angles are 359° and 3°, one would obtain 356° as value. The useful value for the distance is however, 4°, that is, 360° - 356°
		if difference > angles.Angle.straight():
			difference = angles.Angle.perigon() - difference
		return difference
	
	def __repr__(self):
		retstr = "%s %s"%(self.symbol, self.eclipticLongitude.asZodiacPoint)
		if self.isRetrograde:
			retstr += " R"
		return retstr


class Ephemeris:
	"""Represents the ephemeris of Morpurgo's planets for a given event.
	
	Args:
		event (:class:`cruscoplanets.dates.Event`): the event for which the ephemeris must be calculated
		
	Attributes:
		event (:class:`cruscoplanets.dates.Event`): the event for which the ephemeris must be calculated
		sun (:class:`Planet`): the planet instance relative to the Sun
		moon (:class:`Planet`): the planet instance relative to the Moon
		mercury (:class:`Planet`): the planet instance relative to Mercury
		venus (:class:`Planet`): the planet instance relative to Venus
		mars (:class:`Planet`): the planet instance relative to Mars
		jupiter (:class:`Planet`): the planet instance relative to Jupiter
		saturn (:class:`Planet`): the planet instance relative to Saturn
		uranus (:class:`Planet`): the planet instance relative to Uranus
		neptune (:class:`Planet`): the planet instance relative to Neptune
		pluto (:class:`Planet`): the planet instance relative to Pluto
		eris (:class:`Planet`): the planet instance relative to Eris
		houses (tuple): the :class:`House` instances representing the houses of the event's domification (in Placidus' method). This attribute is set to `None` if `self.event.isTimeUnknown` is True
	"""
	SUN = swe.SUN
	MOON = swe.MOON
	MERCURY = swe.MERCURY
	VENUS = swe.VENUS
	MARS = swe.MARS
	JUPITER = swe.JUPITER
	SATURN = swe.SATURN
	URANUS = swe.URANUS
	NEPTUNE = swe.NEPTUNE
	PLUTO = swe.PLUTO
	ERIS = 10

	SWISSEPH_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyswisseph_files")

	def __init__(self, event: dates.Event):
	
		#First we add to swe.EPHE_PATH the path of the directory where Eris' files are stored.
		path_to_initialize = swe.EPHE_PATH + os.pathsep + self.__class__.SWISSEPH_FILES_DIR
		swe.set_ephe_path(path_to_initialize)
					
		self.event = event

		planet, flags = swe.calc_ut(self.event.julianDay, swe.SUN)
		self.sun = Planet(Ephemeris.SUN, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.MOON)
		self.moon = Planet(Ephemeris.MOON, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.MERCURY)
		self.mercury = Planet(Ephemeris.MERCURY, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.VENUS)
		self.venus = Planet(Ephemeris.VENUS, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.MARS)
		self.mars = Planet(Ephemeris.MARS, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.JUPITER)
		self.jupiter = Planet(Ephemeris.JUPITER, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.SATURN)
		self.saturn = Planet(Ephemeris.SATURN, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.URANUS)
		self.uranus = Planet(Ephemeris.URANUS, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.NEPTUNE)
		self.neptune = Planet(Ephemeris.NEPTUNE, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.PLUTO)
		self.pluto = Planet(Ephemeris.PLUTO, planet[0], planet[3])

		planet, flags = swe.calc_ut(self.event.julianDay, swe.AST_OFFSET + 136199)
		self.eris = Planet(Ephemeris.ERIS, planet[0], planet[3])
		
		if not self.event.isTimeUnknown:
			houses, add = swe.houses(self.event.julianDay, self.event.location.latitude.decvalue, self.event.location.longitude.decvalue, hsys=b"P")
			self.houses = tuple(House(i, houses[i]) for i in range(len(houses)))
			self.skypoints = tuple(angles.Angle(skypoint).asZodiacPoint for skypoint in add)
		else:
			self.houses, self.skypoints = None, None

	@property
	def ascendant(self):
		return self.houses[0]
		
	@property
	def mediumCoeli(self):
		return self.houses[9]

	@property
	def planets(self):
		return (self.sun, self.moon, self.mercury,self.venus, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.eris)

	@property
	def isTimeUnknown(self):
		return self.event.isTimeUnknown

	def __repr__(self):
		retstr = ""
		if not self.isTimeUnknown:
			for i in range(11):
				retstr += "\n%-14s  %s"%(self.planets[i], self.houses[i])
			retstr += "\n" + 17*' ' + "%s"%self.houses[11]
		else:
			for planet in self.planets:
				retstr += "\n%s"%planet.__repr__()
		return retstr

if __name__ == "__main__":
	import location
	nardo = location.Location("Nardò", 40.1795300, 18.0317400)
	datetime1 = dates.TimeZonedEvent(1992, 12, 22, 19, 15, 00, nardo)
	ephecalc1 = Ephemeris(datetime1)
	print(ephecalc1)
	rome = location.Location("Rome", 41.9027835, 12.4963655)
	datetime2 = dates.TimeZonedEvent(1993, 8, 9, 12, 00, 00, rome)
	ephecalc2 = Ephemeris(datetime2)
	print(ephecalc2)
	nairobi = location.Location("Nairobi", -1.2833300, 36.8166700)
	datetime3 = dates.UnknownTimeEvent(1322, 4, 5, nairobi)
	ephecalc3 = Ephemeris(datetime3)
	print(ephecalc3)
