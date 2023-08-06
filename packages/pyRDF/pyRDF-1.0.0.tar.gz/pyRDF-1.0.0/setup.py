#!/usr/bin/env python

from setuptools import setup


version = '1.0.0'

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pyRDF',
    version=version,
    author='Xander Wilcke',
    author_email='w.x.wilcke@vu.nl',
    url='https://gitlab.com/wxwilcke/pyRDF',
    download_url = 'https://gitlab.com/wxwilcke/pyRDF/-/archive/' + version + '/pyRDF-' + version + '.tar.gz',
    description='Lightweight RDF Stream Parser',
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GLP3',
    include_package_data=True,
    zip_safe=True,
    keywords=['rdf', 'ntriple'],
    packages=['rdf'],
)
