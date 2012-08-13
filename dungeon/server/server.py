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

    def connectionMade(self):             
        return self.evaluator.initialize(self)

    def connectionLost(self, reason):
        """
        """
        if self.character and getattr(self.character, "name", None):
            if self.players.has_key(self.character.name):
                del self.players[self.character.name]
            del self.character 
        
    def lineReceived(self, line):
        return self.read(line)

    def read(self, line):
        if line:
            return self.evaluator.evaluate(self, line)
            
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
