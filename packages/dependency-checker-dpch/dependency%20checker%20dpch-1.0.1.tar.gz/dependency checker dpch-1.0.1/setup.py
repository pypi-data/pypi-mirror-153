from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'CLI tool for dependency checker'

setup(
		name ='dependency checker dpch',
		version ='1.0.1',
		author ='Jevin Vekaria',
		author_email ='jevin925@gmail.com',
		url ='https://github.com/dyte-submissions/dyte-vit-2022-jevin925',
		description ='Dependency checker for nodeJS',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'dpch = dependency_checker.dpch:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='python package',
		install_requires = requirements,
		zip_safe = False
)
