# -*- coding: utf-8 -*-
"""
    game.commands.menu
    ~~~~~~~~~~~~~~~~~~
    Entry point, handles dispatch for all game commands received and
    pre-processed by the Eval.evaluate listener

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from game.character import Character
from game.world import Room
from game.commands import senses, communication, movement, \
    actions, channels

COMMANDS = {"quit": lambda controller, opt, args: \
                controller.transport.loseConnection(),
            #"save": lambda controller, opt, args: \
                #controller.save
            }
NOP = lambda controller, opt, args: None
CMDS = [(COMMANDS.keys(), lambda controller, opt, args: \
             COMMANDS.get(opt, NOP)(controller, opt, args)),
        (actions.ACTIONS, lambda controller, opt, args: \
             actions.action(controller, opt, args)),
        (actions.OBSERVE, lambda controller, opt, args: \
             actions.observe(controller, opt)),
        (channels.CHANNELS.keys(), lambda controller, opt, args: \
             channels.channel(controller, opt, args)),
        (senses.SENSES.keys(), lambda controller, opt, args: \
             senses.sense(controller, opt, args)),
        (communication.COMMUNICATION.keys(), lambda controller, opt, args: \
             communication.communicate(controller, opt, args)),
        (Room.DIRECTIONS, lambda controller, opt, args: \
             movement.move(controller, opt, args)),
        #(["help"], lambda controller, opt, args
        ]


def login(controller, name):
    """Login the user so long as their name isn't currently active. In
    the future, this will support character accounts and will have to
    validate against a password if the user has a profile within some db
    """
    if not controller.players.has_key(name):
        controller.character = Character(name)
        controller.players[name] = controller
        controller.send("You are now known as %s" % name)
        actions.l(controller)
    else:
        controller.send("Name taken, please choose another name. "
                        "The following names are also taken: "
                        "\n{}".format(", ".join(controller.players)))

