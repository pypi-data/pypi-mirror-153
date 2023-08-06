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

from .config           import onionprobe_version
from prometheus_client import Counter, Gauge, Info, Enum

# Holds all metrics
metrics = {
    #
    # Metametrics: data about the Onionprobe instance itself
    #

    'onionprobe_version': Info(
        'onionprobe_version',
        'Onionprobe version information',
        ),

    'onionprobe_state': Enum(
        'onionprobe_state',
        'Onionprobe latest state',
        states=['starting', 'probing', 'sleeping', 'stopping']
        ),

    #
    # Probing gauges: the basic data
    #

    'onionprobe_wait_seconds': Gauge(
            'onionprobe_wait_seconds',
            'Records how long Onionprobe waited between two probes in seconds',
        ),

    'onion_service_latency_seconds': Gauge(
            'onion_service_latency_seconds',
            'Register Onion Service connection latency in seconds',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    'onion_service_reachable': Gauge(
            'onion_service_reachable',
            "Register if the Onion Service is reachable: value is 1 for " + \
                    "reachability and 0 otherwise",
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    'onion_service_connection_attempts': Gauge(
            'onion_service_connection_attempts',
            "Register the number of attempts when trying to connect to an " + \
                    "Onion Service in a probing round",
            ['name', 'address', 'protocol', 'port', 'path', 'reachable']
        ),

    'onion_service_status_code': Gauge(
            'onion_service_status_code',
            'Register Onion Service connection HTTP status code',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    'onion_service_descriptor_latency_seconds': Gauge(
            'onion_service_descriptor_latency_seconds',
            'Register Onion Service latency in seconds to get the descriptor',
            ['name', 'address']
        ),

    'onion_service_descriptor_reachable': Gauge(
            'onion_service_descriptor_reachable',
            "Register if the Onion Service descriptor is available: value is " + \
                    "1 for reachability and 0 otherwise",
            ['name', 'address']
        ),

    'onion_service_descriptor_fetch_attempts': Gauge(
            'onion_service_descriptor_fetch_attempts',
            "Register the number of attempts required when trying to get an " + \
                    "Onion Service descriptor in a probing round",
            ['name', 'address', 'reachable']
        ),

    'onion_service_introduction_points_number': Gauge(
            'onion_service_introduction_points_number',
            'Register the number of introduction points in the Onion Service descriptor',
            ['name', 'address']
        ),

    'onion_service_match_pattern_matched': Gauge(
            'onion_service_pattern_matched',
            "Register whether a regular expression pattern is matched when " + \
                    "connection to the Onion Service: value is 1 for matched pattern and " + \
                    "0 otherwise",
            ['name', 'address', 'protocol', 'port', 'path', 'pattern']
        ),

    'onion_service_valid_certificate': Gauge(
            'onion_service_valid_certificate',
            "Register whether the Onion Service HTTPS certificate is valid: " + \
               "value is 1 for valid and 0 otherwise, but only for sites reachable " + \
               "using HTTPS",
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    #
    # Probing counters
    #

    # Prometheus documentation says:
    #
    # > "When you have a successful request count and a failed request count, the
    # > best way to expose this is as one metric for total requests and another
    # > metric for failed requests. This makes it easy to calculate the failure
    # > ratio. Do not use one metric with a failed or success label. Similarly,
    # > with hit or miss for caches, it’s better to have one metric for total and
    # > another for hits."
    # >
    # > -- https://prometheus.io/docs/instrumenting/writing_exporters/#naming
    'onion_service_fetch_requests_total': Counter(
            'onion_service_fetch_requests_total',
            'Counts the total number of requests to access an Onion Service',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    #'onion_service_fetch_success_total': Counter(
    #        'onion_service_fetch_success_total',
    #        'Counts the total number of successful fetches of an Onion Service',
    #        ['name', 'address', 'protocol', 'port', 'path']
    #    ),

    'onion_service_fetch_error_total': Counter(
            'onion_service_fetch_error_total',
            'Counts the total number of errors when fetching an Onion Service',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    'onion_service_descriptor_fetch_requests_total': Counter(
            'onion_service_descriptor_fetch_requests_total',
            'Counts the total number of requests to fetch an Onion Service descriptor',
            ['name', 'address']
        ),

    #'onion_service_descriptor_fetch_success_total': Counter(
    #        'onion_service_descriptor_fetch_success_total',
    #        'Counts the total number of successful fetches of an Onion Service descriptor',
    #        ['name', 'address']
    #    ),

    'onion_service_descriptor_fetch_error_total': Counter(
            'onion_service_descriptor_fetch_error_total',
            'Counts the total number of errors when fetching an Onion Service descriptor',
            ['name', 'address']
        ),

    #
    # Requests exception counter
    #

    # Counter for requests.RequestException
    'onion_service_request_exception_total': Counter(
            'onion_service_request_exception_total',
            'Counts the total number of Onion Service general exception errors',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.ConnectionError
    'onion_service_connection_error_total': Counter(
            'onion_service_connection_error_total',
            'Counts the total number of Onion Service connection errors',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.HTTPError
    'onion_service_http_error_total': Counter(
            'onion_service_http_error_total',
            'Counts the total number of Onion Service HTTP errors',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.TooManyRedirects
    'onion_service_too_many_redirects_total': Counter(
            'onion_service_too_many_redirects_total',
            'Counts the total number of Onion Service too many redirects errors',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.ConnectionTimeout
    'onion_service_connection_timeout_total': Counter(
            'onion_service_connection_timeout',
            'Counts the total number of Onion Service connection timeouts',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.ReadTimeout
    'onion_service_read_timeout_total': Counter(
            'onion_service_read_timeout_total',
            'Counts the total number of Onion Service read timeouts',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.Timeout
    'onion_service_timeout_total': Counter(
            'onion_service_timeout',
            'Counts the total number of Onion Service timeouts',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    # Counter for requests.exceptions.SSLError
    'onion_service_certificate_error_total': Counter(
            'onion_service_certificate_error',
            'Counts the total number of HTTPS certificate validation errors',
            ['name', 'address', 'protocol', 'port', 'path']
        ),

    #
    # Infos
    #

    'onion_service_descriptor': Info(
            'onion_service_descriptor',
            'Onion Service descriptor information, including state and Hidden Service ' + \
                    'Directory (HSDir) used',
            ['name', 'address']
        ),

    'onion_service_probe_status': Info(
            'onion_service_probe_status',
            'Register information about the last test made to a given Onion Service, ' + \
                    'including POSIX timestamp',
            ['name', 'address'],
        ),
    }

class OnionprobeMetrics:
    """
    Onionprobe class with metrics methods.
    """

    def initialize_prometheus_exporter(self):
        """
        Initialize the Prometheus Exporter
        """

        from prometheus_client import start_http_server

        port = self.get_config('prometheus_exporter_port')

        self.log('Initializing Prometheus HTTP exporter server at port %s...' % (port))
        start_http_server(port)

    def initialize_metrics(self):
        """
        Initialize the metrics subsystem

        It uses Prometheus metrics even if the Prometheus exporter is not in use.

        This means that the Prometheus metrics are always used, even if only for
        internal purposes, saving resources from preventing us to build additional
        metric logic.
        """

        # The metrics object
        self.metrics = metrics

        # Set version
        self.metrics['onionprobe_version'].info({
            'version': onionprobe_version,
            })

        # Set initial state
        self.metrics['onionprobe_state'].state('starting')

    def set_metric(self, metric, value, labels = {}):
        """
        Set a metric.

        :type  metric: str
        :param metric: Metric name

        :type  value: int
        :param value: Metric value

        :type  labels: dict
        :param labels: Metric labels dictionary.
                       Defaults to an empty dictionary.
        """

        if metric in self.metrics:
            self.metrics[metric].labels(**labels).set(value)

    def inc_metric(self, metric, value = 1, labels = {}):
        """
        Increment a metric.

        :type  metric: str
        :param metric: Metric name

        :type  value: int
        :param value: Increment value. Defaults to 1.

        :type  labels: dict
        :param labels: Metric labels dictionary.
                       Defaults to an empty dictionary.
        """

        if metric in self.metrics:
            self.metrics[metric].labels(**labels).inc(value)

    def state_metric(self, metric, value, labels = {}):
        """
        Set a metric state.

        :type  metric: str
        :param metric: Metric name

        :type  value: Object
        :param value: Increment value.

        :type  labels: dict
        :param labels: Metric labels dictionary.
                       Defaults to an empty dictionary.
        """

        if metric in self.metrics:
            self.metrics[metric].labels(**labels).state(value)

    def info_metric(self, metric, value, labels = {}):
        """
        Set an info metric.

        :type  metric: str
        :param metric: Metric name

        :type  value: dict
        :param value: Increment value.

        :type  labels: dict
        :param labels: Metric labels dictionary.
                       Defaults to an empty dictionary.
        """

        if metric in self.metrics:
            self.metrics[metric].labels(**labels).info(value)
