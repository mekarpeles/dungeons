from game.core import Entity

class Inventory(object):
    
    def __init__(self):
        self.capacity = 20
        self.inventory = {}
        self.clothing = []
        self.coins = []
        self.weapons = []
        self.armor = []

    @classmethod
    def add_item(cls, container, item):
        """
        Containers can have an inventory, a container could be
        something like a treasure chest or it could be like a
        Character
        """
        pass

    def insert(self, item):
        """
        Insert based on Entity.entity_id?
        """
        pass

    def remove(self, item):
        """
        Remove by hash_id?
        """
        pass

    def show_inventory(self):
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

    @classmethod
    def is_character(cls, controller, name):
        return name in controller.characters

    def get_room(self, world):
        return world.rooms[self.position]

    def he_or_she(self):
        return "he" if self.sex == "male" else "she"

    def her_or_his(self):
        return "his" if self.sex == "male" else "her"
