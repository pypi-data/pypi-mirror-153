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

from cruscoplanets import person, ephemeris, aspects, dates, planets_setter
from cruscoplanets import utils, svg_base
import lxml.etree
from cruscoplanets import language_manager
from cruscoplanets import angles
import os
import subprocess
from math import atan, degrees


class Chart:
		
	def __init__(self, person: person.Person, language: language_manager.LanguageManager = None, transits: bool = False):
		self.person = person
		if language == None:
			self.languageManager = language_manager.LanguageManager.getDefault()
		else:
			self.languageManager = language_manager.LanguageManager(language)
		self.birth = self.person.birthEvent
		self.birthEphemeris = ephemeris.Ephemeris(self.birth)
		aspectsParser = aspects.AspectsParser()
		myaspects = tuple(aspectsParser.parseAspect(pair) for pair in self._birthPlanetsPairsIterator())
		self.birthAspects = tuple(filter(lambda x: x != None, myaspects))
		self.svgBase = svg_base.SvgBase()
		if not transits:
			self.xmldom = self.svgBase.buildBaseBirthXml()
		else:
			self.xmldom = self.svgBase.buildBaseTransitXml()

	def _searchBirthAspect(self, planetInt1, planetInt2):
		all_aspects = tuple(filter(lambda aspect: aspect.planetsInts == (planetInt1, planetInt2), self.birthAspects))
		if len(all_aspects) > 0:
			return all_aspects[0]
		return None
		
	def _makePlanetInGrid(self, topleft_x, topleft_y, step, idnum):
		node = lxml.etree.Element('use')
		node.attrib.update({
			'x': str(topleft_x + 0.5*step),
			'y': str(topleft_y + 0.5*step),
			'width': str(step),
			'height': str(step),
			'{http://www.w3.org/1999/xlink}href': '#' + ephemeris.Planet.NAMES[idnum] + '_template'
		})
		return node
		
	def _makeAspectInGrid(self, topleft_x, topleft_y, step, idnum1, idnum2):
		node = lxml.etree.Element('use')
		node.attrib.update({
			'x': str(topleft_x + 0.5*step),
			'y': str(topleft_y + 0.5*step),
			'width': str(step),
			'height': str(step),
		})
		aspect = self._searchBirthAspect(idnum1, idnum2)
		if aspect != None:
			node.attrib.update({
				'{http://www.w3.org/1999/xlink}href': '#' + aspect.name + '_template'
			})
		return node
		
	def _insertSymbolInGrid(self, topleft_x, topleft_y, step, idnum1, idnum2):
		if idnum1 == idnum2:
			node = self._makePlanetInGrid(topleft_x, topleft_y, step, idnum1)
		else:
			node = self._makeAspectInGrid(topleft_x, topleft_y, step, idnum1, idnum2)
		self.xmlroot.append(node)

	def _birthPlanetsPairsIterator(self):
		for i in range(len(self.birthEphemeris.planets)-1):
			for j in range(i+1, len(self.birthEphemeris.planets)):
				yield (self.birthEphemeris.planets[i], self.birthEphemeris.planets[j])	

	def _buildHouseLine(self, house):
		
		startCoordinates = (0, 0)
		endCoordinates = utils.polarToCartesian(house.position.decvalue, self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		line_attrib = {
			"x1": str(startCoordinates[0]), "y1": str(startCoordinates[1]), 
			"x2": str(endCoordinates[0]), "y2": str(endCoordinates[1]), 
			"stroke": str(self.svgBase.settings.HOUSE_LINE_COLOR), "stroke-width": str(self.svgBase.settings.HOUSE_LINE_WIDTH),
			"id": "house-" + str(house.index+1) + "_line"
		}
		new_line = lxml.etree.SubElement(self.zodiacAndHousesNode, "line")
		new_line.attrib.update(line_attrib)
		
		symbol_radius = self.svgBase.settings.ASPECTS_CIRCLE_RADIUS + self.svgBase.settings.HOUSE_SYMBOLS_OFFSET
		symbol_angle = house.position.decvalue + degrees(atan(self.svgBase.settings.HOUSE_SYMBOLS_SIZE/symbol_radius))
		symbol_coordinates = utils.polarToCartesian(symbol_angle, symbol_radius)
		symbol_attribs = {
			"x": str(symbol_coordinates[0]), "y": str(symbol_coordinates[1]),
			"fill": self.svgBase.settings.HOUSE_SYMBOLS_COLOR,
			"font-size": str(self.svgBase.settings.HOUSE_SYMBOLS_SIZE),
			"id": "house_symbol_" + house.symbol,
			"text-anchor": "middle"
		}
		symbol_node = lxml.etree.SubElement(self.zodiacAndHousesNode, "text")
		symbol_node.attrib.update(symbol_attribs)
		symbol_node.text = house.symbol
		self._addTransformation(symbol_node, "rotate(%f, %f, %f)"%(-self.birthEphemeris.ascendant.position.decvalue, symbol_coordinates[0], symbol_coordinates[1]))
		self._addTransformation(symbol_node, "translate(0, %f)"%(self.svgBase.settings.HOUSE_SYMBOLS_SIZE/2.8))#this centers the text elements also vertically

	def _buildAscendantLine(self):
		startCoordinates = utils.polarToCartesian(utils.add180(self.birthEphemeris.ascendant.position.decvalue), self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		endCoordinates = utils.polarToCartesian(self.birthEphemeris.ascendant.position.decvalue, self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		line_attrib = {
			"x1": str(startCoordinates[0]), "y1": str(startCoordinates[1]), 
			"x2": str(endCoordinates[0]), "y2": str(endCoordinates[1]), 
			"stroke": str(self.svgBase.settings.ASCENDANT_LINE_COLOR), "stroke-width": str(self.svgBase.settings.ASCENDANT_LINE_WIDTH),
			"id": "ascendant_line"
		}
		new_line = lxml.etree.SubElement(self.zodiacAndHousesNode, "line")
		new_line.attrib.update(line_attrib)

	def _buildMediumCoeliLine(self):
		startCoordinates = utils.polarToCartesian(utils.add180(self.birthEphemeris.mediumCoeli.position.decvalue), self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		endCoordinates = utils.polarToCartesian(self.birthEphemeris.mediumCoeli.position.decvalue, self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		line_attrib = {
			"x1": str(startCoordinates[0]), "y1": str(startCoordinates[1]), 
			"x2": str(endCoordinates[0]), "y2": str(endCoordinates[1]), 
			"stroke": str(self.svgBase.settings.MOEDIUM_COELI_LINE_COLOR), "stroke-width": str(self.svgBase.settings.MOEDIUM_COELI_LINE_WIDTH),
			"id": "medium_coeli_line"
		}
		new_line = lxml.etree.SubElement(self.zodiacAndHousesNode, "line")
		new_line.attrib.update(line_attrib)
		
	def _addTransformation(self, node, command: str):
		"""Adds a transformation command to the transform attribute of a svg element"""
		transform_attr = node.get("transform")
		if (transform_attr != None):
			transform_attr += ' '
		else:
			transform_attr = ''
		transform_attr += command
		node.set("transform", transform_attr)
		
	def _adjustCharSize(self, charnode, size=None):
		if size == None:
			size = self.svgBase.settings.PLANETS_TABLE_FONT_SIZE
		initial_height = 50
		initial_x = float(charnode.get('x'))
		initial_y = float(charnode.get('y'))
		size_scale = size/initial_height
		translation_corrector = initial_height/size
		translated_x = initial_x*translation_corrector
		translated_y = initial_y*translation_corrector
		charnode.attrib['x'] = str(translated_x)
		charnode.attrib['y'] = str(translated_y)
		self._addTransformation(charnode, "scale(%f)"%size_scale)
		
		
	def _insertZodiacAngle(self, node, angle: angles.Angle):
		"""Inserts the value of angle in Zodiac symbology into an lxml.etree node"""
		angle_tuple = angle.zodiacValueTuple
		sign_node = lxml.etree.SubElement(node, "use")
		sign_node.attrib.update({
			'x': node.get('x'),
			'y': node.get('y'),
			"{http://www.w3.org/1999/xlink}href": "#char-%s_template"%angle_tuple[0],
		})
		self._adjustCharSize(sign_node)
		text_node = lxml.etree.SubElement(node, "text")
		text_x = str(float(node.get('x')) + 1.2*self.svgBase.settings['PLANETS_TABLE_FONT_SIZE'])
		text_node.attrib.update({
			'x': text_x,
			'y': node.get('y'),
			'font-size': str(self.svgBase.settings.PLANETS_TABLE_FONT_SIZE),
			'font-weight': self.svgBase.settings.PLANETS_TABLE_FONT_WEIGHT,
			'font-family': self.svgBase.settings.FONT_FAMILY
		})
		text_node.text = "%02d°%02d'%02d\""%angle_tuple[1:4]
	
	def _makeInnerPlanetAngle(self, planet: ephemeris.Planet):
		planet_angle = lxml.etree.Element("path")
		planet_angle_d = "M %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.POINTERS_CIRCLE_RADIUS)
		planet_angle_d += " L %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		planet_angle_color= self.svgBase.settings['%s_COLOR'%planet.name.upper()]
		planet_angle.set("d", planet_angle_d)
		planet_angle.set("stroke", planet_angle_color)
		planet_angle.set("stroke-width", str(self.svgBase.settings.ANGLE_POINTERS_WIDTH))
		return planet_angle

	def _makeBirthPlanetBody(self, planet: ephemeris.Planet):
		radius = self.svgBase.settings.POINTERS_CIRCLE_RADIUS - self.svgBase.settings.PLANETS_OFFSET		
		planet_coordinates = utils.polarToCartesian(planet.figurePosition.decvalue, radius)
		planet_node = lxml.etree.Element("use")
		planet_node.set("{http://www.w3.org/1999/xlink}href", "#%s_template"%planet.name)
		planet_node.set("x", "%f"%planet_coordinates[0])
		planet_node.set("y", "%f"%planet_coordinates[1])
		planet_node.set('id', "%s_node"%planet.name)
		wrapper = lxml.etree.Element('g')
		wrapper.attrib.update({
			'id': "%s_node_wrapper"%planet.name,
			'height': str(planet_node.get('height')),
			'width': str(planet_node.get('width'))
		})
		wrapper.append(planet_node)
		if planet.isRetrograde:
			retrograde_template = lxml.etree.Element('use')
			retrograde_template.attrib.update({
				'id': '%s_retrograde'%planet.name,
				"{http://www.w3.org/1999/xlink}href": "#retrograde_template",
				'x': "%f"%planet_coordinates[0],
				'y': "%f"%planet_coordinates[1],
				'fill': self.svgBase.settings["%s_COLOR"%planet.name.upper()],
				'stroke': self.svgBase.settings["%s_COLOR"%planet.name.upper()]
			})
			wrapper.append(retrograde_template)
		if not self.birthEphemeris.isTimeUnknown:
			self._addTransformation(wrapper, "rotate(-%f, %f, %f)"%(self.birthEphemeris.ascendant.position.decvalue, planet_coordinates[0], planet_coordinates[1]))
		return wrapper#planet_node

	def _makeBirthPlanet(self, planet: ephemeris.Planet):
		planet_node = self._makeBirthPlanetBody(planet)
		planet_angle = self._makeInnerPlanetAngle(planet)
		return (planet_node, planet_angle)

	def _buildConjunction(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_arc = utils.drawArc(angle1, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_arc.attrib.update({'stroke': self.svgBase.settings.CONJUNCTION_COLOR, 'stroke-width': str(self.svgBase.settings.CONJUNCTION_WIDTH)})
		return aspect_arc
	
	def _buildOpposition(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_line = utils.lineByPolarCoordinates(angle1, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_line.set("stroke", self.svgBase.settings.OPPOSITION_COLOR)
		aspect_line.set("stroke-width", str(self.svgBase.settings.OPPOSITION_WIDTH))
		return aspect_line

	def _buildTrine(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_line = utils.lineByPolarCoordinates(angle1, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_line.set("stroke", self.svgBase.settings.TRINE_COLOR)
		aspect_line.set("stroke-width", str(self.svgBase.settings.TRINE_WIDTH))
		return aspect_line

	def _buildSquare(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_line = utils.lineByPolarCoordinates(angle1, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_line.set("stroke", self.svgBase.settings.SQUARE_COLOR)
		aspect_line.set("stroke-width", str(self.svgBase.settings.SQUARE_WIDTH))
		return aspect_line

	def _buildSextile(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_line = utils.lineByPolarCoordinates(angle1, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_line.set("stroke", self.svgBase.settings.SEXTILE_COLOR)
		aspect_line.set("stroke-width", str(self.svgBase.settings.SEXTILE_WIDTH))
		return aspect_line

	def _buildSemisextile(self, aspect):
		angle1 = aspect.planet1.eclipticLongitude.decvalue
		angle2 = aspect.planet2.eclipticLongitude.decvalue
		aspect_line = utils.lineByPolarCoordinates(angle1, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS, angle2, self.svgBase.settings.ASPECTS_CIRCLE_RADIUS)
		aspect_line.set("stroke", self.svgBase.settings.SEMISEXTILE_COLOR)
		aspect_line.set("stroke-width", str(self.svgBase.settings.SEMISEXTILE_WIDTH))
		return aspect_line
	
	def _insertAspectsGrid(self):
		x0, y0 = self.svgBase.topLeftCoordinates
		x0, y0 = float(x0), float(y0)

		start_x = int(x0+self.svgBase.settings.ASPECTS_GRID_X_OFFSET)
		start_y = int(y0+self.svgBase.settings.ASPECTS_GRID_Y_OFFSET)
		step = int(self.svgBase.settings.ASPECTS_GRID_CELL_LENGTH)
		for i in range(11):
			for j in range(11):
				if i <= j:
					x = start_x + i*step
					y = start_y + j*step
					rect = lxml.etree.SubElement(self.xmlroot, 'rect')
					rect.attrib.update({
						'x': str(x),
						'y': str(y),
						'id': "aspect_cell_%d-%d"%(i, j),
						'width': str(step),
						'height': str(step),
						'fill': self.svgBase.settings.ASPECTS_GRID_FILL_COLOR,
						'stroke': self.svgBase.settings.ASPECTS_GRID_LINE_COLOR,
						'stroke-width': str(self.svgBase.settings.ASPECTS_GRID_LINE_WIDTH)
					})
					self._insertSymbolInGrid(x, y, step, i, j)
	
	def _insertPersonalData(self):
		namefield = self._getElementById('name_field')
		if self.person.sex == 0:
			sex = 'sex_male'
		elif self.person.sex == 1:
			sex = 'sex_female'
		else :
			sex = 'sex_undefined'
		namefield.text = self.person.name + ' ' + self.person.surname + ', ' + self.languageManager.expressions[sex]
		locationfield = self._getElementById('location_field')
		locationfield.text = self.person.birthEvent.location.name
		eventfield = self._getElementById('date_and_time_field')
		event_value = self.person.birthEvent.dateAndTime
		if self.birth.isTimeUnknown:
			event_value += ' (' + self.languageManager.expressions['unknown_time'] + ')'
		eventfield.text = event_value

	def _insertHouses(self):
		for house in self.birthEphemeris.houses:
			self._buildHouseLine(house)
			house_text_node = self._getElementById(house.symbol + '_house_symbol')
			house_text_node.text = house.symbol
			house_degree_node = self._getElementById(house.symbol + '_house_degree')
			self._insertZodiacAngle(house_degree_node, house.position)
		self._buildAscendantLine()
		self._buildMediumCoeliLine()
		self._addTransformation(self.zodiacAndHousesNode, "rotate(%f, 0, 0)"%self.birthEphemeris.ascendant.position.decvalue)
		houses_table_title = self._getElementById('houses_table_title')
		houses_table_title.text = self.languageManager.expressions['houses_table_title']

	
	def _insertBirthPlanets(self):
		planetsSetter = planets_setter.PlanetsSetter(self.birthEphemeris.planets)
		planets = planetsSetter.adjustPlanets()
		planets = tuple(self._makeBirthPlanet(planet) for planet in self.birthEphemeris.planets)
		for planet in planets:
			self.zodiacAndHousesNode.append(planet[0])#planet body
			self.zodiacAndHousesNode.append(planet[1])#planet inner angle

		for planet in self.birthEphemeris.planets:
			symbol_node = self._getElementById('%s_symbol'%planet.name)
			planet_symbol = lxml.etree.SubElement(symbol_node, "use")
			planet_symbol.attrib.update({
				"{http://www.w3.org/1999/xlink}href": "#char-%s_template"%planet.name,
				"x": symbol_node.get('x'),
				"y": symbol_node.get('y')
			})
			self._adjustCharSize(planet_symbol, size=1.4*self.svgBase.settings.PLANETS_TABLE_FONT_SIZE)
			degree_node = self._getElementById('%s_degree'%planet.name)
			self._insertZodiacAngle(degree_node, planet.eclipticLongitude)
		
		planets_table_title = self._getElementById('planets_table_title')
		planets_table_title.text = self.languageManager.expressions['planets_table_title'] + ':'

	def _insertBirthAspects(self):
		for aspect in self.birthAspects:
			if aspect.name == "conjunction":
				aspect_node = self._buildConjunction(aspect)
			elif aspect.name == "opposition":
				aspect_node = self._buildOpposition(aspect)
			elif aspect.name == "trine":
				aspect_node = self._buildTrine(aspect)
			elif aspect.name == "square":
				aspect_node = self._buildSquare(aspect)
			elif aspect.name == "sextile":
				aspect_node = self._buildSextile(aspect)
			elif aspect.name == "semisextile":
				aspect_node = self._buildSemisextile(aspect)
			else:
				raise RuntimeError("Unrecognised aspect")
			aspect_id = "birth-aspect-" + aspect.identifier
			aspect_node.attrib['id'] = aspect_id
			self.zodiacAndHousesNode.append(aspect_node)

	@property
	def xmlroot(self):
		return self.xmldom.getroot()
	
	def _getElementById(self, idstr):
		node = tuple(filter(lambda node: node.get('id') == idstr, self.xmlroot.iter('*')))[0]
		return node
		
	@property
	def zodiacNode(self):
		return self._getElementById("zodiac_circle")

	@property
	def zodiacAndHousesNode(self):
		return self._getElementById("zodiac_and_houses")

	@property
	def houses(self):
		return self.birthEphemeris.houses
		
	@property
	def ascendant(self):
		return self.birthEphemeris.ascendant
		
	@property
	def mediumCoeli(self):
		return self.birthEphemeris.mediumCoeli
		
	@property
	def birthPlanets(self):
		return self.birthEphemeris.planets

	@property
	def svgAsString(self):
		"""Returns the svg tree of the chart as a binary string."""
		return lxml.etree.tostring(self.xmldom)
	
	@property
	def filename(self):
		"""Returns a string with the type of the chart and the perosn name, fit to be used as filename when the graphic will be saved."""
		return "%s_%s-birth_chart"%(self.person.name, self.person.surname)
				
		
class BirthChart(Chart):
	"""Represents a birth chart.
	
	Args:
		person (:class:`cruscoplanets.person.Person`): the person whose astrological data are represented in the chart.
		language (:class:`cruscoplanets.language_manager.LanguageManager`): the language (in ISO639-2 code) of the chart.

	Attributes:
		person (:class:`cruscoplanets.person.Person`): the person whose astrological data are represented in the chart.
		language (:class:`cruscoplanets.language_manager.LanguageManager`): the language (in ISO639-2 code) of the chart.
		birth (:class:`cruscoplanets.dates.Event`): the event of the person's birth
		birthEphemeris (:class:`ephemeris.Ephemeris`): the ephemeris of the person's birth
		birthAspects (tuple): the aspects of the birth event, as instances of :class:`cruscoplanets.aspects_parser.Aspect`
		xmldom (:class:`lxml.etree.ElementTree`): the XMLDom containing the svg representation of the chart
	"""
	
	def __init__(self, person: person.Person, language: language_manager.LanguageManager = None):
		super().__init__(person, language, transits=False)
		self.__buildSvg()
		
	def __buildSvg(self):
		if not self.birthEphemeris.isTimeUnknown:
			self._insertHouses()
		self._insertPersonalData()
		self._insertBirthPlanets()
		self._insertBirthAspects()
		self._insertAspectsGrid()
			
	@property
	def filename(self):
		return "%s_%s-birth_chart"%(self.person.name, self.person.surname)


	def __repr__(self):
		retstr = "Birth Chart of:\n\t%s\nEphemeris:%s"%(self.person, self.birthEphemeris)
		retstr += "\nAspects:"
		for aspect in self.birthAspects:
			retstr += "\n\t%s"%aspect
		return retstr
		
class TransitChart(Chart):
	"""Represents a transit chart.
	
	Args:
		person (:class:`cruscoplanets.person.Person`): the person whose astrological data are represented in the chart.
		transitEvent (:class:`cruscoplanets.dates.Event`): the transit event represented in the chart
		language (:class:`cruscoplanets.language_manager.LanguageManager`): the language (in ISO639-2 code) of the chart.

	Attributes:
		person (:class:`cruscoplanets.person.Person`): the person whose astrological data are represented in the chart.
		language (:class:`cruscoplanets.language_manager.LanguageManager`): the language (in ISO639-2 code) of the chart.
		birth (:class:`cruscoplanets.dates.Event`): the event of the person's birth
		birthEphemeris (:class:`ephemeris.Ephemeris`): the ephemeris of the person's birth
		birthAspects (tuple): the aspects of the birth event, as instances of :class:`cruscoplanets.aspects_parser.Aspect`
		transitAspects (tuple): the aspects between birth and traansit planets, as instances of :class:`cruscoplanets.aspects_parser.Aspect`
		xmldom (:class:`lxml.etree.ElementTree`): the XMLDom containing the svg representation of the chart
	"""
	
	def __init__(self, person: person.Person, transitEvent:dates.Event, language: language_manager.LanguageManager = None):
		self.__transit = transitEvent
		super().__init__(person, language, transits=True)
		self.transitEphemeris = ephemeris.Ephemeris(self.transit)
		aspectsParser = aspects.AspectsParser()
		myaspects = tuple(aspectsParser.parseTransitAspect(pair) for pair in self.transitPlanetsPairsIterator())
		self.transitAspects = tuple(filter(lambda x: x != None, myaspects))
		self.__buildSvg()

	def __buildSvg(self):
		if not self.birthEphemeris.isTimeUnknown:
			self._insertHouses()
		self._insertPersonalData()
		self._insertBirthPlanets()
		self._insertBirthAspects()
		self._buildTransitGraphics()

	def _buildTransitGraphics(self):
		self._insertAspectsGrid()
		self._addTransits()
		
	def updateTransit(self, new_event: dates.Event):
		"""Updates the chart modifying the transit event."""
		self.__deleteCurrentTransits()		
		self.transit = new_event
		self._insertTransitPersonalData()
		self._buildTransitGraphics()


	@property
	def transit(self):
		"""The transit event represented in the chart"""
		return self.__transit
	
	@transit.setter
	def transit(self, event: dates.Event):
		self.__transit = event
		self.transitEphemeris = ephemeris.Ephemeris(event)
		aspectsParser = aspects.AspectsParser()
		myaspects = tuple(aspectsParser.parseTransitAspect(pair) for pair in self.transitPlanetsPairsIterator())
		self.transitAspects = tuple(filter(lambda x: x != None, myaspects))

	def transitPlanetsPairsIterator(self):
		for i in range(len(self.birthEphemeris.planets)):
			for j in range(len(self.transitEphemeris.planets)):
				yield (self.birthEphemeris.planets[i], self.transitEphemeris.planets[j])

	def __deleteCurrentTransits(self):
		for i in range(len(ephemeris.Planet.NAMES)):
			#removing current coordinates from transits table:
			planet_symbol = self._getElementById('transit_' + ephemeris.Planet.NAMES[i] + '_symbol')
			planet_degree = self._getElementById('transit_' + ephemeris.Planet.NAMES[i] + '_degree')
			for child in planet_symbol:
				planet_symbol.remove(child)
			for child in planet_degree:
				planet_degree.remove(child)
			
			#removing transit planets and pointers from chart:
			planet_inner_pointer = self._getElementById("transit_%s_inner_angle"%ephemeris.Planet.NAMES[i])
			planet_outer_pointer = self._getElementById("transit_%s_outer_angle"%ephemeris.Planet.NAMES[i])
			planet_body_wrapper = self._getElementById("transit_%s_node_wrapper"%ephemeris.Planet.NAMES[i])
			planet_inner_pointer.getparent().remove(planet_inner_pointer)
			planet_outer_pointer.getparent().remove(planet_outer_pointer)
			planet_body_wrapper.getparent().remove(planet_body_wrapper)

		#removing event indications
		transit_date = self._getElementById('transit_date_and_time_field')
		transit_date.text = ""
		
		#removing aspect symbols from grid and transit aspect lines from chart
		for child in self.xmlroot.iter():
			if child.get("class") in ("grid_cell", "transit_aspect_line"):
				child.getparent().remove(child)

	@property
	def birthChart(self):
		"""Returns a :class:`cruscoplanets.charts.BirthChart` instance with *self.person* and *self.language* as arguments."""
		birthChart = BirthChart(self.person, self.languageManager.language)
		return birthChart
		
	def _insertPersonalData(self):
		super()._insertPersonalData()
		self._insertTransitPersonalData()

	def _insertTransitPersonalData(self):
		transit_word = self._getElementById('transit_word')
		transit_word.text = self.languageManager.expressions['transits_title']
		transit_date = self._getElementById('transit_date_and_time_field')
		transit_date.text = self.transit.dateAndTime

	def _makeTransitPlanetBody(self, planet: ephemeris.Planet):
		radius = self.svgBase.settings.ZODIAC_CIRCLE_RADIUS + self.svgBase.settings.TRANSIT_PLANETS_OFFSET

		planet_coordinates = utils.polarToCartesian(planet.figurePosition.decvalue, radius)
		planet_node = lxml.etree.Element("use")
		planet_node.set("{http://www.w3.org/1999/xlink}href", "#%s_template"%planet.name)
		planet_node.set("id","transit_%s_body"%planet.name)
		planet_node.set("x", "%f"%planet_coordinates[0])
		planet_node.set("y", "%f"%planet_coordinates[1])
		wrapper = lxml.etree.Element('g')
		wrapper.attrib.update({
			'id': "transit_%s_node_wrapper"%planet.name,
			'height': str(planet_node.get('height')),
			'width': str(planet_node.get('width'))
		})
		wrapper.append(planet_node)
		if planet.isRetrograde:
			retrograde_template = lxml.etree.Element('use')
			retrograde_template.attrib.update({
				'id': 'transit_%s_retrograde'%planet.name,
				"{http://www.w3.org/1999/xlink}href": "#retrograde_template",
				'x': "%f"%planet_coordinates[0],
				'y': "%f"%planet_coordinates[1],
				'fill': self.svgBase.settings["TRANSIT-%s_COLOR"%planet.name.upper()],
				'stroke': self.svgBase.settings["TRANSIT-%s_COLOR"%planet.name.upper()]
			})
			wrapper.append(retrograde_template)
		if not self.birthEphemeris.isTimeUnknown:
			self._addTransformation(planet_node, "rotate(-%f, %f, %f)"%(self.birthEphemeris.ascendant.position.decvalue, planet_coordinates[0], planet_coordinates[1]))
			if planet.isRetrograde:
				self._addTransformation(retrograde_template, "rotate(-%f, %f, %f)"%(self.birthEphemeris.ascendant.position.decvalue, planet_coordinates[0], planet_coordinates[1]))
		return wrapper

	def _makeOuterPlanetAngle(self, planet):
		planet_angle = lxml.etree.Element("path")
		planet_angle.set("id", "transit_%s_outer_angle"%planet.name)
		planet_angle_d = "M %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.ZODIAC_CIRCLE_RADIUS)
		planet_angle_d += " L %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.TRANSIT_POINTERS_RADIUS)
		planet_angle_color= self.svgBase.settings['%s_COLOR'%planet.name.upper()]
		planet_angle.set("d", planet_angle_d)
		planet_angle.set("stroke", planet_angle_color)
		planet_angle.set("stroke-width", str(self.svgBase.settings.ANGLE_POINTERS_WIDTH))
		return planet_angle

	def _makeInnerTransitPlanetAngle(self, planet: ephemeris.Planet):
		planet_angle = lxml.etree.Element("path")
		planet_angle.set("id", "transit_%s_inner_angle"%planet.name)
		planet_angle_d = "M %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.POINTERS_CIRCLE_RADIUS)
		planet_angle_d += " L %f %f"%utils.polarToCartesian(planet.eclipticLongitude.decvalue, self.svgBase.settings.HOUSES_CIRCLE_RADIUS)
		planet_angle_color= self.svgBase.settings['%s_COLOR'%planet.name.upper()]
		planet_angle.set("d", planet_angle_d)
		planet_angle.set("stroke", planet_angle_color)
		planet_angle.set("stroke-width", str(self.svgBase.settings.ANGLE_POINTERS_WIDTH))
		return planet_angle
		
	def _insertTransitPlanet(self, planet: ephemeris.Planet):
		planet_node = self._makeTransitPlanetBody(planet)
		planet_outer_angle = self._makeOuterPlanetAngle(planet)
		planet_inner_angle = self._makeInnerTransitPlanetAngle(planet)
		return (planet_node, planet_outer_angle, planet_inner_angle)

	def _insertTransitPlanets(self):
		planetsSetter = planets_setter.PlanetsSetter(self.transitEphemeris.planets)
		planets = planetsSetter.adjustPlanets()
		planets = tuple(self._insertTransitPlanet(planet) for planet in self.transitEphemeris.planets)
		for planet in planets:
			self.zodiacAndHousesNode.append(planet[0])#planet body
			self.zodiacAndHousesNode.append(planet[1])#planet outer angle
			self.zodiacAndHousesNode.append(planet[2])#planet inner angle
			
		for planet in self.transitEphemeris.planets:
			symbol_node = self._getElementById('transit_%s_symbol'%planet.name)
			planet_symbol = lxml.etree.SubElement(symbol_node, "use")
			planet_symbol.attrib.update({
				"{http://www.w3.org/1999/xlink}href": "#char-%s_template"%planet.name,
				"x": symbol_node.get('x'),
				"y": symbol_node.get('y')
			})
			self._adjustCharSize(planet_symbol, size=1.4*self.svgBase.settings.PLANETS_TABLE_FONT_SIZE)
			degree_node = self._getElementById('transit_%s_degree'%planet.name)
			self._insertZodiacAngle(degree_node, planet.eclipticLongitude)
		transit_table_title = self._getElementById('transits_table_title')
		transit_table_title.text = self.languageManager.expressions['transits_table_title']

	def _insertTransitAspects(self):
		for aspect in self.transitAspects:
			if aspect.name == "conjunction":
				aspect_node = self._buildConjunction(aspect)
			elif aspect.name == "opposition":
				aspect_node = self._buildOpposition(aspect)
			elif aspect.name == "trine":
				aspect_node = self._buildTrine(aspect)
			elif aspect.name == "square":
				aspect_node = self._buildSquare(aspect)
			elif aspect.name == "sextile":
				aspect_node = self._buildSextile(aspect)
			elif aspect.name == "semisextile":
				aspect_node = self._buildSemisextile(aspect)
			else:
				raise RuntimeError("Unrecognised aspect")
			aspect_id = "transit-aspect-" + aspect.identifier
			aspect_node.attrib['id'] = aspect_id
			aspect_node.attrib["class"] = "transit_aspect_line"
			self.zodiacAndHousesNode.append(aspect_node)

	def _addTransits(self):
		self._insertTransitPlanets()
		self._insertTransitAspects()		
	
	#overriding this function to insert transit aspects
	def _makePlanetInGrid(self, topleft_x, topleft_y, step, idnum):
		node = lxml.etree.Element('use')
		node.attrib.update({
			'x': str(topleft_x + 0.5*step),
			'y': str(topleft_y + 0.5*step),
			'width': str(step),
			'height': str(step),
			'{http://www.w3.org/1999/xlink}href': '#' + ephemeris.Planet.NAMES[idnum] + '_template'
		})
		return node	

	def _searchTransitAspect(self, planetInt1, planetInt2):
		all_aspects = tuple(filter(lambda aspect: aspect.planetsInts == (planetInt1, planetInt2), self.transitAspects))
		if len(all_aspects) > 0:
			return all_aspects[0]
		return None

	#overriding this function to insert transit aspects
	def _makeAspectInGrid(self, topleft_x, topleft_y, step, idnum1, idnum2):
		node = lxml.etree.Element('use')
		node.attrib.update({
			'x': str(topleft_x + 0.5*step),
			'y': str(topleft_y + 0.5*step),
			"class": "grid_cell",
			'width': str(step),
			'height': str(step),
		})
		aspect = self._searchTransitAspect(idnum2, idnum1)
		if aspect != None:
			node.attrib.update({
				'{http://www.w3.org/1999/xlink}href': '#' + aspect.name + '_template'
			})
		return node

	#overriding this function to insert transit aspects
	def _insertSymbolInGrid(self, topleft_x, topleft_y, step, idnum1, idnum2):
		if (idnum1 == 0 and idnum2 == 0):#voidCell
			return
		elif (idnum1 == 0 and idnum2 != 0):#birthPlanets
			node = self._makePlanetInGrid(topleft_x, topleft_y, step, idnum2-1)#decrement needed to get planet's id int
		elif (idnum1 != 0 and idnum2 == 0):#transitPlanets
			node = self._makePlanetInGrid(topleft_x, topleft_y, step, idnum1-1)#decrement needed to get planet's id int
		else:
			node = self._makeAspectInGrid(topleft_x, topleft_y, step, idnum1-1, idnum2-1)#decrement needed to get aspect's id int
		self.xmlroot.append(node)

	#overriding this function to insert transit aspects
	def _insertAspectsGrid(self):
		x0, y0 = self.svgBase.topLeftCoordinates
		x0, y0 = float(x0), float(y0)
		
		title_font_size = self.svgBase.settings.ASPECTS_GRID_TITLE_FONT_SIZE
		start_x = int(x0+self.svgBase.settings.ASPECTS_GRID_X_OFFSET+1.5*title_font_size)
		start_y = int(y0+self.svgBase.settings.ASPECTS_GRID_Y_OFFSET+1.5*title_font_size)
		step = int(self.svgBase.settings.ASPECTS_GRID_CELL_LENGTH)
		for i in range(12):
			for j in range(12):
				x = start_x + i*step
				y = start_y + j*step
				rect = lxml.etree.SubElement(self.xmlroot, 'rect')
				rect.attrib.update({
					'x': str(x),
					'y': str(y),
					'id': "aspect_cell_%d-%d"%(i, j),
					'width': str(step),
					'height': str(step),
					'fill': self.svgBase.settings.ASPECTS_GRID_FILL_COLOR,
					'stroke': self.svgBase.settings.ASPECTS_GRID_LINE_COLOR,
					'stroke-width': str(self.svgBase.settings.ASPECTS_GRID_LINE_WIDTH)
				})
				self._insertSymbolInGrid(x, y, step, i, j)

		text = lxml.etree.SubElement(rect, 'text')
		text = lxml.etree.SubElement(self.xmlroot, 'text')
		text.text = self.languageManager.expressions['transits_title']
		text.attrib.update({
			'font-size': str(title_font_size),
			'font-weight': self.svgBase.settings.ASPECTS_GRID_TITLE_FONT_WEIGHT,
			'font-family': self.svgBase.settings.FONT_FAMILY,
			'x': str(x0+self.svgBase.settings.ASPECTS_GRID_X_OFFSET + 6*self.svgBase.settings.ASPECTS_GRID_CELL_LENGTH),
			'y': str(y0+self.svgBase.settings.ASPECTS_GRID_Y_OFFSET),
			'style': 'text-align: center;'
		})
		text2 = lxml.etree.SubElement(self.xmlroot, 'text')
		text2.text = self.languageManager.expressions['planets_table_title']
		text2.attrib.update({
			'font-size': str(title_font_size),
			'font-weight': self.svgBase.settings.ASPECTS_GRID_TITLE_FONT_WEIGHT,
			'font-family': self.svgBase.settings.FONT_FAMILY,
			'x': str(x0+self.svgBase.settings.ASPECTS_GRID_X_OFFSET),
			'y': str(y0+self.svgBase.settings.ASPECTS_GRID_Y_OFFSET+1.5*title_font_size + 8*self.svgBase.settings.ASPECTS_GRID_CELL_LENGTH),
			'transform': 'rotate(-90, %f, %f)'%(
				x0+self.svgBase.settings.ASPECTS_GRID_X_OFFSET,
				y0+self.svgBase.settings.ASPECTS_GRID_Y_OFFSET+1.5*title_font_size-title_font_size + 8*self.svgBase.settings.ASPECTS_GRID_CELL_LENGTH
			),
			'style': 'text-align: center;'
		})

	@property
	def filename(self):
		return "%s_%s-transit_chart"%(self.person.name, self.person.surname)

	def __repr__(self):
		retstr = "Transit Chart of:\n\t%s\nEphemeris:%s"%(self.person, self.birthEphemeris)
		retstr += "\nBirth aspects:"
		for aspect in self.birthAspects:
			retstr += "\n\t%s"%aspect
		retstr += "\n\tTRANSITS for %s\n"%self.transit
		retstr += "\tbirth-transit"
		for transit in self.transitAspects:
			retstr += "\n\t%s"%transit
		return retstr
		
		
if __name__ == "__main__":
	import dates, location

	nardo = location.Location("Nardò", 40.1795300, 18.0317400)
	eventbuilder1 = dates.EventBuilder(1992, 12, 22, 19, 15, 00, nardo)
	event1 = eventbuilder1.getEventByTimeZone()
	person1 = person.Person("Diana", "Artemide", person.Person.FEMALE, event1)
	person1m = person.Person("Emiliano", "Minerba", person.Person.MALE, event1)
	birth_chart1 = BirthChart(person1, 'ita')
	birth_chart1m = BirthChart(person1m, 'eng')
#	print(birth_chart1)
#	print(birth_chart1m)

	event2 = dates.EventBuilder.now()
	transit_chart1 = TransitChart(person1, event2, 'ita')
	transit_chart1m = TransitChart(person1m, event2, 'eng')
	eventbuilder3 = dates.EventBuilder(2030, 12, 22, 19, 15, 00, nardo)
	event3 = eventbuilder3.getEventByTimeZone()
	print(event2)
	print(transit_chart1.transitEphemeris)
	transit_chart1.updateTransit(event3)
	print()
	print(event3)
	print(transit_chart1.transitEphemeris)

	
#	cecina = location.Location('Cecina', 40.306, 10.517)
#	eventbuilder2 = dates.EventBuilder(1994, 10, 2, 20, 30, 0, cecina)
#	event2 = eventbuilder2.getEventByTimeZone()
#	giulia = person.Person("Giulia", "Gronchi", person.Person.FEMALE, event2)
#	carta_giulia = BirthChart(giulia, 'ita')
#	carta_giulia.deploySvg()
	
#	mannheim = location.Location('Mannheim', 49.49, 8.47)
#	event = dates.EventBuilder(1993, 2, 6, 2, 0, 0, mannheim).getEventByTimeZone()
#	lukas = person.Person("Lukas", "Scherer", person.Person.MALE, event)
#	carta_lukas = BirthChart(lukas, 'ita')
#	carta_lukas.deployPng()
	
#	napoli = location.Location("Napoli", 40.8563100, 14.2464100)
#	pozzuoli = location.Location("Pozzuoli", 40.845947, 14.093286)
#	eventbuilder = dates.EventBuilder(1984, 7, 5, 0, 20, 0, napoli)
#	event3 = eventbuilder.getEventByTimeZone()
#	person2 = person.Person("Roberto", "Gaudioso", person.Person.MALE, event3)
#	transit_chart2 = TransitChart(person2, event2, 'ita')
#	transit_chart2.deploySvg()
#	transit_chart2.birthChart.deploySvg()

#	eventbuilder4 = dates.EventBuilder(1965, 3, 17, 12, 00, 00, nardo)
#	event4 = eventbuilder4.getEventByTimeZone()
#	person4 = person.Person("Patrizia", "Cardellicchio", person.Person.FEMALE, event4)
#	birth_chart4 = BirthChart(person4, 'ita')
#	transit_chart4 = TransitChart(person4, event2, 'ita')
#	birth_chart4.deploySvg()
#	transit_chart4.deploySvg()
