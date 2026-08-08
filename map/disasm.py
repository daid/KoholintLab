import os
import re
from .roomobjecteditor import RoomObjectEditor


CONSTS = {
    # These consts are set with EQUS and this cannot be read automatically
    "W_TILESET_KEEP": 0x0F,
    "W_TILESET_CAMERA_SHOP": 0x1A,
    "W_TILESET_TURTLE_ROCK": 0x1C,
    "W_TILESET_SEASHELL_MANSION": 0x1E,
    "W_TILESET_MYSTERIOUS_WOODS": 0x20,
    "W_TILESET_BEACH": 0x22,
    "W_TILESET_PRAIRIE_STONE_HEAD": 0x24,
    "W_TILESET_MABE_VILLAGE": 0x26,
    "W_TILESET_KANALET_CASTLE": 0x28,
    "W_TILESET_FACE_SHRINE": 0x2A,
    "W_TILESET_YARNA_DESERT": 0x2C,
    "W_TILESET_PRAIRIE_SOUTH": 0x2E,
    "W_TILESET_EAGLES_TOWER": 0x30,
    "W_TILESET_RAFTING_GAME": 0x32,
    "W_TILESET_ANGLERS_TUNNEL": 0x34,
    "W_TILESET_GOPONGO_SWAMP": 0x36,
    "W_TILESET_GRAVEYARD": 0x38,
    "W_TILESET_MARTHAS_BAY": 0x3A,
    "W_TILESET_EGG": 0x3C,
    "W_TILESET_TARAMANCH_MIDDLE": 0x3E,

    "W_TILESET_INDOOR_00": 0x00,
    "W_TILESET_INDOOR_01": 0x01,
    "W_TILESET_INDOOR_02": 0x02,
    "W_TILESET_INDOOR_03": 0x03,
    "W_TILESET_INDOOR_04": 0x04,
    "W_TILESET_INDOOR_05": 0x05,
    "W_TILESET_INDOOR_06": 0x06,
    "W_TILESET_INDOOR_07": 0x07,
    "W_TILESET_INDOOR_08": 0x08,
    "W_TILESET_INDOOR_09": 0x09,
    "W_TILESET_INDOOR_0A": 0x0A,
    "W_TILESET_INDOOR_0B": 0x0B,
    "W_TILESET_INDOOR_0C": 0x0C,
    "W_TILESET_INDOOR_0D": 0x0D,
    "W_TILESET_INDOOR_0E": 0x0E,
    "W_TILESET_INDOOR_0F": 0x0F,
    "W_TILESET_INDOOR_17": 0x17,
    "W_TILESET_INDOOR_18": 0x18,
    "W_TILESET_INDOOR_19": 0x19,
    "W_TILESET_WINDFISH_FLOOR": 0x1A,
    "W_TILESET_NO_UPDATE": 0xFF,

    "ROOM_END": 0xFE
}

def read_constants(filename):
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        m = re.match(r"DEF\s+([\w]+)\s+EQU\s+([\$\w]+)", line)
        if m:
            value = m.group(2)
            value = int(value[1:], 16) if value.startswith("$") else int(value)
            CONSTS[m.group(1)] = value
        

def read_rooms(filename):
    """ Read the disassembly room file and return the raw list of bytes for each room in it. """
    rooms = []
    current = None
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.endswith(":"):
            label = line.rstrip(":")
            current = {"label": label, "data": []}
            if not "Unreferenced" in label:
                rooms.append(current)
        elif line.startswith("db "):
            for data_expr in line[3:].split(","):
                data = 0
                for data_value in data_expr.split("|"): # Ugly but works for now.
                    data_value = data_value.strip()
                    if data_value.startswith("$"):
                        data |= int(data_value[1:], 16)
                    elif data_value in CONSTS:
                        data |= CONSTS[data_value]
                    else:
                        raise ValueError(f"Unexpected data in room file: {filename}: {line}: {data_value}")
                current["data"].append(data)
        elif line:
            raise ValueError(f"Unexpected data in room file: {filename}: {line}")
    return rooms


