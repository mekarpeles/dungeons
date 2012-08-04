# -*- coding: utf-8 -*-
"""
    game.commands.senses
    ~~~~~~~~~~~~~~~~~~~~
    Handles all sensory commands in the game including smell, sight, feel, etc.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from configs.formatting import *

def sense(controller, method, objs=None):
    """Handles all top-level sensory requests and dispatches requests
    to the appropriate action function
    """
    method = SENSES[method]
    actor = controller.character
    obj = controller.character.get_room(controller.world)

    # What obj is being sensed?
    if objs:
        objs = objs.split()
        #if Character.is_character(controller, args[0]):

    # Action
    controller.broadcast("\n" + method['broadcast'](actor, obj),
                         protocol=controller)
    # Response / callback
    controller.send(PURPLE_TXT(method['callback'](actor, obj)),
                    protocol=controller)

    #except:
    #    room = controller.character.get_room(controller.world)
    #    controller.sendLine("You don't sense anything unusual. %s" % 
    #                        (room.description))

SENSES = \
    {"look": { "broadcast": lambda character, obj, **kwargs: \
                   "{}'s gaze wanders as {} looks at the {}." \
                   .format(character.name, character.he_or_she(), obj.object_type),
               "callback": lambda character, obj, **kwargs: obj.description,
               },
     "smell": { "broadcast": lambda character, obj, **kwargs: \
                    "{} sniffs the air around the {}." \
                    .format(character.name, obj.object_type),
                "callback": lambda character, obj, **kwargs: \
                    "You smell {}.".format(obj.smell),
               },
     "listen": {"broadcast": lambda character, obj, **kwargs: \
                    "{} listens carefully for a moment.".format(character.name),
                "callback": lambda character, obj, **kwargs: \
                    "You hear the %s" % obj.sound,
                },
     "taste": {"broadcast": lambda character, obj, **kwargs: \
                   "{} tastes the {}.".format(character.name, obj.object_type),
               "callback": lambda character, obj, **kwargs: \
                   "You taste %s." % obj.taste,
               },
     "feel": {"broadcast": lambda character, obj, **kwargs: \
                  "{} feels around the {}."\
                  .format(character.name, obj.object_type),
              "callback": lambda character, obj, **kwargs: \
                  "You feel %s" % obj.texture,
              },
     }
