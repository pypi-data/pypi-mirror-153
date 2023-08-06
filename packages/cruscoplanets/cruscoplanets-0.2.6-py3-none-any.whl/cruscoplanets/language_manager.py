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
import os
import lxml.etree


class LanguageError(Exception):
	
	def __init__(self, expression, lang, default):
		super().__init__()
		self.expression = expression
		self.language = lang
		self.defaultLanguage = default
		
	def __str__(self):
		return "No correspondent found for expression id '%s' either in chosen language(%s) or in default language(%s)"%(self.expression, self.language, self.defaultLanguage)


class LanguageManager(metaclass=utils.PreventEqualInstances):
	"""Returns the strings of the text contents of charts in a given language. This class has :class:`utils.PreventEqualInstances` as metaclasses, that is, all calls with the same values as arguments will
	return the same instance.
	
	Args:
		language (str): the ISO639-2 code of the language that will be used for building the chart.
	
	Attributes:
		language (str): the ISO639-2 code of the language that will be used for building the chart.
		defaultlang (str): the ISO639-2 code of the default language as set in configuration. If an expression has not a translation for a certain text value, the one in the default language will be used.
		expressions (dict): a dictionary whose keys are the string ID of the text contents of the charts and the items are their versions in *language*, or *defaultlang* otherwise.
		
	Raises:
		LanguageError: raised if to certain string ID no version, either in the instance's language or in the default one, is found.
	"""

	LANGUAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "languages.xml")

	def __init__(self, language: str, /):
		langdata = lxml.etree.parse(self.__class__.LANGUAGE_FILE)
		if len(language) == 2:
			self.iso6391 = language
			try:
				language_node = tuple(filter(lambda node: node.get("iso-639-1") == self.iso6391, langdata.iter('languageName')))[0] 
			except IndexError:
				raise RuntimeError("Language '%s' is not (yet) supported"%language)
			self.iso6392 = language_node.attrib['iso-639-2']
		elif len(language) == 3:
			self.iso6392 = language
			try:
				language_node = tuple(filter(lambda node: node.get("iso-639-2") == self.iso6392, langdata.iter('languageName')))[0] 
			except IndexError:
				raise RuntimeError("Language '%s' is not (yet) supported"%language)
			self.iso6391 = language_node.attrib['iso-639-1']
		else:
			raise RuntimeError("Language codes must be either iso-639-1 or iso-639-2")
		self.language_name = language_node.get('lang_name')

		self.defaultlang = langdata.find('defaultLanguage').text
		self.expressions = {}
		expressions = langdata.iter('expression')
		for expression in expressions:
			expr_id = expression.get('id')
			expr_value = expression.find(self.iso6392).text
			if expr_value == None:
				expr_value = expression.find(self.defaultlang).text
			if expr_value == None:
				raise LanguageError(expr_id, self.language, self.defaultlang)
			self.expressions[expr_id] = expr_value

	@classmethod
	def getDefault(cls):
		"""Returns an instance of this class representing the default language."""
		langdata = lxml.etree.parse(cls.LANGUAGE_FILE)
		defaultlang = langdata.find('defaultLanguage').text
		return cls(defaultlang)
	
	@classmethod
	def listLanguages(cls):
		"""Returns a list of the iso-639-2 codes of all the supported languages, the first one being the default language"""
		langdata = lxml.etree.parse(cls.LANGUAGE_FILE)
		defaultlang = langdata.find('defaultLanguage').text
		retlist = [node.get("iso-639-2") for node in langdata.iter("languageName") if node.get("iso-639-2") != defaultlang]
		retlist.insert(0, defaultlang)
		return retlist	
			
	def __str__(self):
		retstr = '\tlanguage iso-639-1: ' + self.iso6391 + '\tlanguage iso-639-2: ' + self.iso6392 + '\n\tlanguage name: ' + self.language_name + '\n\tdefault language: ' + self.defaultlang + '\n'
		for key, value in sorted(self.expressions.items()):
			retstr += "\t" + key + " = " + value + '\n'
		return retstr
