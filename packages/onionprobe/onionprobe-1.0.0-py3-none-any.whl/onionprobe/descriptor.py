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

# Dependencies
import logging

try:
    import stem
except ImportError:
    print("Please install stem library first!")
    raise ImportError

class OnionprobeDescriptor:
    """
    Onionprobe class with Tor descriptor-related methods.
    """

    def get_pubkey_from_address(self, address):
        """
        Extract .onion pubkey from the address

        Leaves out the .onion domain suffix and any existing subdomains.

        :type  address: str
        :param address: Onion Service address

        :rtype: str
        :return: Onion Service public key
        """

        # Extract
        pubkey = address[0:-6].split('.')[-1]

        return pubkey

    def get_endpoint_by_pubkey(self, pubkey):
        """
        Get an endpoint configuration given an Onion Service pubkey.

        :type  pubkey: str
        :param pubkey: Onion Service pubkey

        :rtype: tuple or False
        :return: Endpoint name and configuration if a match is found.
                 False otherwise.
        """

        endpoints = self.get_config('endpoints')

        for name in endpoints:
            if self.get_pubkey_from_address(endpoints[name]['address']) == pubkey:
                return (name, endpoints[name])

        return False

    def get_descriptor(self, endpoint, config, attempt = 1):
        """
        Get Onion Service descriptor from a given endpoint

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :rtype: stem.descriptor.hidden_service.InnerLayer or False
        :return: The Onion Service descriptor inner layer on success.
                 False on error.
        """

        self.log('Trying to get descriptor for {} (attempt {})...'.format(config['address'], attempt))

        pubkey    = self.get_pubkey_from_address(config['address'])
        init_time = self.now()
        timeout   = self.get_config('descriptor_timeout')
        reachable = 1

        # Metrics labels
        labels = {
                'name'   : endpoint,
                'address': config['address'],
                }

        # Get the descriptor
        try:
            # Increment the total number of descriptor fetch attempts
            self.inc_metric('onion_service_descriptor_fetch_requests_total', 1, labels)

            # Try to get the descriptor
            descriptor = self.controller.get_hidden_service_descriptor(pubkey, timeout=timeout)

        except (stem.DescriptorUnavailable, stem.Timeout, stem.ControllerError, ValueError)  as e:
            reachable = 0
            inner     = False
            retries   = self.get_config('descriptor_max_retries')

            # Try again until max retries is reached
            if attempt <= retries:
                return self.get_descriptor(endpoint, config, attempt + 1)

        else:
            # Ensure it's converted to the v3 format
            #
            # See https://github.com/torproject/stem/issues/96
            #     https://stem.torproject.org/api/control.html#stem.control.Controller.get_hidden_service_descriptor
            #     https://gitlab.torproject.org/legacy/trac/-/issues/25417
            from stem.descriptor.hidden_service import HiddenServiceDescriptorV3
            descriptor = HiddenServiceDescriptorV3.from_str(str(descriptor))

            # Decrypt the inner layer
            inner = descriptor.decrypt(pubkey)

            # Get introduction points
            # See https://stem.torproject.org/api/descriptor/hidden_service.html#stem.descriptor.hidden_service.IntroductionPointV3
            #for introduction_point in inner.introduction_points:
            #    self.log(introduction_point.link_specifiers, 'debug')

            if 'introduction_points' in dir(inner):
                self.set_metric('onion_service_introduction_points_number',
                                len(inner.introduction_points), labels)

            elapsed = self.elapsed(init_time, True)

            self.set_metric('onion_service_descriptor_latency_seconds',
                            elapsed, labels)

        finally:
            if inner is False:
                self.inc_metric('onion_service_descriptor_fetch_error_total', 1, labels)
            #else:
            #    # Increment the total number of sucessful descriptor fetch attempts
            #    self.inc_metric('onion_service_descriptor_fetch_success_total', 1, labels)

            labels['reachable'] = reachable

            # Register the number of fetch attempts in the current probing round
            self.set_metric('onion_service_descriptor_fetch_attempts',
                            attempt, labels)

            # Return the inner layer or False
            return inner

    def hsdesc_event(
            self,
            event,
            ):
        """
        Process HS_DESC events.

        Sets the onion_service_descriptor_reachable metric.

        See https://gitlab.torproject.org/tpo/core/torspec/-/blob/main/control-spec.txt

        :type  event : stem.response.events.HSDescEvent
        :param stream: HS_DESC event
        """

        if event.action not in [ 'RECEIVED', 'FAILED' ]:
            return

        # Get the endpoint configuration
        (name, endpoint) = self.get_endpoint_by_pubkey(event.address)

        # Metrics labels
        labels = {
                'name'   : name,
                'address': event.address + '.onion',
                }

        if event.action == 'RECEIVED':
            reason = event.action

            self.set_metric('onion_service_descriptor_reachable', 1, labels)

        elif event.action == 'FAILED':
            # See control-spec.txt section "4.1.25. HiddenService descriptors"
            # FAILED action is split into it's reasons
            reason = event.reason

            self.set_metric('onion_service_descriptor_reachable', 0, labels)

        self.info_metric('onion_service_descriptor', {
            'hsdir': event.directory,
            'state': reason,
            },
            labels)
