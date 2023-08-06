from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()


setup(
		name ='VM for Dyte',
		version ='1.0.0',
		author ='Aayush Chodvadiya',
		author_email ='auc1607@gmail.com',
		url ='https://github.com/dyte-submissions/dyte-vit-2022-aayush1607',
		description ='A simple lightweight cli tool that checks and updates dependency versions on all your node js github repos.',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'vm = vmtool.vm:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"Operating System :: OS Independent",
		),
		install_requires = requirements,
		zip_safe = False
)
