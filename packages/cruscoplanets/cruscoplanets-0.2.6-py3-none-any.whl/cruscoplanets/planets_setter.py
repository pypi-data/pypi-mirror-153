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

from cruscoplanets import svg_settings
from cruscoplanets import ephemeris
import math
from cruscoplanets import angles


class PlanetsSetter:
	"""This class takes as argument the planets of an :class:`cruscoplanets.ephemeris.Ephemeris` instance and modifies slightly the values of the angular positions of their symbols in the chart, so 
	that they do not overlap.
	
	Args:
		planets (tuple): a tuple of :class:`cruscoplanets.ephemeris.Planet` instances whose positions in the chart need to be adjusted
		transit (bool): must be True if the planets passed to the *planets* argument are transit ones, False if otherwise.
	"""

	graphicSettings = svg_settings.SvgSettings()
	birthRadius = graphicSettings.POINTERS_CIRCLE_RADIUS - graphicSettings.PLANETS_OFFSET
	transitRadius = graphicSettings.ZODIAC_CIRCLE_RADIUS + graphicSettings.TRANSIT_PLANETS_OFFSET
	
	#all the planet symbols are enclosed in a circle of a 20 px radius. To make sure that planets do not overlap, one must first find out which planets are far from each other less than 40px.
	#it is more convenient to convert this distance to an angular one (taking the center of the circles of the graphics as vertex). Angular distance can be obtained employing trigonometry.

	#minimum angular distance for birth planets with retrograde sign measured in degrees:
	birthAngularDistance = angles.Angle(math.degrees(math.sin(45/birthRadius)))
	transitAngularDistance = angles.Angle(math.degrees(math.sin(45/transitRadius)))

	def __init__(self, planets: tuple, transit: bool = False):
		#it is more convenient here to have the planets sorted by their angular position
		self.areTransitPlanets = transit
		self.planets = sorted(planets, key=lambda g: g.eclipticLongitude)
		self.overlaps = self._parseOverlaps()
		for overlap in self.overlaps:
			self._handleOverlap(overlap)
			
	def adjustPlanets(self):
		"""Returns a tuple of :class:`cruscoplanets.ephemeris.Planet` instances whose positions in the chart have been adjusted"""
		return self.planets
	
	def _handleOverlap(self, overlap: tuple):
		centerAngle = (overlap[-1].eclipticLongitude + overlap[0].eclipticLongitude)/2
		min_distance = overlap[0].eclipticLongitude - centerAngle
		for i in range(len(overlap), 1):
			distance = abs(overlap[i] - centerAngle)
			if distance < min_distance:
				min_distance = distance
		if not self.areTransitPlanets:
			factor = self.__class__.birthAngularDistance/min_distance
		else:
			factor = self.__class__.transitAngularDistance/min_distance
		for planet in overlap:
			planet.figurePosition = centerAngle + (planet.eclipticLongitude - centerAngle)*factor
		
	def _parseOverlaps(self):
		overlaps = []
		i = 0
		while i < len(self.planets)-1:
			if self.planets[i+1] - self.planets[i] < self.__class__.birthAngularDistance:#here there is an overlap
				if len(overlaps) == 0:
					overlaps.append([self.planets[i], self.planets[i+1]])
				else:
					if overlaps[-1][-1] == self.planets[i]:
						overlaps[-1].append(self.planets[i+1])
					else:
						overlaps.append([self.planets[i], self.planets[i+1]])
			i += 1
		overlaps = tuple(tuple(overlap) for overlap in overlaps)
		return overlaps
		
	def __repr__(self):
		retstr = '\n'.join(str(planet) for planet in self.planets)
		retstr += "\nBirth Angular Distance: %s"%self.__class__.birthAngularDistance
		for overlap in self.overlaps:
			overlapstring = '\n'
			for planet in overlap:
				overlapstring += "%s %s\n"%(planet, planet.figurePosition.asZodiacPoint)
			retstr += overlapstring
		return retstr




if __name__ == '__main__':
	import location, dates
	nardo = location.Location("Nardò", 40.1795300, 18.0317400)
	datetime1 = dates.TimeZonedEvent(1992, 12, 22, 19, 15, 00, nardo)
	ephecalc1 = ephemeris.Ephemeris(datetime1)
	planetsSetter = PlanetsSetter(ephecalc1.planets)
	print(planetsSetter)

