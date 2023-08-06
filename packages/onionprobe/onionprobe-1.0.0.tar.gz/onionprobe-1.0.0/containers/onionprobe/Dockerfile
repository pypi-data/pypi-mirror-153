#
# Dockerfile for Onionprobe.
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
#

FROM debian:stable
MAINTAINER Silvio Rhatto <rhatto@torproject.org>

ENV APP="onionprobe"
ENV APP_BASE="/srv/"
ENV SHELL="/bin/bash"
ENV ONIONPROBE_CONFIG="/srv/onionprobe/configs/tor.yaml"

# Set the PYTHONPATH in the container
ENV PYTHONPATH="/usr/lib/python3/dist-packages:/srv/onionprobe/packages"

RUN apt-get update && \
    apt-get install -y \
    python3-prometheus-client python3-stem python3-cryptography \
    python3-bs4 python3-yaml python3-pytest python3-requests \
    python3-socks tor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_BASE}/${APP}

COPY . ${APP_BASE}/${APP}

USER debian-tor

ENTRYPOINT exec /srv/onionprobe/onionprobe -c ${ONIONPROBE_CONFIG}
