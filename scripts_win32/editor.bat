@echo off
mkdir data
support\\bin\\python.exe KoholintLab\\mapeditor.py data/map.json src/LADX-Origonal --from-disasm
support\\bin\\python.exe KoholintLab\\mapeditor.py data/map.json src/LADX-Hack --edit --to-disasm
