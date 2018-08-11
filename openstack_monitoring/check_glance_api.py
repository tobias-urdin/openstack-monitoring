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
from openstack.glance import GlanceClient

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

parser = argparse.ArgumentParser(description='Check Glance API')

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
parser.add_argument('--glance_url', metavar='http://controller:9292/v2',
                    type=str, required=False, help='Glance endpoint')
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

glance_url = None

if args.glance_url is not None:
    glance_url = args.glance_url

glance = GlanceClient(keystone, glance_url)

if glance is None:
    print('CRITICAL: Could not create glance context')
    sys.exit(STATE_CRITICAL)

images = glance.get_images()

if images is None:
    print('CRITICAL: Did not get any images data')
    sys.exit(STATE_CRITICAL)

if 'images' in images:
    count = len(images['images'])

    if count > 0:
        print('OK: Found %s images' % (count))
        sys.exit(STATE_OK)
    else:
        print('CRITICAL: Did not find any images')
        sys.exit(STATE_CRITICAL)

print('CRITICAL: Could not retrieve glance images')
sys.exit(STATE_CRITICAL)
