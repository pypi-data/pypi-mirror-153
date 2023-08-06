#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Compile an Onionprobe configuration file from the "Real-World Onion Sites"
# repository.
#
# Copyright (C) 2022 Silvio Rhatto <rhatto@torproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies
import os
import sys
import csv
import urllib.parse

from io import StringIO

from onionprobe.config import OnionprobeConfigCompiler, basepath, cmdline_parser_compiler, cmdline_compiler

try:
    import requests
except ImportError:
    print("Please install requests first!")
    raise ImportError

# The list of external databases handled by this implementation
databases = {
        'real-world-onion-sites' : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/master.csv',
        #'securedrop'            : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/securedrop-api.csv',
        }

class RealWorldOnionSites(OnionprobeConfigCompiler):
    """
    Handles the 'Real-World Onion Sites' database

    Inherits from the OnionprobeConfigCompiler class, implementing
    custom procedures.
    """

    def build_endpoints_config(self, database):
        """
        Overrides OnionprobeConfigCompiler.build_endpoints_config()
        method with custom logic.

        :type database : str
        :param database: A database name from the databases dictionary.

        :rtype: dict
        :return: Onion Service endpoints in the format accepted by Onionprobe.

        """

        endpoints = {}

        # Get the Onion Service database from a remote CSV file
        if os.path.exists(self.databases[database]):
            print('Using list of %s database endpoints from %s...' % (
                database, self.databases[database]))

            with open(self.databases[database], 'r') as result:
                data = csv.DictReader(result.readlines())

        else:
            try:
                print('Fetching remote list of %s database endpoints from %s...' % (database, self.databases[database]))

                result = requests.get(self.databases[database])
                data   = csv.DictReader(StringIO(result.text))

            except Exception as e:
                # Log the exception
                print(repr(e))

                # Some error happened: do not proceed generating the config
                exit(1)

        # Parse the database and convert it to the Onionprobe endpoints format
        for item in data:
            print('Processing %s...' % (item['site_name']))

            url      = urllib.parse.urlparse(item['onion_url'])
            address  = url.netloc
            protocol = url.scheme if url.scheme != '' else 'http'
            port     = 80 if protocol == 'http' else 443
            paths    = [{
                'path': url.path if url.path != '' else '/',
                }]

            # Append to the endpoints dictionary
            if item['site_name'] not in endpoints:
                endpoints[item['site_name']] = {
                        'address' : address,
                        'protocol': protocol,
                        'port'    : port,
                        'paths'   : paths,
                        }

        return endpoints

if __name__ == "__main__":
    """Process from CLI"""

    args = cmdline_compiler(databases['real-world-onion-sites'])

    if args.source != None:
        args.databases = {
                'real-world-onion-sites': args.source,
                }

        del args.source

    instance = RealWorldOnionSites(**vars(args))

    instance.compile()
