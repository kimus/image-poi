#!/usr/bin/env python
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
	name = "image-poi",
	version = "1.0.1",

	packages = find_packages(),
	include_package_data=True,

	author = "Helder Rossa",
	author_email = "kimus.linuxus@gmail.com",
	description = "This project makes it possible to choose how an image will be cropped by sorl-thumbnail",
	long_description=README,

	license = "MIT License",
	url = "https://github.com/kimus/image-poi",

	platforms="any",

	classifiers = [
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries :: Application Frameworks',
	],
)
