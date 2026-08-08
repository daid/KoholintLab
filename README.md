# Koholint Lab

Koholint Lab is a set of tools to assist in editing the [Links Awakening DX disassembly](https://github.com/zladx/LADX-Disassembly/). This is not a "one tool does it all" but a collection of tools and utilities for various purposes.

## Installation

You will need python, bla bla, and the disassembly, and some other requirements... (TODO)

## Map editing

The biggest thing is map editing. LADX uses a reasonably complicated format for map data. But even more complicated, it uses a various combinations of tilesets and palettes to all put it together and editing it directly is fairly difficult to follow.

Koholint Labs map editor tries to fix this. It provides a visual editor for rooms and an overview of the map. Allowing for easy editing and more customization.

This works in a multi step process:

1. Export the room data into json (you only do this once, as this is not perfect)
2. Edit the json data with the editor
3. Import the json back into the disassembly

### 1. Export room data into json
`$ python3 mapeditor.py map.json ../LADX-Disassembly/ --from-disasm`

### 2. Edit room data
`$ python3 mapeditor.py map.json ../LADX-Disassembly/ --edit`
Then open a browser to http://127.0.0.1:8000/

### 3. Import room data into disassembly
`$ python3 mapeditor.py map.json ../LADX-Disassembly/ --to-disasm`
Next build the disassembly and see your changes.