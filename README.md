# OpenStack Monitoring
Python based monitoring checks for Nagios and all it's forks.

Provides checks for API and service statuses.

Any improvements are welcome, feel free to create a pull request.

## OpenStack support

Currently in-use on:

* Mitaka

Was used before on (not currently tested but might work):

* Kilo
* Liberty

## Status
[![Build Status](https://travis-ci.org/crystone/openstack-monitoring.svg?branch=master)](https://travis-ci.org/crystone/openstack-monitoring)

## Example usage

Supports both keystone v2.0 and v3 auth, it's selected based on the --auth_url parameter.

`python check_keystone_api.py --auth_url http://10.0.0.10:5000/v2.0 --username myuser --password mypass --project myproject --region myregion`

`python check_keystone_api.py --auth_url http://10.0.0.10:5000/v3 --username myuser --password mypass --domain default --project myproject --region myregion`

Domain defaults to `default` and region defaults to `regionOne` all other is mandatory. For keystone v3 the `--project` parameter is required but not used because it does not create a scoped token.

The same principle applies for all other checks.

## Requirements
See requirements.txt for pip requirements, use 'pip install -r requirements.txt' to install requirements using pip.

If you don't have pip, use 'easy_install pip' to install pip.

* python >= 2.6
* argparse
* requests

## Installation
Copy this folder to your nagios plugins folder, keep the folder structure.

## License
Openstack Monitoring

Copyright (C) 2015 Crystone Sverige AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
