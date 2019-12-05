from setuptools import setup

setup(
	name='PyScorecard',
	url='https://github.com/jladan/package_demo',
	author='Nile Dixon',
	author_email='niledixon475@gmail.com',
	packages=['PyScorecard'],
	install_requires=['requests'],
	version='0.1',
	license='MIT',
	description='An unofficial API wrapper for the College Scorecard API.',
	long_description=open('README.md').read(),
)