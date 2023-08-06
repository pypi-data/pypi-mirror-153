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

class OnionprobeTeardown:
    """
    Onionprobe class with methods related to... stop running!
    """

    def close(self):
        """
        Onionprobe teardown procedure.

        Change the internal metrics state to running.

        Stops the built-in Tor daemon.
        """

        if 'metrics' in dir(self):
            self.metrics['onionprobe_state'].state('stopping')

        if 'controller' in dir(self):
            self.controller.close()

        # Terminate built-in Tor
        if 'tor' in dir(self):
            self.tor.kill()
