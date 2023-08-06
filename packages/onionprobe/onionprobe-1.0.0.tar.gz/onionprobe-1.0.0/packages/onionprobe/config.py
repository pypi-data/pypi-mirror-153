#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Handle Onionprobe configurations.
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
import os
import argparse

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

# The Onionprobe version string
# Uses Semantic Versioning 2.0.0
# See https://semver.org
onionprobe_version = '1.0.0'

# The base path for this project
basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir) + os.sep

# Describe configuration options
config = {
        'log_level': {
            'help'    : 'Log level : debug, info, warning, error or critical',
            'default' : 'info',
            'action'  : 'store',
            },

        'launch_tor': {
            'help'    : "Whether to launch it's own Tor daemon (set to false to use the system-wide Tor process)",
            'default' : True,
            'action'  : argparse.BooleanOptionalAction,
            },

        'tor_address': {
            'help'    : 'Tor listening address if the system-wide service is used',
            'default' : '127.0.0.1',
            'action'  : 'store',
            },

        'socks_port': {
            'help'    : 'Tor SOCKS port',
            'default' : 19050,
            'action'  : 'store',
            },

        'control_port': {
            'help'    : 'Tor control port',
            'default' : 19051,
            'action'  : 'store',
            },

        'control_password': {
            'help'    : """Set Tor control password or use a password prompt
                           (system-wide Tor service) or auto-generate a temporary password
                           (built-in Tor service)""".strip(),
            'default' : None,
            'action'  : 'store',
            },

        'loop': {
            'help'    : 'Run Onionprobe continuously',
            'default' : False,
            'action'  : argparse.BooleanOptionalAction,
            },

        'prometheus_exporter': {
            'help'    : 'Enable Prometheus exporting functionality',
            'default' : False,
            'action'  : argparse.BooleanOptionalAction,
            },

        'prometheus_exporter_port': {
            'help'    : 'Set the Prometheus exporter port',
            'default' : 9935,
            'action'  : 'store',
            },

        'shuffle': {
            'help'    : 'Shuffle the list of endpoints at each probing round',
            'default' : True,
            'action'  : argparse.BooleanOptionalAction,
            },

        'randomize': {
            'help'    : 'Randomize the interval between each probing',
            'default' : True,
            'action'  : argparse.BooleanOptionalAction,
            },

        'new_circuit': {
            'help'    : 'Get a new circuit for every stream',
            'default' : False,
            'action'  : argparse.BooleanOptionalAction,
            },

        'interval': {
            'help'    : 'Max random interval in seconds between probing each endpoint',
            'default' : 60,
            'action'  : 'store',
            },

        'sleep': {
            'help'    : 'Max random interval in seconds to wait between each round of tests',
            'default' : 60,
            'action'  : 'store',
            },

        'rounds': {
            'help'    : """Run only a limited number of rounds (i.e., the
                           number of times that Onionprobe tests all the configured
                           endpoints). Requires the "loop" option to be enabled. Set to 0 to
                           disable this limit.""".strip(),
            'default' : 0,
            'action'  : 'store',
            },

        'descriptor_max_retries': {
            'help'    : 'Max retries when fetching a descriptor',
            'default' : 5,
            'action'  : 'store',
            },

        'descriptor_timeout': {
            'help'    : 'Timeout in seconds when retrieving an Onion Service descriptor',
            'default' : 30,
            'action'  : 'store',
            },

        'http_connect_timeout': {
            'help'    : 'Connection timeout for HTTP/HTTPS requests',
            'default' : 30,
            'action'  : 'store',
            },

        'http_connect_max_retries': {
            'help'    : 'Max retries when doing a HTTP/HTTPS connection to an Onion Service',
            'default' : 3,
            'action'  : 'store',
            },

        'http_read_timeout': {
            'help'    : 'Read timeout for HTTP/HTTPS requests',
            'default' : 30,
            'action'  : 'store',
            },

        'circuit_stream_timeout': {
            'help'    : 'Sets how many seconds until a stream is detached from a circuit and try a new circuit',
            'default' : 60,
            'action'  : 'store',
            },

        'endpoints': {
            'help': 'The list of endpoints to be tested',
            'default': {
                'www.torproject.org': {
                    'address' : '2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion',
                    'protocol': 'http',
                    'port'    : '80',
                    'paths'   : [
                        {
                            'path'   : '/',
                            'pattern': 'Tor Project',
                            },
                        ],
                    },
                }
            },
        }

