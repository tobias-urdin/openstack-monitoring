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

from __future__ import print_function
import sys
import argparse

from openstack.keystone import KeystoneClient
from openstack.nova import NovaClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Nova Service Status')

parser.add_argument('--auth_url', metavar='http://controller:35357/v2.0',
                    type=str, required=True, help='Keystone URL')
parser.add_argument('--username', metavar='username', type=str,
                    required=True, help='Keystone username')
parser.add_argument('--password', metavar='password', type=str,
                    required=True, help='Keystone password')
parser.add_argument('--domain', metavar='domain', type=str,
                    default='default', help='Keystone domain')
parser.add_argument('--project', metavar='project', type=str,
                    required=True, help='Keystone project')
parser.add_argument('--region', metavar='region', type=str,
                    required=True, help='Region')
parser.add_argument('--nova_url', metavar='http://controller:8774/v2',
                    type=str, required=False, help='Nova endpoint')
parser.add_argument('--insecure', action='store_false', dest='verify',
                    required=False, help='Disable SSL')
parser.add_argument('--endpoint', metavar='public', type=str,
                    required=False, help='Endpoint type, default to public')
parser.add_argument('--host', metavar='host', type=str, required=True,
                    help='Host to check binary on')
parser.add_argument('--binary', metavar='binary', type=str, required=True,
                    help='Binary service to check')

args = parser.parse_args()

keystone = KeystoneClient(args.auth_url, args.username, args.password,
                          args.domain, args.project, args.verify,
                          args.region, args.endpoint)

if keystone is None:
    print('CRITICAL: Could not create keystone context')
    sys.exit(STATE_CRITICAL)

if keystone.valid() is False:
    print('CRITICAL: Keystone context is invalid')
    sys.exit(STATE_CRITICAL)

nova_url = None

if args.nova_url is not None:
    nova_url = args.nova_url

nova = NovaClient(keystone, nova_url)

if nova is None:
    print('CRITICAL: Could not create nova context')
    sys.exit(STATE_CRITICAL)

service = nova.get_service(args.host, args.binary)

if service is None:
    print(('CRITICAL: Could not retrieve status '
           'for %s on %s') % (args.binary, args.host))
    sys.exit(STATE_CRITICAL)

if service['status'] == 'enabled':
    status = 'CRITICAL'
    status_code = STATE_CRITICAL

    if service['state'] == 'up':
        status = 'OK'
        status_code = STATE_OK

    print(('%s: %s on %s is enabled with '
           'state %s') % (status, service['binary'],
                          service['host'], service['state']))
    sys.exit(status_code)
else:
        print(('WARNING: %s on %s is disabled with '
               'state %s') % (service['binary'], service['host'],
                              service['state']))
        sys.exit(STATE_WARNING)

print('CRITICAL: Invalid service state for %s on %s' % (args.binary, args.host))
sys.exit(STATE_CRITICAL)
