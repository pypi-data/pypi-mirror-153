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

import csv, math
import lxml.etree

def add180(angle):
	if angle >= 180:
		retvalue = angle - 180
	else:
		retvalue = angle + 180
	return retvalue

def polarToCartesian(myangle:float, radius:float):
	angle = add180(myangle)
	rad_angle = math.radians(angle)
	x = radius*math.cos(rad_angle)
	y = radius*math.sin(rad_angle)
	return (x, -y)#negative y is due to the fact that svg ordinates are positive towards the bottom of the screen


def lineByPolarCoordinates(angle1, radius1, angle2, radius2):
	coor1 = polarToCartesian(angle1, radius1)
	coor2 = polarToCartesian(angle2, radius2)
	new_line = lxml.etree.Element('line')
	attrib_dict = {'x1': '%f'%coor1[0], 'y1': '%f'%coor1[1], 'x2': '%f'%coor2[0], 'y2': '%f'%coor2[1]}
	new_line.attrib.update(attrib_dict)
	return new_line
	
def drawArc(start, end, radius, large_flag=False):
	"""Draws an arc of a circonference, from angle `start` to angle `end`, centred on the origin."""
	start_coor = polarToCartesian(start, radius)
	end_coor = polarToCartesian(end, radius)
	path_d = "M %f %f"%start_coor
	sweep_flag = 0
	if large_flag:
		large_flag_int = 1
	else:
		large_flag_int = 0
	path_d += " A %f %f 0 %d %d %f %f"%(radius, radius, large_flag_int, sweep_flag, end_coor[0], end_coor[1])
	path = lxml.etree.Element('path')
	path.attrib['d'] = path_d
	return path


class Singleton(type):
	"""Metaclass that implements the singleton design pattern."""

	__instances = None

	def __call__(cls, *args, **kwargs):
		if cls.__instances == None:
			cls.__instances = super().__call__(*args, **kwargs)
		return cls.__instances
		
class PreventEqualInstances(type):
	"""Metaclass that implements a design pattern similar to the Singleton: if a class has this metaclass, any call to it with the same positional and keywords arguments will always return the same 
	instance.

	In order to make this class work properly, it is recommended that one forces the class to accept only positional or keywords arguments; in fact, if one calls a class with this metaclass passing the 
	same value to the same argument, once as positional and once as keywords one, one would obtain two different instances.
	"""
	__instances = {}
	
	def __call__(cls, *args, **kwargs):
		kwargs_tuple = tuple(sorted(kwargs.items()))
		arguments = (args, kwargs_tuple)
		if arguments not in cls.__instances.keys():
			cls.__instances[arguments] = super().__call__(*args, **kwargs)
		return cls.__instances[arguments]
		
def parseCSV(filepath):
	with open(filepath, 'r') as csvfile:
		content = csv.reader(csvfile)
		content = tuple(tuple(element.strip() for element in line) for line in content)
	return content

def parseBanalConfig(filepath):
	"""parses configuration files organised in key = value format"""
	with open(filepath, 'r') as configfile:
		config = configfile.readlines()
	for i in range(len(config)):
		comment_index = config[i].find('!')
		if comment_index != -1:
			config[i] = config[i][:comment_index]

	config = list(filter(lambda line: '=' in line, config))
	for i in range(len(config)):
		config[i] = config[i].split("=")
		config[i][0], config[i][1] = config[i][0].strip(), config[i][1].strip()
		if config[i][1] == 'None':
			config[i][1] = None
		config[i] = tuple(config[i])
	return tuple(config)

def buildBanalConfig(pairs_sequence):
	"""Reverse of *parseBanalConfig*. Takes as argument a sequence of tuples of two values and returns a string where each row is occupied by the items of one pair in the following format: el1 = el2.
	If stored in a file, this string can be parsed again with *parseBanalConfig*.
	"""
	values = tuple("%s = %s"%(pair[0], str(pair[1])) for pair in pairs_sequence)
	return '\n'.join(values)
	


