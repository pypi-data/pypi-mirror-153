#!/usr/bin/python
# -*-coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(name='kanimysql',
      version='0.3.0',
      description='A MySQL class for more convenient database manipulations with Python dictionary.',
      long_description=long_description,
      author='Kirin Fx',
      author_email='ono.kirin@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='python mysql class',
      url='https://github.com/fx-kirin/kanimysql',
      install_requires=["PyMySQL>=0.7", "python-string-utils", "interval_decorator", "kaniattrdict", "funcy"],
      )
