# -*- coding: utf-8 -*-
"""
    game.commands.actions
    ~~~~~~~~~~~~~~~~~~~~~
    Handles game actions like GETting items, PUTting items, checking
    inventory, looking at a room, etc

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from configs.formatting import *


OBSERVE = ['l', 'inventory']
ACTIONS = ['get', 'show']

def action(controller, opt, args):
    """Dispatch to the appropriate action method"""
    return globals().get(opt, lambda controller, args: None)(controller, args)

def observe(controller, opt):
    """Dispatch to the appropriate action method"""
    return globals().get(opt, lambda controller: None)(controller)

def l(controller):
    """Displays the contents and description of the room
    controller.character is in. Passively + privately examine the
    state of the world without side effect
    """
    room = controller.character.get_room(controller.world)
    controller.sendLine("\n{}".format(BLUE_TXT(room.name)))
    controller.sendLine(room.description)
    controller.sendLine("{} {}".format(
            LIGHTBLUE_TXT("exits:"),
            controller.character.get_room(controller.world).get_exits()))
    controller.sendLine(YELLOW_TXT("\noccupants:"))
    occupants = ["{} named {}\n".format(c.race, c.name) \
                     for c in controller.world.occupants(controller)]
    controller.sendLine("\r".join(occupants))

def inventory(controller):
    """Lists the user's inventory. Use kwargs to determine if
    inventory or items should be shown to others"""
    pass

def get(controller, args):
    """Potentially want to check for quantity + descriptors within the kwargs"""
    pass

def show(controller, args):
    """Show an item or object to another player"""
    pass

