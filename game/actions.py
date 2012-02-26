import datetime
from game.character import Character
from utils.util import punctuate
from utils.util import sentence_type

from configs.formatting import BLUE_TXT
from configs.formatting import YELLOW_TXT
from configs.formatting import PURPLE_TXT

COMMANDS = {"quit": lambda controller, **kwargs: controller.transport.loseConnection(),
            "say": lambda controller, msg: say(controller, msg),
            "emote": lambda controller, emotion: emote(controller, emotion),
            "l": lambda controller, something, **kwargs: show_room(controller),
           }


SENSES_LAMBDA = lambda controller, op, args: sense(controller, op, args)
SENSES_METHOD = {"look": {"property": "description",
                          "broadcast": lambda character, obj, **kwargs: "%s's gaze wanders as %s looks at the %s." % (character.name,
                                                                                                                      character.he_or_she(),
                                                                                                                      obj.object_type),
                          "callback": lambda character, obj, **kwargs: obj.description,
                          },
                 "smell": {"property": "smell",
                           "broadcast": lambda character, obj, **kwargs: "%s sniffs the air around the %s." % (character.name,
                                                                                                               obj.object_type),
                           "callback": lambda character, obj, **kwargs: "You smell %s." % obj.smell,
                           },
                 "listen": {"property": "sound",
                            "broadcast": lambda character, obj, **kwargs: "%s listens carefully for a moment." % (character.name),
                            "callback": lambda character, obj, **kwargs: "You hear the %s" % obj.sound,
                            },
                 "taste": {"property": "taste",
                           "broadcast": lambda character, obj, **kwargs: "%s tastes the %s." % (character.name, obj.object_type),
                           "callback": lambda character, obj, **kwargs: "You taste %s." % obj.taste,
                           },
                 "feel": {"property": "texture",
                          "broadcast": lambda character, obj, **kwargs: "%s feels around the %s." % (character.name,
                                                                                                    obj.object_type),
                          "callback": lambda character, obj, **kwargs: "You feel %s" % obj.texture,
                          },
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

def login(controller, name):
    # if the (line) character name entered isn't a taken name
    if not controller.characters.has_key(name):
        controller.character = Character(name)
        controller.characters[name] = controller
        controller.send("You are now known as %s" % name)
    else:
        return controller.send("Name taken, please choose another name. \
The following names are also taken: \n%s" % ", ".join(controller.characters))

def show_room(controller):
    room = controller.character.get_room(controller.world)
    controller.sendLine("\n" + BLUE_TXT(room.name))
    controller.sendLine(room.description)
    controller.sendLine(YELLOW_TXT("occupants:") + " %s" % ", ".join(controller.characters))
    controller.sendLine(YELLOW_TXT("exits:") + " %s" % controller.character.get_room(controller.world).get_exits())

def say(controller, msg):
    timestamp = datetime.datetime.now().ctime()
    controller.broadcast('[%s] %s %s, "%s"' % (timestamp,
                                               controller.character.name,
                                               sentence_type(msg),
                                               punctuate(msg)),
                         protocol=controller)
        
def emote(controller, emotion):
    controller.broadcast("%s %s" % (controller.character.name,
                                    punctuate(emotion)),
                         protocol=controller)

def move(controller, mover, what=None):
    return show_room(controller)

def sense(controller, method, what=None):
    method = SENSES_METHOD[method]
    senser = controller.character
    obj = controller.character.get_room(controller.world)

    if what:        
        args = what.split()
        #if Character.is_character(controller, obj):
        
    controller.broadcast(method['broadcast'](senser, obj), protocol=controller)
    controller.send(PURPLE_TXT(method['callback'](senser, obj))+"\n", protocol=controller)
    #except:
    #    room = controller.character.get_room(controller.world)
    #    controller.sendLine("You don't sense anything unusual. %s" % 
    #                        (room.description))
                                 


