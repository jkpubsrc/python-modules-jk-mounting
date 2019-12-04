from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_mounting',
	version='0.2019.12.4',
	description='This python module provides support for mounting/unmounting and retrieving mounting information.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-mediawiki',
	download_url='https://github.com/jkpubsrc/python-module-jk-mediawiki/tarball/0.2017.7.15',
	keywords=['mount', 'nfs'],
	packages=['jk_mounting'],
	install_requires=[
		"jk_utils",
		"jk_simpleexec"
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)








