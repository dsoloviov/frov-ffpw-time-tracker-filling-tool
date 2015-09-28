#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from calendar import monthrange
import datetime
import os
import re


def config_parser(_file):
    """
    Parse config.ini file

    Returns: dictionary:
    +--------------+
    | KEY - VALUE  |
    |--------------|
    |usr - username|
    |psw - password|
    +--------------|
    """
    c = ConfigParser()
    c.readfp(open(_file))
    usr = c.get('Credentials', 'Username')
    psw = c.get('Credentials', 'Password')

    return {'usr': usr, 'psw': psw}


def schedule_parser(command):
    """
    Parse command string from schedule file

    Returns: dictionary:
    +------------------------------+
    |         KEY - VALUE          |
    |------------------------------|
    |TYPE - activity type          |
    |YEAR - current year           |
    |MONTH - month                 |
    |START - start date            |
    |END - end date                |
    |CHECK-IN - time of work start*|
    |CHECK-OUT - time of work end* |
    +------------------------------+
    *CHECK-IN and CHECK-OUT are lists:
        ['HH', 'MM']
    """
    def search(start, end, line):
        """
        Perform search between provided strings

        Returns: string
        """
        return re.search('(?<=%s)(.*)(?=%s)' % (start, end), line).group()

    data = {}  # container for all the data: work type, time, etc.
    data['TYPE'] = search('FILL ', ' FROM', command)  # extract activity type
    data['START'] = search('FROM ', ' TO', command)  # extract start day
    data['END'] = search('TO ', ' \(', command)  # extract end day
    data['MONTH'] = search('IN ', ' MONTH', command)  # extract month
    data['COMMENT'] = search('WITH \'', '\' COMMENT', command)  # extract comment
    time = search(' \(', '\) ', command)  # extract time

    #+----------------------+#
    #| Validate data values |#
    #+----------------------+#

    # Check activity type
    activity = {'work': u'Práce',
                'vacation': u'Dovolená',
                'trip': u'Služebni cesta',
                'sick': u'Nemoc',
                'family': u'Ošetřování člena rodiny',
                'holiday': u'Jiné volno',
                'dayoff': u'Nahradní volno',
                'doctor': u'Celodenní lekař',
                'other': u'Indispoziční volno'}
    data['TYPE'] = activity[data['TYPE']]

    # Parse today's date
    date = datetime.datetime.now()
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))
    day = int(date.strftime("%d"))

    data['YEAR'] = year

    # Check month:
    months = {'January': 1, 'February': 2,
              'March': 3, 'April': 4,
              'May': 5, 'June': 6,
              'July': 7, 'August': 8,
              'September': 9, 'October': 10,
              'November': 11, 'December': 12}
    if data['MONTH'] in months.keys():
        data['MONTH'] = months[data['MONTH']]
    elif data['MONTH'] == 'current':
        data['MONTH'] = month
    else:
        data['MONTH'] = int(data['MONTH'])

    # Check start day:
    if data['START'] == 'yesterday':
        data['START'] = day - 1
    elif data['START'] == 'today':
        data['START'] = day
    elif data['START'] == 'tomorrow':
        data['START'] = day + 1
    elif data['START'] == 'first':
        data['START'] = 1
    elif data['START'] == 'last':
        data['START'] = monthrange(year, data['MONTH'])[-1]
    else:
        data['START'] = int(data['START'])

    # Check end day:
    if data['END'] == 'yesterday':
        data['END'] = day - 1
    elif data['END'] == 'today':
        data['END'] = day
    elif data['END'] == 'tomorrow':
        data['END'] = day + 1
    elif data['END'] == 'first':
        data['END'] = 1
    elif data['END'] == 'last':
        data['END'] = monthrange(year, data['MONTH'])[-1]
    else:
        data['END'] = int(data['END'])

    # Check check-in and check-out time
    time = time.split('-')
    data['CHECK-IN'] = time[0].split(':')
    data['CHECK-OUT'] = time[1].split(':')

    return data
