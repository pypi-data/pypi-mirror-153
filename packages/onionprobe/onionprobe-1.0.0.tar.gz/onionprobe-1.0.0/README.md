# Onionprobe

![](assets/logo.jpg "Onionprobe")

Onionprobe is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/) sites.

It can run a single time or continuously to probe a set of onion services
endpoints and paths, optionally exporting to [Prometheus](https://prometheus.io).

## Requirements

Onionprobe requires the following software:

* [Python 3](https://www.python.org)
* [Stem Tor Control library](https://stem.torproject.org)
* [Prometheus Python client](https://github.com/prometheus/client_python)
* [PyYAML](https://pyyaml.org)
* [Requests](https://docs.python-requests.org)
* [PySocks](https://github.com/Anorov/PySocks)
* [Tor daemon](https://gitlab.torproject.org/tpo/core/tor)

On [Debian](https://debian.org), they can be installed using

    sudo apt install python3 python3-prometheus-client \
                     python3-stem python3-cryptography \
                     python3-yaml python3-requests     \
                     python3-socks tor

## Installation

Onionprobe is [available on PyPI](https://pypi.org/project/onionprobe):

    pip install onionprobe

It's also possible to run it directly from the Git repository:

    git clone https://gitlab.torproject.org/tpo/onion-services/onionprobe
    cd onionprobe

## Usage

Simply ask Onionprobe to try an Onion Service site:

    onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion

It's possible to supply multiple addresses:

    onionprobe -e <onion-address1> <onionaddress2> ...

Onionprobe also accepts a configuration file with a list of .onion endpoints
and options. A [detailed sample config](configs/tor.yaml) is provided and can
be invoked with:

    onionprobe -c configs/tor.yaml

By default, Onionprobe starts it's own Tor daemon instance, so the `tor` binary
must be available in the system.

See the [manual
page](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/blob/main/docs/man/onionprobe.1.md)
for the complete list of options and available metrics.

## Standalone monitoring node

Onionprobe comes with full monitoring environment based on [Docker
Compose](https://docs.docker.com/compose/) with:

* An Onionprobe instance continuously monitoring endpoints.
* Metrics are exported to a [Prometheus](https://prometheus.io) instance.
* Alerts are managed using [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/).
* A [Grafana](https://grafana.com) Dashboard is available for browsing the
  metrics and using a PostgreSQL service container as the database backend.

### Configuring the monitoring node

By default, the monitoring node periodically compiles the Onionprobe configuration
from the official Tor Project Onion Services into `contrib/tpo.yaml`, by using
the [tpo.py script](packages/tpo.py).

This and other configurations can be changed by creating an `.env` file in the
toplevel project folder.

Check the [sample .env](configs/env.sample) for an example.

### Starting the monitoring node

The monitoring node may be started using `docker-compose`:

    docker-compose up -d   # Remove "-d" to not fork into the background
    docker-compose logs -f # View container logs

The monitoring node sets up [storage
volumes](https://docs.docker.com/storage/volumes/), which means that the
monitoring dataset collected is persistent across service container reboots.

### Accessing the monitoring dashboards and the exporter

Once the dashboards are started, point your browser to the following addresses
if you're running locally:

* The built-in Prometheus   dashboard: http://localhost:9090
* The built-in Alertmanager dashboard: http://localhost:9093
* The built-in Grafana      dashboard: http://localhost:3030
* The built-in Onionprobe   Prometheus exporter: http://localhost:9935

These services are also automatically exported as Onion Services,
which addresses can be discovered by running the following commands
when the services are running:

    docker exec -ti onionprobe_tor_1 cat /var/lib/tor/prometheus/hostname
    docker exec -ti onionprobe_tor_1 cat /var/lib/tor/alertmanager/hostname
    docker exec -ti onionprobe_tor_1 cat /var/lib/tor/grafana/hostname
    docker exec -ti onionprobe_tor_1 cat /var/lib/tor/onionprobe/hostname

You can also get this info from the host by browsing directly the
`onionprobe_tor` volume.

It's also possible to replace the automatically generated Onion Service
addresses by using keys with vanity addresses using a tool like
[Onionmine](https://gitlab.torproject.org/tpo/onion-services/onionmine).

### Protecting the monitoring dashboards and the exporter

By default, all dashboards and the are accessible without credentials.

You can protect them by [setting up Client
Authorization](https://community.torproject.org/onion-services/advanced/client-auth/):

0. Enter in the `tor` service container: `docker exec -ti onionprobe_tor_1 /bin/bash`.
1. Setup your client credentials [according to the docs](https://community.torproject.org/onion-services/advanced/client-auth/).
   The `tor` service container already comes with all programs to generate it.
   Onionprobe ships with a handy
   [generate-auth-keys-for-all-onion-services](scripts/generate-auth-keys-for-all-onion-services)
   available at the `tor` service container and which can be invoked with
  `docker exec -ti onionprobe_tor_1 /usr/local/bin/generate-auth-keys-for-all-onion-services`
  (it also accepts an optional auth name parameter allowing multiple credentials to be deployed).
2. Place the `.auth` files at the Onion Services `authorized_clients` folder if you did not
   created them with the `generate-auth-keys-for-all-onion-services` script:
    * Prometheus: `/var/lib/tor/prometheus/authorized_clients`.
    * Alertmanager: `/var/lib/tor/alertmanager/authorized_clients`.
    * Grafana: `/var/lib/tor/grafana/authorized_clients`.
    * Onionprobe: `/var/lib/tor/onionprobe/authorized_clients`.
3. Restart the `tor` service container from the host to ensure that this new
   configuration is applied:

        docker compose stop tor
        docker compose up -d

Note that the Grafana dashboard also comes with it's own user management system,
whose default user and password is `admin`. You might change this default user
and not setup the Client Authorization for Grafana, or maybe use both depending
or your security needs.

### Managing the monitoring node with systemd

The monitoring node can be managed with systemd.
A [sample service file](configs/systemd/onionprobe-monitor.service) is provided
and can be adapted..

### Using the monitoring node

Once your monitoring node is up and running, you can create your dashboards an
visualizations as usual, getting the data compiled by Onionprobe using
Prometheus as the data source.

Grafana already comes with a basic default dashboard as it's homepage:

![](assets/dashboard.png "Grafana Onion Services Dashboard")

## Compiled configurations

Besides the [sample config](configs/tor.yaml) containing sites listed at
https://onion.torproject.org, Onionprobe comes also with other example configs:

0. [Official Tor Project Onion Service Sites](https://onion.torproject.org/onionbalancev3-services.yaml), generated by the [tpo.py](packages/tpo.py) script.
1. [Real-World Onion Sites](https://github.com/alecmuffett/real-world-onion-sites) .onions at
   [real-world-onion-sites.yaml](configs/real-world-onion-sites.yaml), generated by the
   [real-world-onion-sites.py](packages/real-world-onion-sites.py) script.
2. [The SecureDrop API](https://securedrop.org/api/v1/directory/) .onions at
   [securedrop.yaml](configs/securedrop.yaml), generated by the
   [securedrop.py](packages/securedrop.py) script.

You can build your own configuration compiler by using the
[OnionprobeConfigCompiler](packages/onionprobe/config.py) class.

## Folder structure and files

Relevant folders and files in this repository:

* `assets`: logos and other stuff.
* `configs`: miscelaneous configurations.
* `contrib`: folder reserved for storing contributed code and configuration.
* `containers`: container configurations.
* `debian`: debian packaging.
* `docs`: documentation.
* `packages`: python packages codebase.
* `scripts`: provisioning and other configuration scripts.
* `tests`: test procedures.
* `vendors`: other third-party libraries and helpers.
* `kvmxfile`: please ignore this if you're not a [KVMX](https://kvmx.fluxo.info) user.
* `docker-compose.yml`: service container configuration.

## Tasks

Check the [issue tracker](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues).

## Acknowledgements

Thanks to:

* @irl for the idea/specs/tasks.
* @hiro for suggestions.
* @arma and @juga for references.
* @anarcat and @georg for Python and Debian packaging guidance and review.

## Alternatives

* [OnionScan](https://onionscan.org/)
* [Webmon](https://webmon.dev.akito.ooo/) has support for Onion Services
  monitoring if used along with [Orbot](https://guardianproject.info/apps/org.torproject.android/).
* [BrassHornCommunications/OnionWatch: A GoLang daemon for notifying Tor Relay and Hidden Service admins of status changes](https://github.com/BrassHornCommunications/OnionWatch)
* [systemli/prometheus-onion-service-exporter: Prometheus Exporter for Tor Onion Services](https://github.com/systemli/prometheus-onion-service-exporter)
* [prometheus/blackbox_exporter: Blackbox prober
  exporter](https://github.com/prometheus/blackbox_exporter), which could be
  configured using `proxy_url` pointing to a [Privoxy](http://www.privoxy.org/)
  instance relaying traffic to `tor` daemon. See [this
  issue](https://github.com/prometheus/blackbox_exporter/issues/264) for details.

## Known issues

From Stem:

* [Python 3.9 warning · Issue #105 · torproject/stem](https://github.com/torproject/stem/issues/105)
* [noisy log: stem: INFO: Error while receiving a control message (SocketClosed): received exception "peek of closed file" · Issue #112 · torproject/stem · GitHub](https://github.com/torproject/stem/issues/112)

## References

Related software and libraries with useful routines:

* [onbasca](https://gitlab.torproject.org/tpo/network-health/onbasca)
* [sbws](https://gitlab.torproject.org/tpo/network-health/sbws)
* [Stem](https://stem.torproject.org/)
* [txtorcon](https://txtorcon.readthedocs.io/en/latest/)
* [Onionbalance](https://onionbalance.readthedocs.io/en/latest/)
* [hs-health](https://gitlab.com/hs-health/hs-health)

Relevant issues:

* [Write a hidden service hsdir health measurer](https://gitlab.torproject.org/tpo/network-health/metrics/analysis/-/issues/13209)
* [Write tool for onion service health assessment](https://gitlab.torproject.org/tpo/core/tor/-/issues/28841)

Research questions:

* [When an onion service lookup has failed at the first k HSDirs we tried, what are the chances it will still succeed?](https://gitlab.torproject.org/tpo/network-health/analysis/-/issues/28)
* [What's the average number of hsdir fetches before we get the hsdesc?](https://gitlab.torproject.org/tpo/core/tor/-/issues/13208)
