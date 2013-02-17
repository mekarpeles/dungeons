# -*- coding: utf-8 -*-
"""
    engine.py
    ~~~~~~~~~

    This module is run from the command line and triggers the start of
    a new telnet sever.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from reloader import PeriodicReloader
from twisted.internet import reactor
from server.server import Server as GameServer
from configs.config import DEBUG_MODE
from configs.config import PORT
from configs.config import HOST
import os, json

def run(world=None):
    """Entry function for Dungeon
    $ python engine.py <port>
    """
    reactor.listenTCP(PORT, GameServer(world))
    reactor.run()

if __name__ == "__main__":
    m = os.getcwd() + "/static/maps/galaxia"
    world = json.loads(open(m, 'r').read())

    if DEBUG_MODE:
        PeriodicReloader()
    run(world)
