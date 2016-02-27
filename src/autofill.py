#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as r


class Dochazka(object):
    def __init__(self, url, username, password):
        self.url = url
        self.session = r.Session()
        self.session.post(self.url, data={"user_name": username, "password": password})
        self.session.post(self.url, data={"user_name": username, "password": password})  # somehow it doesn't work otherwise O_o

    def fill_form(self, submit, action, work_type, comment, day, hour, month, minute):
        """
        Send POST request to fill the data
        """
        fill_in = {"Submit": submit, "akce1": action,
                   "akce2": work_type, "coment": comment,
                   "den": day, "hodina": hour, "mesic": month,
                   "minuta": minute, "odeslano": "true"}
        self.session.post(self.url, data=fill_in)
