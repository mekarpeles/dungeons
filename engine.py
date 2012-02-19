import io
import ConfigParser

from twisted.internet import reactor
from server.server import ReplFactory

config = ConfigParser.ConfigParser()
config.read('network.cfg')
PORT = int(config.get("telnet", "port"))

def run():
    reactor.listenTCP(PORT, ReplFactory())
    reactor.run()

run()
