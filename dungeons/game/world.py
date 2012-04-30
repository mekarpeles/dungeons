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

def get_direction_name(direction, invert=False):
    if invert:
        direction = opposite_cardinal(direction)
    return Room.DIRECTION_NAMES[direction]

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
    DIRECTION_NAMES = dict(zip(DIRECTIONS, ["north", "northeast", "east", "southeast",
                                            "south", "southwest", "west", "northwest"]))
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
        protocols = controller.players.values()
        occupants = [protocol.character for protocol in protocols if protocol.character.position == controller.character.position]
        return occupants

    def generate_map(self, rooms):
        """
        Generate 'n' nodes, make 'e' edges

        NOTES:
        - Multiple rooms can connect to the same room
        -- These connections must be through different exits
        - Rooms should have a bidirectional rel, moving 'e' then 'w' should bring you back to prev room

        """
        rs = range(rooms)

        # Create all the rooms and add them to the self.rooms dict
        for room_id in rs:
            self.rooms[room_id] = Room(room_id)

        # Create exits dict for each room
        for room_id in rs:
            # every time we make a connection/exit, the linked room should lead back to prev room

            # generate_exits should ignore any existing exits for this room            
            print room_id
            room = self.rooms[room_id]
            directions = self.generate_exits(ignore_exits=room.exits) # ["n", "e"]
            open_rooms = [v for k,v in self.rooms.items() if not k == room_id]

            exits = dict(self.generate_edges(room, directions, open_rooms))
            self.rooms[room_id].exits = exits

            for direction, open_room in exits.items():
                print("direction: %s, opposite: %s" % (direction, opposite_cardinal(direction)))
                room.exits[direction] = open_room
                open_room.exits[opposite_cardinal(direction)] = self.rooms[room_id]

        return self

    def generate_edges(self, room, directions, open_rooms):
        """
        Returns a list of (direction, room) tuples for compatible
        candidates/matches where a match is defined as an open_room in
        open_rooms and !=  room argument where direction not in open_room.exits
        """
        edges = []
        random.shuffle(open_rooms)
        for direction in directions:
            for open_room in open_rooms:
                if opposite_cardinal(direction) not in open_room.exits:
                    edges.append((direction, open_room))
                    open_rooms.remove(open_room)
                    break        
        return edges
            
    def generate_exits(self, directions=(Room.DIRECTIONS), min_exits=1, ignore_exits={}):
        """        
        NOTE: # Rooms must be greater than the number of exits - 8 (math desc. needed)

        Determines the maximum number of exits, taking into
        consideration the number of rooms_remaining

        >>> Map().generate_exits(5)
        ["n", "e", "s", "nw"]

        >>> Map().generate_exits(5, min_exits=5)
        ["n", "e", "s", "nw", "w"]
        """
        # Number of possible exits
        directions = [d for d in directions if d not in ignore_exits.keys()]
        possible_exits = len(directions)

        room_exits = random.randint(min_exits, possible_exits)
        return random.sample(directions, room_exits)
