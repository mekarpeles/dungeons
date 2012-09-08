from game.core import Entity

class Item(Entity):
    
    def __init__(self, item_id, name):
        self.id = item_id
        self.name = name
        self.weight = 0
        self.value = 1000
        self.smell = ""
        self.desc = ""
        self.feel = ""
        self.status = ""
        self.materials = [] # cls?

class RepairableItem(Item):

    def __init__(self, item_id):
        self.repairs = 3
        super(RepairableItem, self).__init__()
        
class Food(Item):

    def __init__(self):
        pass

class Weapon(RepairableItem):

    def __init__(self):
        pass

class Clothing(RepairableItem):

    def __init__(self):
        self.equiped = False

