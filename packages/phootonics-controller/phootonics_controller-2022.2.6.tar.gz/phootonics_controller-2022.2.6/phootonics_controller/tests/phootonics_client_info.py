# -*- coding: utf-8 -*-
"""
Created by olgare on 10.09.2021

Copyright 2021 Alpes Lasers SA, Neuchatel, Switzerland
"""
__author__ = 'olgare'
__copyright__ = "Copyright 2021, Alpes Lasers SA"

from pprint import PrettyPrinter
from time import sleep

import requests
url = 'http://phootonix:5000'

if __name__ == '__main__':
    rsp = requests.get(url + '/info')

    rsp.raise_for_status()
    PrettyPrinter().pprint(rsp.json())
    rsp = requests.post(url + '/scan/start',
                        json={'positions': [(1.0, 1.0), (3.0, 3.0)]})
    if not rsp.status_code == 200:
        print(rsp.json())
        rsp.raise_for_status()
