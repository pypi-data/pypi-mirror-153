% ONIONPROBE(1) Onionprobe User Manual
% Silvio Rhatto <rhatto@torproject.org>
% May 31, 2022

# NAME

Onionprobe - a test and monitoring tool for Onion Services sites

# SYNOPSIS

onionprobe [-h] [-c CONFIG] [-v] [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT] [--control_password CONTROL_PASSWORD] [--control_port CONTROL_PORT] [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                  [--descriptor_timeout DESCRIPTOR_TIMEOUT] [-e [ONION-ADDRESS1 ...]] [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES] [--http_connect_timeout HTTP_CONNECT_TIMEOUT] [--http_read_timeout HTTP_READ_TIMEOUT]
                  [--interval INTERVAL] [--launch_tor | --no-launch_tor] [--log_level LOG_LEVEL] [--loop | --no-loop] [--new_circuit | --no-new_circuit] [--prometheus_exporter | --no-prometheus_exporter]
                  [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT] [--randomize | --no-randomize] [--rounds ROUNDS] [--shuffle | --no-shuffle] [--sleep SLEEP] [--socks_port SOCKS_PORT] [--tor_address TOR_ADDRESS]


# DESCRIPTION

Onionprobe is a tool for testing and monitoring the status of Tor Onion
Services sites.

It can run a single time or continuously to probe a set of
onion services endpoints and paths, optionally exporting to Prometheus.

# FULL INVOCATION, OPTIONS, EXAMPLES AND METRICS

    onionprobe [-h] [-c CONFIG] [-v] [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT] [--control_password CONTROL_PASSWORD] [--control_port CONTROL_PORT] [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                      [--descriptor_timeout DESCRIPTOR_TIMEOUT] [-e [ONION-ADDRESS1 ...]] [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES] [--http_connect_timeout HTTP_CONNECT_TIMEOUT] [--http_read_timeout HTTP_READ_TIMEOUT]
                      [--interval INTERVAL] [--launch_tor | --no-launch_tor] [--log_level LOG_LEVEL] [--loop | --no-loop] [--new_circuit | --no-new_circuit] [--prometheus_exporter | --no-prometheus_exporter]
                      [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT] [--randomize | --no-randomize] [--rounds ROUNDS] [--shuffle | --no-shuffle] [--sleep SLEEP] [--socks_port SOCKS_PORT] [--tor_address TOR_ADDRESS]

    Test and monitor onion services

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Read options from configuration file. All command line parameters can be specified inside a YAML file. Additional command line parameters override those set in the configuration file.
      -v, --version         show program's version number and exit
      --circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT
                            Sets how many seconds until a stream is detached from a circuit and try a new circuit
      --control_password CONTROL_PASSWORD
                            Set Tor control password or use a password prompt (system-wide Tor service) or auto-generate a temporary password (built-in Tor service)
      --control_port CONTROL_PORT
                            Tor control port
      --descriptor_max_retries DESCRIPTOR_MAX_RETRIES
                            Max retries when fetching a descriptor
      --descriptor_timeout DESCRIPTOR_TIMEOUT
                            Timeout in seconds when retrieving an Onion Service descriptor
      -e [ONION-ADDRESS1 ...], --endpoints [ONION-ADDRESS1 ...]
                            Add endpoints to the test list
      --http_connect_max_retries HTTP_CONNECT_MAX_RETRIES
                            Max retries when doing a HTTP/HTTPS connection to an Onion Service
      --http_connect_timeout HTTP_CONNECT_TIMEOUT
                            Connection timeout for HTTP/HTTPS requests
      --http_read_timeout HTTP_READ_TIMEOUT
                            Read timeout for HTTP/HTTPS requests
      --interval INTERVAL   Max random interval in seconds between probing each endpoint
      --launch_tor, --no-launch_tor
                            Whether to launch it's own Tor daemon (set to false to use the system-wide Tor process) (default: True)
      --log_level LOG_LEVEL
                            Log level : debug, info, warning, error or critical
      --loop, --no-loop     Run Onionprobe continuously (default: False)
      --new_circuit, --no-new_circuit
                            Get a new circuit for every stream (default: False)
      --prometheus_exporter, --no-prometheus_exporter
                            Enable Prometheus exporting functionality (default: False)
      --prometheus_exporter_port PROMETHEUS_EXPORTER_PORT
                            Set the Prometheus exporter port
      --randomize, --no-randomize
                            Randomize the interval between each probing (default: True)
      --rounds ROUNDS       Run only a limited number of rounds (i.e., the number of times that Onionprobe tests all the configured endpoints). Requires the "loop" option to be enabled. Set to 0 to disable this limit.
      --shuffle, --no-shuffle
                            Shuffle the list of endpoints at each probing round (default: True)
      --sleep SLEEP         Max random interval in seconds to wait between each round of tests
      --socks_port SOCKS_PORT
                            Tor SOCKS port
      --tor_address TOR_ADDRESS
                            Tor listening address if the system-wide service is used

    Examples:

          onionprobe -c configs/tor.yaml
          onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion

    Available metrics:

      onionprobe_version:
            Onionprobe version information
      onionprobe_state:
            Onionprobe latest state
      onionprobe_wait_seconds:
            Records how long Onionprobe waited between two probes in seconds
      onion_service_latency_seconds:
            Register Onion Service connection latency in seconds
      onion_service_reachable:
            Register if the Onion Service is reachable: value is 1 for reachability and 0 otherwise
      onion_service_connection_attempts:
            Register the number of attempts when trying to connect to an Onion Service in a probing round
      onion_service_status_code:
            Register Onion Service connection HTTP status code
      onion_service_descriptor_latency_seconds:
            Register Onion Service latency in seconds to get the descriptor
      onion_service_descriptor_reachable:
            Register if the Onion Service descriptor is available: value is 1 for reachability and 0 otherwise
      onion_service_descriptor_fetch_attempts:
            Register the number of attempts required when trying to get an Onion Service descriptor in a probing round
      onion_service_introduction_points_number:
            Register the number of introduction points in the Onion Service descriptor
      onion_service_pattern_matched:
            Register whether a regular expression pattern is matched when connection to the Onion Service: value is 1 for matched pattern and 0 otherwise
      onion_service_valid_certificate:
            Register whether the Onion Service HTTPS certificate is valid: value is 1 for valid and 0 otherwise, but only for sites reachable using HTTPS
      onion_service_fetch_requests:
            Counts the total number of requests to access an Onion Service
      onion_service_fetch_error:
            Counts the total number of errors when fetching an Onion Service
      onion_service_descriptor_fetch_requests:
            Counts the total number of requests to fetch an Onion Service descriptor
      onion_service_descriptor_fetch_error:
            Counts the total number of errors when fetching an Onion Service descriptor
      onion_service_request_exception:
            Counts the total number of Onion Service general exception errors
      onion_service_connection_error:
            Counts the total number of Onion Service connection errors
      onion_service_http_error:
            Counts the total number of Onion Service HTTP errors
      onion_service_too_many_redirects:
            Counts the total number of Onion Service too many redirects errors
      onion_service_connection_timeout:
            Counts the total number of Onion Service connection timeouts
      onion_service_read_timeout:
            Counts the total number of Onion Service read timeouts
      onion_service_timeout:
            Counts the total number of Onion Service timeouts
      onion_service_certificate_error:
            Counts the total number of HTTPS certificate validation errors
      onion_service_descriptor:
            Onion Service descriptor information, including state and Hidden Service Directory (HSDir) used
      onion_service_probe_status:
            Register information about the last test made to a given Onion Service, including POSIX timestamp


# CONFIGURATION FILE FORMAT

This is a sample configuration file that can be adapted:

    ---
    # Sample config file for Onionprobe
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

    # Log level: debug, info, warning, error or critical
    log_level: 'info'

    # Whether to launch it's own Tor daemon (set to false to use the system-wide Tor service)
    launch_tor: true

    # Tor listening address if the system-wide service is used
    #tor_address: 'tor'
    tor_address: '127.0.0.1'

    # Tor SOCKS port
    #
    # Use a non-default Tor SOCKS port to avoid conflict with any existing
    # system-wide Tor process listening at TCP port 9050.
    #socks_port: 9050
    socks_port: 19050

    # Tor control port
    #
    # Use a non-default Tor control port to avoid conflict with any existing
    # system-wide Tor process listening at TCP port 9051.
    #control_port: 9051
    control_port: 19051

    # Tor control password
    #
    # Set to false to
    #
    # * Use a temporary auto-generated password when using the built-in Tor
    #   service.
    # * Show a password prompt when using the system-wide Tor service.
    #
    # Do not use the example value in production, as this password is available
    # publicly
    #control_password: false
    #control_password: 'hackedpasswdbSkUMOr2vIlL5u2YEMA1YpwKj08'

    # Whether to run continuously
    loop: true

    # Whether to enable Prometheus exporter functionality
    # Setting it to true automatically enables countinuos run (loop)
    prometheus_exporter: true

    # Prometheus exporter port
    prometheus_exporter_port: 9935

    # Max random time in seconds between probing each endpoint
    interval: 5

    # Max random time in seconds to wait between each round of tests (a round = a
    # pass among all defined endpoints)
    sleep: 5

    # Whether to shuffle list to scramble the ordering of the probe to avoid
    # the endpoint list to be guessed by a third party.
    #
    # This shuffles the list every time Onionprobe starts a new round of
    # tests.
    shuffle: true

    # Whether to randomize both the interval and the sleep time for privacy
    # concerns and to avoid systematic errors
    randomize: true

    # Run only a limited number of rounds (i.e., the number of times that
    # Onionprobe tests all the configured endpoints).
    # Requires the "loop" option to be enabled.
    # Set to 0 to disable this limit.
    rounds: 0

    # Max retries when fetching a descriptor
    # By default it is set to the number of HSDirs the client usually fetch minus one
    # See discussion at https://gitlab.torproject.org/tpo/network-health/analysis/-/issues/28
    descriptor_max_retries: 5

    # Timeout in seconds when retrieving an Onion Service descriptor
    descriptor_timeout: 30

    # Connection timeout for HTTP/HTTPS requests
    http_connect_timeout: 30

    # Max retries when doing a HTTP/HTTPS connection to an Onion Service
    http_connect_max_retries: 3

    # Read timeout for HTTP/HTTPS requests
    http_read_timeout: 30

    # Whether to get a new circuit for every stream
    new_circuit: false

    # Sets how many seconds until a stream is detached from a circuit and try a new
    # circuit (CircuitStreamTimeout Tor daemon config)
    circuit_stream_timeout: 60

    # The list of endpoints to be tested
    endpoints:
      # Using addresses from https://onion.torproject.org
      www.torproject.org:
        address: '2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion'
        protocol: 'http'
        port: 80
        paths:
          - path   : '/'
            # Specifying a per-path pattern makes Onionprobe look for it in the
            # request and hence operating like a basic check if the endpoint
            # is operational.
            #
            # Accepts patterns using Python's regex format
            pattern: 'Tor Project'
      2019.www.torproject.org:
        address: 'jqyzxhjk6psc6ul5jnfwloamhtyh7si74b4743k2qgpskwwxrzhsxmad.onion'
        protocol: 'http'
        port: 80
      api.donate.torproject.org:
        address: 'rbi3fpvpz4vlrx67scoqef2zxz7k4xyiludszg655favvkygjmhz6wyd.onion'
        protocol: 'http'
        port: 80
      archive.torproject.org:
        address: 'uy3qxvwzwoeztnellvvhxh7ju7kfvlsauka7avilcjg7domzxptbq7qd.onion'
        protocol: 'http'
        port: 80
      aus1.torproject.org:
        address: 'ot3ivcdxmalbsbponeeq5222hftpf3pqil24q3s5ejwo5t52l65qusid.onion'
        protocol: 'http'
        port: 80
      aus2.torproject.org:
        address: 'b5t7emfr2rn3ixr4lvizpi3stnni4j4p6goxho7lldf4qg4hz5hvpqid.onion'
        protocol: 'http'
        port: 80
      blog-staging.torproject.org:
        address: '6p4ky5a3wowiv7ww6vt7ikntcdjxkpk2lni5w4um3ddmqg3sx6nkreqd.onion'
        protocol: 'http'
        port: 80
      blog.torproject.org:
        address: 'pzhdfe7jraknpj2qgu5cz2u3i4deuyfwmonvzu5i3nyw4t4bmg7o5pad.onion'
        protocol: 'http'
        port: 80
      bridges.torproject.org:
        address: 'yq5jjvr7drkjrelzhut7kgclfuro65jjlivyzfmxiq2kyv5lickrl4qd.onion'
        protocol: 'http'
        port: 80
      cloud.torproject.org:
        address: 'ui3cpcohcoko6aydhuhlkwqqtvadhaflcc5zb7mwandqmcal7sbwzwqd.onion'
        protocol: 'http'
        port: 80
      collector.torproject.org:
        address: 'pgmrispjerzzf2tdzbfp624cg5vpbvdw2q5a3hvtsbsx25vnni767yad.onion'
        protocol: 'http'
        port: 80
      collector2.torproject.org:
        address: '3srlmjzbyyzz62jvdfqwn5ldqmh6mwnqxre2zamxveb75uz2qrqkrkyd.onion'
        protocol: 'http'
        port: 80
      community.torproject.org:
        address: 'xmrhfasfg5suueegrnc4gsgyi2tyclcy5oz7f5drnrodmdtob6t2ioyd.onion'
        protocol: 'http'
        port: 80
      consensus-health.torproject.org:
        address: 'tkskz5dkjel4xqyw5d5l3k52kgglotwn6vgb5wrl2oa5yi2szvywiyid.onion'
        protocol: 'http'
        port: 80
      crm.torproject.org:
        address: '6ojylpznauimd2fga3m7g24vd7ebkzlemxdprxckevqpzs347ugmynqd.onion'
        protocol: 'http'
        port: 80
      deb.torproject.org:
        address: 'apow7mjfryruh65chtdydfmqfpj5btws7nbocgtaovhvezgccyjazpqd.onion'
        protocol: 'http'
        port: 80
      dev.crm.torproject.org:
        address: 'eewp4iydzyu2a5d6bvqadadkozxdbhsdtmsoczu2joexfrjjsheaecad.onion'
        protocol: 'http'
        port: 80
      dist.torproject.org:
        address: 'scpalcwstkydpa3y7dbpkjs2dtr7zvtvdbyj3dqwkucfrwyixcl5ptqd.onion'
        protocol: 'http'
        port: 80
      donate-api.torproject.org:
        address: 'lkfkuhcx62yfvzuz5o3ju4divuf4bsh2bybwd3oierq47kyp2ig2gvid.onion'
        protocol: 'http'
        port: 80
      donate.torproject.org:
        address: 'yoaenchicimox2qdc47p36zm3cuclq7s7qxx6kvxqaxjodigfifljqqd.onion'
        protocol: 'http'
        port: 80
      exonerator.torproject.org:
        address: 'pm46i5h2lfewyx6l7pnicbxhts2sxzacvsbmqiemqaspredf2gm3dpad.onion'
        protocol: 'http'
        port: 80
      extra.torproject.org:
        address: 'kkr72iohlfix5ipjg776eyhplnl2oiv5tz4h2y2bkhjix3quafvjd5ad.onion'
        protocol: 'http'
        port: 80
      gettor.torproject.org:
        address: 'ueghr2hzndecdntou33mhymbbxj7pir74nwzhqr6drhxpbz3j272p4id.onion'
        protocol: 'http'
        port: 80
      git.torproject.org:
        address: 'xtlfhaspqtkeeqxk6umggfbr3gyfznvf4jhrge2fujz53433i2fcs3id.onion'
        protocol: 'http'
        port: 80
      gitlab.torproject.org:
        address: 'eweiibe6tdjsdprb4px6rqrzzcsi22m4koia44kc5pcjr7nec2rlxyad.onion'
        protocol: 'http'
        port: 80
      gitweb.torproject.org:
        address: 'gzgme7ov25seqjbphab4fkcph3jkobfwwpivt5kzbv3kqx2y2qttl4yd.onion'
        protocol: 'http'
        port: 80
      grafana1.torproject.org:
        address: '7zjnw5lx2x27rwiocxkqdquo7fawj46mf2wiu2l7e6z6ng6nivmdxnad.onion'
        protocol: 'http'
        port: 80
      grafana2.torproject.org:
        address: 'f3vd6fyiccuppybkxiblgigej3pfvvqzjnhd3wyv7h4ee5asawf2fhqd.onion'
        protocol: 'http'
        port: 80
      ircbouncer.torproject.org:
        address: 'moz5kotsnjony4oxccxfo4lwk3pvoxmdoljibhgoonzgzjs5oemtjmqd.onion'
        protocol: 'http'
        port: 80
      metabase.metrics.torproject.org:
        address: 'gr5pseamigereei4c6654hafzhid5z2c3oqzn6cfnx7yfyelt47znhad.onion'
        protocol: 'http'
        port: 80
      metrics.torproject.org:
        address: 'hctxrvjzfpvmzh2jllqhgvvkoepxb4kfzdjm6h7egcwlumggtktiftid.onion'
        protocol: 'http'
        port: 80
      moat.torproject.org:
        address: 'z7m7ogzdhu43nosvjtsuplfmuqa3ge5obahixydhmzdox6owwxfoxzid.onion'
        protocol: 'http'
        port: 80
      nagios.torproject.org:
        address: 'w6vizvw4ckesva5fvlkrepynemxdq6pgo5sh4r76ec6msq5notkhqryd.onion'
        protocol: 'http'
        port: 80
      newsletter.torproject.org:
        address: 'a4ygisnerpgtc5ayerl22pll6cls3oyj54qgpm7qrmb66xrxts6y3lyd.onion'
        protocol: 'http'
        port: 80
      nightlies.tbb.torproject.org:
        address: 'umj4zbqdfcyevlkgqgpq6foxk3z75zzxsbgt5jqmfxofrbrjh3crbnad.onion'
        protocol: 'http'
        port: 80
      nyx.torproject.org:
        address: '3ewfgrt4gzfccp6bnquhqb266r3zepiqpnsk3falwygkegtluwuyevid.onion'
        protocol: 'http'
        port: 80
      onion.torproject.org:
        address: 'xao2lxsmia2edq2n5zxg6uahx6xox2t7bfjw6b5vdzsxi7ezmqob6qid.onion'
        protocol: 'http'
        port: 80
      onionoo.torproject.org:
        address: 'dud2sxm6feahhuwj4y4lzktduy7v3qpaqsfkggtj2ojmzathttkegoid.onion'
        protocol: 'http'
        port: 80
      openpgpkey.torproject.org:
        address: '2yldcptk56shc7lwieozoglw3t5ghty7m6mf2faysvfnzccqavbu2mad.onion'
        protocol: 'http'
        port: 80
      people.torproject.org:
        address: '5ecey6oe4rocdsfoigr4idu42cecm2j7zfogc3xc7kfn4uriehwrs6qd.onion'
        protocol: 'http'
        port: 80
      prometheus1.torproject.org:
        address: 'ydok5jiruh3ak6hcfdlm2g7iuraaxcomeckj2nucjsxif6qmrrda2byd.onion'
        protocol: 'http'
        port: 80
      prometheus2.torproject.org:
        address: 'vyo6yrqhl3by7d6n5t6hjkflaqbarjpqjnvapr5u5rafk4imnfrmcjyd.onion'
        protocol: 'http'
        port: 80
      rbm.torproject.org:
        address: 'nkuz2tpok7ctwd5ueer5bytj3bm42vp7lgjcsnznal3stotg6vyaakyd.onion'
        protocol: 'http'
        port: 80
      research.torproject.org:
        address: 'xhqthou6scpfnwjyzc3ekdgcbvj76ccgyjyxp6cgypxjlcuhnxiktnqd.onion'
        protocol: 'http'
        port: 80
      review.torproject.net:
        address: 'zhkhhhnppc5k6xju7n25rjba3wuip73jnodicxl65qdpchrwvvsilcyd.onion'
        protocol: 'http'
        port: 80
      rpm.torproject.org:
        address: '4ayyzfoh5qdrokqaejis3rdredhvf22n3migyxfudpkpunngfc7g4lqd.onion'
        protocol: 'http'
        port: 80
      snowflake.torproject.org:
        address: 'oljlphash3bpqtrvqpr5gwzrhroziw4mddidi5d2qa4qjejcbrmoypqd.onion'
        protocol: 'http'
        port: 80
      spec.torproject.org:
        address: 'i3xi5qxvbrngh3g6o7czwjfxwjzigook7zxzjmgwg5b7xnjcn5hzciad.onion'
        protocol: 'http'
        port: 80
      staging-api.donate.torproject.org:
        address: 'vorwws6g6mx23djlznmlqva4t5olulpnet6fxyiyytcu5dorp3fstdqd.onion'
        protocol: 'http'
        port: 80
      staging.crm.torproject.org:
        address: 'pt34uujusar4arrvsqljndqlt7tck2d5cosaav5xni4nh7bmvshyp2yd.onion'
        protocol: 'http'
        port: 80
      staging.donate-api.torproject.org:
        address: '7niqsyixinnhxvh33zh5dqnplxnc2yd6ktvats3zmtbbpzcphpbsa6qd.onion'
        protocol: 'http'
        port: 80
      status.torproject.org:
        address: 'eixoaclv7qvnmu5rolbdwba65xpdiditdoyp6edsre3fitad777jr3ad.onion'
        protocol: 'http'
        port: 80
      stem.torproject.org:
        address: 'mf34jlghauz5pxjcmdymdqbe5pva4v24logeys446tdrgd5lpsrocmqd.onion'
        protocol: 'http'
        port: 80
      styleguide.torproject.org:
        address: '7khzpw47s35pwo3lvtctwf2szvnq3kgglvzc22elx7of2awdzpovqmqd.onion'
        protocol: 'http'
        port: 80
      submission.torproject.org:
        address: 'givpjczyrb5jjseful3o5tn3tg7tidbu4gydl4sa5ekpcipivqaqnpad.onion'
        protocol: 'http'
        port: 80
      support-staging.torproject.org:
        address: 'mct6jqxfejsvkr3ynq7puibv6223ycv6j5cu7qzu6gscxy7qdtys22id.onion'
        protocol: 'http'
        port: 80
      support.torproject.org:
        address: 'rzuwtpc4wb3xdzrj3yeajsvm3fkq4vbeubm2tdxaqruzzzgs5dwemlad.onion'
        protocol: 'http'
        port: 80
      survey.torproject.org:
        address: 'eh5esdnd6fkbkapfc6nuyvkjgbtnzq2is72lmpwbdbxepd2z7zbgzsqd.onion'
        protocol: 'http'
        port: 80
      svn-archive.torproject.org:
        address: 'b63iq6es4biaawfilwftlfkw6a6putogxh4iakei2ioppb7dsfucekyd.onion'
        protocol: 'http'
        port: 80
      tb-manual.torproject.org:
        address: 'dsbqrprgkqqifztta6h3w7i2htjhnq7d3qkh3c7gvc35e66rrcv66did.onion'
        protocol: 'http'
        port: 80
      test-api.donate.torproject.org:
        address: 'wiofesr5qt2k7qrlljpk53isgedxi6ddw6z3o7iay2l7ne3ziyagxaid.onion'
        protocol: 'http'
        port: 80
      test-data.tbb.torproject.org:
        address: 'umbk3kbgov4ekg264yulvbrpykfye7ohguqbds53qn547mdpt6o4qkad.onion'
        protocol: 'http'
        port: 80
      test.crm.torproject.org:
        address: 'a4d52y2erv4eijii66cpnyqn7rsnnq3gmtrsdxzt2laoutvu4gz7fwid.onion'
        protocol: 'http'
        port: 80
      test.donate-api.torproject.org:
        address: 'i4zhrn4md3ucd5dfgeo5lnqd3jy2z2kzp3lt4tdisvivzoqqtlrymkid.onion'
        protocol: 'http'
        port: 80
      www-staging.torproject.org:
        address: 'wosihptqvevjrjxqipafogjmwn22kqktgsibfmmnfxl7wb7sqq5xfrid.onion'
        protocol: 'http'
        port: 80
      www.onion-router.net:
        address: 'tttyx2vwp7ihml3vkhywwcizv6nbwrikpgeciy3qrow7l7muak2pnhad.onion'
        protocol: 'http'
        port: 80


# FILES

/etc/onionprobe
:  System-wide Onionprobe configuration files.

# LIMITATIONS

Onionprobe currently has the following limitations:

1. Only works for Onion Services websites, i.e, those served via
   either HTTP or HTTPS.

2. Currently Onionprobe probes runs in a single thread.

3. For other limitations, check the list of issues  available at the Onionprobe
   source code repository.

# SEE ALSO

The *README* file distributed with Onionprobe contains the full documentation.

The Onionprobe source code and all documentation may be downloaded from
<https://gitlab.torproject.org/onion-services/onionprobe>.
