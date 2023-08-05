# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import itertools
from argparse import ArgumentParser
import logging
from time import sleep

import requests

import pandas

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PHOOTONICS_URL = 'http://localhost:5555'


def scan():
    parser = ArgumentParser()
    parser.add_argument('-x', nargs='+', type=float)
    parser.add_argument('-y', nargs='+', type=float)
    args=parser.parse_args()
    x_list = args.x
    y_list = args.y

    positions = list(itertools.product(x_list, y_list))

    rsp = requests.get(PHOOTONICS_URL + '/info')
    rsp.raise_for_status()
    info = rsp.json()
    if info['scan_running']:
        parser.error('Scan command already running.')

    rsp = requests.post(PHOOTONICS_URL + '/scan/start',
                        json={'positions': positions})
    if not rsp.status_code == 200:
        print(rsp.json())
        rsp.raise_for_status()

    while True:
        sleep(1)
        rsp = requests.get(PHOOTONICS_URL + '/info')
        rsp.raise_for_status()
        info = rsp.json()
        print('Completed: {:.0%}'.format(info['scan']['runtime']['completed']))
        if not info['scan_running']:
            break

    rsp = requests.get(PHOOTONICS_URL + '/info')
    rsp.raise_for_status()
    info = rsp.json()

    df = pandas.DataFrame.from_records(info['scan']['results'],
                                       columns=['active_cavity',
                                                'detector_voltage',
                                                'wavelength',
                                                'wavelength_set_point',
                                                'x',
                                                'x_set_point',
                                                'y',
                                                'y_set_point'])
    df.to_csv('outputfile.csv')

if __name__ == '__main__':
    scan()





