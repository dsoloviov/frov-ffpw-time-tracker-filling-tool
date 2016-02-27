#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dmytro Soloviov'
__email__ = 'dmytro.soloviov@gmail.com'
__version__ = '2.0'

import sys
from src.autofill import Dochazka
from src.parser import config_parser
from src.parser import schedule_parser
import datetime


def main(_file, _config):
    def fix_int(value):
        """ Add leading zero to 1-9"""
        if len(str(value)) == 1:
            return '0%s' % value
        return str(value)

    c = config_parser(_config)  # parse config file
    lines = [line for line in open(_file, 'r')]
    commands = [x for x in lines if x.startswith('FILL')]
    d = Dochazka(c['url'], c['usr'], c['psw'])  # log in to the system
    for command in commands:
        schedule = schedule_parser(command)  # parse schedule file

        # Data to be filled in
        WORK_TYPE = schedule['TYPE']
        YEAR = schedule['YEAR']
        MONTH = schedule['MONTH']
        IN = schedule['CHECK-IN']
        OUT = schedule['CHECK-OUT']
        START = schedule['START']
        END = schedule['END']
        COMMENT = schedule['COMMENT']

        for DAY in range(START, END + 1):
            date = datetime.date(YEAR, MONTH, DAY)  # generate date for current day
            if date.weekday() in (5, 6):  # check if current iteration is weekend
                pass
            else:
                # Fill form with provided values
                d.fill_form('Odeslat', 'in', WORK_TYPE, COMMENT, fix_int(DAY), IN[0], fix_int(MONTH), IN[1])
                d.fill_form('Odeslat', 'out', WORK_TYPE, COMMENT, fix_int(DAY), OUT[0], fix_int(MONTH), OUT[1])
                print('Filling in: %s.%s.%s, %s:%s - %s:%s (%s)' % (DAY, MONTH, YEAR,
                                                               IN[0], IN[1],
                                                               OUT[0], OUT[1],
                                                               WORK_TYPE))



def _help():
    """
    Print the help message
    """
    print('Time tracker filling tool')
    print('Version: %s\nAuthor: %s\nEmail: %s\n' % (__version__, __author__, __email__))
    print('usage: dochazka.py [--version] [--help] \n\t\t   [-f <path>] [-c <path>]\n')


if __name__ == '__main__':
    schedule = 'schedule.txt'
    config = 'config.ini'

    # Check for --help or --version
    if '--version' in sys.argv:
        print(__version__)
        sys.exit()
    if '--help' in sys.argv:
        _help()
        sys.exit()
    # Check if schedule and/or config
    # is passed as an argument
    if '-f' in sys.argv:
        i = sys.argv.index('-f')
        schedule = sys.argv[i + 1]
    if '-c' in sys.argv:
        i = sys.argv.index('-c')
        config = sys.argv[i + 1]

    # Run tool
    try:
        main(schedule, config)
    except IOError:
        print('\nERROR! Please make sure that both config.ini'
              ' and schedule.txt are present at tool\'s location or specified'
              ' as an argument\n')
        _help()
