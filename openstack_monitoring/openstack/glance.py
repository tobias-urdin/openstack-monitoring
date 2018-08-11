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


class GlanceClient(object):
    def __init__(self, keystone, glance_url=None, ssl=False):
        self.keystone = keystone
        self.glance_api_version = '/v2'

        if keystone.valid() is False:
            raise Exception('KeystoneClient is invalid, cannot continue')

        if glance_url is not None:
            self.glance_url = glance_url
        else:
            self.glance_url = (keystone.get_endpoint_url('image') +
                               self.glance_api_version)

        self.ssl = ssl

    def get_images(self, token=None):
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
            response = requests.get(self.glance_url + '/images',
                                    headers=headers,
                                    verify=self.ssl).json()
            return response
        except Exception as e:
            return None

        return None
