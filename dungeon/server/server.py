import random
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from utils.util import punctuate
from utils.util import sentence_type
from configs.config import SCOPES

import game.world
from game.character import Character
from game.evaluator import Eval

class Client(LineReceiver):

    def __init__(self, players, world):
        self.evaluator = Eval()
        self.world = world
        self.players = players
        self.character = None

    def purge_connection(self):
        if getattr(self, 'character', None):
            del self.players[self.character.name.lower()]
            self.character = None

    def connectionMade(self):
        self.purge_connection()
        return self.evaluator.initialize(self)

    def connectionLost(self, reason):
        """
        XXX This really needs to do magic with the Server
        use self.server.remove_client()
        """
        self.purge_connection()
        self.transport.loseConnection()
        
    def lineReceived(self, line):
        if line:
            #try:
            return self.evaluator.evaluate(self, line)
            #except:
            #    self.transport.loseConnection()
            
    def send(self, msg, protocol=None):        
        protocol = protocol if protocol else self
        protocol.sendLine("%s" % msg)

    def broadcast(self, msg, scope=SCOPES["room"], protocol=None, send2self=True):
        for name, protocol in self.players.iteritems():
            if not send2self and name == self.character.name.lower():
                continue
            if scope(self, protocol):
                self.send(msg, protocol=protocol)

class Server(Factory):
    """This factory makes Read Evaluate Print Loops"""
    def __init__(self, ctx=None):
        self.clients = {}
        self.ctx = game.world.Map(loadfile=ctx) \
            if ctx else game.world.Map(20)

    def buildProtocol(self, addr):
        return Client(self.clients, self.ctx)

