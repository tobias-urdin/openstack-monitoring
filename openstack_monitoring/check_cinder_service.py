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
from openstack.cinder import CinderClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Cinder Service Status')

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
parser.add_argument('--cinder_url', metavar='http://controller:8776/v2',
                    type=str, required=False, help='Cinder endpoint')
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
    print 'CRITICAL: Could not create keystone context'
    sys.exit(STATE_CRITICAL)

if keystone.valid() is False:
    print 'CRITICAL: Keystone context is invalid'
    sys.exit(STATE_CRITICAL)

cinder_url = None

if args.cinder_url is not None:
    cinder_url = args.cinder_url

cinder = CinderClient(keystone, cinder_url)

if cinder is None:
    print 'CRITICAL: Could not create cinder context'
    sys.exit(STATE_CRITICAL)

service = cinder.get_service(args.host, args.binary)

if service is None:
    print ('CRITICAL: Could not retrieve '
           'status for %s on %s') % (args.binary, args.host)
    sys.exit(STATE_CRITICAL)

if service['status'] == 'enabled':
    status = 'CRITICAL'
    status_code = STATE_CRITICAL

    if service['state'] == 'up':
        status = 'OK'
        status_code = STATE_OK

    print ('%s: %s on %s is enabled '
           'with state %s') % (status, service['binary'],
                               service['host'], service['state'])
    sys.exit(status_code)
else:
    print ('WARNING: %s on %s is disabled '
           'with state %s') % (service['binary'], service['host'],
                               service['state'])
    sys.exit(STATE_WARNING)

print ('CRITICAL: Invalid service state for %s on %s' % (args.binary, args.host))
sys.exit(STATE_CRITICAL)
