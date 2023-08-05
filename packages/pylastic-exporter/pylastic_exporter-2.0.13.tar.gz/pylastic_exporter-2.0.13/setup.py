#!/usr/src/env python

from setuptools import setup, find_packages

pylastic_version = '2.0.13'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pylastic_exporter',
    url='https://github.com/alexperezortuno/elastic-export',
    license='LICENSE',
    version=pylastic_version,
    author='Alex Pérez Ortuño',
    description="Create CSV from elasticsearch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='alexperezortuno@gmail.com',
    install_requires=[
        'numpy==1.22.3',
        'pandas==1.4.2',
        'elastic-transport==8.1.0',
        'elasticsearch==7.17.0',
        'elasticsearch-dsl==7.4.0',
        'coloredlogs==15.0.1',
        'python-dotenv==0.20.0',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'pylastic = pylastic_exporter:run_standalone'
        ]
    }
)