def cmdline_parser():
    """
    Generate command line arguments

    :rtype: argparse.ArgumentParser
    :return: The parser object
    """

    epilog = """Examples:

      onionprobe -c configs/tor.yaml
      onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion
    """

    epilog += """\nAvailable metrics:
    """

    from .metrics import metrics

    for metric in metrics:
        item = metrics[metric].describe()[0]

        epilog += "\n  {}:\n        {}".format(item.name, item.documentation)

    description = 'Test and monitor onion services'
    parser      = argparse.ArgumentParser(
                    prog='onionprobe',
                    description=description,
                    epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    parser.add_argument('-c', '--config', help="""
                        Read options from configuration file. All command line
                        parameters can be specified inside a YAML file.
                        Additional command line parameters override those set
                        in the configuration file.""".strip())

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + onionprobe_version)

    for argument in sorted(config):
        if argument == 'endpoints':
            parser.add_argument('-e', '--endpoints', nargs='*', help='Add endpoints to the test list', metavar="ONION-ADDRESS1")

        else:
            config[argument]['type'] = type(config[argument]['default'])

            parser.add_argument('--' + argument, **config[argument])

    return parser

def cmdline():
    """
    Evalutate the command line.

    :rtype: argparse.Namespace
    :return: Command line arguments.
    """

    parser = cmdline_parser()
    args   = parser.parse_args()

    if args.config is None and args.endpoints is None:
        parser.print_usage()
        exit(1)

    return args

class OnionprobeConfig:
    """
    Onionprobe class with configuration-related methods.
    """

    def get_config(self, item, default = None):
        """
        Helper to get instance configuration

        Retrieve a config parameter from the self.config object or use a
        default value as fallback

        :type  item: str
        :param item: Configuration item name

        :param default: Default config value to be used as a fallback if there's
                        no self.config[item] available.
                        Defaults to None

        :return: The configuration parameter value or the default fallback value.
        """

        if self.config is None:
            self.config = {}

        if item in self.config:
            return self.config[item]

        # Optionally override the default with an argument provided
        elif default is not None:
            self.config[item] = default

            return default

        return config[item]['default']

class OnionprobeConfigCompiler:
    """Base class to build Onionprobe configs from external sources of Onion Services"""

    def __init__(self, databases, config_template, output_folder, wait=0, config_overrides=None, loop=False):
        """
        Constructor for the OnionprobeConfigCompiler class.

        Loads the default Onionprobe configuration to be used as a template.

        Keeps the dictionary of Onion Services databases as a class attribute.

        :type  databases: dict
        :param databases: Dictionary of data sources to fetch .onion sites.
                          Format is { 'database_name': 'database_url' }

        :type  config_template: str
        :param config_template: Configuration file path to be used as template

        :type  output_folder: str
        :param output_folder: Output folder where configs are written
        """

        # Initialize the configuration object
        self.config = {}

        # Save the databases of Onion Services
        self.databases = databases

        # Load the default configuration file as a template
        if os.path.exists(config_template):
            print('Loading configuration template from %s...' % (config_template))

            with open(config_template, 'r') as base_config:
                self.config = yaml.load(base_config, yaml.CLoader)

        else:
            raise FileNotFoundError(config_template)

        # Set the output folder
        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            raise FileNotFoundError(output_folder)

        # Set wait time
        self.wait = wait

        # Set loop configuration
        self.loop = loop

        # Apply overrides
        if config_overrides != None:
            # Copy item by item, ensuring type casting
            for item in config_overrides:
                override = item.split('=')

                if len(override) != 2:
                    print('Skipping malformed override param %s...' % (item))
                    continue

                key   = str(override[0])
                value = override[1]

                if key not in config:
                    print('Skipping unknown parameter %s...' % (key))
                    continue

                cast = type(config[key]['default'])

                if cast == bool:
                    value.lower()

                    self.config[key] = True if value == 'true' else False
                else:
                    self.config[key] = cast(value)

                print('Setting %s to %s.' % (key, value))

    def build_endpoints_config(self, database):
        """
        Build the Onion Service endpoints dictionary.

        This method is only a placeholder.

        By default this method returns an empty dictionary as it's meant to be
        overriden by specific implementations inheriting from the
        OnionprobeConfigCompiler base class and where custom logic for
        extracting .onion endpoints from external databases should be located.

        :type database : str
        :param database: A database name from the databases dictionary. This
                         parameter allows accesing the URL of the external
                         database from the self.databases class attribute.

        :rtype: dict
        :return: Onion Service endpoints in the format accepted by Onionprobe.
        """

        return dict()

    def build_onionprobe_config(self):
        """
        Build an Onionprobe config.

        Writes an Onionprobe-compatible configuration file for each database
        listed in self.databases attribute.

        The Onion Service endpoints are generated from the
        build_endpoints_config() methods. To be effective, it's required that
        classes inheriting from this base class to implement the
        build_endpoints_configs() method.

        The filenames ared derived from the database names (each key from the
        self.databases attribute).
        """

        for database in self.databases:
            try:
                print('Building the list of endpoints for database %s...' % (database))

                # Build list of endpoints
                endpoints = self.build_endpoints_config(database)

                # Create a new config using the default as base
                new_config = dict(self.config)

                # Replace the endpoints
                new_config['endpoints'] = endpoints

                # Build the output path
                output_folder = os.path.normpath(os.path.join(self.output_folder, database + '.yaml'))

                # Save
                with open(output_folder, 'w') as output:
                    print('Saving the generated config for database %s into %s...' % (database, output_folder))

                    output.write(yaml.dump(new_config))

            except Exception as e:
                print(e)

    def build_and_wait(self):
        """
        Build Onionprobe configs, then wait.
        """

        self.build_onionprobe_config()

        if self.wait != 0:
            import time

            print('Waiting %s seconds...' % (self.wait))
            time.sleep(self.wait)

    def compile(self):
        """
        Main compilation procedure.

        """

        if self.loop is True:
            while True:
                self.build_and_wait()
        else:
            self.build_and_wait()

