from typing import List


INDOOR_MACROS = {
    # Key doors
    0xEC: [(0, 0, 0x2D), (1, 0, 0x2E)],
    0xED: [(0, 0, 0x2F), (1, 0, 0x30)],
    0xEE: [(0, 0, 0x31), (0, 1, 0x32)],
    0xEF: [(0, 0, 0x33), (0, 1, 0x34)],
    # Closed doors
    0xF0: [(0, 0, 0x35), (1, 0, 0x36)],
    0xF1: [(0, 0, 0x37), (1, 0, 0x38)],
    0xF2: [(0, 0, 0x39), (0, 1, 0x3A)],
    0xF3: [(0, 0, 0x3B), (0, 1, 0x3C)],
    # Open door
    0xF4: [(0, 0, 0x43), (1, 0, 0x44)],
    0xF5: [(0, 0, 0x8C), (1, 0, 0x08)],
    0xF6: [(0, 0, 0x09), (0, 1, 0x0A)],
    0xF7: [(0, 0, 0x0B), (0, 1, 0x0C)],

    0xF8: [(0, 0, 0xA4), (1, 0, 0xA5)], # boss door
    # 0xF9: [(0, 0, 0xAF), (1, 0, 0xB0)], # stairs door
    0xFA: [(0, 0, 0xB1), (1, 0, 0xB2)], # flipwall
    0xFB: [(0, 0, 0x45), (1, 0, 0x46)], # one way arrow
    0xFC: [
        (0, 0, 0xB3), (1, 0, 0xB4), (2, 0, 0xB4), (3, 0, 0xB5),
        (0, 1, 0xB6), (1, 1, 0xB7), (2, 1, 0xB8), (3, 1, 0xB9),
        (0, 2, 0xBA), (1, 2, 0xBB), (2, 2, 0xBC), (3, 2, 0xBD),
    ],
    0xFD: [(0, 0, 0xC1), (1, 0, 0xC2)],
}


class RoomTemplate:
    WALL_UP = 0x01
    WALL_DOWN = 0x02
    WALL_LEFT = 0x04
    WALL_RIGHT = 0x08

    def __init__(self, flags):
        self.tiles = [None] * 80
        for x in range(0, 10):
            if flags & RoomTemplate.WALL_UP:
                self.tiles[x + 0 * 10] = 0x21
            if flags & RoomTemplate.WALL_DOWN:
                self.tiles[x + 7 * 10] = 0x22
        for y in range(0, 8):
            if flags & RoomTemplate.WALL_LEFT:
                self.tiles[0 + y * 10] = 0x23
            if flags & RoomTemplate.WALL_RIGHT:
                self.tiles[9 + y * 10] = 0x24
        if flags & RoomTemplate.WALL_LEFT and flags & RoomTemplate.WALL_UP:
            self.tiles[0 + 0 * 10] = 0x25
        if flags & RoomTemplate.WALL_RIGHT and flags & RoomTemplate.WALL_UP:
            self.tiles[9 + 0 * 10] = 0x26
        if flags & RoomTemplate.WALL_LEFT and flags & RoomTemplate.WALL_DOWN:
            self.tiles[0 + 7 * 10] = 0x27
        if flags & RoomTemplate.WALL_RIGHT and flags & RoomTemplate.WALL_DOWN:
            self.tiles[9 + 7 * 10] = 0x28


INDOOR_ROOM_TEMPLATES = [
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_UP | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_UP | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_UP),
    RoomTemplate(RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_UP | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_DOWN),
    RoomTemplate(RoomTemplate.WALL_RIGHT | RoomTemplate.WALL_UP),
    RoomTemplate(RoomTemplate.WALL_LEFT | RoomTemplate.WALL_UP),
    RoomTemplate(0),
]

