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

from cruscoplanets import angles
from cruscoplanets import utils
import os


class AspectError(Exception):
	
	def __init__(self):
		super().__init__
	
	def __str__(self):
		return "Unallowed bodyInt: admissible values are only 0, 30, 60, 90, 120, 180."


class Aspect:
	"""Represents an aspect between two planets. The only kinds of aspects allowed are those considered in Morpurgo's school.
	
	Args:
		base_angle (int): the approximated value of the angle between the two planets, corresponding to a certain type of aspect (0 for conjunction, 30 for semisextile, 60 for sextile, et cetera)
		exact_angle (:class:`cruscoplanets.angles.Angle`): the precise value of the angle between the two planets.
		planet1 (:class:`cruscoplanets.ephemeris.Planet`); the first planet of the aspect
		planet2 (:class:`cruscoplanets.ephemeris.Planet`); the second planet of the aspect
	
	Attributes:
		base_angle (int): the approximated value of the angle between the two planets, corresponding to a certain type of aspect (0 for conjunction, 30 for semisextile, 60 for sextile, et cetera)
		exact_angle (:class:`cruscoplanets.angles.Angle`): the precise value of the angle between the two planets.
		planet1 (:class:`cruscoplanets.ephemeris.Planet`); the first planet of the aspect
		planet2 (:class:`cruscoplanets.ephemeris.Planet`); the second planet of the aspect
		
	Raises:
		AspectError: raised is the instance is initialized with an unallowed bodyInt (that is, other than 0, 30, 60, 90, 120, 180)
	"""

	SYMBOLS = {
		"0": "☌",
		"30": "⚺",
		"60": "⚹",
		"90": "□",
		"120": "△",
		"180": "☍",
	}
	
	NAMES = {
		"0": "conjunction",
		"30": "semisextile",
		"60": "sextile",
		"90": "square",
		"120": "trine",
		"180": "opposition",
	}
	
	def __init__(self, base_angle: int, exact_angle: angles.Angle, planet1, planet2):
		if base_angle not in tuple(int(x) for x in self.__class__.NAMES.keys()):
			raise AspectError
		self.base_angle = angles.Angle(base_angle)
		self.exact_angle = exact_angle
		self.planet1, self.planet2 = planet1, planet2
		
	@property
	def planetsInts(self):
		"""Returns a tuple containing the id integers of *planet1* and *planet2* (see class :class:`cruscoplanets.ephemeris.Planet`) """
		return (self.planet1.bodyInt, self.planet2.bodyInt)
		
	@property
	def identifier(self):
		"""Returns a string giving the basic information on the aspect, which identify it in the chart."""
		return "%s-%s-%s"%(self.planet1.name, self.name, self.planet2.name)

	@property
	def orb(self):
		"""Returns the value of the orb of the aspect (the absolute value of the difference between *exact_angle* and *base_angle*) as a :class:`cruscopepper:angles:Angle` instance."""
		if self.exact_angle >= self.base_angle:
			return self.exact_angle - self.base_angle
		else:
			return self.base_angle - self.exact_angle

	@property
	def name(self):
		"""The name of the aspect's type in lowercase (useful for building the svg file)"""
		return self.__class__.NAMES[str(int(self.base_angle.decvalue))]
		
	@property
	def symbol(self):
		"""The symbol of the aspect's type as an Unicode character"""
		return self.__class__.SYMBOLS[str(int(self.base_angle.decvalue))]
		
	def __repr__(self):
		return "%s %s %s Orb: %s"%(self.planet1.symbol, self.symbol, self.planet2.symbol, self.orb)


