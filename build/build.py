"""Resolves macros.py against WoW Forever 1.60.1.70532 tables and writes the addon's Data.lua.
Fails loudly on anything unresolved, too long, or ambiguous. Usage: python3 -I build.py <db dir> <out Data.lua>"""
import csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from macros import MACROS, RACIALS, RACIAL_NAMES, UTILITY

DB, OUT = sys.argv[1], sys.argv[2]
CLASS_ID = {"WARRIOR": 1, "PALADIN": 2, "HUNTER": 3, "ROGUE": 4, "PRIEST": 5, "SHAMAN": 7, "MAGE": 8, "WARLOCK": 9, "DRUID": 11}
RANK_SUFFIX = len("(Rang 12)")
TOKEN = re.compile(r"\{(=?)([^{}]+)\}|<([^<>]+)>")


def rows(name): return list(csv.DictReader(open(os.path.join(DB, name), encoding="utf-8")))


spell_en = {r["ID"]: r["Name_lang"] for r in rows("SpellName.csv")}
spell_de = {r["ID"]: r["Name_lang"] for r in rows("SpellName_deDE.csv")}
by_name = {}
for sid, n in spell_en.items(): by_name.setdefault(n, []).append(int(sid))
skill_cat = {r["ID"]: int(r["CategoryID"]) for r in rows("SkillLine.csv")}
sla = {}
for r in rows("SkillLineAbility.csv"): sla.setdefault(int(r["Spell"]), []).append((r["SkillLine"], int(r["ClassMask"])))
item_en, item_de = {}, {}
for r in rows("ItemSparse.csv"): item_en.setdefault(r["Display_lang"], []).append(int(r["ID"]))
for r in rows("ItemSparse_deDE.csv"): item_de[int(r["ID"])] = r["Display_lang"]

errors, warnings = [], []
spells, items = {}, {}   # key -> ids


def resolve_spell(name, cls):
    ids = by_name.get(name, [])
    if not ids: errors.append(f"spell not in 70532: {name!r} ({cls})"); return None
    bit = 1 << (CLASS_ID[cls] - 1) if cls in CLASS_ID else None
    chosen = []
    for sid in ids:
        for line, mask in sla.get(sid, []):
            cat = skill_cat.get(line)
            if bit is not None:
                if cat in (6, 7) and (mask in (0, -1) or mask & bit): chosen.append(sid); break
            else:
                if cat in (9, 11): chosen.append(sid); break
    if not chosen:
        errors.append(f"spell {name!r} exists ({ids[:6]}) but not in a {cls} skill line")
        return None
    return sorted(set(chosen))


def resolve_item(name):
    ids = item_en.get(name, [])
    if not ids: errors.append(f"item not in 70532: {name!r}"); return None
    if len(ids) > 1: warnings.append(f"item {name!r} has several ids {ids}; using {min(ids)} (same name, /use by name covers all)")
    return min(ids)


def lua_str(s): return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def process(mid, cls, name_de, name_en, body, note):
    if len(name_de.encode()) > 16 or len(name_en.encode()) > 16: errors.append(f"{mid}: name over 16 bytes ({name_de!r}/{name_en!r})")
    worst = 0; parts = []; pos = 0; refs = []
    for m in TOKEN.finditer(body):
        worst += len(body[pos:m.start()].encode()); pos = m.end()
        plain, sname, iname = m.group(1), m.group(2), m.group(3)
        if iname is not None:
            iid = resolve_item(iname)
            if iid is None: continue
            items[iid] = iname
            worst += max(len(iname.encode()), len(item_de.get(iid, iname).encode()))
            refs.append(("I", iid))
        else:
            alts = []
            for alt in sname.split("|"):
                ids = resolve_spell(alt, cls)
                if ids is None: continue
                key = f"{cls}:{alt}"; spells[key] = ids; alts.append(key)
                worst_alt = max(max(len(spell_en[str(i)].encode()), len(spell_de.get(str(i), "").encode())) for i in ids)
            if not alts: continue
            worst += max(max(max(len(spell_en[str(i)].encode()), len(spell_de.get(str(i), "").encode())) for i in spells[k]) for k in alts) + (0 if plain else RANK_SUFFIX)
            refs.append(("P" if plain else "S", alts))
    worst += len(body[pos:].encode())
    if worst > 255: errors.append(f"{mid}: worst-case length {worst} > 255")
    return worst, refs


