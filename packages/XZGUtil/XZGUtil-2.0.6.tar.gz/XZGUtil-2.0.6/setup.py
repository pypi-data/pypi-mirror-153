#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-09 23:20
# @Site    :
# @File    : setup.py
# @Software: PyCharm
from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='XZGUtil',  # 包名
      version='2.0.6',  # 版本号
      description='xzgutil',
      long_description='xzgutil',
      author='xu-zhiguo',
      author_email='x_zg163@163.com',
      url='',
      install_requires=['postcard', 'retrying', 'python-dateutil'],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
