from setuptools import setup

setup(
	name='PyScorecard',
	url='https://github.com/deino475/PyScorecard',
	author='Nile Dixon',
	author_email='niledixon475@gmail.com',
	packages=['PyScorecard'],
	install_requires=['requests'],
	version='0.2.1',
	license='GNU GPL-V2',
	description='An unofficial API wrapper for the College Scorecard API.',
	long_description=open('README.rst').read(),
)