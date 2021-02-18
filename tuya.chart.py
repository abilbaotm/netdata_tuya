# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

from random import SystemRandom

from bases.FrameworkServices.SimpleService import SimpleService

import tuyapower

priority = 90000


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)

        DEVICE = configuration['device']
        ORDER = []
        CHARTS = {}

        CHARTS['power'] = {
            'options': [None, 'watts', None, DEVICE['id'],
                        'tuya.power', 'line'],
            'lines': [
                ['watts', 'W', 'absolute', 1, 100]
            ]
        }
        CHARTS['amps'] = {
            'options': [None, 'amps', None, DEVICE['id'],
                        'tuya.amps', 'line'],
            'lines': [
                ['mA', 'mA', 'absolute', 1, 100]
            ]
        }
        CHARTS['volts'] = {
            'options': [None, 'volts', None, DEVICE['id'],
                        'tuya.volts', 'line'],
            'lines': [
                ['V', 'V', 'absolute', 1, 100]
            ]
        }
        ORDER.append('power')
        ORDER.append('amps')
        ORDER.append('volts')

        self.device = DEVICE
        self.order = ORDER
        self.definitions = CHARTS

    @staticmethod
    def check():
        return True

    def get_data(self):
        data = dict()
        (on, w, mA, V, err) = tuyapower.deviceInfo(self.device['id'],
                                                   self.device['ip'],
                                                   self.device['localKey'],
                                                   self.device['version'])
        data['watts'] = w * 100
        data['mA'] = mA * 100
        data['V'] = V * 100

        return data
