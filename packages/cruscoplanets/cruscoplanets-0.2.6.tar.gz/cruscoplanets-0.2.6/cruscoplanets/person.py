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

from cruscoplanets import dates
from cruscoplanets import location


class Person:
	"""Represents the person for whom the chart is built.
	
	Args:
		name (str): the first name(s) of the person
		surname (str): the first name(s) of the person
		sex (str): an integer representing the sex of the person. It can have only three values: Person.MALE, Person.FEMALE or Person.UNDEFINED
		birthEvent (:class:`cruscoplanets.dates.Event`): the birth event of the person.
	"""
	MALE = 0
	FEMALE = 1
	UNDEFINED = -1
	
	def __init__(self, name: str, surname: str, sex: int, birthEvent: dates.Event):
		if sex not in {Person.MALE, Person.FEMALE, Person.UNDEFINED}:
			raise ValueError("Unrecognised sex integer")
		self.sex = sex
		self.name = name
		self.surname = surname
		self.birthEvent = birthEvent

	@property
	def birthPlace(self):
		"""Returns the location of the birth event as a :class:`cruscoplanets.location.Location` instance."""
		return self.birthEvent.location
		
	def __repr__(self):
		return "%s %s, %d\n\t%s\n\t%s"%(self.name, self.surname, self.sex, self.birthPlace, self.birthEvent)
		
if __name__ == '__main__':
	nardo = location.Location("Nardò", 40.1795300, 18.0317400)
	eventbuilder1 = dates.EventBuilder(1992, 12, 22, 19, 15, 00, nardo)
	event1 = eventbuilder1.getEventByTimeZone()
	person1 = Person("Diana", "Artemide", Person.FEMALE, event1)
	print(person1)
	rome = location.Location("Rome", 41.9027835, 12.4963655)
	eventbuilder2 = dates.EventBuilder(1993, 8, 9 , 7, 0, 0, rome)
	event2 = eventbuilder2.getEventbyUTCTime()
	person2 = Person("Emiliano", "Minerba", Person.MALE, event2)
	print(person2)
	nairobi = location.Location("Nairobi", -1.2833300, 36.8166700)
	eventbuilder3 = dates.EventBuilder(2000, 9, 7, None, None, None, nairobi)
	event3 = eventbuilder3.getUnknownTimeEvent()
	person3 = Person("Juma", "Pondamali", Person.UNDEFINED, event3)
	print(person3)

