from game.character import Character
from utils.util import punctuate
from utils.util import sentence_type

COMMANDS = {"quit": lambda controller, **kwargs: controller.transport.loseConnection(),
            "say": lambda controller, msg: say(controller, msg),
            "emote": lambda controller, emotion: emote(controller, emotion),
            "look": lambda controller, args: sense(controller, "look", args),
           }


SENSES_METHOD = {"look": "description",
                 "smell": "smell",
                 "listen": "sound",
                 "taste": "taste",
                 "feel": "texture",
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

def say(controller, msg):
    controller.broadcast('%s %s, "%s"' % (controller.character.name,
                                          sentence_type(msg),
                                          punctuate(msg)),
                         protocol=controller)
        
def emote(controller, emotion):
    controller.broadcast("%s %s" % (controller.character.name,
                                    punctuate(emotion)),
                         protocol=controller)

def sense(controller, method, what):
    try:
        print("what: %s" % what)
        if not what:
            lookee = controller.character.get_room(controller.world)
        #elif Character.is_character(controller, lookee):
        controller.broadcast("%s %ss %s" % (controller.character.name,
                                            method,
                                            getattr(lookee, SENSE_METHOD[method],
                                                    None)),
                             protocol=controller)
    except:
        room = controller.character.get_room(controller.world)
        controller.sendLine("You don't sense anything unusual. %s" % 
                            (room.description))
                                 


