#!/usr/bin/python

class Entity(object):

    DEFAULT_ENTTIY_TYPE = ""
    DEFAULT_DESCRIPTION = ""
    DEFAULT_APPEARANCE = ""
    DEFAULT_SMELL = ""
    DEFAULT_TASTE = ""
    DEFAULT_FEEL = ""
    DEFAULT_SOUND = ""
    DEFAULT_SIZE = 1
    DEFAULT_WEIGHT = 10 # lbs

    def __init__(self):
        self.name = ""
        #self.entity_id = ?
        #self.entity_type = DEFAULT_ENTITY_TYPE
        self.description = self.DEFAULT_DESCRIPTION
        self.look = self.DEFAULT_APPEARANCE
        self.smell = self.DEFAULT_SMELL
        self.taste = self.DEFAULT_TASTE
        self.texture = self.DEFAULT_FEEL
        self.sound = self.DEFAULT_SOUND
        self.size = self.DEFAULT_SIZE
        self.weight = self.DEFAULT_WEIGHT

