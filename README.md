# ForeverMacros (WoW Forever 1.60.1)

`ForeverMacros/` is the addon folder. `/macros` (or the addon menu at the minimap) opens the window.

Rebuild Data.lua after editing build/macros.py (needs the 70532 CSV tables from wago.tools in a db/ folder):

    python3 -I build/build.py db ForeverMacros/Data.lua
    cd test && luajit test.lua ../ForeverMacros

The test needs test/fixtures.lua (generated from the same tables).
