import http.server
import urllib
import os
import PIL.Image
import PIL.ImageOps
import PIL.ImageDraw
import json
import binascii
import io
import threading
from . import entityDatabase
from . import disasm
from . import tileDatabase
from typing import Union


MAP_NAMES = {
    -1: "-1: Overworld",
    0: "0: D1", 1: "1: D2", 2: "2: D3", 3: "3: D4", 4: "4: D5", 5: "5: D6", 6: "6: D7", 7: "7: D8",
    8: "8: EGG",
    10: "10: CAVES_A",
    14: "14: SHOP",
    15: "15: MINIGAME",
    16: "16: HOUSE",
    17: "17: CAVES_B",
    18: "18: DOGHOUSE",
    19: "19: DREAM",
    20: "20: CASTLE",
    21: "21: MOBLIN_CAVE",
    22: "22: ARMOS_SHRINE",
    29: "29: LIBRARY",
    30: "30: GHOST_HOUSE",
    31: "31: CAVES_C",
    255: "255: COLOR_DUNGEON"
}
OVERWORLD_TILESET_FILES = {
    0x1A: "src/gfx/world/ow_camera_shop.cgb.png",
    0x1C: "src/gfx/world/ow_turtle_rock.cgb.png",
    0x1E: "src/gfx/world/ow_seashell_mansion.cgb.png",
    0x20: "src/gfx/world/ow_mysterious_woods.cgb.png",
    0x22: "src/gfx/world/ow_beach.cgb.png",
    0x24: "src/gfx/world/ow_prairie_stone_head.cgb.png",
    0x26: "src/gfx/world/ow_mabe_village.cgb.png",
    0x28: "src/gfx/world/ow_kanalet_castle.cgb.png",
    0x2A: "src/gfx/world/ow_face_shrine.cgb.png",
    0x2C: "src/gfx/world/ow_yarna_desert.cgb.png",
    0x2E: "src/gfx/world/ow_prairie_south.cgb.png",
    0x30: "src/gfx/world/ow_eagles_tower.cgb.png",
    0x32: "src/gfx/world/ow_rafting_game.cgb.png",
    0x34: "src/gfx/world/ow_anglers_tunnel.cgb.png",
    0x36: "src/gfx/world/ow_gopongo_swamp.cgb.png",
    0x38: "src/gfx/world/ow_graveyard.cgb.png",
    0x3A: "src/gfx/world/ow_marthas_bay.cgb.png",
    0x3C: "src/gfx/world/ow_egg.cgb.png",
    0x3E: "src/gfx/world/ow_taramanch_middle.cgb.png"
}
INDOOR_TILESET_FILES = {
    0x00: "src/gfx/indoor/tilesets/00.cgb.png",
    0x01: "src/gfx/indoor/tilesets/01.cgb.png",
    0x02: "src/gfx/indoor/tilesets/02.cgb.png",
    0x03: "src/gfx/indoor/tilesets/03.cgb.png",
    0x04: "src/gfx/indoor/tilesets/04.cgb.png",
    0x05: "src/gfx/indoor/tilesets/05.cgb.png",
    0x06: "src/gfx/indoor/tilesets/06.cgb.png",
    0x07: "src/gfx/indoor/tilesets/07.cgb.png",
    0x08: "src/gfx/indoor/tilesets/08.cgb.png",
    0x09: "src/gfx/indoor/tilesets/09.cgb.png",
    0x0A: "src/gfx/indoor/tilesets/0A.cgb.png",
    0x0B: "src/gfx/indoor/tilesets/0B.cgb.png",
    0x0C: "src/gfx/indoor/tilesets/0C.cgb.png",
    0x0D: "src/gfx/indoor/tilesets/0D.cgb.png",
    0x0E: "src/gfx/indoor/tilesets/0E.cgb.png",
    0x0F: "src/gfx/indoor/tilesets/0F.cgb.png",
    0x17: "src/gfx/indoor/tilesets/17.cgb.png",
    0x18: "src/gfx/indoor/tilesets/18.cgb.png",
    0x19: "src/gfx/indoor/tilesets/19.cgb.png",
    0x1A: "src/gfx/dungeons/floor/windfish_floor.cgb.png",
}
FLOOR_TILESET_FILES = {
    "HIGH(DungeonFloorATiles)": "src/gfx/dungeons/floor/floor_a.cgb.png",
    "HIGH(DungeonFloorBTiles)": "src/gfx/dungeons/floor/floor_b.cgb.png",
    "HIGH(DungeonFloorCTiles)": "src/gfx/dungeons/floor/floor_c.cgb.png",
    "HIGH(DungeonFloorDTiles)": "src/gfx/dungeons/floor/floor_d.cgb.png",
    "HIGH(DungeonFloorETiles)": "src/gfx/dungeons/floor/floor_e.cgb.png",
    "HIGH(DungeonFloorFTiles)": "src/gfx/dungeons/floor/floor_f.cgb.png",
    "HIGH(DungeonFloorGTiles)": "src/gfx/dungeons/floor/floor_g.cgb.png",
    "HIGH(DungeonFloorHTiles)": "src/gfx/dungeons/floor/floor_h.cgb.png",
    "HIGH(DungeonFloorITiles)": "src/gfx/dungeons/floor/floor_i.cgb.png",
    "HIGH(DungeonFloorJTiles)": "src/gfx/dungeons/floor/floor_j.cgb.png",
    "HIGH(DungeonFloorKTiles)": "src/gfx/dungeons/floor/floor_k.cgb.png",
    "HIGH(DungeonFloorLTiles)": "src/gfx/dungeons/floor/floor_l.cgb.png",
    "HIGH(WindfishFloorTiles)": "src/gfx/dungeons/floor/windfish_floor.cgb.png",
}
WALL_TILESET_FILES = {
    "HIGH(DungeonWallsATiles)": "src/gfx/dungeons/walls/walls_a.cgb.png",
    "HIGH(DungeonWallsBTiles)": "src/gfx/dungeons/walls/walls_b.cgb.png",
    "HIGH(DungeonWallsCTiles)": "src/gfx/dungeons/walls/walls_c.cgb.png",
    "HIGH(DungeonWallsDTiles)": "src/gfx/dungeons/walls/walls_d.cgb.png",
    "HIGH(DungeonWallsETiles)": "src/gfx/dungeons/walls/walls_e.cgb.png",
    "HIGH(DungeonWallsFTiles)": "src/gfx/dungeons/walls/walls_f.cgb.png",
}
ITEM_TILESET_FILES = {
    "HIGH(DungeonItemsATiles)": "src/gfx/items/dungeon_a.cgb.png",
    "HIGH(DungeonItemsBTiles)": "src/gfx/items/dungeon_b.cgb.png",
    "HIGH(DungeonItemsCTiles)": "src/gfx/items/dungeon_c.cgb.png",
    "HIGH(DungeonItemsDTiles)": "src/gfx/items/dungeon_d.cgb.png",
    "HIGH(HouseAItemsTiles)": "src/gfx/items/house_a.cgb.png",
    "HIGH(HouseBItemsTiles)": "src/gfx/items/house_b.cgb.png",
    "HIGH(HouseAItemsTiles)": "src/gfx/items/house_a.cgb.png",
    "HIGH(HouseAItemsTiles)": "src/gfx/items/house_a.cgb.png",
    "HIGH(Npc3Tiles + $2300)": "src/gfx/characters/oam_npc_3.cgb.png", # Only referenced by MAP_09_UNUSED
}

