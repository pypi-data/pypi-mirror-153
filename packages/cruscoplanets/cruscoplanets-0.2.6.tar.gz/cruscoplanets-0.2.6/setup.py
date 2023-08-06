import os
import setuptools

if __name__ == '__main__':
	with open("README.md", 'r') as long_file:
		long_descript = long_file.read()
	setuptools.setup(
		name='cruscoplanets',
		version='0.2.6',
		packages=setuptools.find_packages(exclude=['tests']),
		entry_points={
			'console_scripts': [
				'cruscoplanets = cruscoplanets.cmdline:main',
			],
		},
		install_requires=[
			'wheel',
			'backports.zoneinfo>=0.2.1',
			'lxml>=4.7.1',
			'pyvips>=2.1.16',
			'pyswisseph',
			'timezonefinder',
		],
		tests_require=['pytest'],
		package_data={
		'': [
				'README.md'
			],
		'cruscoplanets': [
				'config/*', 
				'databases/geonames.sql', 
				'pyswisseph_files/*.se1', 
				'svg/templates/*.svg',
				'svg/root.svg'
			]
		},
		author='Emiliano Minerba',
		author_email='emi.nerba@gmail.com',
		description="Graphic editor for Morpurgo's dialectic astrology",
		long_description=long_descript,
		long_description_content_type='text/markdown',
		license='GPL',
		url='https://gitlab.com/kikulacho92/cruscoplanets',
	)
