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
from server.server import ReplFactory
from configs.config import DEBUG_MODE
from configs.config import PORT
from configs.config import HOST

def run():
    """Entry function for Dungeons.
    $ python engine.py <port>
    """
    reactor.listenTCP(PORT, ReplFactory())
    reactor.run()

if __name__ == "__main__":
    if DEBUG_MODE:
        PeriodicReloader()
    run()
