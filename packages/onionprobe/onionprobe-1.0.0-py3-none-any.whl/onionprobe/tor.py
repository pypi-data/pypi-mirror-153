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
import shutil
import random

try:
    import stem
    import stem.control
    import stem.process
    import stem.util
except ImportError:
    print("Please install stem library first!")
    raise ImportError

class OnionprobeTor:
    """
    Onionprobe class with Tor-related methods.
    """

    def initialize_tor(self):
        """
        Initialize Tor control connection

        :rtype: bol
        :return: True if initialization is successful, False on error
        """

        control_address = self.get_config('tor_address')
        control_port    = self.get_config('control_port')

        # Ensure control_address is an IP address, which is the
        # only type currently supported by stem
        #
        # Right now only IPv4 is supported
        import socket
        control_address = socket.gethostbyname(control_address)

        if self.get_config('launch_tor'):
            if self.launch_tor() is False:
                self.log("Error initializing Tor", "critical")

                return False

        try:
            self.controller = stem.control.Controller.from_port(
                    address=control_address,
                    port=control_port)

        except stem.SocketError as exc:
            self.log("Unable to connect to tor on port 9051: %s" % exc, "critical")

            return False

        return True

    def initialize_tor_auth(self):
        """
        Initialize an authenticated Tor control connection

        :rtype: bol
        :return: True if initialization is successful, False on error
        """

        if 'controller' not in dir(self):
            self.log("Unable to find a Tor control connection", "critical")

            return False

        # Evaluate control password only after we're sure that a Tor
        # process is running in the case that 'launch_tor' is True
        control_password = self.get_config('control_password')

        if control_password is False:
            # First try to authenticate without a password
            try:
                self.controller.authenticate()

            # Then fallback to ask for a password
            except stem.connection.MissingPassword:
                import getpass
                control_password = getpass.getpass("Controller password: ")

                try:
                    self.controller.authenticate(password=control_password)
                except stem.connection.PasswordAuthFailed:
                    self.log("Unable to authenticate, password is incorrect", "critical")

                    return False

        else:
            try:
                self.controller.authenticate(password=control_password)
            except stem.connection.PasswordAuthFailed:
                self.log("Unable to authenticate, password is incorrect", "critical")

                return False

        return True

    def initialize_listeners(self):
        """
        Initialize Tor event listeners
        """

        # Stream management
        # See https://stem.torproject.org/tutorials/to_russia_with_love.html
        if self.get_config('new_circuit'):
            self.controller.set_conf('__LeaveStreamsUnattached', '1')
            self.controller.add_event_listener(self.new_circuit, stem.control.EventType.STREAM)

            self.circuit_id = None

        # Add listener for Onion Services descriptors
        self.controller.add_event_listener(self.hsdesc_event, stem.control.EventType.HS_DESC)

    #
    # Tor related logic
    #

    def gen_control_password(self):
        """
        Generates a random password

        :rtype: str
        :return: A random password between 22 and 32 bytes
        """

        import secrets

        return secrets.token_urlsafe(random.randrange(22, 32))

    def hash_password(self, password):
        """
        Produce a hashed password in the format used by HashedControlPassword

        It currently relies on spawning a "tor --hash-password" process so it suffering
        from the security issue of temporarily exposing the unhashed password in the
        operating system's list of running processes.

        :type  password: str
        :param password: A password to be hashed

        :rtype: str
        :return: The hashed password
        """

        import subprocess

        tor    = shutil.which('tor')
        result = subprocess.check_output([tor, '--hash-password', password], text=True)

        return result

    def launch_tor(self):
        """
        Launch a built-in Tor process

        See https://stem.torproject.org/tutorials/to_russia_with_love.html
            https://stem.torproject.org/api/process.html

        """

        # Check if the tor executable is available
        if shutil.which('tor') is None:
            self.log('Cannot find the tor executable. Is it installed?', 'critical')

            return False

        from stem.util import term

        # Helper function to print bootstrap lines
        def print_bootstrap_lines(line):
            if "Bootstrapped " in line:
                self.log(term.format(line), 'debug')

        try:
            self.log('Initializing Tor process...')

            tor_address      = self.get_config('tor_address')
            control_password = self.get_config('control_password', self.gen_control_password())
            self.tor         = stem.process.launch_tor_with_config(
                    config = {
                        'SocksPort'            : tor_address + ':' + str(self.get_config('socks_port')),
                        'ControlPort'          : tor_address + ':' + str(self.get_config('control_port')),
                        'HashedControlPassword': self.hash_password(control_password),
                        'CircuitStreamTimeout' : str(self.get_config('circuit_stream_timeout')),

                        #'Log'                 : [
                        #    'NOTICE stdout',
                        #    ],
                        },
                        init_msg_handler = print_bootstrap_lines,
                    )

        except OSError as e:
            self.log(e, 'error')

            return False

    def new_circuit(self, stream):
        """
        Setup a fresh Tor circuit for new streams

        See https://stem.torproject.org/tutorials/to_russia_with_love.html

        :type  stream: stem.response.events.StreamEvent
        :param stream: Stream event
        """

        self.log('Building new circuit...', 'debug')

        # Remove the old circuit
        if self.circuit_id is not None:
            self.log('Removing old circuit {}...'.format(self.circuit_id), 'debug')
            self.controller.close_circuit(self.circuit_id)

        # Create new circuit
        self.circuit_id = self.controller.new_circuit(await_build=True)

        # Attach the new stream
        if stream.status == 'NEW':
            self.log('Setting up new circuit {}...'.format(self.circuit_id), 'debug')
            self.controller.attach_stream(stream.id, self.circuit_id)
