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


class HeatClient(object):
    def __init__(self, keystone, heat_url=None, ssl=False):
        self.keystone = keystone

        if keystone.valid() is False:
            raise Exception('KeystoneClient is invalid, cannot continue')

        if heat_url is not None:
            self.heat_url = heat_url
        else:
            self.heat_url = keystone.get_endpoint_url('orchestration')

        self.ssl = ssl

    def get_services(self, token=None):
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
            response = requests.get(self.heat_url + '/services',
                                    headers=headers,
                                    verify=self.ssl).json()
            return response
        except Exception as e:
            return None

        return None

    def get_service(self, host, binary):
        matches = []

        try:
            services = self.get_services()

            for service in services['services']:
                if service['host'] == host and service['binary'] == binary:
                    matches.append(service)
        except Exception as e:
            return None

        if len(matches) > 0:
            return matches

        return None
