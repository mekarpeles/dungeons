import random
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from utils.util import punctuate
from utils.util import sentence_type
from configs.formatting import BLUE_TXT
from configs.formatting import YELLOW_TXT
from game import world
import game.actions   
from game.character import Character

class Repl(LineReceiver):

    def __init__(self, characters):
        self.world = world.Map(1)
        self.characters = characters
        self.character = None

    def connectionMade(self):
        self.send("Please choose a character name:")

    def connectionLost(self, reason):
        if self.character and getattr(self.character, "name", None):
            if self.characters.has_key(self.character.name):
                del self.characters[self.character.name]
        
    def lineReceived(self, line):
        return self.read(line)

    def read(self, line):
        # If no name is set
        if not self.character:
            # if the line entered isn't a taken name
            if not self.characters.has_key(line):
                self.character = Character(line)
                self.characters[line] = self
                self.send("You are now known as %s" % line)
                room = self.character.get_room(self.world)
                self.sendLine("\n" + BLUE_TXT(room.name))
                self.sendLine(room.description)
                self.sendLine(YELLOW_TXT("occupants:") + " %s" % ", ".join(self.characters))
                self.sendLine(YELLOW_TXT("exits:") + " %s" % self.character.get_room(self.world).get_exits())
                return
            else:
                return self.send("Name taken, please choose another name. \
The following names are also taken: \n%s" % ", ".join(self.characters))
        self.evaluate(line)

    def evaluate(self, msg):
        op, rest = None, None
        tokens = msg.split(" ")
        num_tokens = len(tokens)
        op = msg.split(" ")[0]
        
        if num_tokens > 1:
            op, rest = msg.split(" ", 1)            

        if op in game.actions.COMMANDS:
            game.actions.COMMANDS[op](self, rest)

        if op in game.actions.SENSES_METHOD.keys():
            game.actions.SENSES_LAMBDA(self, op, rest)
            

    def send(self, msg, protocol=None):        
        protocol = protocol if protocol else self
        protocol.sendLine("%s" % msg)

    def broadcast(self, msg, protocol=None, send2self=True):
        for name, protocol in self.characters.iteritems():
            if not send2self and name == self.character.name:
                continue
            self.send(msg, protocol=protocol)

class ReplFactory(Factory):
    
    def __init__(self):
        self.characters = {}

    def buildProtocol(self, addr):
        return Repl(self.characters)

