#!/usr/bin/python

import game.actions
import game.world

class Eval(object):

    def __init__(self):
        pass

    def evaluate(self, controller, msg):

        # If no name is set
        if not controller.character:
            game.actions.login(controller, name=msg)

        if msg:
            try:
                op, rest = msg.split(" ", 1)
            except:
                rest = ""
                op = ''.join(msg.split(" ", 1))

            if op in game.actions.COMMANDS:
                game.actions.COMMANDS[op](controller, rest)
                
            if op in game.actions.SENSES_METHOD.keys():
                game.actions.SENSES_LAMBDA(controller, op, rest)

            if op in game.world.Room.DIRECTIONS:
                game.actions.move(controller, op)
