# -*- coding: utf-8 -*-
"""
    world.py
    ~~~~~~~~

    This module is responsible for generating Dungeon game worlds,
    rooms, and different environments. It also provides utilities for
    measurements and directions.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import hashlib
import random
import string
from copy import deepcopy
from game.core import Entity
from configs.config import DEBUG

def cardinal_to_numeric(cardinal):
    """Converts/maps cardinal directions like "n" to a numeric
    representations.
    """
    return Room.CARDINAL_DIRECTIONS[cardinal]

def numeric_to_cardinal(index):
    """Converts/maps numeric representations of directions into their
    string literals, e.g. "n" return Room.DIRECTIONS[index]
    """
    return Room.DIRECTIONS[index]

def opposite_cardinal(cardinal):
    """Given a cardinal direction, returns the opposite cardinal
    direction, e.g. given "n", returns "s"
    """
    index = cardinal_to_numeric(cardinal)
    opposite = numeric_to_cardinal(index + 4) if index in range(3) \
        else numeric_to_cardinal(index - 4)
    return opposite

def get_direction_name(direction, invert=False):
    """Returns the full name of a cardinal direction
    >>> get_direction_name("n")
    "north"
    """
    direction = opposite_cardinal(direction) if invert else direction
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
    DIRECTION_NAMES = \
        dict(zip(DIRECTIONS, ["north", "northeast", "east", "southeast",
                              "south", "southwest", "west", "northwest"]))
    CARDINAL_DIRECTIONS = dict(zip(DIRECTIONS,range(len(DIRECTIONS))))
    DEFAULT_EXITS = dict(zip(DIRECTIONS,[None]*len(DIRECTIONS)))

    # Default descriptors should be moved 
    DEFAULT_DESC = \
        "The cavern is pitch black; almost super naturally so. " \
        "The darkness seems to swallow all light, making it " \
        "difficult to navigate."
    DEFAULT_SMELL = \
        random.choice(["a stench of what can only be a thousand infected "
                       "and rotting corpses",
                       "sweet lilac"
                       ])
    DEFAULT_TASTE = \
        random.choice(["salt in the air; there is not much moisture",
                       "ozone and crisp air"
                       ])
    DEFAULT_TEXTURE = \
        random.choice(["coarse, porous rock along the walls and slippery, " \
                       "calcified limestone coating the cavern floor",
                       "cold, wet water running down the walls, collecting in " \
                       "a shallow pool along the floor",
                                    ])
    DEFAULT_SOUND = \
        random.choice(["echoes of thick, hairly insect legs scuttling across " \
                           "the floor in the distance",
                       "water dripping intermittently from the ceiling; the " \
                           "drip of water is all that breaks the silence"
                       ])
    ALTITUDES = range(5) # TBD
    TERRAIN = range(5) # TBD
    
    def __init__(self, room_id, exits=None, name="", desc=DEFAULT_DESC,
                 terrain=0, texture=DEFAULT_TEXTURE, altitude=0,
                 smell=DEFAULT_SMELL, taste=DEFAULT_TASTE, sound=DEFAULT_SOUND):
        self.object_type = "room"
        self.id = room_id
        self.exits = exits if exits else {}
        self.description = desc
        self.terrain = self.TERRAIN[terrain]
        self.texture = texture
        self.altitude = altitude
        self.smell = smell
        self.sound = sound
        self.taste = taste
        self.occupants = {}
        self.items = []
        self.name = name if name else "Room {}".format(self.id)

    def get_exits(self):
        xits = filter(lambda key: self.exits[key], self.exits.keys())
        return xits if xits else None

    @classmethod
    def create_random(cls):
        return Room(exits=random.sample(EXITS, range(8)))

class Map(object):

    def __init__(self, rooms=random.randint(10,20), loadfile=None):
        self.rooms = self.load(loadfile) if loadfile else \
            self._connect_rooms(dict([(room_id, Room(room_id)) \
                                          for room_id in range(rooms)]))

    def next(self, room_id, direction):
        """Returns the next room in the map"""
        if room_id in self.rooms:
            room = self.rooms[room_id]
            if room.exits and direction in room.exits:
                return room.exits[direction].id
        return None

    def occupants(self, controller):
        """Returns a list of protocols/handlers; one for each occupant
        in the room.
        """
        protocols = controller.players.values()
        occupants = [protocol.character for protocol in protocols if \
                         protocol.character.position == \
                         controller.character.position]
        return occupants

    def load(self, rooms):
        """Easy way is to linearly iterate over rooms and load them
        into loaded_rooms and then build exits. The other approach is
        to build the first room and then build all its exits
        recursively (loading these rooms into memory in 1 traversal)
        using an explored list until all paths have been exhausted.
        """
        loaded_rooms = {}

        # Prebuild rooms without exits
        for r in rooms:
            if not r['id'] in loaded_rooms.keys():
                loaded_rooms[r['id']] = Room(r['id'], desc=str(r['desc']),
                                             name="{}".format(r['name']))

        # build exits now that we're guaranteed to have all rooms
        for r in rooms:
            for direction, rid in r['exits']:
                room = loaded_rooms[r['id']]
                room.exits[str(direction)] = loaded_rooms[rid]
        return loaded_rooms

    def _connect_rooms(self, rooms):
        """Generates bi-directional edges between self.rooms
        BUG: See BUG file, in some cases random.randint() is generating an
        invalid range

        NOTES:
        - Multiple Rooms can connect to the same Room via different exits
        - Rooms should have a bidirectional edges, moving 'e' then 'w'
          should bring you back to prev room
        """
        for room in rooms.values():
            # ["n", "e"]
            directions = self._randomly_choose_exits(blacklist=room.exits.keys())

            # [<Room:1>, ..., <Room:n>]
            unexplored = [rooms[k] for k in rooms.keys() if k != room.id]

            # Build bidirectional edges from this room to randomly
            # selected rooms from within the unexplored list, based on
            # the directions specified within the directions set            
            exits = dict(self._generate_edges(room, directions, unexplored))
            rooms[room.id].exits = exits

            for direction, open_room in exits.items():
                room.exits[direction] = open_room
                open_room.exits[opposite_cardinal(direction)] = rooms[room.id]
        return rooms

    def _randomly_choose_exits(self, blacklist, directions=(Room.DIRECTIONS),
                               min_exits=1,):
        """NOTE: # Rooms must be greater than
        the number of exits - 8 (math desc. needed)

        DANGER: when min_exits is not possible, should throw exception

        Determines the maximum number of exits, taking into
        consideration the number of rooms_remaining

        >>> Map().generate_exits(['ne', 'sw', 'w', 'se'])
        ["n", "e", "s", "nw"]
        """
        directions = [d for d in directions if d not in blacklist]
        possible_exits = random.randint(min_exits, len(directions))
        return random.sample(directions, possible_exits)

    def _generate_edges(self, room, directions, open_rooms):
        """Returns a list of (direction, room) tuples for compatible
        candidates/matches where a match is defined as an open_room in
        open_rooms and != room argument where direction not in
        open_room.exits       
        """
        edges = []
        random.shuffle(open_rooms)
        for direction in directions:
            for open_room in open_rooms:
                if (opposite_cardinal(direction) not in open_room.exits):
                    edges.append((direction, open_room))
                    open_rooms.remove(open_room)
                    break
        return edges
