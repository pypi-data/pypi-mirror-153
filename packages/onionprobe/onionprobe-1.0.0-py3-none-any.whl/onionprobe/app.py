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
import sys
import os
import signal

from .init       import OnionprobeInit
from .config     import OnionprobeConfig
from .logger     import OnionprobeLogger
from .time       import OnionprobeTime
from .tor        import OnionprobeTor
from .descriptor import OnionprobeDescriptor
from .metrics    import OnionprobeMetrics
from .prober     import OnionprobeProber
from .http       import OnionprobeHTTP
from .teardown   import OnionprobeTeardown
from .main       import OnionprobeMain

class Onionprobe(
        # Inherit from subsystems
        OnionprobeInit,
        OnionprobeConfig,
        OnionprobeLogger,
        OnionprobeTime,
        OnionprobeTor,
        OnionprobeDescriptor,
        OnionprobeMetrics,
        OnionprobeProber,
        OnionprobeHTTP,
        OnionprobeTeardown,
        OnionprobeMain,
        ):
    """
    Onionprobe class to test and monitor Tor Onion Services
    """

def finish(status=0):
    """
    Stops Onionprobe

    :type  status: int
    :param status: Exit status code.
    """

    try:
        sys.exit(status)
    except SystemExit:
        os._exit(status)

def finish_handler(signal, frame):
    """
    Wrapper around finish() for handling system signals

    :type  signal: int
    :param signal: Signal number.

    :type  frame: object
    :param frame: Current stack frame.
    """

    print('Signal received, stopping Onionprobe..')

    finish(1)

def run(args):
    """
    Run Onionprobe from arguments

    :type  args: dict
    :param args: Instance arguments.
    """

    # Register signal handling
    #signal.signal(signal.SIGINT, finish_handler)
    signal.signal(signal.SIGTERM, finish_handler)

    status = 0

    # Dispatch
    try:
        probe = Onionprobe(args)

        if probe.initialize() is not False:
            probe.run()
        else:
            status = 1

            print('Error: could not initialize')

    # Handle user interruption
    # See https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
    except KeyboardInterrupt as e:
        probe.log('Stopping Onionprobe due to user request...')

    except FileNotFoundError as e:
        status = 1

        print('File not found: ' + str(e))

    except Exception as e:
        status = 1

        print(repr(e))

    finally:
        if 'probe' in locals():
            probe.close()

        finish(status)

def run_from_cmdline():
    """
    Run Onionprobe getting arguments from the command line.
    """

    from .config import cmdline

    run(cmdline())
