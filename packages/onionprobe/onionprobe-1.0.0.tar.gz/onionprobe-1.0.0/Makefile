#
# Onionprobe Makefile.
#
# This Makefile is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or any later version.
#
# This Makefile is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA 02111-1307, USA
#

.PHONY: configs docs

#
# Containers
#

run-containers:
	@docker-compose up -d

watch-containers:
	@watch docker-compose ps

log-containers:
	@docker-compose logs -f

stop-containers:
	@docker-compose down

#
# Configs
#

configs:
	@./packages/real-world-onion-sites.py
	@./packages/securedrop.py

#
# Documentation
#

docs:
	@./packages/manpage.py

#
# Packaging
#

clean:
	@find -name __pycache__ -exec rm -rf {} \; || true

build-python-package: clean
	@python3 -m build

upload-python-test-package:
	@twine upload --skip-existing --repository testpypi dist/*

upload-python-package:
	@twine upload --skip-existing dist/*

update_sbuild:
	@sudo sbuild-update -udcar u

#build-debian-test-package:
#	@dpkg-buildpackage -rfakeroot --no-sign

sbuild: update_sbuild
	@#sbuild -c stable-amd64-sbuild
	@sbuild  -c unstable-amd64-sbuild

#
# Release
#

release: clean configs docs
