# OpenStack Monitoring
Python based monitoring checks for Nagios and all it's forks.

Provides checks for API and service statuses.

Any improvements are welcome, feel free to create a pull request.

## OpenStack support

Currently in-use on:

* Mitaka
* Ocata

Was used before on (not currently tested but might work):

* Kilo
* Liberty

## Status
[![Build Status](https://travis-ci.org/tobias-urdin/openstack-monitoring.svg?branch=master)](https://travis-ci.org/tobias-urdin/openstack-monitoring)

## Example usage

Supports both keystone v2.0 and v3 auth, it's selected based on the --auth_url parameter.

`python check_keystone_api.py --auth_url http://10.0.0.10:5000/v2.0 --username myuser --password mypass --project myproject --region myregion`

`python check_keystone_api.py --auth_url http://10.0.0.10:5000/v3 --username myuser --password mypass --domain default --project myproject --region myregion`

Domain defaults to `default` and region defaults to `regionOne` all other is mandatory. For keystone v3 the `--project` parameter is required but not used because it does not create a scoped token.

The default `--endpoint` type is set to *public* to support newer OpenStack versions (and keystone v3 catalogs). To support backwards compatibility this will also match *publicURL* etc when using keystone v2.0

The same principle applies for all other checks.

## Requirements
See requirements.txt for requirements.

These are the requirements:

* python2 >= 2.7 or python3 >= 3.2 (to get argparse in standard library)
* argparse (should get it by default for above supported python versions)
* requests (needs to be installed)

### Using pip
Use `pip install -r requirements.txt` to install requirements using pip.

If you don't have pip, use your package manager to install it or use `easy_install pip`.

### Using packages

You will need the `requests` module. Install the `python-requests` or `python3-requests` package depending on python version.

Use `apt install python-requests` on Debian based and `yum install python-requests` or `dnf` instead of `yum` if you're on Fedora.

## Installation
Copy the `openstack_monitoring` folder to your nagios plugins folder, keep the folder structure.

You can find example nagios command defintions in the `contrib` folder.

## License
Openstack Monitoring

Copyright (C) 2015 Tobias Urdin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
