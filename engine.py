from twisted.internet import reactor
from server.server import ReplFactory

def run():
    reactor.listenTCP(1337, ReplFactory())
    reactor.run()

run()
