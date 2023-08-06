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

from cruscoplanets import utils
import lxml.etree
from cruscoplanets import ephemeris
from cruscoplanets import svg_settings
import os

class SvgBase:
	"""This class prepares the base xml documents for the Birth and Transit Charts, which will be filled with the positions and aspects of the person and, optionally, the transit event."""

	TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg", "templates/")
	SVG_ROOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg", "root.svg")
		
	def __init__(self):
		self.settings = svg_settings.SvgSettings()
		self.templates = {}
		self.xmldom = lxml.etree.parse(self.__class__.SVG_ROOT_FILE)
		#setting width, height and viewbox
		self.xmlroot.attrib.update({"height": str(self.settings.IMAGE_HEIGHT), "width": str(self.settings.IMAGE_WIDTH), "viewBox": str(self.settings.IMAGE_VIEWBOX)})
		self.defs = lxml.etree.SubElement(self.xmlroot, "defs")
		
		#importing signs templates:
		for sign in (
			"aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
			"char-aries", "char-taurus", "char-gemini", "char-cancer", "char-leo", "char-virgo", "char-libra", "char-scorpio", "char-sagittarius", "char-capricorn", "char-aquarius", "char-pisces"
		):
			imported_template = self._importTemplate(sign)
			imported_template.attrib['stroke'] = self.settings["%s_SIGN_COLOR"%sign.upper()]
			imported_template.attrib['fill'] = self.settings["%s_SIGN_COLOR"%sign.upper()]

	
		#importing planets templates:
		for planet in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "eris",
						"char-sun", "char-moon", "char-mercury", "char-venus", "char-mars", "char-jupiter",
						"char-saturn", "char-uranus", "char-neptune", "char-pluto", "char-eris"
		):
			imported_template = self._importTemplate(planet)
			imported_template.attrib['stroke'] = self.settings["%s_COLOR"%planet.upper()]
			imported_template.attrib['fill'] = self.settings["%s_COLOR"%planet.upper()]
	
		#importing retrograde symbol template:
		self._importTemplate("retrograde")
	
		#importing aspects templates:
		for aspect in ("conjunction", "semisextile", "sextile", "square", "trine", "opposition"):
			imported_template = self._importTemplate(aspect)
			imported_template.attrib['stroke'] = self.settings["%s_COLOR"%aspect.upper()]
			imported_template.attrib['fill'] = self.settings["%s_COLOR"%aspect.upper()]
				
	def _importTemplate(self, template_name):
		with open(self.__class__.TEMPLATES_DIR + "%s.svg"%template_name, 'r') as template_file:
			doc = lxml.etree.parse(template_file)
			template = doc.xpath("//*[@class='symbol']")[0]
			self.defs.append(template)
			return template

	@property
	def xmlroot(self):
		return self.xmldom.getroot()
	
	def __buildZodiacCircle(self):
		aries = self.__createCircularSector(0, 30, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.ARIES_COLOR, idstring="aries")
		aries_symbol = self.__setTemplate("aries_template", 15, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		taurus = self.__createCircularSector(30, 60, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.TAURUS_COLOR, idstring="taurus")
		taurus_symbol = self.__setTemplate("taurus_template", 45, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		gemini = self.__createCircularSector(60, 90, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.GEMINI_COLOR, idstring="gemini")
		gemini_symbol = self.__setTemplate("gemini_template", 75, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		cancer = self.__createCircularSector(90, 120, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.CANCER_COLOR, idstring="cancer")
		cancer_symbol = self.__setTemplate("cancer_template", 105, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		leo = self.__createCircularSector(120, 150, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.LEO_COLOR, idstring="leo")
		leo_symbol = self.__setTemplate("leo_template", 135, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		virgo = self.__createCircularSector(150, 180, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.VIRGO_COLOR, idstring="virgo")
		virgo_symbol = self.__setTemplate("virgo_template", 165, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		libra = self.__createCircularSector(180, 210, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.LIBRA_COLOR, idstring="libra")
		libra_symbol = self.__setTemplate("libra_template", 195, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		scorpio = self.__createCircularSector(210, 240, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.SCORPIO_COLOR, idstring="scorpio")
		scorpio_symbol = self.__setTemplate("scorpio_template", 225, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		sagittarius = self.__createCircularSector(240, 270, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.SAGITTARIUS_COLOR, idstring="sagittarius")
		sagittarius_symbol = self.__setTemplate("sagittarius_template", 255, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		capricorn = self.__createCircularSector(270, 300, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.CAPRICORN_COLOR, idstring="capricorn")
		capricorn_symbol = self.__setTemplate("capricorn_template", 285, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		aquarius = self.__createCircularSector(300, 330, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.AQUARIUS_COLOR, idstring="aquarius")
		aquarius_symbol = self.__setTemplate("aquarius_template", 315, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)

		pisces = self.__createCircularSector(330, 360, self.settings.ZODIAC_CIRCLE_RADIUS, self.settings.PISCES_COLOR, idstring="pisces")
		pisces_symbol = self.__setTemplate("pisces_template", 345, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.ZODIAC_SIGNS_OFFSET)
		
		zodiacCircleNode = lxml.etree.Element('g', id="zodiac_circle")
		for node in (aries, aries_symbol, 
						taurus, taurus_symbol, 
						gemini, gemini_symbol,
						cancer, cancer_symbol,
						leo, leo_symbol,
						virgo, virgo_symbol,
						libra, libra_symbol,
						scorpio, scorpio_symbol,
						sagittarius, sagittarius_symbol,
						capricorn, capricorn_symbol,
						aquarius, aquarius_symbol,
						pisces, pisces_symbol,
					):
			zodiacCircleNode.append(node)
		return zodiacCircleNode
	
	def __setTemplate(self, template_id, angle, radius, rotate=True):
		coordinates = utils.polarToCartesian(angle, radius)
		rotate_attr = 'rotate(%f, %f, %f)'%(270-angle, coordinates[0], coordinates[1])
		use_node = lxml.etree.Element("use")
		use_node.attrib.update({'{http://www.w3.org/1999/xlink}href': '#' + template_id, 'x': '%f'%coordinates[0], 'y': '%f'%coordinates[1], 'transform': rotate_attr})
		return use_node
	
	@property
	def topLeftCoordinates(self):
		return tuple(self.settings.IMAGE_VIEWBOX.split(' ')[0:2])
	
	@property
	def bottomRightCoordinates(self):
		return tuple(self.settings.IMAGE_VIEWBOX.split(' ')[2:4])
		
	def __buildBackgroundColorNode(self):#BACKGROUND_COLOR
		node = lxml.etree.Element('rect')
		x0, y0 = self.topLeftCoordinates
		node.attrib.update({
			'x': x0, 
			'y': y0, 
			"height": str(self.settings.IMAGE_HEIGHT), 
			"width": str(self.settings.IMAGE_WIDTH), 
			"viewBox": str(self.settings.IMAGE_VIEWBOX), 
			"fill": self.settings.BACKGROUND_COLOR
		})
		return node
		
	def __createCircularSector(self, start_degree, end_degree, radius, fill_color, idstring=None):
		startpoint = utils.polarToCartesian(start_degree, radius)
		endpoint = utils.polarToCartesian(end_degree, radius)
		x_axis_rotation = 0
		large_arc_flag = 0
		sweep_flag = 0
		path_d = "M 0 0 L %f %f A %f %f %d %d %d %f %f Z"%(startpoint[0], startpoint[1], radius, radius, x_axis_rotation, large_arc_flag, sweep_flag, endpoint[0], endpoint[1])
		path_node = lxml.etree.Element("path")
		path_node.attrib.update({'d': path_d, 'fill': fill_color, 'fill-opacity': str(self.settings.ZODIAC_OPACITY)})
		if idstring != None:
			path_node.attrib['id'] = idstring
		return path_node
	
	def __buildOuterBorder(self):
		node = lxml.etree.Element('circle')
		attrib_dict = {
			'cx': "0", 
			'cy': "0", 
			'r': "%f"%self.settings.ZODIAC_CIRCLE_RADIUS, 
			'stroke': "%s"%self.settings.OUTER_BORDER_COLOR, 
			'fill-opacity': "0", 'stroke-width': "%f"%self.settings.OUTER_BORDER_WIDTH
		}
		node.attrib.update(attrib_dict)
		return node

	def __buildDegreeCircle(self):
		sweep_flag = 0
		path = []
		startpoint = utils.polarToCartesian(0, self.settings.HOUSES_CIRCLE_RADIUS)
		path.append("M %f %f"%startpoint)
		for i in range(360):
			if i % 10 == 0:
				end_line = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.TENTH_DEGREE_LINE)
				path.append("L %f %f"%end_line)
				come_back = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS)
				path.append("L %f %f"%come_back)
			elif i % 5 == 0:
				end_line = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.FIFTH_DEGREE_LINE)
				path.append("L %f %f"%end_line)
				come_back = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS)
				path.append("L %f %f"%come_back)
			else:
				end_line = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS + self.settings.DEGREE_LINE)
				path.append("L %f %f"%end_line)
				come_back = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS)
				path.append("L %f %f"%come_back)
			next_point = utils.polarToCartesian(i+1, self.settings.HOUSES_CIRCLE_RADIUS)
			path.append("A %f %f 0 0 %d %f %f"%(self.settings.HOUSES_CIRCLE_RADIUS, self.settings.HOUSES_CIRCLE_RADIUS, sweep_flag, next_point[0], next_point[1]))
		path = ' '.join(path)
		node = lxml.etree.Element('path')
		attrib_dict = {
			'id': 'degree_circle', 
			'stroke': self.settings.DEGREES_CIRCLE_COLOR, 
			'fill': self.settings.DEGREES_CIRCLE_FILL_COLOR, 
			'stroke-opacity': str(self.settings.DEGREES_CIRCLE_OPACITY), 
			'd': path
		}
		node.attrib.update(attrib_dict)
		return node
	
	def __buildAspectsCircle(self):
		node = lxml.etree.Element('circle')
		node.attrib.update({
			'cx': '0',
			'cy': '0',
			'r': "%f"%self.settings.ASPECTS_CIRCLE_RADIUS,
			"stroke": "%s"%self.settings.ASPECTS_CIRCLE_COLOR,
			"fill": "%s"%self.settings.ASPECTS_CIRCLE_FILL_COLOR,
			'stroke-opacity': str(self.settings.ASPECTS_CIRCLE_OPACITY)
		})
		return node
	
	def __buildSignBorders(self):
		lines_list = []
		for i in range(0, 360, 30):
			start = utils.polarToCartesian(i, self.settings.HOUSES_CIRCLE_RADIUS)
			end = utils.polarToCartesian(i, self.settings.ZODIAC_CIRCLE_RADIUS)
			node = lxml.etree.Element("line", x1="%f"%start[0], y1="%f"%start[1], x2="%f"%end[0], y2="%f"%end[1], stroke=self.settings.SIGN_BORDERS_COLOR)
			node.set("stroke-width", "%f"%self.settings.SIGN_BORDERS_WIDTH)
			lines_list.append(node)
		return tuple(lines_list)
	
	def __buildZodiacAndHousesG(self):
		node = lxml.etree.Element('g', id="zodiac_and_houses")
		node.append(self.__buildZodiacCircle())
		node.extend(self.__buildSignBorders())
		node.append(self.__buildOuterBorder())
		node.append(self.__buildDegreeCircle())
		node.append(self.__buildAspectsCircle())
		return node
	
	def __buildPersonalDataField(self, transit: bool=False):
		wrapper = lxml.etree.Element('g')

		x0, y0 = self.topLeftCoordinates
		x0, y0 = float(x0), float(y0)

		rect = lxml.etree.Element('rect')
		rect.attrib.update({
			'id': "personaldatarect",
			'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET),
			'y': str(y0+self.settings.PERSONAL_DATA_Y_OFFSET),
			'width': str(self.settings.PERSONAL_DATA_WIDTH),
			'height': str(self.settings.PERSONAL_DATA_HEIGHT),
			'stroke': self.settings.PERSONAL_DATA_BORDER_COLOR,
			'fill': self.settings.PERSONAL_DATA_FILL_COLOR,
			'font-family': self.settings.FONT_FAMILY
		})
		#wrapper.append(rect)

		node = lxml.etree.SubElement(wrapper, 'text')
		node.attrib.update({
			'id': "personaldata",
			'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET),
			'y': str(y0+self.settings.PERSONAL_DATA_Y_OFFSET),
			'width': str(self.settings.PERSONAL_DATA_WIDTH),
			'height': str(self.settings.PERSONAL_DATA_HEIGHT),
			'font-size': str(self.settings.PERSONAL_DATA_FONT_SIZE),
			'font-weight': self.settings.PERSONAL_DATA_FONT_WEIGHT,
			'fill': self.settings.PERSONAL_DATA_FONT_COLOR
		})
		namefield = lxml.etree.SubElement(node, "tspan")
		namefield.attrib.update({'id': 'name_field', 'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET), 'y': str(y0+self.settings.PERSONAL_DATA_FONT_SIZE+self.settings.PERSONAL_DATA_Y_OFFSET)})
		locationfield = lxml.etree.SubElement(node, "tspan")
		locationfield.attrib.update({'id': 'location_field', 'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET), 'dy': '%f'%(1.5*self.settings.PERSONAL_DATA_FONT_SIZE)})
		datefield = lxml.etree.SubElement(node, "tspan")
		datefield.attrib.update({'id': 'date_and_time_field', 'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET), 'dy': '%f'%(1.5*self.settings.PERSONAL_DATA_FONT_SIZE)})
		if transit:
			transitword = lxml.etree.SubElement(node, "tspan")
			transitword.attrib.update({'id': 'transit_word', 'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET), 'dy': '%f'%(1*1.5*self.settings.PERSONAL_DATA_FONT_SIZE)})
			transitdatefield = lxml.etree.SubElement(node, "tspan")
			transitdatefield.attrib.update({'id': 'transit_date_and_time_field', 'x': str(x0+self.settings.PERSONAL_DATA_X_OFFSET), 'dy': '%f'%(1.5*self.settings.PERSONAL_DATA_FONT_SIZE)})
		return wrapper
	
	def __buildPlanetsTable(self, transit: bool=False):

		x0, y0 = self.topLeftCoordinates
		x0, y0 = float(x0), float(y0)
		
		x = x0 + self.settings.PLANETS_TABLE_X_OFFSET
		y = y0 + self.settings.PLANETS_TABLE_Y_OFFSET

		#we adjust coordinates for transit tables (where tables need to be lowered)
		if transit:
			y += 2*self.settings.PERSONAL_DATA_FONT_SIZE

		table_node = lxml.etree.Element('g')
		table_node.attrib.update({
			'id': "planets-table",
			'x': str(x),
			'y': str(y),
			'width': str(self.settings.PLANETS_TABLE_WIDTH),
			'height': str(11*1.5*self.settings.PLANETS_TABLE_FONT_SIZE),
		})
		planets_table_title = lxml.etree.SubElement(table_node, 'text')
		planets_table_title.attrib.update({
			'x': str(x),
			'y': str(y),
			'id': 'planets_table_title',
			'width': str(self.settings.PLANETS_TABLE_WIDTH),
			'height': str(1.5*self.settings.PLANETS_TABLE_FONT_SIZE),
			'fill': self.settings.PLANETS_TABLE_FONT_COLOR,
			'font-size': str(self.settings.PLANETS_TABLE_FONT_SIZE),
			'font-weight': self.settings.PLANETS_TABLE_FONT_WEIGHT,
			'font-family': self.settings.FONT_FAMILY
		})
		for i in range(11):
			planet_node = lxml.etree.SubElement(table_node, 'g')
			planet_node.attrib.update({
				'x': str(x),
				'y': str(y+1.5*(i+1)*self.settings.PLANETS_TABLE_FONT_SIZE),#i+1 for not overlapping the first row with the table title
				'id': ephemeris.Planet.NAMES[i] + '_symbol'
			})
			degree_node = lxml.etree.SubElement(table_node, 'g')
			degree_node.attrib.update({
				'id': ephemeris.Planet.NAMES[i] + '_degree',
				'x': str(x + self.settings.PLANETS_TABLE_CELL_LENGTH),
				'y': str(y + 1.5*(i+1)*self.settings.PLANETS_TABLE_FONT_SIZE),#i+1 for not overlapping the first row with the table title
			})

		return table_node	

	def __buildHousesTable(self, transit: bool=False):

		x0, y0 = self.topLeftCoordinates
		x0, y0 = float(x0), float(y0)
		x = x0 + self.settings.HOUSES_TABLE_X_OFFSET
		y = y0 + self.settings.HOUSES_TABLE_Y_OFFSET
		#we adjust coordinates for transit tables (where tables need to be lowered)
		if transit:
			y += 2*self.settings.PERSONAL_DATA_FONT_SIZE

		table_node = lxml.etree.Element('g')
		table_node.attrib.update({
			'id': "houses-table",
			'x': str(x),
			'y': str(y),
			'width': str(self.settings.HOUSES_TABLE_WIDTH),
			'height': str(12*1.5*self.settings.HOUSES_TABLE_FONT_SIZE),
			'fill': self.settings.HOUSES_TABLE_FONT_COLOR,
			'font-size': str(self.settings.HOUSES_TABLE_FONT_SIZE),
			'font-weight': self.settings.HOUSES_TABLE_FONT_WEIGHT,
			'font-family': self.settings.FONT_FAMILY
		})
		houses_table_title = lxml.etree.SubElement(table_node, 'text')
		houses_table_title.attrib.update({
				'x': str(x),
				'y': str(y),
				'id': 'houses_table_title'
		})
		for i in range(12):
			house_node = lxml.etree.SubElement(table_node, 'text')
			house_node.attrib.update({
				'x': str(x),
				'y': str(y + (i+1)*1.5*self.settings.HOUSES_TABLE_FONT_SIZE),
				'id': ephemeris.House.SYMBOLS[i] + '_house_symbol'
			})
			degree_node = lxml.etree.SubElement(table_node, 'g')
			degree_node.attrib.update({
				'id': ephemeris.House.SYMBOLS[i] + '_house_degree',
				'x': str(x + self.settings.HOUSES_TABLE_CELL_LENGTH),
				'y': str(y + (i+1)*1.5*self.settings.HOUSES_TABLE_FONT_SIZE),
			})
		return table_node	

	def __buildTransitsTable(self):

		x0, y0 = self.topLeftCoordinates
		x0, y0 = float(x0), float(y0)
		x = x0 + self.settings.TRANSITS_TABLE_X_OFFSET
		y = y0 + self.settings.TRANSITS_TABLE_Y_OFFSET
		y += 2*self.settings.PERSONAL_DATA_FONT_SIZE

		table_node = lxml.etree.Element('g')
		table_node.attrib.update({
			'id': "transits_table",
			'x': str(x),
			'y': str(y),
			'width': str(self.settings.TRANSITS_TABLE_WIDTH),
			'height': str(11*1.5*self.settings.TRANSITS_TABLE_FONT_SIZE),
			'fill': self.settings.TRANSITS_TABLE_FONT_COLOR,
			'font-size': str(self.settings.TRANSITS_TABLE_FONT_SIZE),
			'font-weight': self.settings.TRANSITS_TABLE_FONT_WEIGHT,
			'font-family': self.settings.FONT_FAMILY
		})
		transits_table_title = lxml.etree.SubElement(table_node, 'text')
		transits_table_title.attrib.update({
				'x': str(x),
				'y': str(y),
				'id': 'transits_table_title'
		})
		for i in range(len(ephemeris.Planet.NAMES)):
			planet_node = lxml.etree.SubElement(table_node, 'g')
			planet_node.attrib.update({
				'x': str(x),
				'y': str(y + (i+1)*1.5*self.settings.TRANSITS_TABLE_FONT_SIZE),
				'id': 'transit_' + ephemeris.Planet.NAMES[i] + '_symbol'
			})
			degree_node = lxml.etree.SubElement(table_node, 'g')
			degree_node.attrib.update({
				'id': 'transit_' + ephemeris.Planet.NAMES[i] + '_degree',
				'x': str(x + self.settings.TRANSITS_TABLE_CELL_LENGTH),
				'y': str(y + (i+1)*1.5*self.settings.TRANSITS_TABLE_FONT_SIZE)
			})
		return table_node	

	def __repr__(self):
		return self.settings.__repr__()
		
	def buildBaseBirthXml(self):
		"""Builds the xml document representing the base of a Birth Chart.
		
		Returns:
			self.xmldom (lxml.etree.ElementTree): the object representing the DOM of the svg code of the base of the Birth Chart.
		"""
		self.xmlroot.append(self.__buildBackgroundColorNode())
		self.xmlroot.append(self.__buildPersonalDataField())
		self.xmlroot.append(self.__buildPlanetsTable())
		self.xmlroot.append(self.__buildHousesTable())
		self.xmlroot.append(self.__buildZodiacAndHousesG())
		return self.xmldom
		
	def buildBaseTransitXml(self):
		"""Builds the xml document representing the base of a Transit Chart.
		
		Returns:
			self.xmldom (lxml.etree.ElementTree): the object representing the DOM of the svg code of the base of the Transit Chart.
		"""
		self.xmlroot.append(self.__buildBackgroundColorNode())
		self.xmlroot.append(self.__buildPersonalDataField(transit=True))
		self.xmlroot.append(self.__buildPlanetsTable(transit=True))
		self.xmlroot.append(self.__buildHousesTable(transit=True))
		self.xmlroot.append(self.__buildZodiacAndHousesG())
		self.xmlroot.append(self.__buildTransitsTable())
		return self.xmldom

if __name__ == '__main__':
	svgfigures = SvgBase()
	print(svgfigures)
	svgfigures.buildBaseBirthXml().write("svg/birth-zodiac.svg", pretty_print=True)
	svgfigures.buildBaseTransitXml().write("svg/transit-zodiac.svg", pretty_print=True)
