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

from __future__ import print_function
import sys
import argparse

from openstack.keystone import KeystoneClient
from openstack.neutron import NeutronClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Neutron API')

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

floatingips = neutron.get_floatingips()

if floatingips is None:
    print('CRITICAL: Did not get any floating ips')
    sys.exit(STATE_CRITICAL)

if 'floatingips' in floatingips:
    count = len(floatingips['floatingips'])

    if count > 0:
        print('OK: Found %s floating ips' % (count))
        sys.exit(STATE_OK)
    else:
        print('CRITICAL: Did not find any floating ips')
        sys.exit(STATE_CRITICAL)

print('CRITICAL: Could not retrieve neutron floating ips')
sys.exit(STATE_CRITICAL)
