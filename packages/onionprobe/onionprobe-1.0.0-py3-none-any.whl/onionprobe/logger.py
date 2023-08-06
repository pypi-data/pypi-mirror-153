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

from .config import onionprobe_version

try:
    import stem.util
except ImportError:
    print("Please install stem library first!")
    raise ImportError

class OnionprobeLogger:
    """
    Onionprobe class with logging methods.
    """

    def initialize_logging(self):
        """
        Initialize Onionprobe's logging subsystem

        :rtype: bol
        :return: True if initialization is successful, False on error
        """

        log_level = self.get_config('log_level').upper()

        if log_level in dir(logging):
            level = getattr(logging, log_level)

            logging.basicConfig(level=level, format='%(asctime)s %(levelname)s: %(message)s')

            # See https://stem.torproject.org/api/util/log.html
            stem_logger = stem.util.log.get_logger()

            stem_logger.setLevel(level)

        else:
            logging.error("Invalid log level %s" % (log_level))

            return False

        self.log('Starting Onionprobe version %s...' % (onionprobe_version))

        return True

    def log(self, message, level='info'):
        """
        Helper log function

        Appends a message into the logging subsystem.

        :type  message: str
        :param message: The message to be logged.

        :type  level: str
        :param level: The log level. Defaults to 'info'.
                      For the available log levels, check
                      https://docs.python.org/3/howto/logging.html#logging-levels
        """

        # Just a wrapper for the logging() function
        getattr(logging, level)(message)
