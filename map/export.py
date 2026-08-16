import os
from . import disasm
from . import roomobjecteditor
from . import entityDatabase


def do_export(basepath, data):
    print(f"Exporting data to disassembly at {basepath}")
    if not _export_spritesheet_tables(basepath, data):
        return
    for filename, label_prefix, ids in [
        ("src/data/rooms/overworld_a.asm", "Overworld", list(range(0x000, 0x080)) + ["006Alt", "00EAlt", "01BAlt", "02BAlt", "079Alt"]),
        ("src/data/rooms/overworld_b.asm", "Overworld", list(range(0x080, 0x100)) + ["08CAlt"]),
        ("src/data/rooms/indoors_a.asm", "IndoorsA", list(range(0x100, 0x200)) + ["1F5Alt"]),
        ("src/data/rooms/indoors_b.asm", "IndoorsB", list(range(0x200, 0x300)) + []),
        ("src/data/rooms/color_dungeon.asm", "ColorDungeon", list(range(0x300, 0x316)) + []),
    ]:
        f = open(os.path.join(basepath, filename), "wt")
        for room_id in ids:
            if isinstance(room_id, str):
                f.write(f"{label_prefix}{room_id[1:]}::\n")
            else:
                f.write(f"{label_prefix}{room_id&0xFF:02X}::\n")
            room_objects = _encode_room_objects(data[str(room_id)], data)
            f.write("  db " + ", ".join([f"${b:02X}" for b in room_objects]) + "\n")
        f.close()
    for filename, start_label, label_prefix, ids in [
        ("src/data/rooms_gbc_overlays/overworld_a.asm", "RoomGBCOverlaysA", "RoomGBCOverlay", list(range(0x000, 0x0CC)) + []),
        ("src/data/rooms_gbc_overlays/overworld_b.asm", "RoomGBCOverlaysB", "RoomGBCOverlay", list(range(0x0CC, 0x100)) + ["006Alt", "00EAlt", "01BAlt", "02BAlt", "079Alt", "08CAlt"]),
    ]:
        f = open(os.path.join(basepath, filename), "wt")
        f.write(f"{start_label}::\n")
        for room_id in ids:
            if isinstance(room_id, str):
                f.write(f"{label_prefix}{room_id[1:]}::\n")
            else:
                f.write(f"{label_prefix}{room_id&0xFF:02X}::\n")
            f.write("  db " + ", ".join([f"${b:02X}" for b in data[str(room_id)]["tiles"]]) + "\n")
        f.close()

    # TODO: Also support full overworld tileset table, not the limited 2x2 blocks (requires asm patches)
    f = open(os.path.join(basepath, "src/data/rooms_gfx/overworld_tileset_table.asm"), "wt")
    f.write("OverworldTilesetsTable::\n")
    for y in range(8):
        row = []
        for x in range(8):
            tileset = data[str(x*2+y*32)]["tileset"]
            if data[str(x*2+y*32+1)]["tileset"] != tileset:
                print("Warning 2x2 overworld tileset mismatch")
            if data[str(x*2+y*32+16)]["tileset"] != tileset:
                print("Warning 2x2 overworld tileset mismatch")
            if data[str(x*2+y*32+17)]["tileset"] != tileset:
                print("Warning 2x2 overworld tileset mismatch")
            row.append(tileset)
        f.write("  db " + ", ".join([f"${b:02X}" for b in row]) + "\n")
    f.close()

    object_attributes_pointers = disasm.read_pointer_list(os.path.join(basepath, "src/data/object_attributes/pointers.asm"))
    f = open(os.path.join(basepath, "src/data/object_attributes/pointers.asm"), "wt")
    f.write("BGAttributesPointers_Overworld::\n")
    for n in range(0x000, 0x100):
        f.write(f"  dw {data[str(n)]["attribute_table"]}\n")
    f.write("BGAttributesPointers_IndoorsA::\n")
    for n in range(0x100, 0x200): # As these are weird per map, we copy the from the previous version of the file
        f.write(f"  dw {object_attributes_pointers[n]}\n")
    f.write("BGAttributesPointers_IndoorsB::\n")
    for n in range(0x200, 0x300): # As these are weird per map, we copy the from the previous version of the file
        f.write(f"  dw {object_attributes_pointers[n]}\n")
    f.close()

    palette_tables = disasm.read_palette_tables(os.path.join(basepath, "src/data/palettes/tables.asm"))
    for n in range(0x000, 0x100):
        palette_tables["OverworldPaletteMap"]["data"][n] = data[str(n)]["palette_index"]
    for n in range(0x100, 0x300):
        room = data[str(n)]
        if room["map_id"] < 0x0A:
            continue
        table_label = palette_tables["IndoorPaletteMaps"]["data"][room["map_id"] - 0x0A]
        palette_tables[table_label]["data"][n&0xFF] = room["palette_index"]
    f = open(os.path.join(basepath, "src/data/palettes/tables.asm"), "wt")
    for label, palette_table in palette_tables.items():
        f.write(f"{label}::\n")
        if len(palette_table["data"]) == 0x100:
            f.write("  db " + ", ".join([f"${b:02X}" for b in palette_table["data"]]) + "\n")
        else:
            f.write("  dw " + ", ".join([f"{s}" for s in palette_table["data"]]) + "\n")
    f.close()

    for filename, start_label, ids in [
        ("src/data/chests/overworld.asm", "RoomChestsTable", range(0x000, 0x100)),
        ("src/data/chests/indoors_a.asm", None, range(0x100, 0x200)),
        ("src/data/chests/indoors_b.asm", None, range(0x200, 0x300)),
        ("src/data/chests/color_dungeon.asm", "ColorDungeonRoomChestsTable", range(0x300, 0x320)),
    ]:
        f = open(os.path.join(basepath, filename), "wt")
        if start_label:
            f.write(f"{start_label}::\n")
        for room_id in ids:
            item = data[str(room_id)]["chestitem"] if str(room_id) in data else 0
            f.write(f"  db ${item:02X}\n")
        f.close()


