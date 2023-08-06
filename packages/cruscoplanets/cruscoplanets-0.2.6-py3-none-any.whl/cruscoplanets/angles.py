#    This file is part of Cruscoplanets.
#
#   Cruscoplanets is free software: you can redistribute it and/or modify
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


class Angle:
	"""Represent angles and provides methods for converting from decimal to sessagesimal degrees and viceversa. 
	This class works with decimal grades. A class method for initialising angles by their degree values is also provided, but it could lessen the accuracy of calculations, 
	and therefore is not recommended
	
	Args:
		decvalue: the angular measure, in decimal degrees.

	Attributes:
		decvalue: the angular measure, in decimal degrees.
	"""

	zodiac_symbols = "♈♉♊♋♌♍♎♏♐♑♒♓"
	zodiac_names = ('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces')
	
	def __init__(self, decvalue: float):
		decvalue = float(decvalue)
		self.decvalue = decvalue

	@classmethod
	def straight(cls):
		"""Returns an instance representing a straight angle"""
		return cls(180.0)

	@classmethod
	def perigon(cls):
		"""Returns an instance representing a perigon angle"""
		return cls(360.0)
		
	def __add__(self, other):
		"""Returns an instance corresponding to the sum of two angles"""
		return Angle(self.decvalue + other.decvalue)
		
	def __sub__(self, other):
		"""Returns an instance corresponding to the difference between two angles"""
		return Angle(self.decvalue - other.decvalue)
		
	def __mul__(self, other):
		"""Returns an instance corresponding to the multiplication of the angle for a real number"""
		return Angle(self.decvalue * other)
		
	def __rmul__(self, other):
		"""Returns an instance corresponding to the multiplication of the angle for a real number"""
		return Angle(self.decvalue * other)
		
	def __truediv__(self, other):
		"""Returns an instance corresponding to the division of an angle for a real number."""
		if isinstance(other, float) or isinstance(other, int):
			return Angle(self.decvalue / other)
		elif isinstance(other, Angle):
			return self.decvalue / other.decvalue
		else:
			raise NotImplementedError

	def __lt__(self, other):
		return self.decvalue < other.decvalue
		
	def __ge__(self, other):
		return self.decvalue >= other.decvalue

	def __eq__(self, other):
		return self.decvalue == other.decvalue

	@property
	def hoursvalue(self):
		"""Return the angular measure of the instance expressed in hours (1 hour = 15 degrees)"""
		return self.decvalue/15
		
	@classmethod
	def fromDegrees(cls, degrees: int, minutes: int, seconds: int, isNegative: bool = False):
		"""Takes a value expressed in sessagesimal degrees and returns an instance of :class:`Angle`.
		
		Args:
			degrees (int): the degrees of the angle
			minutes (int): the first minutes
			seconds (int): the second minutes
			isNegative (bool): True if the angle is negative

		Returns:
			dec_angle (:class:`Angle`): the angle in decimal degrees
		"""
		decvalue = abs(degrees) + abs(minutes)/60 + abs(seconds)/3600
		if isNegative:
			decvalue *= -1
		return cls(decvalue)
		
	@property
	def isNegative(self):
		if self.decvalue < 0:
			return True
		else:
			return False
		
	@property
	def degreesvalue(self):
		"""Returns a tuple of three integers, representing respectively the degrees, first minutes and second minutes of the angle in sexagesimal notation."""
		return self.__degreesvalue(self.decvalue)

	def __degreesvalue(self, value):
		startvalue = self.__geometricValue(value)
		degrees = int(startvalue)
		first_decimal_part = startvalue - degrees
		first_decimal_part_to_degrees = first_decimal_part*60
		first_minutes = int(first_decimal_part_to_degrees)
		second_decimal_part = first_decimal_part_to_degrees - first_minutes
		second_decimal_part_to_degrees = second_decimal_part*60
		second_minutes = int(second_decimal_part_to_degrees)
		return (degrees, first_minutes, second_minutes)
	
	@property
	def zodiacValueTuple(self):
		"""Returns a tuple of four items, the first being the name of the Zodiac sign in lowercase letters, the others being the degrees, first and second minutes of the angle in the sign"""
		degrees, first, second = self.degreesvalue
		sixties = degrees // 30
		degrees %= 30
		sixties = self.__class__.zodiac_names[sixties]
		return (sixties, degrees, first, second)

	def __geometricValue(self, value):
		while value < 0:
			value += 360
		while value >= 360:
			value -= 360
		return value		

	@property
	def geometricValue(self):
		"""Expresses the value of the angle between 0 and 360 degrees"""
		return self.__geometricValue(self.decvalue)
		
	def __getZodiacSymbol(self, int_sign):
		return self.__class__.zodiac_symbols[int_sign]

	@property
	def asZodiacPoint(self):
		"""Expresses the angle as Zodiac point"""
		geometric_angle = self.geometricValue
		sign_int = int(geometric_angle // 30)
		rest = geometric_angle % 30
		degrees_rest = "%02d°%02d'%02d\""%self.__degreesvalue(rest)
		return "%s%s"%(self.__getZodiacSymbol(sign_int), degrees_rest)
		
	
	def reprAsLatitude(self):
		if not self.isNegative:
			return "%d°%02d'%02d\"N"%self.degreesvalue
		else:
			return "%d°%02d'%02d\"S"%self.degreesvalue
		
	def reprAsLongitude(self):
		if not self.isNegative:
			return "%d°%02d'%02d\"E"%self.degreesvalue
		else:
			return "%d°%02d'%02d\"W"%self.degreesvalue

	def __repr__(self):
		if not self.isNegative:
			return "%d°%02d'%02d\""%self.degreesvalue
		else:
			return "-%d°%02d'%02d\""%self.degreesvalue


if __name__ == '__main__':
	angle1 = Angle(-60.123)
	print(angle1, angle1.decvalue)
	angle2 = Angle.fromDegrees(140, 13, 15)
	print(angle2, angle2.decvalue)
	angle3 = Angle.fromDegrees(140, 13, 15, True)
	print(angle3, angle3.decvalue)