def draw_text(image, x, y, s):
    draw = PIL.ImageDraw.Draw(image)
    for xo in range(3):
        for yo in range(3):
            draw.text((x + 1 + xo, y + yo), s, (0, 0, 0))
    draw.text((x + 2, y + 1), s, (255, 255, 255))


class EditorServer(http.server.ThreadingHTTPServer):
    def __init__(self, disasm_path):
        self._disasm_path = disasm_path
        self.__tile_cache = {}
        self.__img_cache = {}
        self.__img_cache_lock = threading.Lock()
        self._palette_tables = disasm.read_palette_tables(os.path.join(disasm_path, "src/data/palettes/tables.asm"))
        self._palette_colors = disasm.read_palette_colors(os.path.join(disasm_path, "src/data/palettes/overworld.asm"))
        self._palette_colors.update(disasm.read_palette_colors(os.path.join(disasm_path, "src/data/palettes/dungeons.asm")))
        self._palette_colors.update(disasm.read_palette_colors(os.path.join(disasm_path, "src/data/palettes/interior.asm")))
        self._palette_colors.update(disasm.read_palette_colors(os.path.join(disasm_path, "src/data/palettes/default_sprites.asm")))
        self._overworld_metatiles = disasm.read_db_data(os.path.join(disasm_path, "src/data/objects_tilemaps/overworld.cgb.asm"))
        self._indoor_metatiles = disasm.read_db_data(os.path.join(disasm_path, "src/data/objects_tilemaps/indoor.cgb.asm"))
        self._colordungeon_metatiles = disasm.read_db_data(os.path.join(disasm_path, "src/data/objects_tilemaps/color_dungeon.asm"))
        self._floor_wall_tables = {d["label"]: d for d in disasm.read_db_data(os.path.join(disasm_path, "src/data/rooms_gfx/floor_wall_tables.asm"), with_labels=True, as_strings=True)}
        self._tile_attribs = {}
        self.tile_db = tileDatabase.TileDatabase()
        for filename in ["indoors_a.asm", "indoors_b.asm", "overworld_a.asm", "overworld_b.asm", "overworld_c.asm"]:
            for record in disasm.read_db_data(os.path.join(disasm_path, "src/data/object_attributes", filename), with_labels=True):
                if len(record["data"]) == 1024:
                    self._tile_attribs[record["label"]] = record["data"]
        print("Starting map edit server at http://127.0.0.1:8000/")
        super().__init__(("127.0.0.1", 8000), RequestHandler)

    def load_map_json(self, filename):
        self.storage_filename = filename
        self.room_data = {to_room_id(k): v for k, v in json.load(open(filename, "rt")).items()}

    def export_full_json(self, filename: str):
        json.dump(self.room_data, open(filename, "wt"), indent=2)

    def get_entities_info(self):
        result = []
        for e in entityDatabase.entities_list:
            result.append({"id": e["id"], "name": entityDatabase.NAME[e["id"]]})
        return result

    def get_maps(self):
        return [{"id": map_id, "name": MAP_NAMES.get(map_id, f"{map_id}")} for map_id in sorted(set(info["map_id"] for info in self.room_data.values()))]

    def get_map_info(self, map_id):
        rooms = []
        for room_id, info in self.room_data.items():
            if info['map_id'] == map_id:
                rooms.append(info)
        return rooms

    def get_room_info(self, room_id):
        return self.room_data[room_id]

    def _get_tileset(self, room_id):
        tileset = [None] * 0x100
        room = self.room_data[room_id]
        if room["num"] < 0x100:
            # Overworld tiles.
            if room["tileset"] != 0x0F:
                for n in range(0, 0x20):
                    tileset[n] = (OVERWORLD_TILESET_FILES[room["tileset"]], n)
            for n in range(0x20, 0x80):
                tileset[n] = ("src/gfx/world/overworld_landscape.cgb.png", n - 0x20)
            for n in range(0xF0, 0x100):
                tileset[n] = ("src/gfx/world/overworld_1.cgb.png", n - 0xF0)
        else:
            switch_blocks = 0xDB in room['tiles'] or 0xDC in room['tiles']
            for n in range(0x40, 0x80):
                tileset[n] = ("src/gfx/dungeons/doors.cgb.png", n - 0x40)

            if room["tileset"] != 0xFF:
                for n in range(0x00, 0x10):
                    tileset[n] = (INDOOR_TILESET_FILES[room["tileset"]], n)

            if room["sidescroll"]:
                if (room["map_id"] == 6 or room["map_id"] >= 0x0A) and room["num"] != 0x2E9:
                    for n in range(0x00, 0x80):
                        tileset[n] = ("src/gfx/dungeons/sideview_1.cgb.png", n)
                else:
                    for n in range(0x00, 0x80):
                        tileset[n] = ("src/gfx/dungeons/sideview_2.cgb.png", n)
            elif room["map_id"] == 0xFF:
                # TODO: Color dungeon is still bit messed up (It's always color dungeon..., might be related to data_020_45EA)
                for n in range(0x10, 0x20):
                    tileset[n] = ("src/gfx/dungeons/walls/walls_d.cgb.png", n - 0x10)
                for n in range(0x20, 0x40):
                    tileset[n] = ("src/gfx/dungeons/walls/walls_a.cgb.png", n - 0x20)
            else:
                for n in range(0x10, 0x20):
                    tileset[n] = (FLOOR_TILESET_FILES[self._floor_wall_tables["DungeonFloorTilesPointers"]["data"][room["map_id"]]], n - 0x10)
                for n in range(0x20, 0x40):
                    tileset[n] = (WALL_TILESET_FILES[self._floor_wall_tables["DungeonWallsTilesPointers"]["data"][room["map_id"]]], n - 0x20)
                for n in range(0x10):
                    tileset[0xF0 + n] = (ITEM_TILESET_FILES[self._floor_wall_tables["DungeonItemsTilesPointers"]["data"][room["map_id"]]], n) # TODO: This should depend on map, see DungeonItemsTilesPointers
            
            # # Camera shop override (still looks wrong)
            # if self.map_id == 0x10 and self.room_nr == 0x2B5:
            #     for n in range(0x20):
            #         subtiles[(0xF0 + n) & 0xFF] = (0x35, 0x2600 + n * 0x10)
            if switch_blocks:
                for n in range(4):
                    tileset[4 + n] = ("src/gfx/items/switch_block.cgb.png", n)
                    tileset[8 + n] = ("src/gfx/items/switch_block.cgb.png", n + 4)

        if room["animation"] is not None and room["animation"] >= 2:
            offset = (0, 0, 1, 2, 3, 4, 5, 3, 6, 7, 8, 0, 9, 11, 12, 10, 13)[room["animation"]] * 16
            for n in range(0x6C, 0x70):
                tileset[n] = ("src/gfx/world/animated_tiles.w32.cgb.png", n - 0x6C + offset)
            if room["animation"] == 0x07:
                for n in range(4): # Conveyer tiles
                    tileset[0x0C + n] = ("src/gfx/items/items_1.cgb.png", 60 + n)
        return tileset

    def draw_tile(self, img, ox, oy, subtile_id, attr, palette, *, sprite=False):
        if subtile_id is None:
            return
        if (subtile_id, attr, palette) not in self.__tile_cache:
            with self.__img_cache_lock: # Pillow does not like multi-threaded access to the same image files.
                filename = os.path.join(self._disasm_path, subtile_id[0])
                if filename not in self.__img_cache:
                    self.__img_cache[filename] = PIL.Image.open(filename)
                    self.__img_cache[filename].load()
                source = self.__img_cache[filename]
                w = (source.size[0] // 8)
                x = subtile_id[1] % w
                y = subtile_id[1] // w
                tile = source.crop((x*8, y*8, x*8+8, y*8+8)).convert("RGBA").convert("P", colors=4)
                if attr & 0x20:
                    tile = PIL.ImageOps.mirror(tile)
                if attr & 0x40:
                    tile = PIL.ImageOps.flip(tile)
                assert tile.size == (8, 8)
                target_palette = self._palette_colors[palette]["data"][(attr&7)*4:(attr&7)*4+4]
                current_palette = tile.getpalette()
                if len(target_palette) == 4:
                    for n in range(len(current_palette) // 3):
                        if sprite:
                            if current_palette[n*3] == 0:
                                current_palette[n*3:n*3+3] = target_palette[3]
                                if "transparency" not in tile.info:
                                    tile.info["transparency"] = n
                            elif current_palette[n*3] == 255:
                                current_palette[n*3:n*3+3] = target_palette[0]
                            elif current_palette[n*3] < 128:
                                current_palette[n*3:n*3+3] = target_palette[1]
                            else:
                                current_palette[n*3:n*3+3] = target_palette[2]
                        else:
                            if current_palette[n*3] == 0:
                                current_palette[n*3:n*3+3] = target_palette[3]
                            elif current_palette[n*3] == 255:
                                current_palette[n*3:n*3+3] = target_palette[0]
                            elif current_palette[n*3] < 128:
                                current_palette[n*3:n*3+3] = target_palette[2]
                            else:
                                current_palette[n*3:n*3+3] = target_palette[1]
                tile.putpalette(current_palette)

                self.__tile_cache[(subtile_id, attr, palette)] = tile.convert("RGBA")
        tile = self.__tile_cache[(subtile_id, attr, palette)]
        img.paste(tile, (ox, oy), tile)

    def _get_room_render_info(self, room_id):
        room = self.room_data[room_id]

        if room["map_id"] == -1:
            metatiles = self._overworld_metatiles
            palette = self._palette_tables["OverworldPalettes"]["data"][room["palette_index"]]
        elif room["map_id"] == 255:
            metatiles = self._colordungeon_metatiles
            palette = "ColorDungeonPalette"
        else:
            metatiles = self._indoor_metatiles
            if room["map_id"] < 9: # Dungeons have fixed palettes
                if room["sidescroll"]:
                    palette = self._palette_tables["DungeonPalettesB"]["data"][room["map_id"]]
                else:
                    palette = self._palette_tables["DungeonPalettesA"]["data"][room["map_id"]]
            else:
                palette = self._palette_tables["InteriorPalettes"]["data"][room["palette_index"]]
        attributes = self._tile_attribs[room["attribute_table"]]
        tileset = self._get_tileset(room_id)
        return metatiles, attributes, palette, tileset

    def render_room(self, room_id):
        room = self.room_data[room_id]
        metatiles, attributes, palette, tileset = self._get_room_render_info(room_id)

        result = PIL.Image.new('RGBA', (8 * 20, 8 * 16))
        for y in range(8):
            for x in range(10):
                tile_nr = room['tiles'][x + y * 10]
                metatile = metatiles[tile_nr * 4:tile_nr * 4 + 4]
                attrtile = attributes[tile_nr * 4:tile_nr * 4 + 4]
                self.draw_tile(result, x * 16, y * 16, tileset[metatile[0]], attrtile[0], palette)
                self.draw_tile(result, x * 16 + 8, y * 16, tileset[metatile[1]], attrtile[1], palette)
                self.draw_tile(result, x * 16, y * 16 + 8, tileset[metatile[2]], attrtile[2], palette)
                self.draw_tile(result, x * 16 + 8, y * 16 + 8, tileset[metatile[3]], attrtile[3], palette)
                tile_info = self.tile_db.get(tile_nr, room["num"], room["sidescroll"])
                if tile_info and tile_info.bombable:
                    draw_text(result, x * 16, y * 16, "B")
        for e in room["entities"]:
            self.render_entity(e["id"], result, e["x"] * 16, e["y"] * 16, room_id=room_id)
        return result

    def render_tileset(self, room_id):
        room = self.room_data[room_id]
        metatiles, attributes, palette, tileset = self._get_room_render_info(room_id)

        result = PIL.Image.new('RGBA', (16 * 16, 17 * 16))
        x = 0
        y = 0
        for tile_info in self.tile_db.get_list(room["num"], room["sidescroll"]):
            tile_nr = tile_info.id
            if tile_info.main_tileset and room["tileset"] not in tile_info.main_tileset:
                continue
            if tile_info.animation and room["animation"] not in tile_info.animation:
                continue
            metatile = metatiles[tile_nr * 4:tile_nr * 4 + 4]
            attrtile = attributes[tile_nr * 4:tile_nr * 4 + 4]
            if metatile:
                self.draw_tile(result, x * 16, y * 16, tileset[metatile[0]], attrtile[0], palette)
                self.draw_tile(result, x * 16 + 8, y * 16, tileset[metatile[1]], attrtile[1], palette)
                self.draw_tile(result, x * 16, y * 16 + 8, tileset[metatile[2]], attrtile[2], palette)
                self.draw_tile(result, x * 16 + 8, y * 16 + 8, tileset[metatile[3]], attrtile[3], palette)
            if tile_info.bombable:
                draw_text(result, x * 16, y * 16, "B")
            x += 1
            if x == 16:
                x = 0
                y += 1

        draw = PIL.ImageDraw.Draw(result)
        for idx, pal in enumerate(self._palette_colors[palette]["data"]):
            x = idx%32
            y = idx//32*8+256
            draw.rectangle((x*8, y, x*8+7, y+7), pal)
        return result

    def get_tileset_info(self, room_id):
        room = self.room_data[room_id]
        metatiles, attributes, palette, tileset = self._get_room_render_info(room_id)
        result = []
        for tile_info in self.tile_db.get_list(room["num"], room["sidescroll"]):
            if tile_info.main_tileset and room["tileset"] not in tile_info.main_tileset:
                continue
            if tile_info.animation and room["animation"] not in tile_info.animation:
                continue
            result.append({"id": tile_info.id, "attr":  binascii.hexlify(bytes(attributes[tile_info.id*4:tile_info.id*4+4])).decode("ascii")})
            if tile_info.bombable:
                result[-1]['bombable'] = True
        return result

    def update_tile_attr(self, room_id, tile_id, attr):
        print(f"Not implemented yet: update_tile_attr {room_id} {tile_id} {attr}")

    def render_entities(self, *, room_id=0x2B6):
        result = PIL.Image.new('RGBA', (16 * 16, 16 * 16), 0)
        x = 0
        y = 0
        for info in entityDatabase.entities_list:
            self.render_entity(info["id"], result, x * 16, y * 16, room_id=room_id)
            x += 1
            if x == 16:
                x = 0
                y += 1
        return result

    def render_entity(self, eid, target, x, y, *, room_id=0x2B6):
        info = entityDatabase.entities_dict[eid]
        sd = entityDatabase.SPRITE_DATA[info["id"]] if info["id"] in entityDatabase.SPRITE_DATA else None
        if callable(sd):
            sd = sd(room_id)
        if sd is None:
            sd = (1, 0x91)

        tileset = []
        for gfx_idx in range(1, len(sd), 2):
            gfx_nr = sd[gfx_idx]
            if isinstance(gfx_nr, set):
                gfx_nr = list(sorted(gfx_nr))[0]
            filename = ["src/gfx/characters/oam_color_dungeon.png", "src/gfx/characters/oam_npc_2.cgb.png", "src/gfx/characters/oam_npc_1.cgb.png", "src/gfx/characters/oam_npc_3.cgb.png"][gfx_nr >> 6]
            index = (gfx_nr & 0x3F)
            for n in range(0, 8):
                tx = (index*8+n) % 8
                ty = (index*8+n) // 8
                tileset.append((filename, tx + ty * 16))
        if "tiles" in info:
            for n in range(len(info["tiles"])):
                if isinstance(info["tiles"][n], tuple) or info["tiles"][n] >= 0:
                    a = tileset[info["tiles"][n]] if isinstance(info["tiles"][n], int) else info["tiles"][n]
                    if isinstance(a[0], int):
                        continue
                    b = (a[0], a[1] + 8)
                    if info["attr"][n] & 0x100:
                        b = (a[0], a[1] + 1)
                    if info["attr"][n] & 0x40:
                        a, b = b, a
                    if len(info["tiles"]) & 1:
                        self.draw_tile(target, x + 4, y, a, info["attr"][n], "ObjectPalettes", sprite=True)
                        self.draw_tile(target, x + 4, y + 8, b, info["attr"][n], "ObjectPalettes", sprite=True)
                    else:
                        self.draw_tile(target, x + (n % 2 * 8), y, a, info["attr"][n], "ObjectPalettes", sprite=True)
                        self.draw_tile(target, x + (n % 2 * 8), y + 8, b, info["attr"][n], "ObjectPalettes", sprite=True)
        else:
            draw_text(target, x, y, f"{eid:02X}")
            # for n, tile in enumerate(tileset):
            #     x = idx * 16 + (n // 32) * 8
            #     y = (n % 32) * 8
            #     self.drawSubtile(result, x, y, tile, 0, "ObjectPalettes")


def to_room_id(room_id: str) -> Union[int, str]:
    try:
        return int(room_id)
    except ValueError:
        return room_id


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), "www"), **kwargs)

    def do_GET(self):
        parts = urllib.parse.urlsplit(self.path)
        if parts.path == "/render_room":
            self.send_reply(self.server.render_room(to_room_id(parts.query)).convert("RGBA").tobytes())
        elif parts.path == "/render_tileset":
            self.send_reply(self.server.render_tileset(to_room_id(parts.query)).convert("RGBA").tobytes())
        elif parts.path == "/render_entities":
            self.send_reply(self.server.render_entities(room_id=to_room_id(parts.query)).convert("RGBA").tobytes())
        # elif parts.path == "/unknown_tiles":
        #     self.send_reply(self.server.render_unknown_tiles())
        elif parts.path == "/maps":
            self.send_reply(self.server.get_maps())
        elif parts.path == "/map_info":
            self.send_reply(self.server.get_map_info(int(parts.query)))
        elif parts.path == "/room_info":
            self.send_reply(self.server.get_room_info(to_room_id(parts.query)))
        elif parts.path == "/get_tileset_info":
            self.send_reply(self.server.get_tileset_info(to_room_id(parts.query)))
        elif parts.path == "/get_entities_info":
            self.send_reply(self.server.get_entities_info())
        elif parts.path == "/room_copy":
            query = urllib.parse.parse_qs(parts.query)
            source = to_room_id(query["source"][0])
            target = to_room_id(query["target"][0])
            self.server.room_data[target]['tiles'] = self.server.room_data[source]['tiles'][:]
            self.server.room_data[target]['entities'] = self.server.room_data[source]['entities'][:]
            self.send_reply(b"COPIED")
        elif parts.path == "/update_room_tile":
            query = urllib.parse.parse_qs(parts.query)
            room_id = to_room_id(query['room'][0])
            x, y = int(query["x"][0]), int(query["y"][0])
            self.server.room_data[room_id]['tiles'][x+y*10] = int(query["tile"][0])
            self.send_reply(self.server.render_room(room_id).convert("RGBA").tobytes())
        elif parts.path == "/update_tile_attr":
            query = urllib.parse.parse_qs(parts.query)
            room_id = to_room_id(query['room'][0])
            tile_id = int(query["tile"][0])
            attr = binascii.unhexlify(query["attr"][0])
            self.server.update_tile_attr(room_id, tile_id, attr)
            self.send_reply(self.server.render_room(room_id).convert("RGBA").tobytes())
        elif parts.path == "/move_room":
            query = urllib.parse.parse_qs(parts.query)
            room_id = to_room_id(query['room'][0])
            x, y = int(query["x"][0]), int(query["y"][0])
            self.send_reply(self.server.move_room(room_id, x, y))
        elif parts.path == "/save":
            self.server.export_full_json(self.server.storage_filename)
            print("Saved")
            self.send_reply(b"SAVED")
        elif parts.path == "/update_room_entity":
            query = urllib.parse.parse_qs(parts.query)
            room_id = to_room_id(query['room'][0])
            x, y = int(query["x"][0]), int(query["y"][0])
            entity = int(query["entity"][0])
            room = self.server.room_data[room_id]
            found = False
            for idx, e in enumerate(room["entities"]):
                if e["x"] == x and e["y"] == y:
                    room["entities"].pop(idx)
                    found = True
            if not found:
                room["entities"].append({"x": x, "y": y, "id": entity})
            self.send_reply(self.server.render_room(room_id).convert("RGBA").tobytes())
        elif parts.path == "/update_room_data":
            query = urllib.parse.parse_qs(parts.query)
            room_id = to_room_id(query['room'][0])
            key = query['key'][0]
            value = query['value'][0]
            try:
                value = int(value)
            except ValueError:
                pass
            if key == "warpdata":
                value = json.loads(value)
            self.server.room_data[room_id][key] = value
            self.send_reply(self.server.render_room(room_id).convert("RGBA").tobytes())
        else:
            super().do_GET()

    def send_reply(self, data: Union[PIL.Image.Image, bytes, list, dict]):
        if isinstance(data, PIL.Image.Image):
            buffer = io.BytesIO()
            data.save(buffer, "png")
            data = buffer.getvalue()
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data).encode("ascii")
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # def log_message(self, fmt, *args):
    #     pass
