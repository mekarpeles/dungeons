import datetime
import random
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from utils.util import punctuate
from utils.util import sentence_type
   
class Repl(LineReceiver):

    OPERANDS = {"quit": lambda self, **kwargs: self.transport.loseConnection(),
                "say": lambda self, msg: self.say(msg),
                "emote": lambda self, emotion: self.emote(emotion),
                }

    SENSES = {"look": 0,
              "smell": 0,
              "listen": 0,
              "taste": 0,
              "feel": 0,
              "touch": 0,
              }

    ATTACKS = {"kick": 0,
               "parry": 0,
               "punch": 0,
               "poke": 0,
               "slap": 0,
               "headbutt": 0,
               "trip": 0,
               "bite": 0,
               "pinch": 0,
               "jimmytap": 0,
               }

    EMOTES = {"laugh": "%s laughs %s",
              "smile": "%s smiles %s",
              "glare": "%s glares %s",
              }

    def __init__(self, characters):
        self.characters = characters
        self.character = None

    def connectionMade(self):
        self.send("Please choose a character name:")

    def connectionLost(self, reason):
        if self.characters.has_key(self.character):
            del self.characters[self.character]
        
    def lineReceived(self, line):
        # If no name is set
        if not self.character:
            # if the line entered isn't a taken name
            if not self.characters.has_key(line):
                self.character = line
                self.characters[line] = self
                return self.send("You are now known as %s" % line)
            else:
                return self.send("Name taken, please choose another name. The following names are also taken: \n%s" % ", ".join(self.characters))
        self.preprocess(line)

    def preprocess(self, msg):
        op, rest = None, None
        try:
            op, rest = msg.split(" ", 1)            
        except:
            op = msg.split(" ")[0]
        if op in self.OPERANDS:
            self.OPERANDS[op](self, rest)
        else:
            pass

    def send(self, msg, protocol=None):
        timestamp = datetime.datetime.now().ctime()
        protocol = protocol if protocol else self
        protocol.sendLine("[%s] %s" % (timestamp, msg))

    def cmd(self, command):
        pass

    def say(self, msg):        
        for name, protocol in self.characters.iteritems():            
            print sentence_type(msg)
            self.send('%s %s, "%s"' % (self.character, sentence_type(msg), punctuate(msg)),
                      protocol=protocol)
    
    def emote(self, emotion):        
        self.send("%s %s" % (self.character,
                             punctuate(emotion)), protocol=self)

    def login(self):
        return "Hello!"

class ReplFactory(Factory):
    
    def __init__(self):
        self.characters = {}

    def buildProtocol(self, addr):
        return Repl(self.characters)

