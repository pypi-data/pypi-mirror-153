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

class OnionprobeMain:
    """
    Onionprobe class with main application logic.
    """

    def run(self):
        """
        Main application loop

        Checks if should be run indefinitely.
        Then dispatch to a round of probes.

        If runs continuously, waits before starting the next round.

        If not, just returns.
        """

        # Check if should loop
        if self.get_config('loop'):
            iteration = 1
            rounds    = self.get_config('rounds')

            while True:
                self.log('Starting round %s, probing all defined endpoints...' % (iteration))

                # Call for a round
                self.round()

                # Check rounds
                if rounds > 0 and iteration >= rounds:
                    self.log('Stopping after %s rounds' % (iteration))

                    break

                self.log('Round %s completed.' % (iteration))

                # Then wait
                self.wait(self.get_config('sleep'))

                # Update iterations counter
                iteration += 1

        else:
            # Single pass, only one round
            self.round()

    def round(self):
        """
        Process a round of probes

        Each round is composed of the entire set of the endpoints
        which is optionally shuffled.

        Each endpoint is then probed.
        """

        # Shuffle the deck
        endpoints = sorted(self.get_config('endpoints'))

        if self.get_config('shuffle'):
            # Reinitializes the random number generator to avoid predictable
            # results if running countinuously for long periods.
            random.seed()

            endpoints = random.sample(endpoints, k=len(endpoints))

        # Probe each endpoint
        for key, endpoint in enumerate(endpoints):
            self.metrics['onionprobe_state'].state('probing')

            result = self.probe(endpoint)

            # Wait if not last endpoint
            if key != len(endpoints) - 1:
                self.wait(self.get_config('interval'))
