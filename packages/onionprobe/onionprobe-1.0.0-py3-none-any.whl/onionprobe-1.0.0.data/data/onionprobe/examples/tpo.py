#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Compile an Onionprobe configuration file from The Tor Project official
# Onion Services list.
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
import json
import argparse
import urllib.parse

from onionprobe.config import OnionprobeConfigCompiler, basepath, cmdline_parser_compiler, cmdline_compiler

try:
    import requests
except ImportError:
    print("Please install requests first!")
    raise ImportError

# The list of external databases handled by this implementation
databases = {
        'tpo': 'https://onion.torproject.org/onionbalancev3-services.yaml',
        }

class TPOSites(OnionprobeConfigCompiler):
    """
    Handles official Tor Project Onion Services list.

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

        data = {}

        # Get the Onion Service database from a remote API
        if os.path.exists(self.databases[database]):
            print('Using list of %s database endpoints from %s...' % (
                database, self.databases[database]))

            with open(self.databases[database], 'r') as result:
                for line in result.readlines():
                    items = data.update(json.loads(line))

        else:
            try:
                print('Fetching remote list of %s database endpoints from %s...' % (database, self.databases[database]))
                result = requests.get(self.databases[database])

            except Exception as e:
                # Log the exception
                print(repr(e))

                # Some error happened: do not proceed generating the config
                exit(1)

            for line in result.text.split('\n'):
                if line != '':
                    data.update(json.loads(line))

        endpoints = {}

        # Parse the database and convert it to the Onionprobe endpoints format
        for item in data:
            print('Processing %s...' % (data[item]))

            # Complete parsing
            # Does not work right now since the 'onion_address' field is not
            # RFC 1808 compliant.
            # See https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
            #url      = urllib.parse.urlparse(data[item])
            #address  = url.netloc
            #protocol = url.scheme if url.scheme != '' else 'http'
            #port     = 80 if protocol == 'http' else 443
            #paths    = [{
            #    'path': url.path if url.path != '' else '/',
            #    }]

            # Simpler parsing, assuming HTTP on port 80 and default path
            address  = data[item]
            protocol = 'http'
            port     = 80
            paths    = [{
                'path': '',
                }]

            # Append to the endpoints dictionary
            if item not in endpoints:
                # We can index either by the project title or by it's Onion Name
                #endpoints[item['onion_name']] = {
                endpoints[item] = {
                        'address' : address,
                        'protocol': protocol,
                        'port'    : port,
                        'paths'   : paths,
                        }

        return endpoints

    def build_onionprobe_config(self):
        """
        Overrides OnionprobeConfigCompiler.build_onionprobe_config()
        method with custom logic.

        """

        # Set the interval and disable shuffling and randomization
        print('Enforcing shuffle, randomize, interval and sleep configurations, no matter what the template or the user says.')
        self.config['shuffle']   = False
        self.config['randomize'] = False
        self.config['interval']  = 60
        self.config['sleep']     = 60

        # Build the configuration
        super().build_onionprobe_config()

if __name__ == "__main__":
    """Process from CLI"""

    args = cmdline_compiler(databases['tpo'])

    if args.source != None:
        args.databases = {
                'tpo': args.source,
                }

        del args.source

    instance = TPOSites(**vars(args))

    instance.compile()
