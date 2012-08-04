# -*- coding: utf-8 -*-
"""
    game.commands.communication
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Handles speech between and amongst characters

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

#from datetime import datetime
from utils.util import punctuate
from utils.util import sentence_type

NOP = lambda controller, opt, msg: None
def communicate(controller, opt, msg):
    """Dispatch to the appropriate communication method"""
    return globals().get(opt, NOP)(controller, opt, msg)

def say(controller, opt, msg):
    #timestamp = datetime.now().ctime()
    controller.broadcast('{} {}, "{}"'.format(controller.character.name,
                                              sentence_type(msg),
                                              punctuate(msg)),
                         protocol=controller)
        
def emote(controller, opt, msg):
    controller.broadcast("{} {}".format(controller.character.name,
                                        punctuate(msg)),
                         protocol=controller)

COMMUNICATION = \
    {"say": lambda controller, method, msg: \
         say(controller, method, msg),
     "emote": lambda controller, method, msg: \
         emote(controller, msg),
     } # add shout, whisper, also see channels
