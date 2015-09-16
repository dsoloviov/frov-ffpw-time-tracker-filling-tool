#!/usr/bin/env python

from src.main import main

"""
@ FFPW TIME TRACKER FILLING TOOL

@ Author: Dmytro Soloviov {dsoloviov@frov.jcu}
@ Dependencies:
@ - Selenium 2.4
"""

_file = 'schedule.txt'
try:
    main(_file)
except IOError:
    print('[ERROR]: Cannot find file: %s' % _file)