import os

from setuptools import setup


setup(
	name = 'ql-cq',
	author = 'Quantlane',
	author_email = 'code@quantlane.com',
	version = open('version.txt').read().strip(),
	url = 'https://gitlab.com/quantlane/meta/cq',
	license = 'Apache License, Version 2.0',
	long_description = open('README.md').read(),
	long_description_content_type = 'text/markdown',
	install_requires = [
		# all dependencies listed to lock the versions
		'pylint==2.13.9',
		'isort>=5.6.0,<6.0.0',
		'pyflakes-ext==2.0.0',
		'pyflakes==2.4.0',
		'ql-orange>=1.1.0,<2.0.0',
		'mypy==0.960',
		'types-pkg-resources>=0.1.3,<0.2.0',
		'types-setuptools>=57.0.0,<58.0.0',
		'bellybutton>=0.3.0,<0.4.0',
		'astpath[xpath]==0.6.1',
		'safety==1.10.3',
		'click>=3.0,<9.0',
		'toolz>=0.8.2,<1.0.0',
		'requirements-parser>=0.1.0,<1.0.0',
		'pip>=19.0.0',
	],
	packages = ['cq', 'cq.checkers', 'cq.fixers'],
	package_data = {'cq': ['checkers/pylintrc', 'checkers/.bellybutton.yml']},
	entry_points = {'console_scripts': ['cq=cq.main:main']},
)
