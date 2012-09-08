# -*- coding: utf-8 -*-
"""
    game.commands.common
    ~~~~~~~~~~~~~~~~~~~~
    Commands shared between commands modules
"""

from configs.formatting import *

def who(controller):
    """Lists all players online"""
    controller.send("\nWho's online")
    controller.send("============")
    for n in controller.players:
        controller.send(n.title())

def list_occupants(controller, broadcast=False):
    occupants = ["{} named {}\n".format(c.race, c.name) \
                     for c in controller.world.occupants(controller)]

    if broadcast:
        controller.broadcast(YELLOW_TXT("\noccupants:"),
                             protocol=controller,
                             send2self=False)
        for occupant in occupants:
            controller.broadcast(occupant,
                                 protocol=controller,
                                 send2self=False)
    else:
        controller.sendLine(YELLOW_TXT("\noccupants:"))
        for occupant in occupants:
            controller.sendLine(occupant)
