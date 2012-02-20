import networkx as nx
import hashlib
import random
import string

def cardinal_to_numeric(cardinal):
    return Room.CARDINAL_DIRECTIONS[cardinal]

def numeric_to_cardinal(index):
    return Room.DIRECTIONS[index]

def opposite_cardinal(cardinal):
    index = cardinal_to_numeric(cardinal)
    if index in range(3):
        return numeric_to_cardinal(index + 4)
    else:
        return numeric_to_cardinal(index - 4)

class Room(object):
    """
    Exits:
    7 0 1
    6 * 2
    5 4 3
    """    
    DIRECTIONS = ["n", "ne", "e", "se",
                  "s", "sw", "w", "nw"]
    CARDINAL_DIRECTIONS = dict(zip(DIRECTIONS,range(len(DIRECTIONS))))
    DEFAULT_EXITS = dict(zip(DIRECTIONS,[None]*len(DIRECTIONS)))
    DEFAULT_DESC = "The room looks bland."
    DEFAULT_SMELL = "This room smells like nothing"
    ALTITUDES = range(5) # TBD
    TERRAIN = range(5) # TBD

    def __init__(self, room_id, exits=DEFAULT_EXITS, desc=DEFAULT_DESC,
                 terrain=0, altitude=0, smell=DEFAULT_SMELL):
        self.room_id = room_id
        self.exits = exits
        self.description = desc
        self.terrain = self.TERRAIN[terrain]
        self.altitude = altitude
        self.smell = smell
        self.occupants = {}
        self.items = []
        self.name = "= Room %s =" % room_id

    def add_occupant(self, character):
        self.occupants[character.name] = character

    def remove_occupant(self, character):
        del self.occupants[character.name]

    @classmethod
    def create_random(cls):
        return Room(exits=random.sample(EXITS, range(8)))

class Map(object):
       
    def __init__(self, rooms=random.randint(5,20)):
        self.rooms = {}
        self.generate_map(rooms)

    def next(self, room, direction):
        """
        Returns the next room in the map
        """
        pass

    def generate_map(self, rooms):
        #rooms = nx.random_regular_graph(8, 20)
        room_id = 0
        #room_exits = self.generate_exits(room_id)
        self.rooms[room_id] = Room(room_id)
        return self

    def generate_exits(self, rooms_remaining, possible_exits=len(Room.DIRECTIONS),
                       min_exits=1):
        """
        Determines the maximum number of exits, taking into
        consideration the number of rooms_remaining

        >>> Map().generate_exits(5)
        ["n", "e", "s", "nw"]

        >>> Map().generate_exits(5, min_exits=5)
        ["n", "e", "s", "nw", "w"]
        """
        # Number of possible exits
        room_exits = random.randint(min_exits, possible_exits) if rooms_remaining > possible_exits else rooms_remaining
        return random.sample(Room.DIRECTIONS, room_exits)
