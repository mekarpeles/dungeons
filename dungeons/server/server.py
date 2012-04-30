import random
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from utils.util import punctuate
from utils.util import sentence_type
from configs.config import SCOPES

import game.world
from game.character import Character
from game.evaluator import Eval

class Repl(LineReceiver):
    """
    Read Evaluate Print Loop
    """
    def __init__(self, players, world):
        self.evaluator = Eval()
        self.world = world
        self.players = players
        self.character = None

    def connectionMade(self):
        self.send("Please choose a character name:")

    def connectionLost(self, reason):
        if self.character and getattr(self.character, "name", None):
            if self.players.has_key(self.character.name):
                del self.players[self.character.name]
        
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
            if name == self.character.name and not send2self:
                continue
            if scope(self, protocol):
                self.send(msg, protocol=protocol)

class ReplFactory(Factory):
    """
    This factory makes Read Evaluate Print Loops
    """
    def __init__(self):
        self.players = {}
        self.world = game.world.Map(20) # 20 rooms

    def buildProtocol(self, addr):
        return Repl(self.players, self.world)
