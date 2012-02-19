
from game.items import Item

class Inventory(object):
    
    def __init__(self):
        
        pass

class Character(object):
    
    def __init__(self):
        self.inventory = Inventory()
        self.race = RACE
        self.level = 1
        self.npc = False
        self.hp = 0
        self.sp = 0
        self.ep = 0