class AspectsParser(metaclass=utils.Singleton):
	"""An instance of this class reads the settings about aspects angles and orbs from the configuration files and calculate aspects for pairs of planets, returning Aspect instances or None.
	This class is a Singleton: initializing is more times will always return the same instance
	"""

	CONFIGFILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "aspects.txt")
	
	def __init__(self):

		config = utils.parseBanalConfig(self.__class__.CONFIGFILEPATH)
		for line in config:
			self.__dict__[line[0]] = int(line[1])
				
	def __repr__(self):
		keys = sorted(self.__dict__.keys())
		values = tuple("%s = %s"%(key, self.__dict__[key]) for key in keys)
		return "\n".join(values)
		
	def __isInRange(self, angle, angle_type: str):
		angle_value = self.__dict__["%s_VALUE"%angle_type]
		orb_value = self.__dict__["%s_ORB"%angle_type]
		if (abs(angle.decvalue) >= (angle_value - orb_value) and abs(angle.decvalue) <= (angle_value + orb_value)):
			return True
		else:
			return False
		
	def __isInTransitRange(self, angle, angle_type: str):
		angle_value = self.__dict__["%s_VALUE"%angle_type]
		orb_value = self.__dict__["TRANSIT_%s_ORB"%angle_type]
		if (abs(angle.decvalue) >= (angle_value - orb_value) and abs(angle.decvalue) <= (angle_value + orb_value)):
			return True
		else:
			return False

	def parseAspect(self, planet_pair: tuple):
		"""Returns an Aspect instance if the planet_pair forms an aspect, else None.
		
		Args:
			planet_pair (tuple): a tuple of :class:`cruscoplanets.ephemeris.Planet` instances, for which the existence of an aspect will be checked.
		"""
		planet1, planet2 = planet_pair
		angle = planet1 - planet2
		if (self.__isInRange(angle, "CONJUNCTION")):
			return Aspect(self.CONJUNCTION_VALUE, angle, planet1, planet2)

		elif (self.__isInRange(angle, "OPPOSITION")):
			return Aspect(self.OPPOSITION_VALUE, angle, planet1, planet2)

		elif (self.__isInRange(angle, "TRINE")):
			return Aspect(self.TRINE_VALUE, angle, planet1, planet2)

		elif (self.__isInRange(angle, "SEXTILE")):
			return Aspect(self.SEXTILE_VALUE, angle, planet1, planet2)

		elif (self.__isInRange(angle, "SEMISEXTILE")):
			return Aspect(self.SEMISEXTILE_VALUE, angle, planet1, planet2)

		elif (self.__isInRange(angle, "SQUARE")):
			return Aspect(self.SQUARE_VALUE, angle, planet1, planet2)
		else:
			return None

	def parseTransitAspect(self, planet_pair: tuple):
		"""Returns an Aspect instance if the planet_pair forms an aspect, else None. Transit aspects are different from birth aspects mainly in the maximum orb allowed, which is much lower (2 degrees)
		
		Args:
			planet_pair (tuple): a tuple of two :class:`cruscoplanets.ephemeris.Planet` instances, for which the existence of an aspect will be checked.
		"""
		planet1, planet2 = planet_pair
		angle = planet1 - planet2
		if (self.__isInTransitRange(angle, "CONJUNCTION")):
			return Aspect(self.CONJUNCTION_VALUE, angle, planet1, planet2)

		elif (self.__isInTransitRange(angle, "OPPOSITION")):
			return Aspect(self.OPPOSITION_VALUE, angle, planet1, planet2)

		elif (self.__isInTransitRange(angle, "TRINE")):
			return Aspect(self.TRINE_VALUE, angle, planet1, planet2)

		elif (self.__isInTransitRange(angle, "SEXTILE")):
			return Aspect(self.SEXTILE_VALUE, angle, planet1, planet2)

		elif (self.__isInTransitRange(angle, "SEMISEXTILE")):
			return Aspect(self.SEMISEXTILE_VALUE, angle, planet1, planet2)

		elif (self.__isInTransitRange(angle, "SQUARE")):
			return Aspect(self.SQUARE_VALUE, angle, planet1, planet2)
		else:
			return None