def _export_spritesheet_tables(basepath, data) -> bool:
    overworld_table = []
    indoor_table = []
    index_table = [0] * 0x320
    result = True
    for idx in range(len(index_table)):
        if str(idx) not in data:
            continue
        room = data[str(idx)]
        entities = {e['id'] for e in room["entities"]}
        table = [None] * 4
        source = [None] * 4
        if idx < 0x100:
            table[0] = {0xA4}  # Overworld always loads bowwow in first slot, but can replace it with followers
            source[0] = 0x6D
        if room["chestitem"] == 0x22: # Zol chest
            entities.add(0x1B)
        for eid in entities:
            sprite_data = entityDatabase.SPRITE_DATA[eid]
            if callable(sprite_data):
                sprite_data = sprite_data(idx)
            if sprite_data is None:
                continue
            for n in range(0, len(sprite_data), 2):
                target_idx = sprite_data[n]
                graphics_sheets = sprite_data[n + 1]
                if isinstance(graphics_sheets, int):
                    graphics_sheets = {graphics_sheets}
                if table[target_idx] is None:
                    table[target_idx] = graphics_sheets
                    source[target_idx] = eid
                if not table[target_idx].intersection(graphics_sheets):
                    print(f"Failed to setup sprite graphics. Conflict in room {idx:03x}")
                    print(f"Conflict between {entityDatabase.NAME[source[target_idx]]} and {entityDatabase.NAME[eid]}")
                    result = False
                else:
                    table[target_idx] = table[target_idx].intersection(graphics_sheets)
        table = tuple(0xFF if gs is None else sorted(gs)[0] for gs in table)
        target_table = overworld_table if idx < 0x100 else indoor_table
        if table not in target_table:
            target_table.append(table)
            if len(target_table) >= 0xFF:
                print("Failed to setup sprite graphics tables, overflowed table size...")
                result = False
        index_table[idx] = target_table.index(table)
    if not result:
        return result
    f = open(os.path.join(basepath, "src/data/rooms_gfx/room_spritesheet_tables.asm"), "wt")
    f.write("; Automatically generated by KoholintLab\n")
    f.write("RoomSpritesheetGroupsTable::\n")
    for idx in range(len(index_table)):
        f.write("  db " if idx % 16 == 0 else ", ")
        f.write(f"${index_table[idx]:02X}")
        if idx % 16 == 15:
            f.write("\n")
    f.write("OverworldEntitySpritesheetsTable::\n")
    for row in overworld_table:
        f.write(f"  db ${row[0]:02X}, ${row[1]:02X}, ${row[2]:02X}, ${row[3]:02X}\n")
    f.write("IndoorEntitySpritesheetsTable::\n")
    for row in indoor_table:
        f.write(f"  db ${row[0]:02X}, ${row[1]:02X}, ${row[2]:02X}, ${row[3]:02X}\n")
    f.close()
    return result


