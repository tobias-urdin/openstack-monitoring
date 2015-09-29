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
import json


class TokenRequest(object):
    def __init__(self, username, password, project):
        self.auth = {
            "tenantName": project,
            "passwordCredentials": {
                "username": username,
                "password": password,
            }
        }

    def get_data(self):
        return json.dumps(self.__dict__)


class KeystoneClient(object):
    def __init__(self, auth_url, username, password, project, ssl=False,
                 region='regionOne', endpoint='internalURL'):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project = project

        if ssl is not None:
            self.ssl = ssl
        else:
            self.ssl = False

        if region is not None:
            self.region = region
        else:
            self.region = 'regionOne'

        if endpoint is not None:
            self.endpoint = endpoint
        else:
            self.endpoint = 'internalURL'

        self.headers = {
            'content-type': 'application/json'
        }

        self.token = None
        self.projectid = None
        self.catalog = None

        self.create_token()

    def valid(self):
        if (self.token is None or self.projectid is None
           or self.catalog is None):
            return False

        return True

    def get_token(self):
        return self.token

    def get_project_id(self):
        return self.projectid

    def get_catalog(self):
        return self.catalog

    def get_region(self):
        return self.region

    def get_endpoint_url(self, service_type):
        if self.catalog is None:
            return False

        for service in self.catalog:
            if service['type'] == service_type:
                if self.region is not False:
                    for regionurls in service['endpoints']:
                        if regionurls['region'] == self.region:
                            return regionurls[self.endpoint]
                        else:
                            return service['endpoints'][0][self.endpoint]

        return None

    def create_token(self):
        tokenreq = TokenRequest(self.username, self.password, self.project)
        request = tokenreq.get_data()

        try:
            response = requests.post(self.auth_url + '/tokens',
                                     data=request,
                                     headers=self.headers,
                                     verify=self.ssl).json()
        except Exception as e:
            self.token = None
            self.projectid = None
            self.catalog = None
            return

        if not response['access']['token']['id']:
            self.token = None
            self.projectid = None
            self.catalog = None
            return

            self.token = response['access']['token']['id']
            self.projectid = response['access']['token']['tenant']['id']
            self.catalog = response['access']['serviceCatalog']
