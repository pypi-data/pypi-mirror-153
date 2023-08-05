# -*- coding: utf-8 -*-
# vim: set ts=4

# Copyright 2017 Rémi Duraffort
# This file is part of lavacli.
#
# lavacli is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lavacli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with lavacli.  If not, see <http://www.gnu.org/licenses/>

import re
import xmlrpc.client

from ruamel.yaml import YAML


VERSION_LATEST = (3000, 1)

# yaml objects

flow_yaml = YAML(typ="safe")
flow_yaml.default_flow_style = False
log_yaml = YAML(typ="safe")
log_yaml.default_flow_style = True
log_yaml.default_style = '"'
log_yaml.width = 10 ** 6
safe_yaml = YAML(typ="safe")


def parse_version(version):
    pattern = re.compile(r"(?P<major>20\d{2})\.(?P<minor>\d{1,2})")
    if not isinstance(version, str):
        version = str(version)
    m = pattern.match(version)
    if m is None:
        return VERSION_LATEST
    res = m.groupdict()
    return (int(res["major"]), int(res["minor"]))


def exc2str(exc):
    if isinstance(exc, xmlrpc.client.ProtocolError):
        return exc.errmsg
    return str(exc)
