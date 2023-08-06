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

try:
    import requests
except ImportError:
    print("Please install requests first!")
    raise ImportError

class OnionprobeHTTP:
    """
    Onionprobe class with HTTP methods.
    """

    def build_url(self, config, path = None):
        """
        Build an Onion Service URL to be probed

        :type  config: dict
        :param config: Endpoint configuration

        :type  path: str
        :param path: The path to be chosen in the endpoint configuration.

        :rtype: str
        :return: The Onion Service URL for the given config and path

        """

        # Get the base URL
        url = config['address']

        # Set the protocol
        if 'protocol' in config:
            url = config['protocol'] + '://' + url

        # Set the port
        if 'port' in config:
            url += ':' + str(config['port'])

        # Set the path
        #if 'path' in config:
        #    url += config['path']
        if path is not None:
            url += path

        return url

    def query(self, endpoint, config, path, attempt = 1):
        """
        Fetches endpoint from URL

        Tries an HTTP connection to the URL and update metrics when needed.

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :type  path: str
        :param path: The path to be chosen in the endpoint configuration.

        :rtype: requests.Response or False
        :return: The query result on success.
                 False on error.
        """

        # Setup query parameters
        url         = self.build_url(config, path)
        result      = False
        exception   = None
        init_time   = self.now()
        tor_address = self.get_config('tor_address')
        socks_port  = self.get_config('socks_port')
        valid_cert  = 1

        # Request everything via Tor, including DNS queries
        proxies = {
                'http' : 'socks5h://{}:{}'.format(tor_address, socks_port),
                'https': 'socks5h://{}:{}'.format(tor_address, socks_port),
                }

        # Metric labels
        labels = {
                'name'     : endpoint,
                'address'  : config['address'],
                'protocol' : config['protocol'],
                'port'     : config['port'],
                'path'     : path,
                }

        timeout = (
                self.get_config('http_connect_timeout'),
                self.get_config('http_read_timeout'),
                )

        try:
            self.log('Trying to connect to {} (attempt {})...'.format(url, attempt))
            self.inc_metric('onion_service_fetch_requests_total', 1, labels)

            # Fetch results and calculate the elapsed time
            result  = requests.get(url, proxies=proxies, timeout=timeout)
            elapsed = self.elapsed(init_time, True)

            # Update metrics
            self.set_metric('onion_service_latency_seconds', elapsed, labels)

        except requests.exceptions.TooManyRedirects as e:
            result    = False
            exception = 'too_many_redirects'

            self.log(e, 'error')

        except requests.exceptions.SSLError as e:
            result     = False
            exception  = 'certificate_error'
            valid_cert = 0

            self.log(e, 'error')

        # Requests that produced this error are safe to retry, but we are not
        # doing that right now
        except requests.exceptions.ConnectionTimeout as e:
            result    = False
            exception = 'connection_timeout'

            self.log(e, 'error')

        except requests.exceptions.ReadTimeout as e:
            result    = False
            exception = 'connection_read_timeout'

            self.log(e, 'error')

        except requests.exceptions.Timeout as e:
            result    = False
            exception = 'timeout'

            self.log(e, 'error')

        except requests.exceptions.HTTPError as e:
            result    = False
            exception = 'http_error'

            self.log(e, 'error')

        except requests.exceptions.ConnectionError as e:
            result    = False
            exception = 'connection_error'

            self.log(e, 'error')

        except requests.exceptions.RequestException as e:
            result    = False
            exception = 'request_exception'

            self.log(e, 'error')

        else:
            self.log('Status code is {}'.format(result.status_code))

            # Register status code in the metrics
            self.set_metric('onion_service_status_code', result.status_code, labels)

        finally:
            reachable = 0 if result is False else 1

            if result is False:
                retries   = self.get_config('http_connect_max_retries')

                # Try again until max retries is reached
                if attempt <= retries:
                    return self.query(endpoint, config, path, attempt + 1)

            # Register reachability on metrics
            self.set_metric('onion_service_reachable', reachable, labels)

            if config['protocol'] == 'https':
                self.set_metric('onion_service_valid_certificate', valid_cert, labels)

            if exception is not None:
                # Count exceptions
                self.inc_metric('onion_service_' + exception + '_total', 1, labels)

                # Count errors
                self.inc_metric('onion_service_fetch_error_total', 1, labels)

            #else:
            #    # Increment the total number of successful fetches
            #    self.inc_metric('onion_service_fetch_success_total', 1, labels)

            # Register the number of attempts on metrics
            labels['reachable'] = reachable
            self.set_metric('onion_service_connection_attempts', attempt, labels)

            return result
