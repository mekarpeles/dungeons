import hashlib
import random
import string
from game.core import Entity

import networkx as nx

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

class Room(Entity):
    """
    Exits:
    7 0 1
    6 * 2
    5 4 3
    """    
    ENTRY_ID = 0
    DIRECTIONS = ["n", "ne", "e", "se",
                  "s", "sw", "w", "nw"]
    CARDINAL_DIRECTIONS = dict(zip(DIRECTIONS,range(len(DIRECTIONS))))
    DEFAULT_EXITS = dict(zip(DIRECTIONS,[None]*len(DIRECTIONS)))
    DEFAULT_DESC = "The cavern is pitch black; almost super naturally so. The darkness seems to swallow all light, making it difficult to navigate."
    DEFAULT_SMELL = random.choice(["a stench of what can only be a thousand infected and rotting corpses",
                                  "sweet lilac"
                                  ])
    DEFAULT_TASTE = random.choice(["salt in the air; there is not much moisture",
                                  "ozone and crisp air"
                                  ])
    DEFAULT_TEXTURE = random.choice(["coarse, porous rock along the walls and slippery, calcified limestone coating the cavern floor",
                                    "cold, wet water running down the walls, collecting in a shallow pool along the floor",
                                    ])
    DEFAULT_SOUND = random.choice(["echoes of thick, hairly insect legs scuttling across the floor in the distance",
                                  "water dripping intermittently from the ceiling; the drip of water is all that breaks the silence"
                                  ])
    ALTITUDES = range(5) # TBD
    TERRAIN = range(5) # TBD
    
    def __init__(self, room_id, exits={}, desc=DEFAULT_DESC,
                 terrain=0, texture=DEFAULT_TEXTURE, altitude=0, smell=DEFAULT_SMELL,
                 taste=DEFAULT_TASTE, sound=DEFAULT_SOUND):
        self.object_type = "room"
        self.room_id = room_id
        self.exits = exits        
        self.description = desc
        self.terrain = self.TERRAIN[terrain]
        self.texture = texture
        self.altitude = altitude
        self.smell = smell
        self.sound = sound
        self.taste = taste
        self.occupants = {}
        self.items = []
        self.name = "Room %s" % room_id

    def get_exits(self):
        xits = filter(lambda key: self.exits[key], self.exits.keys())
        return xits if xits else None

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

    def next(self, room_id, direction):
        """
        Returns the next room in the map
        """
        if room_id in self.rooms:
            room = self.rooms[room_id]
            if room.exits and direction in room.exits:
                return room.exits[direction].room_id
        return None

    def occupants(self, controller):
        protocols = controller.characters.values()
        return [protocol.character for protocol in protocols if protocol.character.position == controller.character.position]

    def generate_map(self, rooms):
        """
        Generate 'n' nodes, make 'e' edges
        """
        rs = range(rooms)

        # Create all the rooms and add them to the self.rooms dict        
        for room_id in rs:
            self.rooms[room_id] = Room(room_id)

        # Create exits dict for each room
        for room_id in rs:
            # every time we make a connection/exit, the linked room should lead back to prev room

            # generate_exits should ignore any existing exits for this room            
            room = self.rooms[room_id]
            directions = self.generate_exits(ignore_exits=room.exits) # ["n", "e"]

            open_rooms = [v for k,v in self.rooms.items() if not k == room_id]
            num_exits = len(directions)
            exits = dict(zip(directions, random.sample(open_rooms, num_exits)))
            self.rooms[room_id].exits = exits

        return self
            
    def generate_exits(self, directions=(Room.DIRECTIONS), min_exits=1, ignore_exits={}):
        """
        NOTE: # Rooms must be greater than the number of exits - 8

        Determines the maximum number of exits, taking into
        consideration the number of rooms_remaining

        >>> Map().generate_exits(5)
        ["n", "e", "s", "nw"]

        >>> Map().generate_exits(5, min_exits=5)
        ["n", "e", "s", "nw", "w"]
        """
        # Number of possible exits
        directions = [d for d in directions if d not in ignore_exits.keys()]
        possible_exits = len(directions) - 1
        room_exits = random.randint(min_exits, possible_exits)
        return random.sample(directions, room_exits)
