entities_list = [
    {'id': 0x09, 'tiles': [0, 0], 'attr': [2, 34]},  # OCTOROCK
    {'id': 0x0B, 'tiles': [0, 1], 'attr': [1, 1]},  # MOBLIN
    {'id': 0x0D, 'tiles': [4, 4], 'attr': [2, 34]},  # TEKTITE
    {'id': 0x0E, 'tiles': [0, 0], 'attr': [1, 33]},  # LEEVER
    {'id': 0x0F, 'tiles': [0, 1], 'attr': [4, 4]},  # ARMOS_STATUE
    {'id': 0x10, 'tiles': [6, 7], 'attr': [3, 3]},  # HIDING_GHINI
    {'id': 0x11, 'tiles': [3, 4], 'attr': [2, 2]},  # GIANT_GHINI
    {'id': 0x12, 'tiles': [6, 7], 'attr': [2, 2]},  # GHINI
    {'id': 0x14, 'tiles': [0, 1, -1, ("src/gfx/characters/oam_link_1.cgb.png", 2)], 'attr': [1, 1, 0, 256]},  # MOBLIN_SWORD
    {'id': 0x15, 'tiles': [5, 5], 'attr': [3, 35]},  # ANTI_FAIRY
    {'id': 0x16, 'tiles': [6, 6], 'attr': [0, 32]},  # SPARK_COUNTER_CLOCKWISE
    {'id': 0x17, 'tiles': [6, 6], 'attr': [4, 36]},  # SPARK_CLOCKWISE
    {'id': 0x18, 'tiles': [0, 0], 'attr': [1, 33]},  # POLS_VOICE
    {'id': 0x19, 'tiles': [0, 0], 'attr': [1, 33]},  # KEESE
    {'id': 0x1A, 'tiles': [5, 6], 'attr': [0, 0]},  # STALFOS_AGGRESSIVE
    {'id': 0x1B, 'tiles': [1, 1], 'attr': [0, 32]},  # GEL
    {'id': 0x1C, 'tiles': [3], 'attr': [0, 0]},  # MINI_GEL
    {'id': 0x1E, 'tiles': [5, 6], 'attr': [1, 1]},  # STALFOS_EVASIVE
    {'id': 0x1F, 'tiles': [10, 11], 'attr': [1, 1]},  # GIBDO
    {'id': 0x20, 'tiles': [2, 2], 'attr': [3, 35]},  # HARDHAT_BEETLE
    {'id': 0x21, 'tiles': [0, 0], 'attr': [0, 32]},  # WIZROBE
    {'id': 0x23, 'tiles': [6, 6], 'attr': [1, 33]},  # LIKE_LIKE
    {'id': 0x24, 'tiles': [0, 1], 'attr': [2, 2]},  # IRON_MASK
    {'id': 0x27, 'tiles': [0, 0], 'attr': [3, 35]},  # SPIKE_TRAP
    {'id': 0x28, 'tiles': [0, 1], 'attr': [1, 1]},  # MIMIC
    {'id': 0x29, 'tiles': [3, 4], 'attr': [0, 0]},  # MINI_MOLDORM
    {'id': 0x2A, 'tiles': [0, 0], 'attr': [0, 32]},  # LASER
    {'id': 0x2C, 'tiles': [0, 0], 'attr': [0, 32]},  # SPIKED_BEETLE
    {'id': 0x2D, 'tiles': [("src/gfx/items/items_2.cgb.png", 40)], 'attr': [0x104, 0]},  # DROPPABLE_HEART
    {'id': 0x2E, 'tiles': [("src/gfx/items/items_2.cgb.png", 38)], 'attr': [0x105, 0]},  # DROPPABLE_RUPEE
    {'id': 0x2F, 'tiles': [("src/gfx/characters/oam_vfx.cgb.png", 0)], 'attr': [2, 2]},  # DROPPABLE_FAIRY
    {'id': 0x30, 'tiles': [("src/gfx/items/inventory_indoor_items.cgb.png", 10)], 'attr': [0x106, 0]},  # KEY_DROP_POINT
    {'id': 0x31, 'tiles': [("src/gfx/characters/oam_link_1.cgb.png", 2)], 'attr': [64, 0]},  # SWORD
    {'id': 0x35, 'tiles': [("src/gfx/items/items_2.cgb.png", 44), ("src/gfx/items/items_2.cgb.png", 44)], 'attr': [0x102, 0x122]},  # HEART_PIECE
    {'id': 0x37, 'tiles': [("src/gfx/characters/oam_vfx.cgb.png", 5), ("src/gfx/characters/oam_vfx.cgb.png", 5)], 'attr': [1, 33]},  # DROPPABLE_ARROWS
    {'id': 0x38, 'tiles': [("src/gfx/items/items_2.cgb.png", 0)], 'attr': [0x105, 0]},  # DROPPABLE_BOMBS
    {'id': 0x39, 'tiles': [("src/gfx/characters/oam_npc_2.cgb.png", 16*16), ("src/gfx/characters/oam_npc_2.cgb.png", 16*16+1)], 'attr': [0, 0]},  # INSTRUMENT_OF_THE_SIRENS
    {'id': 0x3A, 'tiles': [7, 7], 'attr': [2, 34]},  # SLEEPY_TOADSTOOL
    {'id': 0x3B, 'tiles': [("src/gfx/items/items_2.cgb.png", 14)], 'attr': [0x104, 0]},  # DROPPABLE_MAGIC_POWDER
    {'id': 0x3C, 'tiles': [("src/gfx/items/slime_key.cgb.png", 0)], 'attr': [0x104, 4]},  # HIDING_SLIME_KEY
    {'id': 0x3D, 'tiles': [("src/gfx/items/inventory_overworld_items.cgb.png", 10)], 'attr': [0x104, 0]},  # DROPPABLE_SECRET_SEASHELL
    {'id': 0x3E, 'tiles': [4, 5], 'attr': [1, 1]},  # MARIN
    {'id': 0x3F, 'tiles': [4, 5], 'attr': [2, 2]},  # RACOON
    {'id': 0x40, 'tiles': [4, 5], 'attr': [2, 2]},  # WITCH
    {'id': 0x41},  # OWL_EVENT
    {'id': 0x42, 'tiles': [7, 7], 'attr': [1, 33]},  # OWL_STATUE
    {'id': 0x43},  # SEASHELL_MANSION_TREES
    {'id': 0x44},  # YARNA_TALKING_BONES
    {'id': 0x45, 'tiles': [6, 7], 'attr': [1, 1]},  # BOULDERS
    {'id': 0x46},  # MOVING_BLOCK_LEFT_TOP
    {'id': 0x47},  # MOVING_BLOCK_LEFT_BOTTOM
    {'id': 0x48},  # MOVING_BLOCK_BOTTOM_LEFT
    {'id': 0x49},  # MOVING_BLOCK_BOTTOM_RIGHT
    {'id': 0x4A, 'tiles': [4], 'attr': [0, 0]},  # COLOR_DUNGEON_BOOK
    {'id': 0x4D, 'tiles': [0, 1], 'attr': [3, 3]},  # SHOP_OWNER
    {'id': 0x4F, 'tiles': [0, 1], 'attr': [3, 3]},  # TRENDY_GAME_OWNER
    {'id': 0x50, 'tiles': [0, 1], 'attr': [3, 3]},  # BOO_BUDDY
    {'id': 0x51, 'tiles': [0, 1], 'attr': [2, 2]},  # KNIGHT
    {'id': 0x52, 'tiles': [6, 6], 'attr': [3, 35]},  # TRACTOR_DEVICE
    {'id': 0x53, 'tiles': [6, 6], 'attr': [0, 32]},  # TRACTOR_DEVICE_REVERSE
    {'id': 0x54, 'tiles': [0, 1], 'attr': [3, 3]},  # FISHERMAN_FISHING_GAME
    {'id': 0x55, 'tiles': [7, 7], 'attr': [0, 32]},  # BOUNCING_BOMBITE
    {'id': 0x56, 'tiles': [0, 1], 'attr': [0, 0]},  # TIMER_BOMBITE
    {'id': 0x57, 'tiles': [0, 1], 'attr': [0, 0]},  # PAIRODD
    {'id': 0x59, 'tiles': [6, 7], 'attr': [3, 3]},  # MOLDORM
    {'id': 0x5A, 'tiles': [20, 21], 'attr': [3, 3]},  # FACADE
    {'id': 0x5B, 'tiles': [2, 3], 'attr': [3, 3]},  # SLIME_EYE
    {'id': 0x5C, 'tiles': [4, 5], 'attr': [2, 2]},  # GENIE
    {'id': 0x5D, 'tiles': [6, 7], 'attr': [3, 3]},  # SLIME_EEL
    {'id': 0x5E, 'tiles': [0, 0], 'attr': [0, 32]},  # GHOMA
    {'id': 0x5F, 'tiles': [1, 2], 'attr': [3, 3]},  # MASTER_STALFOS
    {'id': 0x60, 'tiles': [0, 0], 'attr': [0, 32]},  # DODONGO_SNAKE
    {'id': 0x61},  # WARP
    {'id': 0x62, 'tiles': [4, 5], 'attr': [2, 2]},  # HOT_HEAD
    {'id': 0x63, 'tiles': [3, 4], 'attr': [2, 2]},  # EVIL_EAGLE
    {'id': 0x65, 'tiles': [6, 7], 'attr': [3, 3]},  # ANGLER_FISH
    {'id': 0x66, 'tiles': [4, 4], 'attr': [1, 33]},  # CRYSTAL_SWITCH
    {'id': 0x69},  # MOVING_BLOCK_MOVER
    {'id': 0x6A, 'tiles': [6, 6], 'attr': [1, 33]},  # RAFT_RAFT_OWNER
    {'id': 0x6C, 'tiles': [0, 1], 'attr': [1, 1]},  # CUCCO
    {'id': 0x6D, 'tiles': [1, 1], 'attr': [3, 35]},  # BOW_WOW
    {'id': 0x6E, 'tiles': [7], 'attr': [3, 3]},  # BUTTERFLY
    {'id': 0x6F, 'tiles': [4, 5], 'attr': [1, 1]},  # DOG
    {'id': 0x70},  # KID_70
    {'id': 0x71},  # KID_71
    {'id': 0x72},  # KID_72
    {'id': 0x73},  # KID_73
    {'id': 0x74, 'tiles': [1, 2], 'attr': [0, 0]},  # PAPAHLS_WIFE
    {'id': 0x75, 'tiles': [0, 1], 'attr': [1, 1]},  # GRANDMA_ULRIRA
    {'id': 0x76, 'tiles': [0, 1], 'attr': [2, 2]},  # MR_WRITE
    {'id': 0x77, 'tiles': [2, 3], 'attr': [1, 2]},  # GRANDPA_ULRIRA
    {'id': 0x78, 'tiles': [0, 1], 'attr': [2, 2]},  # YIP_YIP
    {'id': 0x79, 'tiles': [0, 1], 'attr': [2, 2]},  # MADAM_MEOWMEOW
    {'id': 0x7A, 'tiles': [0, 1], 'attr': [3, 3]},  # CROW
    {'id': 0x7B, 'tiles': [0, 1], 'attr': [2, 2]},  # CRAZY_TRACY
    {'id': 0x7C, 'tiles': [1, 1], 'attr': [2, 34]},  # GIANT_GOPONGA_FLOWER
    {'id': 0x7E, 'tiles': [1, 1], 'attr': [2, 34]},  # GOPONGA_FLOWER
    {'id': 0x7F, 'tiles': [1, 1], 'attr': [2, 34]},  # TURTLE_ROCK_HEAD
    {'id': 0x80, 'tiles': [0, 1], 'attr': [2, 2]},  # TELEPHONE
    {'id': 0x81, 'tiles': [3, 4], 'attr': [2, 2]},  # ROLLING_BONES
    {'id': 0x82, 'tiles': [6, 6], 'attr': [1, 33]},  # ROLLING_BONES_BAR
    {'id': 0x83},  # DREAM_SHRINE_BED
    {'id': 0x84},  # BIG_FAIRY
    {'id': 0x85},  # MR_WRITES_BIRD
    {'id': 0x86},  # FLOATING_ITEM
    {'id': 0x87},  # DESERT_LANMOLA
    {'id': 0x88, 'tiles': [0, 1], 'attr': [2, 2]},  # ARMOS_KNIGHT
    {'id': 0x89, 'tiles': [1, 2], 'attr': [2, 2]},  # HINOX
    {'id': 0x8A},  # TILE_GLINT_SHOWN
    {'id': 0x8B},  # TILE_GLINT_HIDDEN
    {'id': 0x8E, 'tiles': [0, 1], 'attr': [2, 2]},  # CUE_BALL
    {'id': 0x8F, 'tiles': [0, 1], 'attr': [1, 1]},  # MASKED_MIMIC_GORIYA
    {'id': 0x90, 'tiles': [0, 1], 'attr': [1, 1]},  # THREE_OF_A_KIND
    {'id': 0x91, 'tiles': [0, 1], 'attr': [1, 1]},  # ANTI_KIRBY
    {'id': 0x92, 'tiles': [0, 1], 'attr': [3, 3]},  # SMASHER
    {'id': 0x93},  # MAD_BOMBER
    {'id': 0x94},  # KANALET_BOMBABLE_WALL
    {'id': 0x95},  # RICHARD
    {'id': 0x96},  # RICHARD_FROG
    {'id': 0x97},  # DIVE_SPOT
    {'id': 0x98},  # HORSE_PIECE
    {'id': 0x99, 'tiles': [0, 0], 'attr': [0, 32]},  # WATER_TEKTITE
    {'id': 0x9A},  # FLYING_TILES
    {'id': 0x9B, 'tiles': [1, 1], 'attr': [2, 34]},  # HIDING_GEL
    {'id': 0x9C, 'tiles': [3, 4], 'attr': [0, 0]},  # STAR
    {'id': 0x9D},  # LIFTABLE_STATUE
    {'id': 0x9E},  # FIREBALL_SHOOTER
    {'id': 0x9F, 'tiles': [5, 6], 'attr': [2, 2]},  # GOOMBA
    {'id': 0xA0, 'tiles': [0, 0], 'attr': [2, 34]},  # PEAHAT
    {'id': 0xA1, 'tiles': [2, 3], 'attr': [0, 0]},  # SNAKE
    {'id': 0xA2},  # PIRANHA_PLANT
    {'id': 0xA3},  # SIDE_VIEW_PLATFORM_HORIZONTAL
    {'id': 0xA4},  # SIDE_VIEW_PLATFORM_VERTICAL
    {'id': 0xA5},  # SIDE_VIEW_PLATFORM
    {'id': 0xA6},  # SIDE_VIEW_WEIGHTS
    {'id': 0xA7},  # SMASHABLE_PILLAR
    {'id': 0xA9, 'tiles': [4, 4], 'attr': [0, 32]},  # BLOOPER
    {'id': 0xAA},  # CHEEP_CHEEP_HORIZONTAL
    {'id': 0xAB},  # CHEEP_CHEEP_VERTICAL
    {'id': 0xAC},  # CHEEP_CHEEP_JUMPING
    {'id': 0xAD},  # KIKI_THE_MONKEY
    {'id': 0xAE, 'tiles': [0, 0, (0x2C, 0x220), (0x2C, 0x220)], 'attr': [2, 34, 0, 32]},  # WINGED_OCTOROK
    {'id': 0xAF},  # TRADING_ITEM
    {'id': 0xB0, 'tiles': [0, 0], 'attr': [2, 34]},  # PINCER
    {'id': 0xB1, 'tiles': [0, 0], 'attr': [2, 34]},  # HOLE_FILLER
    {'id': 0xB2, 'tiles': [0, 1], 'attr': [1, 1]},  # BEETLE_SPAWNER
    {'id': 0xB3, 'tiles': [0, 0], 'attr': [1, 33]},  # HONEYCOMB
    {'id': 0xB4, 'tiles': [0, 1], 'attr': [2, 2]},  # TARIN
    {'id': 0xB5, 'tiles': [1, 2], 'attr': [2, 2]},  # BEAR
    {'id': 0xB6, 'tiles': [0, 1], 'attr': [2, 2]},  # PAPAHL
    {'id': 0xB7, 'tiles': [0, 1], 'attr': [2, 2]},  # MERMAID
    {'id': 0xB8, 'tiles': [16, 17], 'attr': [2, 2]},  # FISHERMAN_UNDER_BRIDGE
    {'id': 0xB9, 'tiles': [0, 0], 'attr': [0, 32]},  # BUZZ_BLOB
    {'id': 0xBA, 'tiles': [2, 1], 'attr': [2, 2]},  # BOMBER
    {'id': 0xBB, 'tiles': [6, 7], 'attr': [2, 2]},  # BUSH_CRAWLER
    {'id': 0xBC, 'tiles': [1, 2], 'attr': [3, 3]},  # GRIM_CREEPER
    {'id': 0xBD, 'tiles': [0, 1], 'attr': [2, 2]},  # VIRE
    {'id': 0xBE, 'tiles': [4, 5], 'attr': [1, 1]},  # BLAINO
    {'id': 0xBF, 'tiles': [4, 5], 'attr': [2, 2]},  # ZOMBIE
    {'id': 0xC0},  # MAZE_SIGNPOST
    {'id': 0xC1},  # MARIN_AT_THE_SHORE
    {'id': 0xC2},  # MARIN_AT_TAL_TAL_HEIGHTS
    {'id': 0xC3, 'tiles': [9, 10], 'attr': [0, 0]},  # MAMU_AND_FROGS
    {'id': 0xC4, 'tiles': [9, 10], 'attr': [1, 1]},  # WALRUS
    {'id': 0xC5, 'tiles': [6, 7], 'attr': [3, 3]},  # URCHIN
    {'id': 0xC6, 'tiles': [4, 4], 'attr': [2, 34]},  # SAND_CRAB
    {'id': 0xC7, 'tiles': [8, 9], 'attr': [3, 3]},  # MANBO_AND_FISHES
    {'id': 0xCA, 'tiles': [0, 1], 'attr': [2, 2]},  # MAD_BATTER
    {'id': 0xCB, 'tiles': [3, 3], 'attr': [1, 33]},  # ZORA
    {'id': 0xCC, 'tiles': [2, 3], 'attr': [3, 3]},  # FISH
    {'id': 0xCD},  # BANANAS_SCHULE_SALE
    {'id': 0xCE},  # MERMAID_STATUE
    {'id': 0xCF},  # SEASHELL_MANSION
    {'id': 0xD0},  # ANIMAL_D0
    {'id': 0xD1},  # ANIMAL_D1
    {'id': 0xD2},  # ANIMAL_D2
    {'id': 0xD3},  # BUNNY_D3
    {'id': 0xD6},  # SIDE_VIEW_POT
    {'id': 0xD7, 'tiles': [5, 5], 'attr': [3, 35]},  # THWIMP
    {'id': 0xD8, 'tiles': [8, 9], 'attr': [5, 5]},  # THWOMP
    {'id': 0xD9, 'tiles': [0, 1], 'attr': [2, 2]},  # THWOMP_RAMMABLE
    {'id': 0xDA},  # PODOBOO
    {'id': 0xDB},  # GIANT_BUBBLE
    {'id': 0xDC},  # FLYING_ROOSTER_EVENTS
    {'id': 0xDD},  # BOOK
    {'id': 0xDE},  # EGG_SONG_EVENT
    {'id': 0xE0},  # MONKEY
    {'id': 0xE1},  # WITCH_RAT
    {'id': 0xE2},  # FLAME_SHOOTER
    {'id': 0xE3, 'tiles': [2, 2], 'attr': [0, 32]},  # POKEY
    {'id': 0xE4, 'tiles': [13, 14], 'attr': [2, 2]},  # MOBLIN_KING
    {'id': 0xE5},  # FLOATING_ITEM_2
    {'id': 0xE6},  # FINAL_NIGHTMARE
    {'id': 0xE7},  # KANALET_CASTLE_GATE_SWITCH
    {'id': 0xEC, 'tiles': [0, 0], 'attr': [2, 34]},  # COLOR_GHOUL_RED
    {'id': 0xED, 'tiles': [0, 0], 'attr': [0, 32]},  # COLOR_GHOUL_GREEN
    {'id': 0xEE, 'tiles': [0, 0], 'attr': [3, 35]},  # COLOR_GHOUL_BLUE
    {'id': 0xE9}, # ENTITY_COLOR_SHELL_RED
    {'id': 0xEA}, # ENTITY_COLOR_SHELL_GREEN
    {'id': 0xEB}, # ENTITY_COLOR_SHELL_BLUE
    {'id': 0xF4, 'tiles': [1, 2], 'attr': [1, 1]},  # AVALAUNCH
    {'id': 0xF8, 'tiles': [0, 1], 'attr': [0, 0]},  # GIANT_BUZZ_BLOB
    {'id': 0xEF, 'tiles': [0, 0], 'attr': [2, 34]},  # ENTITY_ROTOSWITCH_RED
    {'id': 0xF0, 'tiles': [1, 2], 'attr': [1, 1]},  # ENTITY_ROTOSWITCH_YELLOW
    {'id': 0xF1, 'tiles': [0, 0], 'attr': [3, 35]},  # ENTITY_ROTOSWITCH_BLUE
    {'id': 0xF3},  # ENTITY_HOPPER
    {'id': 0xF2},  # ENTITY_FLYING_HOPPER_BOMBS
    {'id': 0xF6},  # ENTITY_COLOR_GUARDIAN_BLUE
    {'id': 0xF7},  # ENTITY_COLOR_GUARDIAN_RED
    {'id': 0xF8},  # ENTITY_GIANT_BUZZ_BLOB
    {'id': 0xF9},  # ENTITY_HARDHIT_BEETLE
    {'id': 0xFA},  # PHOTOGRAPHER
]
entities_dict = {e['id']: e for e in entities_list}