def label_to_room_id(label):
    base_nr = None
    if label.startswith("Overworld"):
        base_nr = 0x000
        label = label[9:]
    elif label.startswith("IndoorsA"):
        base_nr = 0x100
        label = label[8:]
    elif label.startswith("IndoorsB"):
        base_nr = 0x200
        label = label[8:]
    elif label.startswith("ColorDungeon"):
        base_nr = 0x300
        label = label[12:]
    else:
        raise ValueError(f"Unexpected room label: {label}")
    if label.endswith("Alt"):
        return f"{base_nr + int(label[:-3], 16):03X}Alt"
    return base_nr + int(label, 16)

def read_entities(filename):
    entities = []
    current = None
    skip = False
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.endswith(":"):
            label = line.rstrip(":")
            assert label.endswith("Entities")
            current = {"label": label, "entities": []}
            if label.startswith("Overworld"):
                current["id"] = int(label[9:-8], 16)
            elif label.startswith("IndoorsA"):
                current["id"] = int(label[8:-8], 16) + 0x100
            elif label.startswith("IndoorsB"):
                current["id"] = int(label[8:-8], 16) + 0x200
            elif label.startswith("ColorDungeon"):
                current["id"] = int(label[12:-8], 16) + 0x300
            else:
                raise ValueError(f"Unexpected data in entities file: {filename}: {line}")
            entities.append(current)
        elif line == "entities_end":
            pass
        elif line.startswith("entity "):
            if skip:
                continue
            y, x, entity = map(str.strip, line[7:].split(","))
            x = int(x[1:], 16)
            y = int(y[1:], 16)
            entity = CONSTS[entity]
            current["entities"].append((x, y, entity))
        elif line == "IF __PATCH_0__": # Hacks to deal with some conditionals
            skip = False
        elif line == "IF !__PATCH_0__":
            skip = True
        elif line == "ENDC":
            skip = False
        elif line:
            raise ValueError(f"Unexpected data in entities file: {filename}: {line}")
    return entities

def read_map_layouts(filename):
    layouts = []
    current = None
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.endswith(":"):
            label = line.rstrip(":")
            assert label.startswith("MapLayout")
            current = {"id": int(label[9:]), "data": []}
            layouts.append(current)
        elif line.startswith("db "):
            for data in line[3:].split(","):
                data = data.strip()
                if data.startswith("$"):
                    data = int(data[1:], 16)
                else:
                    data = int(data)
                current["data"].append(data)
        elif line:
            raise ValueError(f"Unexpected data in layout file: {filename}: {line}")
    return layouts


def read_pointer_list(filename):
    result = []
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.startswith("._"):
            line = line.partition(" ")[2]
        if line.endswith(":"):
            label = line.rstrip(":")
        elif line.startswith("dw "):
            for data in line[3:].split(","):
                data = data.strip()
                result.append(data)
        elif line:
            raise ValueError(f"Unexpected data in data file: {filename}: {line}")
    return result

def read_palette_tables(filename):
    result = {}
    current = None
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.endswith(":"):
            label = line.rstrip(":")
            current = {"label": label, "data": []}
            result[label] = current
        elif line.startswith("db "):
            for data in line[3:].split(","):
                data = data.strip()
                if data.startswith("$"):
                    data = int(data[1:], 16)
                elif data in CONSTS:
                    data = CONSTS[data]
                else:
                    data = int(data)
                current["data"].append(data)
        elif line.startswith("dw "):
            for data in line[3:].split(","):
                data = data.strip()
                current["data"].append(data)
        elif line:
            raise ValueError(f"Unexpected data in data file: {filename}: {line}")
    return result

def read_palette_colors(filename):
    result = {}
    current = None
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.endswith(":"):
            label = line.rstrip(":")
            if not current or len(current["data"]) >= 32: # Ugly hack working around extra label in OverworldPalette03
                current = {"label": label, "data": []}
            result[label] = current
        elif line.startswith("rgb "):
            for data in line[3:].split(","):
                data = data.strip()
                if data.startswith("#"):
                    data = int(data[1:], 16)
                    data = (((data >> 16) & 0xFF), ((data >> 8) & 0xFF), ((data >> 0) & 0xFF))
                else:
                    raise ValueError(f"Unexpected data in palette file: {filename}: {line}")
                current["data"].append(data)
        elif line:
            raise ValueError(f"Unexpected data in palette file: {filename}: {line}")
    return result

