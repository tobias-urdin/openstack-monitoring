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
from openstack.neutron import NeutronClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Neutron Agent Status')

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
parser.add_argument('--neutron_url', metavar='http://controller:9696/v2.0',
                    type=str, required=False, help='Neutron endpoint')
parser.add_argument('--insecure', action='store_false', dest='verify',
                    required=False, help='Disable SSL')
parser.add_argument('--endpoint', metavar='public', type=str,
                    required=False, help='Endpoint type, default to public')
parser.add_argument('--host', metavar='host', type=str, required=True,
                    help='Host to check binary on')
parser.add_argument('--binary', metavar='binary', type=str, required=True,
                    help='Binary agent to check')

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

neutron_url = None

if args.neutron_url is not None:
    neutron_url = args.neutron_url

neutron = NeutronClient(keystone, neutron_url)

if neutron is None:
    print('CRITICAL: Could not create neutron context')
    sys.exit(STATE_CRITICAL)

agent = neutron.get_agent(args.host, args.binary)

if agent is None:
    print(('CRITICAL: Could not retrieve status '
           'for %s on %s') % (args.binary, args.host))
    sys.exit(STATE_CRITICAL)

if agent['admin_state_up'] is True:
    status = 'CRITICAL'
    status_code = STATE_CRITICAL
    state = 'dead'

    if agent['alive'] is True:
        status = 'OK'
        status_code = STATE_OK
        state = 'alive'

    print(('%s: %s on %s is enabled with '
           'state %s') % (status, agent['binary'], agent['host'], state))
    sys.exit(status_code)
else:
    print(('WARNING: %s on %s is disabled with '
           'state %s') % (agent['binary'], agent['host'], state))
    sys.exit(STATE_WARNING)

print('CRITICAL: Invalid service state for %s on %s' % (args.binary, args.host))
sys.exit(STATE_CRITICAL)
