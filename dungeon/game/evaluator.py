# -*- coding: utf-8 -*-
"""
    game.evaluator
    ~~~~~~~~~~~~~~
    This module acts as the eval component of the game repl

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from game.commands.menu import CMDS, login
from game.character import Character

class Eval(object):

    def __init__(self, cmds=CMDS):
        self.cmds = cmds

    def evaluate(self, controller, msg):
        """Evaluate the client's commands"""
        if not msg.isspace():
            if not controller.character:
                login(controller, msg)
            else:
                try:
                    opt, rest = msg.split(" ", 1)
                except:
                    rest = ""
                    opt = ''.join(msg.split(" ", 1))
                    
                opt = opt.lower()
                for opts, action in self.cmds:
                    if opt in opts:
                        action(controller, opt, rest)
                                      
