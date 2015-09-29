#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# OpenStack Monitoring
# Copyright (C) 2015 Crystone Sverige AB

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import requests


class CeilometerClient(object):
    def __init__(self, keystone, ceilometer_url=None, ssl=False):
        self.keystone = keystone
        self.ceilometer_api_version = '/v2'

        if keystone.valid() is False:
            raise Exception('KeystoneClient is invalid, cannot continue')

        if ceilometer_url is not None:
            self.ceilometer_url = ceilometer_url
        else:
            self.ceilometer_url = (keystone.get_endpoint_url('metering') +
                                   self.ceilometer_api_version)

        self.ssl = ssl

    def get_alarms(self, token=None):
        auth_token = token

        try:
            if auth_token is None:
                auth_token = self.keystone.get_token()
        except Exception as e:
            return None

        headers = {
            'content-type': 'application/json',
            'X-Auth-Token': auth_token
        }

        try:
            response = requests.get(self.ceilometer_url + '/alarms',
                                    headers=headers,
                                    verify=self.ssl).json()
            return response
        except Exception as e:
            return None

        return None
