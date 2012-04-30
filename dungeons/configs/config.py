# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    This module is the middle man for handling/consolidating
    configurations for the Dungeons project.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import io
import os
import ConfigParser

config = ConfigParser.ConfigParser()

# network.cfg is an unversioned file : and does not exist by
# default. A fallback file with default values is provided as
# network_default.cfg
if os.path.isfile('configs/network.cfg'):
    config.read('configs/network.cfg')
else:
    config.read('configs/network_default.cfg')

PORT = int(config.get("telnet", "port"))
HOST = config.get("telnet", "host")
DEBUG_MODE = bool(config.get("server", "debug"))

SCOPES = {"room": lambda controller, protocol: controller.character.position == protocol.character.position,
          "world": lambda controller, protocol: True}
