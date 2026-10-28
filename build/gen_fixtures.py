"""Writes test/fixtures.lua: English and German name and rank text of every spell and item Data.lua uses, from the
same 70532 tables build.py reads. Usage: python3 -I gen_fixtures.py <db dir> <Data.lua> <out fixtures.lua>"""
import csv, os, re, sys

DB, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]


def rows(name): return list(csv.DictReader(open(os.path.join(DB, name), encoding="utf-8")))


data = open(DATA, encoding="utf-8").read()
spells_block = data[data.index("ns.SPELLS = {"):data.index("ns.ITEMS = {")]
items_block = data[data.index("ns.ITEMS = {"):data.index("ns.MACROS = {")]
spell_ids = sorted({int(i) for ids in re.findall(r"= \{ ([\d, ]+) \}", spells_block) for i in ids.split(", ")})
item_ids = sorted(int(i) for i in re.findall(r"\[(\d+)\] =", items_block))

name = {"enUS": {r["ID"]: r["Name_lang"] for r in rows("SpellName.csv")},
        "deDE": {r["ID"]: r["Name_lang"] for r in rows("SpellName_deDE.csv")}}
sub = {"enUS": {r["ID"]: r["NameSubtext_lang"] for r in rows("Spell.csv")},
       "deDE": {r["ID"]: r["NameSubtext_lang"] for r in rows("Spell_deDE.csv")}}
item = {"enUS": {r["ID"]: r["Display_lang"] for r in rows("ItemSparse.csv")},
        "deDE": {r["ID"]: r["Display_lang"] for r in rows("ItemSparse_deDE.csv")}}


def lua(s): return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


out = ["FIX = { spell = {}, item = {} }"]
for loc in ("enUS", "deDE"):
    out.append(f"FIX.spell.{loc} = {{")
    for i in spell_ids:
        n = name[loc].get(str(i)) or name["enUS"].get(str(i), "")
        out.append(f"[{i}]={{{lua(n)},{lua(sub[loc].get(str(i), ''))}}},")
    out.append("}")
    out.append(f"FIX.item.{loc} = {{")
    for i in item_ids:
        out.append(f"[{i}]={lua(item[loc].get(str(i)) or item['enUS'][str(i)])},")
    out.append("}")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"fixtures: {len(spell_ids)} spells, {len(item_ids)} items")
