
from game.items import Item

class Inventory(object):
    
    def __init__(self):
        
        pass

class Character(object):
    
    DEFAULT_RACE = "human"
    DEFAULT_SEX = "male"
    DEFAULT_APPEARANCE = "bland appearance"
    DEFAULT_SMELL = "smells like nothing"

    def __init__(self, name, passwd_hash=None,
                 appearance=DEFAULT_APPEARANCE,
                 sex=DEFAULT_SEX, race=DEFAULT_RACE,
                 smell=DEFAULT_SMELL):
        self.position = 0
        self.name = name
        self.appearance = appearance
        self.smell = smell
        self.race = race
        self.inventory = Inventory()
        self.level = 1
        self.encumberance = 0
        self.hp = 0
        self.sp = 0
        self.ep = 0

    @classmethod
    def is_character(cls, controller, name):
        return name in controller.characters

    def get_room(self, world):
        return world.rooms[self.position]