NAME = [
    "ARROW",
    "BOOMERANG",
    "BOMB",
    "HOOKSHOT_CHAIN",
    "HOOKSHOT_HIT",
    "LIFTABLE_ROCK",
    "PUSHED_BLOCK",
    "CHEST_WITH_ITEM",
    "MAGIC_POWDER_SPRINKLE",
    "OCTOROCK",
    "OCTOROCK_ROCK",
    "MOBLIN",
    "MOBLIN_ARROW",
    "TEKTITE",
    "LEEVER",
    "ARMOS_STATUE",
    "HIDING_GHINI",
    "GIANT_GHINI",
    "GHINI",
    "BROKEN_HEART_CONTAINER",
    "MOBLIN_SWORD",
    "ANTI_FAIRY",
    "SPARK_COUNTER_CLOCKWISE",
    "SPARK_CLOCKWISE",
    "POLS_VOICE",
    "KEESE",
    "STALFOS_AGGRESSIVE",
    "GEL",
    "MINI_GEL",
    "DISABLED",
    "STALFOS_EVASIVE",
    "GIBDO",
    "HARDHAT_BEETLE",
    "WIZROBE",
    "WIZROBE_PROJECTILE",
    "LIKE_LIKE",
    "IRON_MASK",
    "SMALL_EXPLOSION_ENEMY",
    "SMALL_EXPLOSION_ENEMY_2",
    "SPIKE_TRAP",
    "MIMIC",
    "MINI_MOLDORM",
    "LASER",
    "LASER_BEAM",
    "SPIKED_BEETLE",
    "DROPPABLE_HEART",
    "DROPPABLE_RUPEE",
    "DROPPABLE_FAIRY",
    "KEY_DROP_POINT",
    "SWORD",
    "32",
    "PIECE_OF_POWER",
    "GUARDIAN_ACORN",
    "HEART_PIECE",
    "HEART_CONTAINER",
    "DROPPABLE_ARROWS",
    "DROPPABLE_BOMBS",
    "INSTRUMENT_OF_THE_SIRENS",
    "SLEEPY_TOADSTOOL",
    "DROPPABLE_MAGIC_POWDER",
    "HIDING_SLIME_KEY",
    "DROPPABLE_SECRET_SEASHELL",
    "MARIN",
    "RACOON",
    "WITCH",
    "OWL_EVENT",
    "OWL_STATUE",
    "SEASHELL_MANSION_TREES",
    "YARNA_TALKING_BONES",
    "BOULDERS",
    "MOVING_BLOCK_LEFT_TOP",
    "MOVING_BLOCK_LEFT_BOTTOM",
    "MOVING_BLOCK_BOTTOM_LEFT",
    "MOVING_BLOCK_BOTTOM_RIGHT",
    "COLOR_DUNGEON_BOOK",
    "POT",
    "DISABLED",
    "SHOP_OWNER",
    "4D",
    "TRENDY_GAME_OWNER",
    "BOO_BUDDY",
    "KNIGHT",
    "TRACTOR_DEVICE",
    "TRACTOR_DEVICE_REVERSE",
    "FISHERMAN_FISHING_GAME",
    "BOUNCING_BOMBITE",
    "TIMER_BOMBITE",
    "PAIRODD",
    "PAIRODD_PROJECTILE",
    "MOLDORM",
    "FACADE",
    "SLIME_EYE",
    "GENIE",
    "SLIME_EEL",
    "GHOMA",
    "MASTER_STALFOS",
    "DODONGO_SNAKE",
    "WARP",
    "HOT_HEAD",
    "EVIL_EAGLE",
    "SOUTH_FACE_SHRINE_DOOR",
    "ANGLER_FISH",
    "CRYSTAL_SWITCH",
    "67",
    "68",
    "MOVING_BLOCK_MOVER",
    "RAFT_RAFT_OWNER",
    "TEXT_DEBUGGER",
    "CUCCO",
    "BOW_WOW",
    "BUTTERFLY",
    "DOG",
    "KID_70",
    "KID_71",
    "KID_72",
    "KID_73",
    "PAPAHLS_WIFE",
    "GRANDMA_ULRIRA",
    "MR_WRITE",
    "GRANDPA_ULRIRA",
    "YIP_YIP",
    "MADAM_MEOWMEOW",
    "CROW",
    "CRAZY_TRACY",
    "GIANT_GOPONGA_FLOWER",
    "GOPONGA_FLOWER_PROJECTILE",
    "GOPONGA_FLOWER",
    "TURTLE_ROCK_HEAD",
    "TELEPHONE",
    "ROLLING_BONES",
    "ROLLING_BONES_BAR",
    "DREAM_SHRINE_BED",
    "BIG_FAIRY",
    "MR_WRITES_BIRD",
    "FLOATING_ITEM",
    "DESERT_LANMOLA",
    "ARMOS_KNIGHT",
    "HINOX",
    "TILE_GLINT_SHOWN",
    "TILE_GLINT_HIDDEN",
    "8C",
    "8D",
    "CUE_BALL",
    "MASKED_MIMIC_GORIYA",
    "THREE_OF_A_KIND",
    "ANTI_KIRBY",
    "SMASHER",
    "MAD_BOMBER",
    "KANALET_BOMBABLE_WALL",
    "RICHARD",
    "RICHARD_FROG",
    "DIVE_SPOT",
    "HORSE_PIECE",
    "WATER_TEKTITE",
    "FLYING_TILES",
    "HIDING_GEL",
    "STAR",
    "LIFTABLE_STATUE",
    "FIREBALL_SHOOTER",
    "GOOMBA",
    "PEAHAT",
    "SNAKE",
    "PIRANHA_PLANT",
    "SIDE_VIEW_PLATFORM_HORIZONTAL",
    "SIDE_VIEW_PLATFORM_VERTICAL",
    "SIDE_VIEW_PLATFORM",
    "SIDE_VIEW_WEIGHTS",
    "SMASHABLE_PILLAR",
    "WRECKING_BALL",
    "BLOOPER",
    "CHEEP_CHEEP_HORIZONTAL",
    "CHEEP_CHEEP_VERTICAL",
    "CHEEP_CHEEP_JUMPING",
    "KIKI_THE_MONKEY",
    "WINGED_OCTOROK",
    "TRADING_ITEM",
    "PINCER",
    "HOLE_FILLER",
    "BEETLE_SPAWNER",
    "HONEYCOMB",
    "TARIN",
    "BEAR",
    "PAPAHL",
    "MERMAID",
    "FISHERMAN_UNDER_BRIDGE",
    "BUZZ_BLOB",
    "BOMBER",
    "BUSH_CRAWLER",
    "GRIM_CREEPER",
    "VIRE",
    "BLAINO",
    "ZOMBIE",
    "MAZE_SIGNPOST",
    "MARIN_AT_THE_SHORE",
    "MARIN_AT_TAL_TAL_HEIGHTS",
    "MAMU_AND_FROGS",
    "WALRUS",
    "URCHIN",
    "SAND_CRAB",
    "MANBO_AND_FISHES",
    "BUNNY_CALLING_MARIN",
    "MUSICAL_NOTE",
    "MAD_BATTER",
    "ZORA",
    "FISH",
    "BANANAS_SCHULE_SALE",
    "MERMAID_STATUE",
    "SEASHELL_MANSION",
    "ANIMAL_D0",
    "ANIMAL_D1",
    "ANIMAL_D2",
    "BUNNY_D3",
    "GHOST",
    "ROOSTER",
    "SIDE_VIEW_POT",
    "THWIMP",
    "THWOMP",
    "THWOMP_RAMMABLE",
    "PODOBOO",
    "GIANT_BUBBLE",
    "FLYING_ROOSTER_EVENTS",
    "BOOK",
    "EGG_SONG_EVENT",
    "SWORD_BEAM",
    "MONKEY",
    "WITCH_RAT",
    "FLAME_SHOOTER",
    "POKEY",
    "MOBLIN_KING",
    "FLOATING_ITEM_2",
    "FINAL_NIGHTMARE",
    "KANALET_CASTLE_GATE_SWITCH",
    "ENDING_OWL_STAIR_CLIMBING",
    "COLOR_SHELL_RED",
    "COLOR_SHELL_GREEN",
    "COLOR_SHELL_BLUE",
    "COLOR_GHOUL_RED",
    "COLOR_GHOUL_GREEN",
    "COLOR_GHOUL_BLUE",
    "ROTOSWITCH_RED",
    "ROTOSWITCH_YELLOW",
    "ROTOSWITCH_BLUE",
    "FLYING_HOPPER_BOMBS",
    "HOPPER",
    "AVALAUNCH",
    "BOUNCING_BOULDER",
    "COLOR_GUARDIAN_BLUE",
    "COLOR_GUARDIAN_RED",
    "GIANT_BUZZ_BLOB",
    "HARDHIT_BEETLE",
    "PHOTOGRAPHER",
]

