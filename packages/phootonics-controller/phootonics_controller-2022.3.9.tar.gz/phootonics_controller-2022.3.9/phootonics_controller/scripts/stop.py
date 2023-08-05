# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import requests


def stop(url='http://0.0.0.0:5000'):
    rsp = requests.post(url + '/scan/stop')
    rsp.raise_for_status()


if __name__ == '__main__':
    stop(url='http://phootonix:5000')