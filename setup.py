#!/usr/bin/env python

from setuptools import setup

author = 'Yervand Azatian'

setup(name='stools',
      version='1.0',
      # list folders, not files
      packages=['stools'],
      scripts=['bin/findgene', 'bin/afasta2meta']
      )