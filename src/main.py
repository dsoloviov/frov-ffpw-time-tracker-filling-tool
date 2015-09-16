#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from autofill import Dochazka
from parser import config_parser
from parser import schedule_parser
import datetime


def main(_file):
    def fix_int(value):
        """ Add leading zero to 1-9"""
        if len(str(value)) == 1:
            return '0%s' % value
        return str(value)

    c = config_parser('config.ini')  # parse config file
    lines = [line for line in open(_file, 'r')]
    commands = [x for x in lines if x.startswith('FILL')]
    d = Dochazka(c['usr'], c['psw'])  # log in to the system
    for command in commands:  # perform action for each command
        schedule = schedule_parser(command)  # parse schedule file

        # Data to be filled in
        WORK_TYPE = schedule['TYPE']
        YEAR = schedule['YEAR']
        MONTH = schedule['MONTH']
        IN = schedule['CHECK-IN']
        OUT = schedule['CHECK-OUT']
        START = schedule['START']
        END = schedule['END']

        for DAY in range(START, END + 1):
            date = datetime.date(YEAR, MONTH, DAY)  # generate date for current day
            if date.weekday() in (5, 6):  # check if current iteration is weekend
                pass
            else:
                # Fill form with provided values
                d.fill_form(WORK_TYPE, u'příchod', fix_int(MONTH), fix_int(DAY), IN[0], IN[1])
                d.fill_form(WORK_TYPE, u'odchod', fix_int(MONTH), fix_int(DAY), OUT[0], OUT[1])
