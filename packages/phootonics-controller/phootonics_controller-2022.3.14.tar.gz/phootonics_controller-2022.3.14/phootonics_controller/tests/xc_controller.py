# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import logging
from time import sleep

from phootonics_controller.base_controllers.config import CAVITY1_INDEX
from phootonics_controller.base_controllers.xc_controller import ECController

if __name__ == '__main__':
    ecc = ECController('http://phootonix:5003/ec/api/v1.0', index=CAVITY1_INDEX, monitor_interval=0.1)
    ecc.start()
    while True:
        sleep(0.2)
        try:
            print(ecc.xc_ready_to_action())
        except Exception as e:
            logging.exception(e)

