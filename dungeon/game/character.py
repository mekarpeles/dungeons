from game.core import Entity
from game.items import Item

class Inventory(object):
    
    def __init__(self, *args, **kwargs):
        self.capacity = kwargs.get('capacity', 20)
        self.items = {}
        self.load(*args)

    def load(self, *items):
        for item in items:
            self.items[item.id] = item

    def add(self, item):
        """
        Insert based on Entity.entity_id?
        """
        self.items[item.id] = item        

    def remove(self, item):
        """
        Remove by hash_id?
        """
        pass

    def show(self):
        pass

    def show_coins(self):
        pass

    def show_armor(self):
        pass

    def show_weapons(self):
        pass

    def show_clothing(self):
        pass

class Sentient(Entity):

    DEFAULT_SEX = "male"
    DEFAULT_RACE = "human"

    def __init__(self):
        super(Sentient, self).__init__()
        self.race = self.DEFAULT_RACE
        self.sex = self.DEFAULT_SEX
        self.inventory = Inventory()
        self.position = 1
        self.level = 1
        self.encumberance = 0
        self.hp = 0
        self.sp = 0
        self.ep = 0

class Character(Sentient):
    
    def __init__(self, name, passwd_hash=None, **sentient):
        super(Character, self).__init__()
        self.name = name.title()
        self.xp = 0
        self.skills = []
        self.guild = "immigrant"
        self.char_class = None
        self.inventory = Inventory()

    def get_room(self, world):
        return world.rooms[self.position]

    def he_or_she(self):
        return "he" if self.sex == "male" else "she"

    def her_or_his(self):
        return "his" if self.sex == "male" else "her"

    @classmethod
    def is_character(cls, controller, name):
        return name in controller.characters

