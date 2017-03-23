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
import argparse

from openstack.keystone import KeystoneClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Keystone API')

parser.add_argument('--auth_url', metavar='http://controller:35357/v2.0',
                    type=str, required=True, help='Keystone URL')
parser.add_argument('--username', metavar='username', type=str,
                    required=True, help='Keystone username')
parser.add_argument('--password', metavar='password', type=str,
                    required=True, help='Keystone password')
parser.add_argument('--project', metavar='project', type=str,
                    required=True, help='Keystone project')
parser.add_argument('--region', metavar='region', type=str,
                    required=True, help='Region')
parser.add_argument('--insecure', action='store_false', dest='verify',
                    required=False, help='Disable SSL')
parser.add_argument('--endpoint', metavar='publicURL', type=str,
                    required=False, help='Endpoint type, default to publicURL')

args = parser.parse_args()

keystone = KeystoneClient(args.auth_url, args.username, args.password,
                          args.project, args.verify,
                          args.region, args.endpoint)

if keystone is None:
    print 'CRITICAL: Could not create keystone context'
    sys.exit(STATE_CRITICAL)

if keystone.valid() is False:
    print 'CRITICAL: Keystone failed to create token region %s user %s in'
    'project %s' % (keystone.get_region(), args.username, args.project)
    sys.exit(STATE_CRITICAL)

token = keystone.get_token()

if token is None:
    print ('CRITICAL: Could not get token for '
           'region %s user % in project %s') % (keystone.get_region(),
                                                args.username, args.project)
    sys.exit(STATE_CRITICAL)

print ('OK: Successfully created token - region %s '
       'user %s in project %s') % (keystone.get_region(),
                                   args.username, args.project)
sys.exit(STATE_OK)
