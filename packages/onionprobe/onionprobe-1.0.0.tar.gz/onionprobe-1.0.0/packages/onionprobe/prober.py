#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Onionprobe test/monitor tool.
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

class OnionprobeProber:
    """
    Onionprobe class with probing methods.
    """

    def probe(self, endpoint):
        """
        Probe an unique endpoint

        Checks for a valid and published Onion Service descriptor for the endpoint.

        Then probes each path configured for the endpoint, storing the results in
        a dictionary.

        Ensure that each probe starts with a cleared Stem Controller cache.

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :rtype: dict or False
        :return: A dictionary of results for each path configured for the endpoint.
                 False in case of Onion Service descriptor error.
        """

        self.log("Processing {}...".format(endpoint))

        endpoints = self.get_config('endpoints')
        config    = endpoints[endpoint]

        # Check if the addres is valid
        from stem.util.tor_tools import is_valid_hidden_service_address

        if 'address' not in config:
            self.log('No address set for {}'.format(endpoint), 'error')

            return False

        elif is_valid_hidden_service_address(
                self.get_pubkey_from_address(config['address']), 3) is False:
            self.log('Invalid onion service address set for {}: {}'.format(
                endpoint, config['address']), 'error')

            return False

        # Register test metadata
        self.info_metric('onion_service_probe_status', {
            'last_tested_at_posix_timestamp': str(self.timestamp()),
            },
            {
            'name'   : endpoint,
            'address': config['address'],
            })

        # Ensure we always begin with a cleared cache
        # This allows to discover issues with published descriptors
        self.controller.clear_cache()

        # Ensure we use a new circuit every time
        # Needs to close all other circuits?
        # Needs to setup a 'controler' circuit?
        # Replaced by event listener at the initialize() method
        #circuit = self.controller.new_circuit()

        # Get Onion Service descriptor
        descriptor = self.get_descriptor(endpoint, config)

        if descriptor is False:
            self.log('Error getting the descriptor', 'error')

            return False

        # Ensure at least a single path
        if 'paths' not in config:
            config['paths'] = [
                        {
                            'path'   : '/',
                            'pattern': None,
                        },
                    ]

        results = {}

        # Query each path
        for path in config['paths']:
            result = self.query(endpoint, config, path['path'])

            if result is not False:
                # Check for a match
                if 'pattern' in path and path['pattern'] is not None:
                    import re
                    pattern = re.compile(path['pattern'])
                    match   = pattern.search(result.text)

                    self.log('Looking for pattern {}...'.format(path['pattern']))

                    if match is not None:
                        self.log('Match found: "%s"' % (path['pattern']))

                        matched               = 1
                        results[path['path']] = result
                    else:
                        self.log('Match not found: "%s"' % (path['pattern']))

                        matched               = 0
                        results[path['path']] = False

                    # Update metrics
                    self.set_metric('onion_service_pattern_matched',
                                    matched, {
                                        'name'     : endpoint,
                                        'address'  : config['address'],
                                        'protocol' : config['protocol'],
                                        'port'     : config['port'],
                                        'path'     : path,
                                        'pattern'  : path['pattern'],
                                    })

                else:
                    results[path['path']] = result

            else:
                self.log('Error querying {}'.format(config['address']), 'error')

                results[path['path']] = False

        return results