def cmdline_parser_compiler(default_source=None):
    """
    Generate command line arguments for the configuration compiler

    :rtype: argparse.ArgumentParser
    :return: The parser object
    """

    description = 'Generates an Onionprobe config file from ' + default_source
    parser      = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    # Try to use the configs/ folder as the default config_template (will match
    # when running directly from the Onionprobe repository or from the python
    # package)
    config_template = os.path.normpath(os.path.join(basepath, 'configs', 'tor.yaml'))

    # Fallback config_template to /etc/onionprobe
    if not os.path.exists(config_template):
        config_template = os.path.normpath(os.path.join(os.sep, 'etc', 'onionprobe', 'tor.yaml'))

    # Try to use the configs/ folder as the default output_folder (will match
    # when running directly from the Onionprobe repository or from the python
    # package)
    output_folder = os.path.join(basepath, 'configs')

    # Fallback output_folder to the current working directory
    if not os.path.exists(output_folder):
        output_folder = os.getcwd()

    parser.add_argument('-s', '--source',
            dest='source',
            default=default_source,
            help="Database source file or endpoint (default: %(default)s)")

    parser.add_argument('-t', '--config_template',
            dest='config_template',
            default=config_template,
            help="Configuration template to use (default %(default)s)")

    parser.add_argument('-o', '--output_folder',
            dest='output_folder',
            default=output_folder,
            help="Output folder where config should be saved (default: current working directory)")

    parser.add_argument('-w', '--wait',
            dest='wait',
            default=0,
            type=int,
            help="""Wait a number of seconds before exiting after writing the config.
                    Useful for a configurator container service tha should run periodically
                    (default: %(default)s)""".strip())

    parser.add_argument('-l', '--loop',
            dest='loop',
            action='store_true',
            default=False,
            help="""Whether to continuously generate configuration.
                    Useful when set in conjunction with --wait (default: %(default)s)""")

    parser.add_argument('-c', '--config_overrides',
            dest='config_overrides',
            default=None,
            nargs='*',
            help="Override configuration parameters in the form of param1=value1 ... paramN=valueN")

    return parser

def cmdline_compiler(default_source=None):
    """
    Evalutate the command line for the configuration compiler.

    :rtype: argparse.Namespace
    :return: Command line arguments.
    """

    parser = cmdline_parser_compiler(default_source)
    args   = parser.parse_args()

    return args