def _moblinSpriteData(room_id):
    if room_id in (0x002, 0x013): # Tal tal heights exception
        return (2, 0x9C)  # Hooded stalfos
    if room_id < 0x100:
        x = room_id & 0x0F
        y = (room_id >> 4) & 0x0F
        if x < 0x04: # Left side is woods and mountain moblins
            return (2, 0x7C) # Moblin
        if 0x08 <= x <= 0x0B and 4 <= y <= 0x07: # Castle
            return (2, 0x92)  # Knight
        # Everything else is pigs
        return (2, 0x83) # Pig
    elif room_id < 0x1DF: # Dungeons contain hooded stalfos
        return (2, 0x9C)  # Hooded stalfos
    elif room_id < 0x200: # Caves contain moblins
        return (2, 0x7C)  # Moblin
    elif room_id < 0x276: # Dungeons contain hooded stalfos
        return (2, 0x9C)  # Hooded stalfos
    elif room_id < 0x300: # Caves contain moblins
        x = room_id & 0x0F
        y = (room_id >> 4) & 0x0F
        if 2 <= x <= 6 and 0x0C <= y <= 0x0D: # Castle indoors
            return (2, 0x92)  # Knight
        return (2, 0x7C)  # Moblin
    else: # Dungeon contains hooded stalfos
        return (2, 0x9C)  # Hooded stalfos

