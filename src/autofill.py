#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


class Dochazka(object):
    def __init__(self, usr, psw):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = 'http://www.auc.cz/'

        # Login to time tracking system
        self.driver.get(self.base_url + '/ipb/dochazka')
        self.driver.find_element_by_id('username').clear()
        self.driver.find_element_by_id('username').send_keys(usr)
        self.driver.find_element_by_id('password').clear()
        self.driver.find_element_by_id('password').send_keys(psw)
        self.driver.find_element_by_id('submit').click()

    def fill_form(self, wtype, check, month, day, hour, minute, comment):
        """
        Fill form. All arguments are strings
        """
        Select(self.driver.find_element_by_id('akce1')).select_by_visible_text(check)
        Select(self.driver.find_element_by_id('akce2')).select_by_visible_text(wtype)
        Select(self.driver.find_element_by_id('mesic')).select_by_visible_text(month)
        Select(self.driver.find_element_by_id('den')).select_by_visible_text(day)
        Select(self.driver.find_element_by_id('hodina')).select_by_visible_text(hour)
        Select(self.driver.find_element_by_id('minuta')).select_by_visible_text(minute)
        self.driver.find_element_by_id("coment").clear()
        self.driver.find_element_by_id("coment").send_keys(comment)
        self.driver.find_element_by_id('Submit').click()

    def __del__(self):
        """ Logout from time tracking system """
        self.driver.find_element_by_link_text('Odhlásit se').click()
        self.driver.quit()