def _encode_room_objects(room, all_rooms):
    tiles = room["tiles"].copy()
    is_overworld = room["num"] < 0x100
    if is_overworld:
        for n in range(80):
            # Cheat to generate smaller overworld rooms that only look correct on GBC
            if tiles[n] in {0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
                            0x33, 0x34, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
                            0x48, 0x49, 0x4B, 0x4C, 0x4E,
                            0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F}:
                tiles[n] = 0x3A  # Solid tiles
            if tiles[n] in {0x08, 0x09, 0x0C, 0x44,
                            0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF}:
                tiles[n] = 0x04  # Open tiles
        counts = {}
        for n in tiles:
            counts[n] = counts.get(n, 0) + 1
        floor_object = max(counts, key=counts.get) if len(counts) > 0 else 5
        template_tiles = [floor_object] * 80
    else:
        counts = {}
        for n in tiles:
            if n < 0x0F:
                counts[n] = counts.get(n, 0) + 1
        if counts:
            floor_object = max(counts, key=counts.get)
        else:
            floor_object = 0x0D

        template_scores = {}
        for template_index, template in enumerate(roomobjecteditor.INDOOR_ROOM_TEMPLATES):
            score = 0
            for idx, tile in enumerate(template.tiles):
                if tile is None:
                    tile = floor_object
                if tiles[idx] == tile:
                    score += 1
            template_scores[template_index] = score
        template_index = max(template_scores, key=template_scores.get)
        template_tiles = [floor_object] * 80
        for idx, tile in enumerate(roomobjecteditor.INDOOR_ROOM_TEMPLATES[template_index].tiles):
            if tile is not None:
                template_tiles[idx] = tile
        floor_object |= template_index << 4

    result = bytearray([room["animation"], floor_object])
    done = [tiles[n] == template_tiles[n] for n in range(80)]
    for y in range(8):
        for x in range(10):
            obj = tiles[x + y * 10]
            if done[x + y * 10]:
                continue
            # Figure out if we should do a horizontal or vertical strip.
            xmax = x
            for x1 in range(x + 1, 10):
                if done[x1 + y * 10]:
                    break
                if tiles[x1 + y * 10] == obj:
                    xmax = x1
            ymax = y
            for y1 in range(y + 1, 8):
                if done[x + y1 * 10]:
                    break
                if tiles[x + y1 * 10] == obj:
                    ymax = y1
            w = xmax - x + 1
            h = ymax - y + 1
            if is_overworld and obj in {0xE1, 0xE2, 0xE3, 0xBA}:
                w, h = 1, 1  # Do not encode entrances into strips
            if w > h:
                for n in range(w):
                    if tiles[x + n + y * 10] == obj:
                        done[x + n + y * 10] = True
                result += bytes([0x80 | w, x | (y << 4), obj])
            elif h > 1:
                for n in range(h):
                    if tiles[x + (y + n) * 10] == obj:
                        done[x + (y + n) * 10] = True
                result += bytes([0xC0 | h, x | (y << 4), obj])
            else:
                # Check if we might be able to place a macro (TODO: overworld macros)
                macro = None
                if not is_overworld:
                    for macro_id, macro_data in roomobjecteditor.INDOOR_MACROS.items():
                        if macro_data[0][2] == obj:
                            ok = True
                            for mx, my, mobj in macro_data:
                                if x + mx >= 10 or y + my >= 8 or tiles[x + mx + (y + my) * 10] != mobj:
                                    ok = False
                                    break
                            if ok:
                                macro = macro_id
                if macro:
                    result += bytes([x | (y << 4), macro])
                    for mx, my, mobj in roomobjecteditor.INDOOR_MACROS[macro]:
                        done[x + mx + (y + my) * 10] = True
                else:
                    done[x + y * 10] = True
                    result += bytes([x | (y << 4), obj])
    for warp in room["warpdata"]:
        target = all_rooms[str(warp["target"])]
        warp_type = 0 if warp["target"] < 0x100 else 1
        if target["sidescroll"]:
            warp_type =  2
        map_id = target["map_id"] if warp_type else 0
        result += bytes([0xE0 | warp_type, map_id, warp["target"] & 0xFF, warp["target_x"], warp["target_y"]])
    result.append(0xFE)
    return result
