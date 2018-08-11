#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# OpenStack Monitoring
# Copyright (C) 2015 Tobias Urdin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