_CAVES_B_ROOMS = {0x2B6, 0x2B7, 0x2B8, 0x2B9, 0x285, 0x286, 0x2FD, 0x2F3, 0x2ED, 0x2EE, 0x2EA, 0x2EB, 0x2EC, 0x287, 0x2F1, 0x2F2, 0x2FE, 0x2EF, 0x2BA, 0x2BB, 0x2BC, 0x28D, 0x2F9, 0x2FA, 0x280, 0x281, 0x282, 0x283, 0x284, 0x28C, 0x288, 0x28A, 0x290, 0x291, 0x292, 0x28E, 0x29A, 0x289, 0x28B, 0x297, 0x293, 0x294, 0x295, 0x296, 0x2AB, 0x2AC, 0x298, 0x27A, 0x27B, 0x2E6, 0x2E7, 0x2BD, 0x27C, 0x27D, 0x27E, 0x2F6, 0x2F7, 0x2DE, 0x2DF}

# For each entity, which sprite slot is used and which value should be used.
SPRITE_DATA = {
    0x09: (2, 0xE3), # OCTOROCK
    0x0B: _moblinSpriteData, # MOBLIN
    0x0D: (1, 0x87), # TEKTITE
    0x0E: (1, 0x81), # LEEVER
    0x0F: (2, 0x78), # ARMOS_STATUE
    0x10: (1, 0x42), # HIDING_GHINI
    0x11: (2, 0x8A), # GIANT_GHINI
    0x12: (1, 0x42), # GHINI
    0x13: (0, 0xe8, 1, 0xe9, 2, 0xea, 3, 0xeb),  # BROKEN_HEART_CONTAINER (used for nightmare minibosses)
    0x14: _moblinSpriteData, # MOBLIN_SWORD
    0x15: (1, 0x91), # ANTI_FAIRY
    0x16: (1, {0x91, 0x65}), # SPARK_COUNTER_CLOCKWISE
    0x17: (1, {0x91, 0x65}), # SPARK_CLOCKWISE
    0x18: (3, 0x93), # POLS_VOICE
    0x19: lambda room_id: (2, 0x90) if room_id in _CAVES_B_ROOMS else (0, 0x90), # KEESE
    0x1A: (0, {0x90, 0x77}), # STALFOS_AGGRESSIVE
    0x1B: None,      # GEL
    0x1C: (1, 0x91), # MINI_GEL
    0x1E: (0, {0x90, 0x77}), # STALFOS_EVASIVE
    0x1F: lambda room_id: (0, 0x77) if 0x230 <= room_id <= 0x26B else (0, 0x90, 3, 0x93), # GIBDO
    0x20: lambda room_id: (2, 0x90) if room_id in _CAVES_B_ROOMS else (0, 0x90), # HARDHAT_BEETLE
    0x21: (2, 0x95), # WIZROBE
    0x23: (3, 0x93), # LIKE_LIKE
    0x24: (2, 0x94, 3, 0x9F), # IRON_MASK
    0x27: (1, 0x91), # SPIKE_TRAP
    0x28: (2, 0x96), # MIMIC
    0x29: (3, 0x98), # MINI_MOLDORM
    0x2A: (3, 0x99), # LASER
    0x2C: lambda room_id: (2, 0x9B) if 0x15E <= room_id <= 0x17F else (3, 0x9B), # SPIKED_BEETLE
    0x2D: None,      # DROPPABLE_HEART
    0x2E: None,      # DROPPABLE_RUPEE
    0x2F: None,      # DROPPABLE_FAIRY
    0x30: None,      # KEY_DROP_POINT
    0x31: None,      # SWORD
    0x35: None,      # HEART_PIECE
    0x37: None,      # DROPPABLE_ARROWS
    0x38: None,      # DROPPABLE_BOMBS
    0x39: (2, 0x4F), # INSTRUMENT_OF_THE_SIRENS
    0x3A: (1, 0x8E), # SLEEPY_TOADSTOOL
    0x3B: None,      # DROPPABLE_MAGIC_POWDER
    0x3C: None,      # HIDING_SLIME_KEY
    0x3D: None,      # DROPPABLE_SECRET_SEASHELL
    0x3E: lambda room_id: (0, 0x8D, 2, 0x8F) if room_id == 0x2A3 else (2, 0xE6), # MARIN
    0x3F: lambda room_id: (1, 0x8E, 3, 0x6A) if room_id == 0x2A3 else (1, 0x6C, 3, 0xC8), # RACOON
    0x40: (2, 0xA3), # WITCH
    0x41: None,      # OWL_EVENT
    0x42: lambda room_id: (1, 0xD5) if room_id == 0x26F else (1, 0x91), # OWL_STATUE
    0x43: None,      # SEASHELL_MANSION_TREES
    0x44: None,      # YARNA_TALKING_BONES
    0x45: (1, 0x44), # BOULDERS
    0x46: None,      # MOVING_BLOCK_LEFT_TOP
    0x47: None,      # MOVING_BLOCK_LEFT_BOTTOM
    0x48: None,      # MOVING_BLOCK_BOTTOM_LEFT
    0x49: None,      # MOVING_BLOCK_BOTTOM_RIGHT
    0x4A: (1, 0xd5), # COLOR_DUNGEON_BOOK
    0x4C: None,      # Used by Bingo board, otherwise unused.
    0x4D: (2, 0x88, 3, 0xC7), # SHOP_OWNER
    0x4F: (2, 0x84, 3, 0x89), # TRENDY_GAME_OWNER
    0x50: (2, 0x97), # BOO_BUDDY
    0x51: (3, 0x9A), # KNIGHT
    0x52: lambda room_id: (3, {0x7b, 0xa6}) if 0x120 <= room_id <= 0x13F else (0, {0x7b, 0xa6}), # TRACTOR_DEVICE
    0x53: lambda room_id: (3, {0x7b, 0xa6}) if 0x120 <= room_id <= 0x13F else (0, {0x7b, 0xa6}), # TRACTOR_DEVICE_REVERSE
    0x54: lambda room_id: (0, 0xA0, 1, 0xA1) if room_id == 0x2B1 else (3, 0x4e), # FISHERMAN_FISHING_GAME
    0x55: (3, 0x9d), # BOUNCING_BOMBITE
    0x56: (3, 0x9d), # TIMER_BOMBITE
    0x57: (3, 0x9e), # PAIRODD
    0x59: (2, 0xb0, 3, 0xb1), # MOLDORM
    0x5A: (0, 0x66, 2, 0xb2, 3, 0xb3), # FACADE
    0x5B: (2, 0xb4, 3, 0xb5), # SLIME_EYE
    0x5C: (2, 0xb6, 3, 0xb7), # GENIE
    0x5D: (2, 0xb8, 3, 0xb9), # SLIME_EEL
    0x5E: (2, 0xa8), # GHOMA
    0x5F: (2, 0x62, 3, 0x63), # MASTER_STALFOS
    0x60: lambda room_id: (3, 0xaa) if 0x230 <= room_id <= 0x26B else (2, 0xaa), # DODONGO_SNAKE
    0x61: None,      # WARP
    0x62: (2, 0xba, 3, 0xbb), # HOT_HEAD
    0x63: (0, 0xbc, 1, 0xbd, 2, 0xbe, 3, 0xbf), # EVIL_EAGLE
    0x65: (0, 0xac, 1, 0xad, 2, 0xae, 3, 0xaf), # ANGLER_FISH
    0x66: (1, 0x91), # CRYSTAL_SWITCH
    0x69: (0, 0x66), # MOVING_BLOCK_MOVER
    0x6A: lambda room_id: (1, 0x87, 2, 0x84) if room_id >= 0x100 else (1, 0x87), # RAFT_RAFT_OWNER
    0x6C: (1, 0xE5), # CUCCO
    0x6D: (3, 0xA4), # BOW_WOW
    0x6E: lambda room_id: (1, 0xE5) if room_id & 0x0F < 8 else (1, 0xC4), # BUTTERFLY
    0x6F: (1, 0xE5), # DOG
    0x70: (3, 0xE7), # KID_70
    0x71: (3, 0xE7), # KID_71
    0x72: (3, 0xE7), # KID_72
    0x73: (3, 0xDC), # KID_73
    0x74: (2, 0x45), # PAPAHLS_WIFE
    0x75: (2, 0x43), # GRANDMA_ULRIRA
    0x76: lambda room_id: (3, 0x74) if room_id == 0x2D9 else (3, 0x4b), # MR_WRITE
    0x77: (3, 0x46), # GRANDPA_ULRIRA
    0x78: (3, 0x48), # YIP_YIP
    0x79: (2, 0x47), # MADAM_MEOWMEOW
    0x7A: lambda room_id: (1, 0xC6) if room_id < 0x040 else (1, 0x42), # CROW
    0x7B: (2, 0x49), # CRAZY_TRACY
    0x7C: (3, 0x40), # GIANT_GOPONGA_FLOWER
    0x7E: (1, 0x4A), # GOPONGA_FLOWER
    0x7F: (3, 0x41), # TURTLE_ROCK_HEAD
    0x80: (1, 0x4C), # TELEPHONE
    0x81: lambda room_id: (3, 0xAB) if 0x230 <= room_id <= 0x26B else (2, 0xAB), # ROLLING_BONES (sometimes in slot 3?)
    0x82: lambda room_id: (3, 0xAB) if 0x230 <= room_id <= 0x26B else (2, 0xAB), # ROLLING_BONES_BAR (sometimes in slot 3?)
    0x83: (1, 0x8D), # DREAM_SHRINE_BED
    0x84: (1, 0x4D), # BIG_FAIRY
    0x85: (2, 0x4C), # MR_WRITES_BIRD
    0x86: None,      # FLOATING_ITEM
    0x87: (3, 0x52), # DESERT_LANMOLA
    0x88: (3, 0x53), # ARMOS_KNIGHT
    0x89: (2, 0x54), # HINOX
    0x8A: None,      # TILE_GLINT_SHOWN
    0x8B: None,      # TILE_GLINT_HIDDEN
    0x8E: (2, 0x56), # CUE_BALL
    0x8F: lambda room_id: (2, 0x86) if room_id == 0x1F5 else (2, 0x58), # MASKED_MIMIC_GORIYA
    0x90: (3, 0x59), # THREE_OF_A_KIND
    0x91: (2, 0x55), # ANTI_KIRBY
    0x92: (2, 0x57), # SMASHER
    0x93: (3, 0x5A), # MAD_BOMBER
    0x94: (2, 0x92), # KANALET_BOMBABLE_WALL
    0x95: (1, 0x5b), # RICHARD
    0x96: (2, 0x5c), # RICHARD_FROG
    0x97: None,      # DIVE_SPOT
    0x98: (2, 0x5e), # HORSE_PIECE
    0x99: (3, 0x60), # WATER_TEKTITE
    0x9A: lambda room_id: (0, 0x66) if 0x200 <= room_id <= 0x22F else (0, 0xa6), # FLYING_TILES
    0x9B: None,      # HIDING_GEL
    0x9C: (3, 0x60), # STAR
    0x9D: (0, 0xa6), # LIFTABLE_STATUE
    0x9E: None,      # FIREBALL_SHOOTER
    0x9F: (0, 0x5f), # GOOMBA
    0xA0: (0, {0x5f, 0x68}), # PEAHAT
    0xA1: (0, {0x5f, 0x7b}), # SNAKE
    0xA2: (3, 0x64), # PIRANHA_PLANT
    0xA3: (1, 0x65), # SIDE_VIEW_PLATFORM_HORIZONTAL
    0xA4: (1, 0x65), # SIDE_VIEW_PLATFORM_VERTICAL
    0xA5: (1, 0x65), # SIDE_VIEW_PLATFORM
    0xA6: (1, 0x65), # SIDE_VIEW_WEIGHTS
    0xA7: (0, 0x66), # SMASHABLE_PILLAR
    0xA9: (2, 0x5d), # BLOOPER
    0xAA: (2, 0x5d), # CHEEP_CHEEP_HORIZONTAL
    0xAB: (2, 0x5d), # CHEEP_CHEEP_VERTICAL
    0xAC: (2, 0x5d), # CHEEP_CHEEP_JUMPING
    0xAD: (3, 0x67), # KIKI_THE_MONKEY
    0xAE: (1, 0xE3), # WINGED_OCTOROCK
    0xAF: None,      # TRADING_ITEM
    0xB0: (2, 0x8B), # PINCER
    0xB1: (0, 0x7b), # HOLE_FILLER (or 0x77)
    0xB2: (3, 0x8C), # BEETLE_SPAWNER
    0xB3: (3, 0x6B), # HONEYCOMB
    0xB4: (1, 0x6C), # TARIN
    0xB5: (3, 0x69), # BEAR
    0xB6: (3, 0x6D), # PAPAHL
    0xB7: (3, 0x71), # MERMAID
    0xB8: (1, 0xa1, 2, 0x75, 3, 0x4e), # FISHERMAN_UNDER_BRIDGE
    0xB9: (2, 0x79), # BUZZ_BLOB
    0xBA: (3, 0x76), # BOMBER
    0xBB: (3, 0x76), # BUSH_CRAWLER
    0xBC: (2, 0xa9), # GRIM_CREEPER
    0xBD: (2, 0x7a), # VIRE
    0xBE: (2, 0xa7), # BLAINO
    0xBF: (2, 0x82), # ZOMBIE
    0xC0: None,      # MAZE_SIGNPOST
    0xC1: (2, 0x8F), # MARIN_AT_THE_SHORE
    0xC2: (1, 0x6C, 2, 0x8F), # MARIN_AT_TAL_TAL_HEIGHTS
    0xC3: (1, 0x7d, 2, 0x7e, 3, 0x7F), # MAMU_AND_FROGS
    0xC4: (2, 0x6E, 3, 0x6F), # WALRUS
    0xC5: (1, 0x81), # URCHIN
    0xC6: (1, 0x81), # SAND_CRAB
    0xC7: (0, 0xC0, 1, 0xc1, 2, 0xc2, 3, 0xc3), # MANBO_AND_FISHES
    0xCA: (3, 0xc7), # MAD_BATTER
    0xCB: (1, 0x61), # ZORA
    0xCC: (1, 0x4A), # FISH
    0xCD: lambda room_id: (1, 0xCC, 2, 0xCD, 3, 0xCE) if room_id == 0x2DD else (1, 0xD1, 2, 0xD2, 3, 0x6A) if room_id == 0x2FE else (3, 0xD4), # BANANAS_SCHULE_SALE
    0xCE: (3, 0x73), # MERMAID_STATUE
    0xCF: (1, 0xC9, 2, 0xCA, 3, 0xCB), # SEASHELL_MANSION
    0xD0: (1, 0xC4), # ANIMAL_D0
    0xD1: (3, 0xCF), # ANIMAL_D1
    0xD2: (3, 0xCF), # ANIMAL_D2
    0xD3: (1, 0xC4), # BUNNY_D3
    0xD6: (1, 0x65), # SIDE_VIEW_POT
    0xD7: (1, 0x65), # THWIMP
    0xD8: (2, 0xDA, 3, 0xDB), # THWOMP
    0xD9: (1, 0xD9), # THWOMP_RAMMABLE
    0xDA: (3, 0x64), # PODOBOO
    0xDB: (2, 0xDA), # GIANT_BUBBLE
    0xDC: lambda room_id: (0, 0xDD, 2, 0xDE) if room_id == 0x1E4 else (2, 0xD3, 3, 0xDD) if room_id == 0x29F else (3, 0xDC),      # FLYING_ROOSTER_EVENTS
    0xDD: (1, 0xD5), # BOOK
    0xDE: None,      # EGG_SONG_EVENT
    0xE0: (3, 0xD4), # MONKEY
    0xE1: (1, 0xDF), # WITCH_RAT
    0xE2: (3, 0xF4), # FLAME_SHOOTER
    0xE3: (3, 0x8C), # POKEY
    0xE4: (1, 0x80, 3, 0xA5), # MOBLIN_KING
    0xE5: None,      # FLOATING_ITEM_2
    0xE6: (0, 0xe8, 1, 0xe9, 2, 0xea, 3, 0xeb), # FINAL_NIGHTMARE
    0xE7: None,      # KANALET_CASTLE_GATE_SWITCH
    0xE9: (0, 0x04, 1, 0x05), # COLOR_SHELL_RED
    0xEA: (0, 0x04, 1, 0x05), # COLOR_SHELL_GREEN
    0xEB: (0, 0x04, 1, 0x05), # COLOR_SHELL_BLUE
    0xEC: (2, 0x06), # COLOR_GHOUL_RED
    0xED: (2, 0x06), # COLOR_GHOUL_GREEN
    0xEE: (2, 0x06), # COLOR_GHOUL_BLUE
    0xEF: (3, 0x07), # ROTOSWITCH_RED
    0xF0: (3, 0x07), # ROTOSWITCH_YELLOW
    0xF1: (3, 0x07), # ROTOSWITCH_BLUE
    0xF2: (3, 0x07), # FLYING_HOPPER_BOMBS
    0xF3: (3, 0x07), # HOPPER
    0xF4: (0, 0x08, 1, 0x09, 2, 0x0A), # AVALAUNCH
    0xF6: (0, 0x0E, 1, 0x1A), # COLOR_GUARDIAN_BLUE
    0xF7: (0, 0x0E, 1, 0x1A), # COLOR_GUARDIAN_RED
    0xF8: (0, 0x0B, 1, 0x0C, 3, 0x0D), # GIANT_BUZZ_BLOB
    0xF9: (0, 0x11, 2, 0x10), # HARDHIT_BEETLE
    0xFA: lambda room_id: (0, 0x44) if room_id == 0x2F5 else None, # PHOTOGRAPHER
}