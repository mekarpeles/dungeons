from reloader import PeriodicReloader

from twisted.internet import reactor
from server.server import ReplFactory

from configs.config import PORT
from configs.config import HOST
from configs.config import DEBUG_MODE

def run():
    reactor.listenTCP(PORT, ReplFactory())
    reactor.run()

if __name__ == "__main__":
    if DEBUG_MODE:
        PeriodicReloader()
    run()
