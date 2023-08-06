#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

long_description = readme

setup(
    name='pyrunp',
    version='0.0.3',
    description='pyrunp exports Python functions from files to the command line',
    long_description=long_description,
    author='alex',
    author_email='',
    url='https://github.com/alex-testlab/pyrunp',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'runp = runp.runp:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
)