class RoomObjectEditor:
    def __init__(self, data):
        self.room = data["id"]
        if isinstance(self.room, str):
            self.room = int(self.room[:-3], 16)
        self.entities = []
        self.objects = []
        self.tileset_index = None
        self.palette_index = None
        self.attribset = None

        if "entities" in data:
            self.entities = data["entities"][:]

        objects_raw = data["data"]

        self.animation_id = objects_raw[0]
        self.floor_object = objects_raw[1]
        self.overlay = data.get("overlay")
        idx = 2
        while objects_raw[idx] != 0xFE:
            x = objects_raw[idx] & 0x0F
            y = objects_raw[idx] >> 4
            if y == 0x08:  # horizontal
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectHorizontal(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0C: # vertical
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectVertical(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0E:  # warp
                self.objects.append(ObjectWarp(objects_raw[idx] & 0x0F, objects_raw[idx + 1], objects_raw[idx + 2], objects_raw[idx + 3], objects_raw[idx + 4]))
                idx += 5
            else:
                self.objects.append(Object(x, y, objects_raw[idx + 1]))
                idx += 2
        assert idx == len(objects_raw) - 1

    def addEntity(self, x, y, type_id):
        self.entities.append((x, y, type_id))

    def removeEntities(self, type_id):
        self.entities = list(filter(lambda e: e[2] != type_id, self.entities))

    def hasEntity(self, type_id):
        return any(map(lambda e: e[2] == type_id, self.entities))

    def hasObject(self, type_id):
        return any(map(lambda o: o.type_id == type_id, self.objects))

    def changeObject(self, x, y, new_type):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                obj.type_id = new_type
                if self.overlay is not None:
                    self.overlay[x + y * 10] = new_type

    def removeObject(self, x, y):
        self.objects = list(filter(lambda obj: obj.x != x or obj.y != y, self.objects))

    def moveObject(self, x, y, new_x, new_y):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                if self.overlay is not None:
                    self.overlay[x + y * 10] = self.floor_object
                    self.overlay[new_x + new_y * 10] = obj.type_id
                obj.x = new_x
                obj.y = new_y

    def getWarps(self) -> List["ObjectWarp"]:
        return list(filter(lambda obj: isinstance(obj, ObjectWarp), self.objects))

    def updateOverlay(self, preserve_floor=False):
        if self.overlay is None:
            return
        if not preserve_floor:
            for n in range(80):
                self.overlay[n] = self.floor_object
        for obj in self.objects:
            if isinstance(obj, ObjectHorizontal):
                for n in range(obj.count):
                    self.overlay[obj.x + n + obj.y * 10] = obj.type_id
            elif isinstance(obj, ObjectVertical):
                for n in range(obj.count):
                    self.overlay[obj.x + n * 10 + obj.y * 10] = obj.type_id
            elif not isinstance(obj, ObjectWarp):
                self.overlay[obj.x + obj.y * 10] = obj.type_id

    def getTileArray(self):
        if self.room < 0x100:
            tiles = [self.floor_object] * 80
        else:
            tiles = [self.floor_object & 0x0F] * 80
        def objHSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        def objVSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        def getObject(x, y):
            x, y = (x & 15), (y & 15)
            if x < 10 and y < 8:
                return tiles[x + y * 10]
            return 0
        if self.room < 0x100:
            def placeObject(x, y, type_id):
                if type_id == 0xF5:
                    if getObject(x, y) in (0x1B, 0x28, 0x29, 0x83, 0x90):
                        placeObject(x, y, 0x29)
                    else:
                        placeObject(x, y, 0x25)
                    if getObject(x + 1, y) in (0x1B, 0x27, 0x82, 0x86, 0x8A, 0x90, 0x2A):
                        placeObject(x + 1, y, 0x2A)
                    else:
                        placeObject(x + 1, y, 0x26)
                    if getObject(x, y + 1) in (0x26, 0x2A):
                        placeObject(x, y + 1, 0x2A)
                    elif getObject(x, y + 1) == 0x90:
                        placeObject(x, y + 1, 0x82)
                    else:
                        placeObject(x, y + 1, 0x27)
                    if getObject(x + 1, y + 1) in (0x25, 0x29):
                        placeObject(x + 1, y + 1, 0x29)
                    elif getObject(x + 1, y + 1) == 0x90:
                        placeObject(x + 1, y + 1, 0x83)
                    else:
                        placeObject(x + 1, y + 1, 0x28)
                elif type_id == 0xF6:  # two door house
                    placeObject(x + 0, y, 0x55)
                    placeObject(x + 1, y, 0x5A)
                    placeObject(x + 2, y, 0x5A)
                    placeObject(x + 3, y, 0x5A)
                    placeObject(x + 4, y, 0x56)
                    placeObject(x + 0, y + 1, 0x57)
                    placeObject(x + 1, y + 1, 0x59)
                    placeObject(x + 2, y + 1, 0x59)
                    placeObject(x + 3, y + 1, 0x59)
                    placeObject(x + 4, y + 1, 0x58)
                    placeObject(x + 0, y + 2, 0x5B)
                    placeObject(x + 1, y + 2, 0xE2)
                    placeObject(x + 2, y + 2, 0x5B)
                    placeObject(x + 3, y + 2, 0xE2)
                    placeObject(x + 4, y + 2, 0x5B)
                elif type_id == 0xF7:  # large house
                    placeObject(x + 0, y, 0x55)
                    placeObject(x + 1, y, 0x5A)
                    placeObject(x + 2, y, 0x56)
                    placeObject(x + 0, y + 1, 0x57)
                    placeObject(x + 1, y + 1, 0x59)
                    placeObject(x + 2, y + 1, 0x58)
                    placeObject(x + 0, y + 2, 0x5B)
                    placeObject(x + 1, y + 2, 0xE2)
                    placeObject(x + 2, y + 2, 0x5B)
                elif type_id == 0xF8:  # catfish
                    placeObject(x + 0, y, 0xB6)
                    placeObject(x + 1, y, 0xB7)
                    placeObject(x + 2, y, 0x66)
                    placeObject(x + 0, y + 1, 0x67)
                    placeObject(x + 1, y + 1, 0xE3)
                    placeObject(x + 2, y + 1, 0x68)
                elif type_id == 0xF9:  # palace door
                    placeObject(x + 0, y, 0xA4)
                    placeObject(x + 1, y, 0xA5)
                    placeObject(x + 2, y, 0xA6)
                    placeObject(x + 0, y + 1, 0xA7)
                    placeObject(x + 1, y + 1, 0xE3)
                    placeObject(x + 2, y + 1, 0xA8)
                elif type_id == 0xFA:  # stone pig head
                    placeObject(x + 0, y, 0xBB)
                    placeObject(x + 1, y, 0xBC)
                    placeObject(x + 0, y + 1, 0xBD)
                    placeObject(x + 1, y + 1, 0xBE)
                elif type_id == 0xFB:  # palmtree
                    if x == 15:
                        placeObject(x + 1, y + 1, 0xB7)
                        placeObject(x + 1, y + 2, 0xCE)
                    else:
                        placeObject(x + 0, y, 0xB6)
                        placeObject(x + 0, y + 1, 0xCD)
                        placeObject(x + 1, y + 0, 0xB7)
                        placeObject(x + 1, y + 1, 0xCE)
                elif type_id == 0xFC:  # square "hill with hole" (seen near lvl4 entrance)
                    placeObject(x + 0, y, 0x2B)
                    placeObject(x + 1, y, 0x2C)
                    placeObject(x + 2, y, 0x2D)
                    placeObject(x + 0, y + 1, 0x37)
                    placeObject(x + 1, y + 1, 0xE8)
                    placeObject(x + 2, y + 1, 0x38)
                    placeObject(x - 1, y + 2, 0x0A)
                    placeObject(x + 0, y + 2, 0x33)
                    placeObject(x + 1, y + 2, 0x2F)
                    placeObject(x + 2, y + 2, 0x34)
                    placeObject(x + 0, y + 3, 0x0A)
                    placeObject(x + 1, y + 3, 0x0A)
                    placeObject(x + 2, y + 3, 0x0A)
                    placeObject(x + 3, y + 3, 0x0A)
                elif type_id == 0xFD:  # small house
                    placeObject(x + 0, y, 0x52)
                    placeObject(x + 1, y, 0x52)
                    placeObject(x + 2, y, 0x52)
                    placeObject(x + 0, y + 1, 0x5B)
                    placeObject(x + 1, y + 1, 0xE2)
                    placeObject(x + 2, y + 1, 0x5B)
                else:
                    x, y = (x & 15), (y & 15)
                    if x < 10 and y < 8:
                        tiles[x + y * 10] = type_id
        else:
            def placeObject(x, y, type_id):
                x, y = (x & 15), (y & 15)
                if type_id == 0xEC:  # key door
                    placeObject(x, y, 0x2D)
                    placeObject(x + 1, y, 0x2E)
                elif type_id == 0xED:
                    placeObject(x, y, 0x2F)
                    placeObject(x + 1, y, 0x30)
                elif type_id == 0xEE:
                    placeObject(x, y, 0x31)
                    placeObject(x, y + 1, 0x32)
                elif type_id == 0xEF:
                    placeObject(x, y, 0x33)
                    placeObject(x, y + 1, 0x34)
                elif type_id == 0xF0:  # closed door
                    placeObject(x, y, 0x35)
                    placeObject(x + 1, y, 0x36)
                elif type_id == 0xF1:
                    placeObject(x, y, 0x37)
                    placeObject(x + 1, y, 0x38)
                elif type_id == 0xF2:
                    placeObject(x, y, 0x39)
                    placeObject(x, y + 1, 0x3A)
                elif type_id == 0xF3:
                    placeObject(x, y, 0x3B)
                    placeObject(x, y + 1, 0x3C)
                elif type_id == 0xF4:  # open door
                    placeObject(x, y, 0x43)
                    placeObject(x + 1, y, 0x44)
                elif type_id == 0xF5:
                    placeObject(x, y, 0x8C)
                    placeObject(x + 1, y, 0x08)
                elif type_id == 0xF6:
                    placeObject(x, y, 0x09)
                    placeObject(x, y + 1, 0x0A)
                elif type_id == 0xF7:
                    placeObject(x, y, 0x0B)
                    placeObject(x, y + 1, 0x0C)
                elif type_id == 0xF8:  # boss door
                    placeObject(x, y, 0xA4)
                    placeObject(x + 1, y, 0xA5)
                elif type_id == 0xF9:  # stairs door
                    placeObject(x, y, 0xAF)
                    placeObject(x + 1, y, 0xB0)
                elif type_id == 0xFA:  # flipwall
                    placeObject(x, y, 0xB1)
                    placeObject(x + 1, y, 0xB2)
                elif type_id == 0xFB:  # one way arrow
                    placeObject(x, y, 0x45)
                    placeObject(x + 1, y, 0x46)
                elif type_id == 0xFC:  # entrance
                    placeObject(x + 0, y, 0xB3)
                    placeObject(x + 1, y, 0xB4)
                    placeObject(x + 2, y, 0xB4)
                    placeObject(x + 3, y, 0xB5)
                    placeObject(x + 0, y + 1, 0xB6)
                    placeObject(x + 1, y + 1, 0xB7)
                    placeObject(x + 2, y + 1, 0xB8)
                    placeObject(x + 3, y + 1, 0xB9)
                    placeObject(x + 0, y + 2, 0xBA)
                    placeObject(x + 1, y + 2, 0xBB)
                    placeObject(x + 2, y + 2, 0xBC)
                    placeObject(x + 3, y + 2, 0xBD)
                elif type_id == 0xFD:  # entrance
                    placeObject(x, y, 0xC1)
                    placeObject(x + 1, y, 0xC2)
                else:
                    if x < 10 and y < 8:
                        tiles[x + y * 10] = type_id

            def addWalls(flags):
                for x in range(0, 10):
                    if flags & 0b0010:
                        placeObject(x, 0, 0x21)
                    if flags & 0b0001:
                        placeObject(x, 7, 0x22)
                for y in range(0, 8):
                    if flags & 0b1000:
                        placeObject(0, y, 0x23)
                    if flags & 0b0100:
                        placeObject(9, y, 0x24)
                if flags & 0b1000 and flags & 0b0010:
                    placeObject(0, 0, 0x25)
                if flags & 0b0100 and flags & 0b0010:
                    placeObject(9, 0, 0x26)
                if flags & 0b1000 and flags & 0b0001:
                    placeObject(0, 7, 0x27)
                if flags & 0b0100 and flags & 0b0001:
                    placeObject(9, 7, 0x28)

            if self.floor_object & 0xF0 == 0x00:
                addWalls(0b1111)
            if self.floor_object & 0xF0 == 0x10:
                addWalls(0b1101)
            if self.floor_object & 0xF0 == 0x20:
                addWalls(0b1011)
            if self.floor_object & 0xF0 == 0x30:
                addWalls(0b1110)
            if self.floor_object & 0xF0 == 0x40:
                addWalls(0b0111)
            if self.floor_object & 0xF0 == 0x50:
                addWalls(0b1001)
            if self.floor_object & 0xF0 == 0x60:
                addWalls(0b0101)
            if self.floor_object & 0xF0 == 0x70:
                addWalls(0b0110)
            if self.floor_object & 0xF0 == 0x80:
                addWalls(0b1010)
        for obj in self.objects:
            if isinstance(obj, ObjectWarp):
                pass
            elif isinstance(obj, ObjectHorizontal):
                for n in range(0, obj.count):
                    placeObject(obj.x + n * objHSize(obj.type_id), obj.y, obj.type_id)
            elif isinstance(obj, ObjectVertical):
                for n in range(0, obj.count):
                    placeObject(obj.x, obj.y + n * objVSize(obj.type_id), obj.type_id)
            else:
                placeObject(obj.x, obj.y, obj.type_id)
        return tiles


class Object:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type_id = type_id

    def export(self):
        return bytearray([self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02X" % (self.__class__.__name__, self.x, self.y, self.type_id)


class ObjectHorizontal(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0x80 | self.count, self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02Xx%d" % (self.__class__.__name__, self.x, self.y, self.type_id, self.count)


class ObjectVertical(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0xC0 | self.count, self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02Xx%d" % (self.__class__.__name__, self.x, self.y, self.type_id, self.count)


class ObjectWarp(Object):
    def __init__(self, warp_type, map_nr, room_nr, target_x, target_y):
        super().__init__(None, None, None)
        if warp_type > 0:
            # indoor map
            if map_nr == 0xff:
                room_nr += 0x300  # color dungeon
            elif 0x06 <= map_nr < 0x1A:
                room_nr += 0x200  # indoor B
            else:
                room_nr += 0x100  # indoor A
        self.warp_type = warp_type
        self.room = room_nr
        self.map_nr = map_nr
        self.target_x = target_x
        self.target_y = target_y

    def export(self):
        return bytearray([0xE0 | self.warp_type, self.map_nr, self.room & 0xFF, self.target_x, self.target_y])

    def copy(self):
        return ObjectWarp(self.warp_type, self.map_nr, self.room & 0xFF, self.target_x, self.target_y)

    def __repr__(self):
        return "%s:%d:%03x:%02x:%d,%d" % (self.__class__.__name__, self.warp_type, self.room, self.map_nr, self.target_x, self.target_y)
