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


class TokenRequestV2(object):
    def __init__(self, username, password, domain, project):
        self.auth = {
            "tenantName": project,
            "passwordCredentials": {
                "username": username,
                "password": password,
            }
        }

    def get_data(self):
        return json.dumps(self.__dict__)


class TokenRequestV3(object):
    def __init__(self, username, password, domain, project=None):
        self.auth = {
          "identity": {
            "methods": ["password"],
            "password": {
              "user": {
                "name": username,
                "domain": { "id": domain },
                "password": password
              }
            }
          }
        }

        # Dont need scoped tokens for now
        #if project is not None:
        #    self.auth['scope'] = {
        #        "project": {
        #          "id": project
        #        }
        #    }

    def get_data(self):
        return json.dumps(self.__dict__)



class KeystoneClient(object):
    def __init__(self, auth_url, username, password, domain='default', project=None,
                 ssl=False, region='regionOne', endpoint='internal'):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.domain = domain
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
            self.endpoint = 'internal'

        self.headers = {
            'content-type': 'application/json'
        }

        self.token = None
        self.projectid = None
        self.catalog = None

        self.create_token()

    def valid(self):
        if 'v2.0' in self.auth_url:
            if (self.token is None or self.projectid is None
               or self.catalog is None):
                return False
        elif 'v3' in self.auth_url:
            if (self.token is None or self.domain is None
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
            return None

        for service in self.catalog:
            if service['type'] == service_type:
                for regionurls in service['endpoints']:
                    if 'v3' in self.auth_url:
                        if regionurls['interface'] == self.endpoint:
                            return regionurls['url']
                    else:
                        if regionurls['region'].lower() == self.region.lower():
                            for key, val in regionurls.items():
                                if self.endpoint in key:
                                    return val
                        else:
                            for i in service['endpoints']:
                                for key, val in i.items():
                                    if self.endpoint in key:
                                        return val

        return None

    def create_token(self):
        tokenreq = None
        if 'v3' in self.auth_url:
            tokenreq = TokenRequestV3(self.username, self.password, self.domain, self.project)
            url = self.auth_url + '/auth/tokens'
        else:
            tokenreq = TokenRequestV2(self.username, self.password, self.domain, self.project)
            url = self.auth_url + '/tokens'

        request = tokenreq.get_data()

        try:
            result = requests.post(url,
                                   data=request,
                                   headers=self.headers,
                                   verify=self.ssl)
            response = result.json()
        except Exception as e:
            self.token = None
            self.projectid = None
            self.catalog = None
            return

        if 'v2.0' in self.auth_url:
            if not response['access']['token']['id']:
                self.token = None
                self.projectid = None
                self.catalog = None
                return

            self.token = response['access']['token']['id']
            self.projectid = response['access']['token']['tenant']['id']
            self.catalog = response['access']['serviceCatalog']

        if 'v3' in self.auth_url:
            if 'X-Subject-Token' not in result.headers or not result.headers['X-Subject-Token']:
                self.token = None
                self.projectid = None
                self.catalog = None
                return

            self.catalog = response['token']['catalog']
            self.token = result.headers['X-Subject-Token']
            self.projectid = response['token']['project']['id']
