import datetime
from game.character import Character
from utils.util import punctuate
from utils.util import sentence_type

COMMANDS = {"quit": lambda controller, **kwargs: controller.transport.loseConnection(),
            "say": lambda controller, msg: say(controller, msg),
            "emote": lambda controller, emotion: emote(controller, emotion),
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

def sense(controller, method, what=None):
    looker = controller.character
    lookee = controller.character.get_room(controller.world)

    if what:        
        args = what.split()
        #if Character.is_character(controller, lookee):

    x = SENSES_METHOD[method]
    controller.broadcast(x['broadcast'](looker, lookee), protocol=controller)
    controller.send("\033[94m" + x['callback'](looker, lookee) + "\033[0m\n",
                    protocol=controller)
    #except:
    #    room = controller.character.get_room(controller.world)
    #    controller.sendLine("You don't sense anything unusual. %s" % 
    #                        (room.description))
                                 


