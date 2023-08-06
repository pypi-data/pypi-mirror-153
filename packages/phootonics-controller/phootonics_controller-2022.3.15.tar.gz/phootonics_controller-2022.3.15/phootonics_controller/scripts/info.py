# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

from pprint import PrettyPrinter

import requests


def monitor(url='http://0.0.0.0:5000'):
    rsp = requests.get(url + '/info')
    rsp.raise_for_status()
    pp = PrettyPrinter(indent=1)
    pp.pprint(rsp.json()['monitoring'])



def info(url='http://0.0.0.0:5000'):
    rsp = requests.get(url + '/info')
    rsp.raise_for_status()
    pp = PrettyPrinter(indent=1)
    pp.pprint(rsp.json())



if __name__ == '__main__':
    info(url='http://phootonix:5000')