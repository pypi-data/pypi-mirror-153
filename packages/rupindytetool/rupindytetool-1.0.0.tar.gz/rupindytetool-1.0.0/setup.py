from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'tool Package made for a dyte task of its making for myawsometool by rupin patel'

setup(
		name ='rupindytetool',
		version ='1.0.0',
		author ='Rupin Patel',
		author_email ='patelrupin63@gmail.com',
		url ='https://github.com/patel-rupin2000/dyte_test',
		description ='Dyte task myawsometool by Rupin Patel.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'rupindytetool = rupindytetool.rupindytetool:main'
			]
		},
		classifiers =[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		],
		install_requires = requirements,
		zip_safe = False
)
