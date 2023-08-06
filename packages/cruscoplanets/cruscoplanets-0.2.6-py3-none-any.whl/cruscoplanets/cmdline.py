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

from cruscoplanets import location
from cruscoplanets import person
from cruscoplanets import dates
from cruscoplanets import charts
from cruscoplanets import chart_printer
from cruscoplanets import language_manager
import argparse

def searchLocation(name: str):
	return location.Location.fromCityName(name)

def doBirthChart(
	birthdateandtime: str, locationid: int, 
	pname: str = '', psurname: str = '', psex:int = -1, 
	outputdir: str = '.', outputformat: str = 'svg', language: str = None
):
	try:
		birthplace = location.Location.searchLocationFromGeonamesDatabase(locationid)
	except location.MissingDefaultLocationError:
		print("FATAL ERROR: A default location has not yet been set. Do it using the 'search_location' and 'set_default_location' commands")
		return
	birthevent = dates.EventBuilder.buildEvent(birthdateandtime, birthplace)
	theperson = person.Person(pname, psurname, psex, birthevent)
	thechart = charts.BirthChart(theperson, language)
	chartprinter = chart_printer.ChartPrinter(thechart)
	chartprinter.deployinFormat(outputdir, outputformat)

def doTransitChart(
	birthdateandtime: str, birthlocationid: int, 
	transitdateandtime: str, transitlocationid: int, 
	pname: str = '', psurname: str = '', psex:int = -1, 
	outputdir: str = '.', outputformat: str = 'svg', language: str = None
):
	try:
		birthplace = location.Location.searchLocationFromGeonamesDatabase(birthlocationid)
		transitplace = location.Location.searchLocationFromGeonamesDatabase(transitlocationid)
	except location.MissingDefaultLocationError:
		print("FATAL ERROR: A default location has not yet been set. Do it using the 'search_location' and 'set_default_location' commands")
		return
	birthevent = dates.EventBuilder.buildEvent(birthdateandtime, birthplace)
	transitevent = dates.EventBuilder.buildEvent(transitdateandtime, transitplace)
	theperson = person.Person(pname, psurname, psex, birthevent)
	thechart = charts.TransitChart(theperson, transitevent, language)
	chartprinter = chart_printer.ChartPrinter(thechart)
	chartprinter.deployinFormat(outputdir, outputformat)

def main():

	#I collect here the supported languages:
	langlist = language_manager.LanguageManager.listLanguages()

	parser = argparse.ArgumentParser(prog="cruscoplanets")
	subparsers = parser.add_subparsers(help="the operation to perform", dest="operation")

	list_supported_languages = subparsers.add_parser("list_languages", help="list the iso-639-2 codes of the supported languages, the first being the default one")

	search_location = subparsers.add_parser("search_location", help="search id of a location")
	search_location.add_argument('name', type=str, help="The name of the searched location")

	get_default_location = subparsers.add_parser("get_default_location", help="get data of the default location")
	
	set_default_location = subparsers.add_parser("set_default_location", help="set a new default location by its id")
	set_default_location.add_argument('location_id', type=int, help="the id of the location to set as default")
	
	birth_chart_builder = subparsers.add_parser("birth_chart", help="build a Birth Chart")
	birth_chart_builder.add_argument('--birthtime', type=str, help='birth date in [L|U]YYYY-MM-DD[-hh-mm-ss|![hh-mm-ss]] format (see documentation)')
	birth_chart_builder.add_argument('--name', type=str, help="The subject's first name(s)")
	birth_chart_builder.add_argument('--surname', type=str, help="The subject's surname")
	birth_chart_builder.add_argument('--sex', type=str, help="The subject's sex", choices = ['male', 'female', 'undefined'], default='undefined')
	birth_chart_builder.add_argument('--birthlocation', type=int, help="The id of the birth place (see the `get_location` command). If omitted, default location will be employed.", default=-1)
	birth_chart_builder.add_argument('--language', type=str, help="The language to produce the chart within", choices= langlist, default=langlist[0])
	birth_chart_builder.set_defaults(output_dir='.')
	birth_chart_builder.add_argument('--format', type=str, help="file's format", default = 'svg', choices= ['svg', 'png', 'jpeg'])
	birth_chart_builder.add_argument('--output_dir', type=str, help="the path of the directory where the file will be stored", default = '.')
	
	transit_chart_builder = subparsers.add_parser("transit_chart", help="build a Transit Chart")
	transit_chart_builder.add_argument('--birthtime', type=str, help='birth date in [L|U]YYYY-MM-DD[-hh-mm-ss|![hh-mm-ss]] format (see documentation)')
	transit_chart_builder.add_argument('--transittime', type=str, help='transit date in [L|U]YYYY-MM-DD[-hh-mm-ss|![hh-mm-ss]] format (see documentation). If you need the transits for the current moment, insert `now` as value')
	transit_chart_builder.add_argument('--name', type=str, help="The subject's first name(s)")
	transit_chart_builder.add_argument('--surname', type=str, help="The subject's surname")
	transit_chart_builder.add_argument('--sex', type=str, help="The subject's sex", choices = ['male', 'female', 'undefined'], default='undefined')
	transit_chart_builder.add_argument('--birthlocation', type=int, help="The id of the birth place (see the `get_location` command). If omitted, default location will be employed.", default=-1)
	transit_chart_builder.add_argument('--transitlocation', type=int, help="The id of the transits place (see the `get_location` command). If omitted, default location will be employed.", default=-1)
	transit_chart_builder.add_argument('--language', type=str, help="The language to produce the chart within", choices= langlist, default=langlist[0])
	transit_chart_builder.set_defaults(output_dir='.')
	transit_chart_builder.add_argument('--format', type=str, help="file's format", default = 'svg', choices= ['svg', 'png', 'jpeg'])
	transit_chart_builder.add_argument('--output_dir', type=str, help="the path of the directory where the file will be stored", default = '.')

	args = parser.parse_args()
	if args.operation == "list_languages":
		print(' '.join(langlist))
	if args.operation == "search_location":
		results = searchLocation(args.name)
		print('id', 'name', 'country', 'timezone', 'latitude', 'longitude', sep='\t')
		for result in results:
			print(result['id'], result['name'], result['country'], result['timezone'], result['latitude'], result['longitude'], sep='\t')
	if args.operation == "get_default_location":
		try:
			defloc = location.Location.default()
		except location.MissingDefaultLocationError:
			print("FATAL ERROR: A default location has not yet been set. Do it using the 'search_location' and 'set_default_location' commands")
			return
		defloc_id = int(location.LocationConfiguration().DEFAULT_LOCATION_ID)
		print("Default location id: %d.\n%s"%(defloc_id, defloc))
	if args.operation == "set_default_location":
		location.Location.setDefault(args.location_id)
		print("Default location successfully changed.")
		
	if args.operation == "birth_chart":
		if args.sex == 'male':
			sex_int = 0
		elif args.sex == 'female':
			sex_int = 1
		else:
			sex_int = -1
		doBirthChart(args.birthtime, args.birthlocation, args.name, args.surname, sex_int, args.output_dir, args.format, args.language)
	if args.operation == "transit_chart":
		if args.sex == 'male':
			sex_int = 0
		elif args.sex == 'female':
			sex_int = 1
		else:
			sex_int = -1
		doTransitChart(
			args.birthtime, args.birthlocation, args.transittime, args.transitlocation,
			args.name, args.surname, sex_int, args.output_dir, args.format, args.language
		)
			
		
if __name__ == '__main__':
	main()
