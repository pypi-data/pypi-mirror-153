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

from phootonics_controller.base_controllers.config import WL_INCREMENT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PHOOTONICS_URL = 'http://0.0.0.0:5000'


def scan():
    parser = ArgumentParser()
    parser.add_argument('-x', nargs='+', type=float)
    parser.add_argument('-y', nargs='+', type=float)
    parser.add_argument('-wl_step', type=float, required=False, default=WL_INCREMENT)
    parser.add_argument('-scan', type=str, choices=['default', 'fast'], required=True)
    parser.add_argument('-url', type=str, required=False, default=PHOOTONICS_URL)
    args=parser.parse_args()


    rsp = requests.get(args.url + '/info')
    rsp.raise_for_status()
    info = rsp.json()
    if info['scan_running']:
        parser.error('Scan command already running.')


    if args.scan == 'default':
        x_list = args.x
        y_list = args.y

        positions = list(itertools.product(x_list, y_list))

        rsp = requests.post(args.url + '/scan/start/default',
                            json={'positions': positions, 'wl_step': args.wl_step})
        if not rsp.status_code == 200:
            print(rsp.json())
            rsp.raise_for_status()
    elif args.scan == 'fast':
        rsp = requests.post(args.url + '/scan/start/fast',
                            json={'wl_step': args.wl_step})
        if not rsp.status_code == 200:
            print(rsp.json())
            rsp.raise_for_status()

    while True:
        sleep(1)
        rsp = requests.get(args.url + '/info')
        rsp.raise_for_status()
        info = rsp.json()
        print('Completed: {:.0%}'.format(info['scan']['runtime']['completed']))
        if not info['scan_running']:
            break

    rsp = requests.get(args.url + '/info')
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





