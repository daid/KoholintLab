from typing import Optional


class TileInfo:
    def __init__(self, tid, *, main_tileset=None, animation=None, bombable=False):
        self.id = tid
        self.main_tileset = main_tileset
        self.animation = animation
        self.bombable = bombable


class TileDatabase:
    def __init__(self):
        self.__overworld_list = [
            TileInfo(0x00),
            TileInfo(0x1C),
            TileInfo(0x09),
            TileInfo(0x03),
            TileInfo(0x0B),

            TileInfo(0x04),
            TileInfo(0x44, animation={0x03, 0x10}), # Flowers
            TileInfo(0xF5),  # DX-Grass
            TileInfo(0xF6),  # DX-Grass
            TileInfo(0xF7),  # DX-Grass
            TileInfo(0xF8),  # DX-Grass
            TileInfo(0xF9),  # DX-Grass
            TileInfo(0xFA),  # DX-Grass
            TileInfo(0xFB),  # DX-Grass
            TileInfo(0xFC),  # DX-Grass
            TileInfo(0xFD),  # DX-Grass
            TileInfo(0xFE),  # DX-Grass
            TileInfo(0xFF),  # DX-Grass

            TileInfo(0xE5),
            TileInfo(0x0A),
            TileInfo(0x38),
            TileInfo(0x37),
            TileInfo(0x4D),
            TileInfo(0x2E),
            TileInfo(0x48),
            TileInfo(0xE0),
            TileInfo(0x49),
            TileInfo(0x4E),
            TileInfo(0x39),
            TileInfo(0x3A),
            TileInfo(0x3B),
            TileInfo(0x50),
            TileInfo(0x2F),
            TileInfo(0x33),
            TileInfo(0x34),
            TileInfo(0x4B),
            TileInfo(0x4C),
            TileInfo(0x3D),
            TileInfo(0x3C),
            TileInfo(0x3E),
            TileInfo(0x3F),
            TileInfo(0xDE),
            TileInfo(0x2C),
            TileInfo(0x2D),
            TileInfo(0xDD),
            TileInfo(0x2B),
            TileInfo(0x32),
            TileInfo(0x36),
            TileInfo(0x35),
            TileInfo(0x47),
            TileInfo(0x31),
            TileInfo(0xF2),
            TileInfo(0xEA),
            TileInfo(0xF4),
            TileInfo(0xF1),
            TileInfo(0x46),
            TileInfo(0xD8),
            TileInfo(0xDA),

            TileInfo(0x4A),  # Half Ledge
            TileInfo(0xF3),  # Half Ledge
            TileInfo(0xF0),  # Half Ledge
            TileInfo(0x43),  # Half Ledge with path

            TileInfo(0x25),  # Tree
            TileInfo(0x26),  # Tree
            TileInfo(0x27),  # Tree
            TileInfo(0x28),  # Tree
            TileInfo(0x29),  # Tree
            TileInfo(0x2A),  # Tree
            TileInfo(0x6E),

            TileInfo(0xA0),
            TileInfo(0xE1),
            TileInfo(0xE2),
            TileInfo(0xC6),
            TileInfo(0xBA),
            TileInfo(0x52),
            TileInfo(0x5B),

            TileInfo(0x45),  # Telephone
            TileInfo(0xD4),  # Sign
            TileInfo(0x6F),  # Owl
            TileInfo(0x20),  # Rock
            TileInfo(0xE8),  # Pit
            TileInfo(0x5C),  # Bush
            TileInfo(0xD3),  # Bush with pit/stairs

            TileInfo(0x62, main_tileset={0x26, 0x1A, 0x24, 0x2E}),  # Fence/Dungeon bars
            TileInfo(0xE6, main_tileset={0x26}),  # Single fence post
            TileInfo(0x5F, main_tileset={0x26}),  # Wall/dream hut
            TileInfo(0x55, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x56, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x40, main_tileset={0x26, 0x1A}),  # Shop/Camera-House
            TileInfo(0x42, main_tileset={0x26, 0x1A}),  # Shop/Camera-House
            TileInfo(0x60, main_tileset={0x26, 0x1A}),  # Stone wall/Photo-house
            TileInfo(0x61, main_tileset={0x26, 0x1A}),  # Well/Photo-house
            TileInfo(0x5A, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x57, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x59, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x58, main_tileset={0x26, 0x1A}),  # House
            TileInfo(0x41, main_tileset={0x26}),  # Shop-House

            TileInfo(0x1B, animation={0x03, 0x0B}),  # Shallow water
            TileInfo(0x0E, animation={0x03, 0x0E, 0x0A, 0x0B}),  # Deep water
            TileInfo(0xE9, animation={0x0A, 0x0B}),  # Waterfall
            TileInfo(0xCA, main_tileset={0x3A, 0x3E}),

            TileInfo(0x21, main_tileset={0x32}),  # Rapids tree
            TileInfo(0x4F, main_tileset={0x32}),  # Rapids tree

            TileInfo(0xED, animation={0x0A, 0x09}),  # Rapids
            TileInfo(0xEB, animation={0x0A, 0x09}),  # Rapids
            TileInfo(0xEC, animation={0x09}),  # Rapids
            TileInfo(0xEE, animation={0x09}),  # Rapids

            TileInfo(0x53, main_tileset={0x3E}),  # Waterfall "cave"

            TileInfo(0xCD, main_tileset={0x1C, 0x38, 0x2C, 0x22, 0x1E, 0x32, 0x34}),  # D8 back entrance/Dead tree/Desert skull/Beach tree/seashell tree/rapids tree/D4
            TileInfo(0xD7, main_tileset={0x1C, 0x36, 0x34}),  # D8 back entrance/D2 entrance/D4
            TileInfo(0xC8, main_tileset={0x1C, 0x3E, 0x3C, 0x38, 0x22, 0x2C, 0x32}),  # Mountain rock/Above witch entrance/beach nut/desert bones/rapids roots

            TileInfo(0x7A, main_tileset={0x1C, 0x3E, 0x3C}),  # Bridge
            TileInfo(0x7B, main_tileset={0x1C, 0x3E}),  # Bridge
            TileInfo(0x78, main_tileset={0x1C, 0x3E}),  # Bridge
            TileInfo(0x79, main_tileset={0x1C, 0x3E}),  # Bridge
            TileInfo(0x7C, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Cloud
            TileInfo(0x7D, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Cloud
            TileInfo(0x7E, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Cloud
            TileInfo(0x80, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Mountain top left
            TileInfo(0x81, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Mountain top right
            TileInfo(0x1D, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Mountain top left
            TileInfo(0x5D, main_tileset={0x1C, 0x3E, 0x3C, 0x30}),  # Mountain top right
            TileInfo(0xEF, animation={0x0B}),  # Horizon animation

            TileInfo(0x82, main_tileset={0x20}),  # Forest
            TileInfo(0x83, main_tileset={0x20}),  # Forest
            TileInfo(0x8E, main_tileset={0x20}),  # Forest
            TileInfo(0x8F, main_tileset={0x20}),  # Forest
            TileInfo(0x87, main_tileset={0x20}),  # Forest
            TileInfo(0x08, main_tileset={0x20, 0x22, 0x2C, 0x38}),  # Forest/Beach/Desert floor/Plant
            TileInfo(0x8D, main_tileset={0x20}),  # Forest
            TileInfo(0x84, main_tileset={0x20}),  # Forest
            TileInfo(0x89, main_tileset={0x20}),  # Forest
            TileInfo(0x90, main_tileset={0x20}),  # Forest
            TileInfo(0x8A, main_tileset={0x20}),  # Forest
            TileInfo(0x85, main_tileset={0x20}),  # Forest
            TileInfo(0x88, main_tileset={0x20}),  # Forest
            TileInfo(0x8C, main_tileset={0x20}),  # Forest
            TileInfo(0x86, main_tileset={0x20}),  # Forest
            TileInfo(0x8B, main_tileset={0x20}),  # Forest
            TileInfo(0x92, main_tileset={0x20}),  # Forest
            TileInfo(0xE4, main_tileset={0x20}),  # Forest
            TileInfo(0xE3, main_tileset={0x20, 0x3A, 0x2A, 0x28}),  # Forest/Catfish/Armos/castle entrance

            TileInfo(0xCE, main_tileset={0x38, 0x2C, 0x32, 0x22, 0x1E, 0x34}),  # Dead tree/desert skull/rapids tree/Beach tree/seashell tree/D4
            TileInfo(0xC4, main_tileset={0x38}),  # Gravestone
            TileInfo(0xC5, main_tileset={0x38}),  # Gravestone (pushable)

            TileInfo(0x30, main_tileset={0x36}),  # Swamp
            TileInfo(0x51, main_tileset={0x36, 0x3A, 0x38}),  # Swamp roots/Stone in water/graveyard fence
            TileInfo(0x11, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x13, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x17, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x15, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x12, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x18, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x14, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x19, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x10, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x1A, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x16, main_tileset={0x36, 0x2E}),  # Swamp
            TileInfo(0x0F, main_tileset={0x36, 0x2E}),  # Swamp

            TileInfo(0x72, main_tileset={0x30}),  # D7
            TileInfo(0x73, main_tileset={0x30}),  # D7
            TileInfo(0x74, main_tileset={0x30}),  # D7
            TileInfo(0x75, main_tileset={0x30}),  # D7
            TileInfo(0xD6, main_tileset={0x30, 0x34}),  # D7/D4
            TileInfo(0xD5, main_tileset={0x34}),  # D4
            TileInfo(0x76, main_tileset={0x30}),  # D7
            TileInfo(0x77, main_tileset={0x30}),  # D7
            TileInfo(0x54, main_tileset={0x30, 0x34}),  # D7/D4 keyhole
            TileInfo(0xB6, main_tileset={0x30, 0x38, 0x2C, 0x22, 0x3A, 0x24, 0x2E, 0x2A, 0x1E, 0x28, 0x1C, 0x36, 0x34, 0x32, 0x3E}),  # D7/Dead tree/desert tree/beach tree/catfish maw/tail statue/slime statue/armos pillar/seashell tree/castle/D7 hut/D2 entrance/mambo sign/rapid tree/raft house
            TileInfo(0xB7, main_tileset={0x30, 0x38, 0x2C, 0x22, 0x3A, 0x24, 0x2E, 0x2A, 0x1E, 0x28, 0x1C, 0x36, 0x34, 0x32, 0x3E}),  # D7/Dead tree/desert tree/beach tree/catfish maw/tail statue/slime statue/armos pillar/seashell tree/castle/D7 hut/D2 entrance/mambo sign/rapid tree/raft house

            TileInfo(0x05, main_tileset={0x3C}),  # EGG
            TileInfo(0x06, main_tileset={0x3C}),  # EGG
            TileInfo(0x07, main_tileset={0x3C}),  # EGG
            TileInfo(0x63, main_tileset={0x3C}),  # EGG
            TileInfo(0x64, main_tileset={0x3C}),  # EGG
            TileInfo(0x65, main_tileset={0x3C}),  # EGG
            TileInfo(0x71, main_tileset={0x3C}),  # EGG
            TileInfo(0x7F, main_tileset={0x3C}),  # EGG
            TileInfo(0xA9, main_tileset={0x3C}),  # EGG
            TileInfo(0xAA, main_tileset={0x3C}),  # EGG
            TileInfo(0xBF, main_tileset={0x3C}),  # EGG
            TileInfo(0xC1, main_tileset={0x3C}),  # EGG
            TileInfo(0xCB, main_tileset={0x3C}),  # EGG

            TileInfo(0xCF, animation={0x08}),  # Quicksand
            TileInfo(0xD0, animation={0x08}),  # Quicksand
            TileInfo(0xD1, animation={0x08}),  # Quicksand
            TileInfo(0xD2, animation={0x08}),  # Quicksand

            TileInfo(0x1E, animation={0x02}),  # Beach
            TileInfo(0x1F, animation={0x02}),  # Beach
            TileInfo(0x23, main_tileset={0x22}),  # Beach
            TileInfo(0x24, main_tileset={0x22}),  # Beach

            TileInfo(0x9B, main_tileset={0x28}),  # Castle
            TileInfo(0x99, main_tileset={0x28}),  # Castle
            TileInfo(0x96, main_tileset={0x28}),  # Castle
            TileInfo(0x93, main_tileset={0x28}),  # Castle
            TileInfo(0x9A, main_tileset={0x28}),  # Castle
            TileInfo(0x9E, main_tileset={0x28}),  # Castle
            TileInfo(0x98, main_tileset={0x28}),  # Castle
            TileInfo(0x95, main_tileset={0x28}),  # Castle
            TileInfo(0x9C, main_tileset={0x28}),  # Castle
            TileInfo(0x9D, main_tileset={0x28}),  # Castle
            TileInfo(0x97, main_tileset={0x28}),  # Castle
            TileInfo(0x94, main_tileset={0x28}),  # Castle
            TileInfo(0x0C, main_tileset={0x28, 0x24, 0x1A, 0x26}),  # Castle roof/stone path
            TileInfo(0x0D, main_tileset={0x28, 0x26}),  # Castle flooring/town flooring
            TileInfo(0xA4, main_tileset={0x28}),  # Castle
            TileInfo(0xA5, main_tileset={0x28}),  # Castle
            TileInfo(0xA6, main_tileset={0x28}),  # Castle
            TileInfo(0xA7, main_tileset={0x28}),  # Castle
            TileInfo(0xA8, main_tileset={0x28}),  # Castle
            TileInfo(0xA2, main_tileset={0x28}),  # Castle
            TileInfo(0xAB, main_tileset={0x28}),  # Castle
            TileInfo(0xAC, main_tileset={0x28}),  # Castle
            TileInfo(0x9F, main_tileset={0x28}),  # Castle
            TileInfo(0xA3, main_tileset={0x28}),  # Castle

            TileInfo(0x91, main_tileset={0x26}, animation={0x10}),  # Wind indicator
            TileInfo(0x5E, main_tileset={0x26}),  # Wind indicator

            TileInfo(0xBB, main_tileset={0x24}),  # Big skull
            TileInfo(0xBC, main_tileset={0x24}),  # Big skull
            TileInfo(0xBD, main_tileset={0x24}),  # Big skull
            TileInfo(0xBE, main_tileset={0x24}),  # Big skull

            TileInfo(0xB9, main_tileset={0x2A}),  # Armos
            TileInfo(0xB3, main_tileset={0x2A}),  # Armos
            TileInfo(0xB8, main_tileset={0x2A}),  # Armos
            TileInfo(0x70, main_tileset={0x2A}),  # Armos
            TileInfo(0xAD, main_tileset={0x2A}),  # Armos
            TileInfo(0xAF, main_tileset={0x2A}),  # Armos
            TileInfo(0xB1, main_tileset={0x2A}),  # Armos
            TileInfo(0xE7, main_tileset={0x2A}),  # Armos
            TileInfo(0xAE, main_tileset={0x2A}),  # Armos
            TileInfo(0xB0, main_tileset={0x2A}),  # Armos
            TileInfo(0xB2, main_tileset={0x2A}),  # Armos

            TileInfo(0x6A, main_tileset={0x2E}),  # D3
            TileInfo(0x6B, main_tileset={0x2E}),  # D3
            TileInfo(0x6C, main_tileset={0x2E}),  # D3
            TileInfo(0xC2, main_tileset={0x24, 0x2E}),  # D1/D3 entrance tile
            TileInfo(0xC0, main_tileset={0x24, 0x2E}),  # D1/D3 key tile

            TileInfo(0xC3, main_tileset={0x1E}),  # Seashell house

            TileInfo(0x66, main_tileset={0x3E, 0x3A}),  # Raft house/Catfish maw
            TileInfo(0x69, main_tileset={0x2C}),  # Desert cactus
            TileInfo(0x67, main_tileset={0x3A}),  # Catfish maw
            TileInfo(0x68, main_tileset={0x3A}),  # Catfish maw
            TileInfo(0xDB, main_tileset={0x3A}),  # Vertical bridge
        ]
        self.__overworld_dict = {ti.id: ti for ti in self.__overworld_list}
        self.__underworld_list = [
            TileInfo(0x00),  # Upper layer
            TileInfo(0x03),  # Upper layer
            TileInfo(0x05),  # Floor
            TileInfo(0x0D),  # Floor
            TileInfo(0x0F),  # Floor
            TileInfo(0x8B),  # Floor
            TileInfo(0x07),  # Floor-checkerboard
            TileInfo(0xDF),  # Floor-cracked
            TileInfo(0xDA),  # Floor flying tile
            TileInfo(0x8D, main_tileset={0x09}),  # D4 puzzle floor tile
            TileInfo(0x97),  # Stairs
            TileInfo(0x98),  # Stairs2
            TileInfo(0xC0),  # Statue

            TileInfo(0x23),  # Wall
            TileInfo(0x24),  # Wall
            TileInfo(0x25),  # Wall
            TileInfo(0x21),  # Wall
            TileInfo(0x29),  # Wall
            TileInfo(0x2A),  # Wall
            TileInfo(0x2B),  # Wall
            TileInfo(0x2C),  # Wall
            TileInfo(0x26),  # Wall
            TileInfo(0x27),  # Wall
            TileInfo(0x22),  # Wall
            TileInfo(0x28),  # Wall
            TileInfo(0xC7, animation={0x04, 0x07, 0x0C}),  # Walltorches
            TileInfo(0xC8, animation={0x04, 0x07, 0x0C}),  # Walltorches
            TileInfo(0xC9, animation={0x04, 0x07, 0x0C}),  # Walltorches
            TileInfo(0xCA, animation={0x04, 0x07, 0x0C}),  # Walltorches
            TileInfo(0xAB, animation={0x04, 0x06, 0x07}),  # Unlit fire pit
            TileInfo(0xAC, animation={0x04, 0x06, 0x07}),  # Lit fire pit

            TileInfo(0x3F),  # Wall-cracked
            TileInfo(0x40),  # Wall-cracked
            TileInfo(0x41),  # Wall-cracked
            TileInfo(0x42),  # Wall-cracked

            TileInfo(0x47, bombable=True),  # Wall-bomb-hidden
            TileInfo(0x48, bombable=True),  # Wall-bomb-hidden
            TileInfo(0x49, bombable=True),  # Wall-bomb-hidden
            TileInfo(0x4A, bombable=True),  # Wall-bomb-hidden

            TileInfo(0x3D),  # Wall-destroyed
            TileInfo(0x3E),  # Wall-destroyed

            TileInfo(0x35),  # Door (closed)
            TileInfo(0x36),  # Door (closed)
            TileInfo(0x37),  # Door (closed)
            TileInfo(0x38),  # Door (closed)
            TileInfo(0x39),  # Door (closed)
            TileInfo(0x3A),  # Door (closed)
            TileInfo(0x3B),  # Door (closed)
            TileInfo(0x3C),  # Door (closed)
            TileInfo(0x8C),  # Door (open)
            TileInfo(0x08),  # Door (open)
            TileInfo(0x09),  # Door (open)
            TileInfo(0x0A),  # Door (open)
            TileInfo(0x0B),  # Door (open)
            TileInfo(0x0C),  # Door (open)
            TileInfo(0x43),  # Door (open)
            TileInfo(0x44),  # Door (open)
            TileInfo(0x2D),  # Door (key)
            TileInfo(0x2E),  # Door (key)
            TileInfo(0x2F),  # Door (key)
            TileInfo(0x30),  # Door (key)
            TileInfo(0x31),  # Door (key)
            TileInfo(0x32),  # Door (key)
            TileInfo(0x33),  # Door (key)
            TileInfo(0x34),  # Door (key)

            TileInfo(0xA4, main_tileset={0x00, 0x06, 0x0A, 0x0E, 0x17}),  # Door (boss)
            TileInfo(0xA5, main_tileset={0x00, 0x06, 0x0A, 0x0E, 0x17}),  # Door (boss)

            TileInfo(0xB1, main_tileset={0x02, 0x0B}),  # Door (flip)
            TileInfo(0xB2, main_tileset={0x02, 0x0B}),  # Door (flip)
            TileInfo(0x45),  # Door (flip-exit)
            TileInfo(0x46),  # Door (flip-exit)

            TileInfo(0xC1, main_tileset={0x00, 0x04, 0x05, 0x08, 0x0C, 0x19}),  # Entrance
            TileInfo(0xC2, main_tileset={0x00, 0x04, 0x05, 0x08, 0x0C, 0x19}),  # Entrance

            TileInfo(0x10),  # Mini-wall
            TileInfo(0x11),  # Mini-wall
            TileInfo(0x12),  # Mini-wall
            TileInfo(0x13),  # Mini-wall
            TileInfo(0x14),  # Mini-wall
            TileInfo(0x15),  # Mini-wall
            TileInfo(0x16),  # Mini-wall
            TileInfo(0x17),  # Mini-wall
            TileInfo(0x93),  # Mini-wall
            TileInfo(0x94),  # Mini-wall
            TileInfo(0x95),  # Mini-wall
            TileInfo(0x96),  # Mini-wall

            TileInfo(0x20),  # Pot
            TileInfo(0x8E),  # Pot-button
            TileInfo(0xA6),  # Block
            TileInfo(0xA7),  # Block pushable
            TileInfo(0xA9),  # Block cracked

            TileInfo(0xBE),  # Warp-Stairs-Down
            TileInfo(0xBF),  # Hidden Warp-Stairs-Down
            TileInfo(0xCB, main_tileset={0x00, 0x0A, 0x0F, 0xC, 0x05, 0x17, 0x0B, 0x18}),  # Warp-Stairs-Up
            TileInfo(0xA3, main_tileset={0x03, 0x07}),  # Wall stairs-up
            TileInfo(0xA2, main_tileset={0x03, 0x0B}),  # Wall stairs-down
            TileInfo(0xA8, main_tileset={0x0E, 0x17}),  # Wall stairs-up

            TileInfo(0xAA),  # Button
            TileInfo(0xDD, main_tileset={0x05}),  # Crystal (sword)
            TileInfo(0xDE, main_tileset={0x02, 0x06, 0x07, 0x09, 0x0A}),  # Keyblock

            TileInfo(0x01),  # Pit
            TileInfo(0xAE),  # Pit
            TileInfo(0xAF),  # Pit
            TileInfo(0xB0),  # Pit

            TileInfo(0xA0),  # Chest
            TileInfo(0xA1),  # Open-chest (hidden)

            TileInfo(0x1C),  # Pit-warp
            TileInfo(0x1D),  # Pit-warp
            TileInfo(0x1E),  # Pit-warp
            TileInfo(0x1F),  # Pit-warp

            TileInfo(0xB3, main_tileset={0x01}),  # Entrance
            TileInfo(0xB4, main_tileset={0x01}),  # Entrance
            TileInfo(0xB5, main_tileset={0x01}),  # Entrance
            TileInfo(0xB6, main_tileset={0x01}),  # Entrance
            TileInfo(0xB7, main_tileset={0x01}),  # Entrance
            TileInfo(0xB8, main_tileset={0x01}),  # Entrance
            TileInfo(0xB9, main_tileset={0x01}),  # Entrance
            TileInfo(0xBA, main_tileset={0x01}),  # Entrance
            TileInfo(0xBB, main_tileset={0x01}),  # Entrance
            TileInfo(0xBC, main_tileset={0x01}),  # Entrance
            TileInfo(0xBD, main_tileset={0x01}),  # Entrance

            TileInfo(0x4E, main_tileset={0x0C}),  # Dash block
            TileInfo(0x4F, main_tileset={0x09}),  # Dash block
            TileInfo(0x88, main_tileset={0x0A}),  # Dash block

            TileInfo(0x1B, animation={0x0C}),  # Shallow water
            TileInfo(0x0E, animation={0x0C}),  # Deep water
            TileInfo(0x06, animation={0x06}),  # Lava

            TileInfo(0xCF, animation={0x07}),  # Conveyer
            TileInfo(0xD0, animation={0x07}),  # Conveyer
            TileInfo(0xD1, animation={0x07}),  # Conveyer
            TileInfo(0xD2, animation={0x07}),  # Conveyer

            TileInfo(0xD4, animation={0x04}),  # Spiked floor

            TileInfo(0x9E, main_tileset={0x07}),  # Hookshot pull bridge
            TileInfo(0x9F, main_tileset={0x07}),  # Hookshot pull bridge

            TileInfo(0xCE, main_tileset={0x04, 0x08, 0x19, 0x0F}),  # Register/Fairy statue bottom/Mad batter statue
            TileInfo(0x87, main_tileset={0x19, 0x0F}),  # Fairy statue top/Mad batter statue
            TileInfo(0xCD, main_tileset={0x04}),  # Shop edge
            TileInfo(0xD3, main_tileset={0x04}),  # Shop edge
            TileInfo(0xC5, main_tileset={0x08}),  # Bed
            TileInfo(0xC6, main_tileset={0x08}),  # Bed
            TileInfo(0x9B, main_tileset={0x08}),  # Table
            TileInfo(0x9C, main_tileset={0x08}),  # Table

            TileInfo(0x99),  # Bookcase
            TileInfo(0x9A),  # Bookcase

            TileInfo(0x86, main_tileset={0x0F}),  # Mad batter well
            TileInfo(0x90, main_tileset={0x03}),  # Castle wall with guard

            TileInfo(0xDB),  # TODO: Switch block (down)
            TileInfo(0xDC),  # TODO: Switch block (up)

            TileInfo(0xE7, main_tileset={0x1A}),  # Windfish floor
            TileInfo(0xE8, main_tileset={0x1A}),  # Windfish floor
            TileInfo(0xE9, main_tileset={0x1A}),  # Windfish floor
            TileInfo(0xEA, main_tileset={0x1A}),  # Windfish floor
        ]
        self.__underworld_dict = {ti.id: ti for ti in self.__underworld_list}
        self.unknown_list = []
        # for n in range(0x100):
        #     if n not in self.__overworld_dict:
        #         print(f"Overworld tile not in DB: 0x{n:02x}")
        #     if n not in self.__underworld_dict:
        #         print(f"Underworld tile not in DB: 0x{n:02x}")
        self.__sidescroll_list = [TileInfo(n) for n in range(0x100)]
        self.__sidescroll_dict = {ti.id: ti for ti in self.__sidescroll_list}

    def get_list(self, room_nr: int, sidescroll: bool):
        if sidescroll:
            return self.__sidescroll_list
        if room_nr >= 0x100:
            return self.__underworld_list
        return self.__overworld_list

    def get(self, tile_id, room_nr: int, sidescroll: bool, *, allow_add=False) -> Optional[TileInfo]:
        db = self.__overworld_dict
        if room_nr >= 0x100:
            db = self.__underworld_dict
        if sidescroll:
            db = self.__sidescroll_dict
        if tile_id not in db:
            if allow_add:
                print(f"TileInfo not found for: {tile_id:02x} (room: {room_nr:03x})")
                db[tile_id] = TileInfo(tile_id)
                self.unknown_list.append((db[tile_id], room_nr))
            else:
                return None
        return db[tile_id]
