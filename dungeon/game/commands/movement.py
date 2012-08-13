# -*- coding: utf-8 -*-
"""
    game.commands.movement
    ~~~~~~~~~~~~~~~~~~~~~~
    Handles responses when character submits a movement request via
    cardinal directions

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from configs.formatting import *
from game.world import get_direction_name
from game.commands.actions import l

def move(controller, direction, what=None):
    """Moves an object from one position to another"""
    # XXX Player shouldn't see his own movements
    pos = controller.character.position
    pos2 = controller.world.next(pos, direction)
    print pos, pos2, direction
    if pos2:
        controller.broadcast(
            YELLOW_TXT("\n{} walks away {}.".format(
                    controller.character.name,
                    get_direction_name(direction))),
            protocol=controller, send2self=False)

        # Change position
        controller.character.position = pos2

        controller.broadcast(
            YELLOW_TXT("{} arrives from the {}.".format(
                    controller.character.name,
                    get_direction_name(direction, invert=True))),
            protocol=controller, send2self=False)
        return l(controller)