out_macros = []
for mid, cls, nde, nen, body, note in MACROS:
    w, refs = process(mid, cls, nde, nen, body, note); out_macros.append((mid, "class", cls, nde, nen, body, note, w))
for mid, spell in RACIALS:
    body = "#showtooltip {%s}\n/cast {%s}" % (spell, spell)
    nde, nen = RACIAL_NAMES.get(mid, (None, None))
    w, refs = process(mid, "RACE", nde or spell, nen or spell, body, None); out_macros.append((mid, "race", "RACE", nde, nen, body, None, w))
for mid, group, nde, nen, body, note in UTILITY:
    w, refs = process(mid, "UTILITY", nde, nen, body, note); out_macros.append((mid, "utility", group, nde, nen, body, note, w))

ids = [m[0] for m in out_macros]
for d in {i for i in ids if ids.count(i) > 1}: errors.append(f"duplicate id {d}")
for scope in ("class", "utility"):
    seen = {}
    for m in out_macros:
        if m[1] != scope: continue
        for n in (m[3], m[4]):
            k = (m[2] if scope == "class" else "", n)
            if n and k in seen and seen[k] != m[0]: errors.append(f"duplicate name {n!r}: {seen[k]} / {m[0]}")
            seen[k] = m[0]

# racial macro names (spell names in both languages) must not collide with class or utility names
racial_names = set()
for mid, spell in RACIALS:
    nde, nen = RACIAL_NAMES.get(mid, (None, None))
    for sid in by_name.get(spell, []):
        if any(skill_cat.get(l) == 9 for l, _ in sla.get(sid, [])):
            racial_names.add(nde or spell_de.get(str(sid), spell)[:16]); racial_names.add(nen or spell[:16]); break
for m in out_macros:
    if m[1] in ("class", "utility"):
        for n in (m[3], m[4]):
            if n in racial_names: errors.append(f"{m[0]}: name {n!r} collides with a racial macro")

for w in warnings: print("WARN", w)
if errors:
    for e in errors: print("ERROR", e)
    sys.exit(1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("-- Generated by build.py from WoW Forever 1.60.1.70532 tables (SpellName, SkillLineAbility, ItemSparse). Do not edit.\n")
    f.write("local _, ns = ...\n\nns.BUILD = \"1.60.1.70532\"\n\n-- spell key -> every spell id (ranks) with that name in the class/profession skill lines\nns.SPELLS = {\n")
    for k in sorted(spells): f.write(f"\t[{lua_str(k)}] = {{ {', '.join(map(str, spells[k]))} }},\n")
    f.write("}\n\n-- item id -> English name (the game resolves the localized name at install time)\nns.ITEMS = {\n")
    for k in sorted(items): f.write(f"\t[{k}] = {lua_str(items[k])},\n")
    f.write("}\n\n-- id, scope (class|race|utility), class token or utility group, German name, English name, body, German note\nns.MACROS = {\n")
    for mid, scope, group, nde, nen, body, note, w in out_macros:
        # tokens rewritten to keys: {S:key|key}, {P:key}, {I:id}
        def sub(m):
            plain, sname, iname = m.group(1), m.group(2), m.group(3)
            if iname is not None: return "{I:%d}" % min(item_en[iname])
            cls = group if scope == "class" else ("RACE" if scope == "race" else "UTILITY")
            return "{%s:%s}" % ("P" if plain else "S", "|".join(f"{cls}:{a}" for a in sname.split("|")))
        tb = TOKEN.sub(sub, body)
        f.write(f"\t{{ id = {lua_str(mid)}, scope = {lua_str(scope)}, group = {lua_str(group)}, "
                + (f"nameDE = {lua_str(nde)}, nameEN = {lua_str(nen)}, " if nde else "")
                + f"body = {lua_str(tb)}" + (f", note = {lua_str(note)}" if note else "") + " },\n")
    f.write("}\n")
print(f"OK: {len(out_macros)} macros, {len(spells)} spells, {len(items)} items; longest worst case "
      f"{max(m[7] for m in out_macros)} bytes ({max(out_macros, key=lambda m: m[7])[0]})")
