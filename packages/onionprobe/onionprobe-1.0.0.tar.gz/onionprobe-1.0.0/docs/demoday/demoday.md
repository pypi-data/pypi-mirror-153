---
title: Onionprobe Demo Day
date: 2022-03-23
author: Silvio Rhatto
---

This file was superseded by [demoday.tex](demoday.tex).

# About

* What: Monitors Onion Services from "the outside".
* Goal: Be a generic monitoring tool for Onion Services.
* Where: https://gitlab.torproject.org/tpo/onion-services/onionprobe/
* Status: WARNING: alpha stage! It's only about a week old!

# Current features

* Check if can get .onion descriptor.
* Check if can make a HTTP request to the service.
* Can run continuously.
* Cache is cleared before each probe!
* Configurable using `YAML`.
* Built-in Prometheus exporter.

# Current use cases

* Planned to monitor existing deployments.
* Sample configuration has all https://onion.torproject.org services and can
  be an alternative monitoring instance.

# Demo

* Using docker-compose and Prometheus exporting/aggregation.
* Using the command line.

# Planned improvements

* Better metrics.
* Enhanced UX (command line etc).
* See the task list :)

# Existing alternatives

* https://onionscan.org
* https://github.com/systemli/prometheus-onion-service-exporter/

# Questions

* Python/Stem:
  * How to get the descriptor from different `HSDirs`? Does this already happens
    automatically as each probing uses a fresh cache?

  * How to choose an specific introduction point when connecting to an .onion?

* What functionality you would like to have?

* Where should the repository live? https://gitlab.torproject.org/tpo/network-health ?
