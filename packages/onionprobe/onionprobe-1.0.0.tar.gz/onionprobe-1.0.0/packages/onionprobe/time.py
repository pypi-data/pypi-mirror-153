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
import random
import time

from datetime import datetime, timedelta

class OnionprobeTime:
    """
    Onionprobe class with timing-related methods.
    """

    def now(self):
        """
        Wrapper around datetime.now()

        :rtype: datetime.datetime
        :return: Current time.
        """

        return datetime.now()

    def wait(self, value):
        """
        Helper to wait some time

        :type  value: int
        :param value: Number of seconds to wait.
        """

        # Randomize if needed
        if self.get_config('randomize'):
            value = random.random() * value

        # Sleep, collecting metrics about it
        self.log('Waiting {} seconds...'.format(str(round(value))))
        self.metrics['onionprobe_wait_seconds'].set(value)
        self.metrics['onionprobe_state'].state('sleeping')
        time.sleep(value)

    def elapsed(self, init_time, verbose = False):
        """
        Calculate the time elapsed since an initial time.

        :type  init_time: datetime.datetime
        :param init_time: Initial time.

        :type  verbose: bol
        :param verbose: If verbose is True, logs the elapsed time.
                        Defaults to False.

        :rtype: int
        :return: Number of elapsed time in seconds
        """

        # Calculate the elapsed time
        elapsed = (datetime.now() - init_time)

        # Log the elapsed time
        if verbose:
            self.log("Elapsed time: " + str(elapsed))

        return timedelta.total_seconds(elapsed)

    def timestamp(self):
        """
        Wrapper around datetime.now().timestamp()

        :rtype: datetime.datetime
        :return: Current time.
        """

        return datetime.now().timestamp()
