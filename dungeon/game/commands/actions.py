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
from game.commands import common

OBSERVE = ['l', 'inventory', 'i', 'who']
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
    common.list_occupants(controller)

def i(controller):
    return inventory(controller)

def inventory(controller):
    """Lists the user's inventory. Use kwargs to determine if
    inventory or items should be shown to others"""
    controller.sendLine("\n")
    controller.sendLine("Inventory:")
    controller.sendLine("==========")
    for index, item in controller.character.inventory.items.items():
        controller.sendLine("{}: {}".format(index, item.name))

def get(controller, args):
    """Potentially want to check for quantity + descriptors within the kwargs"""
    pass

def who(controller):
    common.who(controller)

def show(controller, args):
    """Show an item or object to another player"""
    pass