def read_db_data(filename, *, with_labels=False, as_strings=False):
    result = []
    current = None
    skip = False
    for line in open(filename, "rt"):
        line = line.strip()
        if ";" in line:
            line = line[:line.find(";")].strip()
        if line.startswith("._"):
            line = line.partition(" ")[2]
        if skip:
            if line == "ENDC":
                skip = False
            continue
        if line == "IF !__PATCH_1__":
            skip = True
        elif line.endswith(":"):
            label = line.rstrip(":")
            if with_labels:
                current = {"label": label, "data": []}
                result.append(current)
        elif line.startswith("db "):
            for data in line[3:].split(","):
                data = data.strip()
                if not as_strings:
                    if data.startswith("$"):
                        data = int(data[1:], 16)
                    elif data in CONSTS:
                        data = CONSTS[data]
                    else:
                        data = int(data)
                if with_labels:
                    current["data"].append(data)
                else:
                    result.append(data)
        elif line:
            raise ValueError(f"Unexpected data in data file: {filename}: {line}")
    return result


def room_data_to_json(basepath):
    read_constants(os.path.join(basepath, "src/constants/animated_tiles.asm"))
    read_constants(os.path.join(basepath, "src/constants/room_templates.asm"))
    read_constants(os.path.join(basepath, "src/constants/entities.asm"))
    read_constants(os.path.join(basepath, "src/constants/gameplay.asm"))

    room_to_map_id = {}
    room_sidescroll = {}
    room_pos = {}

    rooms = []
    room_by_id = {}
    for filename in ["overworld_a.asm", "overworld_b.asm", "indoors_a.asm", "indoors_b.asm", "color_dungeon.asm"]:
        full_filename = os.path.join(basepath, "src/data/rooms", filename)
        for room in read_rooms(full_filename):
            room["id"] = label_to_room_id(room["label"])
            room["filename"] = filename
            rooms.append(room)
            room_by_id[room["id"]] = room
    for idx in range(len(rooms)): # Fix up that some labels are double used.
        if not rooms[idx]["data"] and rooms[idx]["id"] != 0x2FF:
            idx2 = idx + 1
            while not rooms[idx2]["data"]:
                idx2 += 1
            rooms[idx]["data"] = rooms[idx2]["data"]
    for filename in ["overworld_a.asm", "overworld_b.asm"]:
        full_filename = os.path.join(basepath, "src/data/rooms_gbc_overlays", filename)
        for result in read_db_data(full_filename, with_labels=True):
            assert result["label"].startswith("RoomGBCOverlay")
            result_id = result["label"][14:]
            if result_id.startswith("s"):
                continue
            if result_id.endswith("Alt"):
                result_id = f"0{result_id}"
            else:
                result_id = int(result_id, 16)
            for room in rooms:
                if room["id"] == result_id:
                    room["overlay"] = result["data"]
    for filename in ["overworld.asm", "indoors_a.asm", "indoors_b.asm", "color_dungeon.asm"]:
        full_filename = os.path.join(basepath, "src/data/entities", filename)
        for entities in read_entities(full_filename):
            if entities["id"] < 0x316:
                room_by_id[entities["id"]]["entities"] = entities["entities"]
    for room in rooms:
        if room["id"] == 0x2FF and not room["data"]: # Fix room 2FF not having any data
            room["data"] = [0, 0, 0xFE]
        for warp in RoomObjectEditor(room).getWarps():
            room_to_map_id[warp.room] = warp.map_nr
            room_sidescroll[warp.room] = warp.warp_type > 1
    for layout in read_map_layouts(os.path.join(basepath, "src/data/maps/layouts.asm")):
        for idx, room_nr in enumerate(layout["data"]):
            room_nr += 0x100
            if layout["id"] > 5:
                room_nr += 0x100
            if layout["id"] == 11:
                room_nr += 0x100
            if room_nr not in room_pos:
                room_pos[room_nr] = idx % 8, idx // 8
            if room_nr not in room_to_map_id:
                room_to_map_id[room_nr] = layout["id"] if layout["id"] < 11 else 0xFF
    for room_id in range(0x100):
        room_to_map_id[room_id] = -1

    # Fix up some data we are not being able to get from the room data. (This is partially why you should not export twice!)
    room_sidescroll[0x1FF] = True  # D4 boss
    room_sidescroll[0x2E8] = True  # D7 boss
    room_to_map_id[0x15D] = 1  # Empty unused D2 room
    room_to_map_id[0x17E] = 3  # Empty unused D4 room
    room_to_map_id[0x17F] = 3  # Empty unused D4 room
    room_to_map_id[0x1AD] = 4  # Empty unused D5 room
    room_to_map_id[0x1AE] = 4  # Empty unused D5 room
    room_to_map_id[0x1AF] = 4  # Empty unused D5 room
    room_to_map_id[0x1DE] = 5  # Empty unused D6 room
    room_to_map_id[0x1DF] = 5  # Empty unused D6 room
    room_to_map_id[0x1E4] = room_to_map_id[0x1F4]  # Rooster cave
    room_to_map_id[0x1E6] = room_to_map_id[0x1E5]  # Swimming connector cave to mad batter
    room_to_map_id[0x1E8] = room_to_map_id[0x1F9]  # Desert heartpiece cave
    room_to_map_id[0x1E9] = room_to_map_id[0x1EA]  # D4 connector cave
    room_to_map_id[0x1F8] = room_to_map_id[0x1F9]  # Desert heartpiece cave
    room_to_map_id[0x1ED] = room_to_map_id[0x1EE]  # Unused fireball cave
    room_to_map_id[0x1FC] = 0x11  # Unused beta cave

    room_to_map_id[0x22f] = 6  # Empty unused D7 room
    room_to_map_id[0x233] = 7  # Empty unused D8 room
    room_to_map_id[0x236] = 7  # Empty unused D8 room
    room_to_map_id[0x26c] = room_to_map_id[0x28F]  # Unused armos temple room
    room_to_map_id[0x26d] = room_to_map_id[0x28F]  # Unused armos temple room
    room_to_map_id[0x26e] = room_to_map_id[0x28F]  # Unused armos temple room
    room_to_map_id[0x26f] = room_to_map_id[0x28F]  # Final armos temple room
    room_to_map_id[0x277] = 0x11  # Unused bird key cave
    room_to_map_id[0x278] = 0x11  # Unused bird key cave
    room_to_map_id[0x279] = 0x11  # Unused bird key cave
    room_to_map_id[0x27f] = room_to_map_id[0x28F]  # Armos miniboss
    room_to_map_id[0x29e] = room_to_map_id[0x29F]  # Unused inside house
    room_to_map_id[0x2be] = 0x13  # Dream shrine
    room_to_map_id[0x2bf] = 0x13  # Dream shrine
    room_to_map_id[0x2ce] = 0x13  # Dream shrine
    room_to_map_id[0x2cf] = 0x13  # Dream shrine
    room_to_map_id[0x2c0] = 0x11  # Catfish maw dive cave
    room_to_map_id[0x2c1] = 0x11  # Catfish maw dive cave
    room_sidescroll[0x2c0] = True  # Catfish maw dive cave
    room_sidescroll[0x2c1] = True  # Catfish maw dive cave
    room_to_map_id[0x2c4] = 0x14  # Unused castle connector
    room_to_map_id[0x2c6] = 0x14  # Castle interior
    room_to_map_id[0x2d2] = 0x14  # Castle interior
    room_to_map_id[0x2d4] = 0x14  # Unused castle connector
    room_to_map_id[0x2d8] = room_to_map_id[0x2C8]  # Richard cave
    room_to_map_id[0x2dc] = room_to_map_id[0x2DB]  # Right side of animal house
    room_to_map_id[0x2e0] = room_to_map_id[0x2F0]  # Moblin cave
    room_to_map_id[0x2e1] = room_to_map_id[0x2F0]  # Moblin cave
    room_to_map_id[0x2e2] = room_to_map_id[0x2F0]  # Moblin cave
    room_to_map_id[0x2e4] = 0x11  # Boots&bomb cave
    room_to_map_id[0x2e5] = 0x11  # Boots&bomb cave
    room_to_map_id[0x2f5] = 0x0F  # Fisherman under the bridge
    room_sidescroll[0x2f5] = True  # Fisherman under the bridge

    room_pos[0x300] = (1, 3) # Fix the color dungeon boss room position, which we cannot read properly from the files.

    chest_data = read_db_data(os.path.join(basepath, "src/data/chests/overworld.asm")) + \
        read_db_data(os.path.join(basepath, "src/data/chests/indoors_a.asm")) + \
        read_db_data(os.path.join(basepath, "src/data/chests/indoors_b.asm")) + \
        read_db_data(os.path.join(basepath, "src/data/chests/color_dungeon.asm"))
    event_data = read_db_data(os.path.join(basepath, "src/data/events/dungeons.asm"))
    attribute_data = read_pointer_list(os.path.join(basepath, "src/data/object_attributes/pointers.asm"))
    attribute_data += ["ColorDungeonBGAttributes"] * 32
    palette_tables = read_palette_tables(os.path.join(basepath, "src/data/palettes/tables.asm"))
    overworld_tileset_data = read_db_data(os.path.join(basepath, "src/data/rooms_gfx/overworld_tileset_table.asm"))
    indoors_tileset_data = read_db_data(os.path.join(basepath, "src/data/rooms_gfx/indoors_tileset_table.asm"))

    alt_room_y = 0
    rooms_json = {}
    for room in rooms:
        room_nr = room["id"] if isinstance(room["id"], int) else int(room["id"][:-3], 16)
        x = room_nr % 16
        y = (room_nr // 16) % 16
        if room_nr in room_pos:
            x, y = room_pos[room_nr]
        if not isinstance(room["id"], int):
            x = 16
            y = alt_room_y
            alt_room_y += 1
        roe = RoomObjectEditor(room)
        map_id = room_to_map_id.get(room_nr, 0x1F if room_nr < 0x200 else 0x11)
        if room_nr < 0x100:
            palette_index = palette_tables["OverworldPaletteMap"]["data"][room_nr]
        elif map_id < 9 or map_id == 0xFF:
            palette_index = None
        else:
            table_name = palette_tables["IndoorPaletteMaps"]["data"][map_id - 10]
            palette_index = palette_tables[table_name]["data"][room_nr & 0xFF]
        if room_nr < 0x100:
            if len(overworld_tileset_data) >= 0x100:
                main_tileset_id = overworld_tileset_data[room_nr]
            else:
                main_tileset_id = overworld_tileset_data[(room_nr % 16) // 2 + ((room_nr // 16) // 2) * 8]
            attribute_table = attribute_data[room_nr]
        else:
            main_tileset_id = indoors_tileset_data[room_nr - 0x100]
            if map_id == 0xFF:
                attribute_table = "ColorDungeonBGAttributes"
            elif map_id in (6, 7) or room_nr < 0x200:
                attribute_table = attribute_data[0x100 + map_id]
            else:
                attribute_table = attribute_data[0x200 + map_id]
        room_json = {
            'id': room["id"],
            'num': room_nr,
            'x': x, 'y': y,
            'tiles': list(roe.overlay) if room_nr < 0x100 else roe.getTileArray(),
            'map_id': map_id,
            'sidescroll': room_sidescroll.get(room_nr, False),
            'attribute_table': attribute_table,
            'palette_index': palette_index,
            'tileset': main_tileset_id,
            'animation': roe.animation_id,
            'entities': [{'x': e[0], 'y': e[1], 'id': e[2]} for e in roe.entities],
            'warpdata': [{'target': w.room, 'target_x': w.target_x, 'target_y': w.target_y} for w in roe.getWarps()],
            'chestitem': chest_data[room_nr]
        }
        if room_nr >= 0x100:
            room_json['event'] = event_data[room_nr - 0x100]
        rooms_json[room_json["id"]] = room_json
    return rooms_json
