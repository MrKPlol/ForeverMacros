"""Resolves macros.py against WoW Forever 1.60.1.70532 tables and writes the addon's Data.lua.
Fails loudly on anything unresolved, too long, or ambiguous. Usage: python3 -I build.py <db dir> <out Data.lua>"""
import csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from macros import MACROS, RACIALS, RACIAL_NAMES, UTILITY

DB, OUT = sys.argv[1], sys.argv[2]
CLASS_ID = {"WARRIOR": 1, "PALADIN": 2, "HUNTER": 3, "ROGUE": 4, "PRIEST": 5, "SHAMAN": 7, "MAGE": 8, "WARLOCK": 9, "DRUID": 11}
RANK_SUFFIX = len("(Rang 12)")
TOKEN = re.compile(r"\{(=?)(?!T:)([^{}]+)\}|<([^<>]+)>")
TARGET = re.compile(r"\{T:([a-z]+)(?::([^{}]*))?\}")
# Mirror of ns.TARGETS in Core.lua: clause per option, in priority order. ground options exclude each other.
CLAUSES = {
    "help": ["@mouseover,help,nodead", "@focus,help,nodead", "help,nodead", "@player"],
    "harm": ["@mouseover,harm,nodead", "@focus,harm,nodead", "harm,nodead"],
    "any": ["@mouseover,exists,nodead", "@focus,exists,nodead", "exists,nodead"],
    "dead": ["@mouseover,help,dead", "@focus,help,dead", "help,dead"],
    "unit": ["@mouseover,exists,nodead", "@focus,exists,nodead", ""],   # last: always, plain
    "ground": ["@cursor", "@player"],
}


def target_worst(kind, cond):
    """Longest text a {T:kind:cond} token can become with any option set."""
    def clause(c): return "[" + ",".join(x for x in (cond, c) if x) + "]"
    if kind == "ground": return max(len(clause(c)) for c in CLAUSES[kind])
    return sum(len(clause(c)) for c in CLAUSES[kind])


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
    kinds = {m.group(1) for m in TARGET.finditer(body)}
    for k in kinds:
        if k not in CLAUSES: errors.append(f"{mid}: unknown target kind {k!r}")
    if len(kinds) > 1: errors.append(f"{mid}: several target kinds {sorted(kinds)}")
    worst = sum(target_worst(m.group(1), m.group(2)) for m in TARGET.finditer(body) if m.group(1) in CLAUSES)
    body = TARGET.sub("", body)
    parts = []; pos = 0; refs = []
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
for mid, body, note in RACIALS:
    spell = re.search(r"\{([^{}|=]+)\}", body).group(1)
    nde, nen = RACIAL_NAMES.get(mid, (None, None))
    w, refs = process(mid, "RACE", nde or spell, nen or spell, body, note); out_macros.append((mid, "race", "RACE", nde, nen, body, note, w))
for mid, group, nde, nen, body, note in UTILITY:
    w, refs = process(mid, "UTILITY", nde, nen, body, note); out_macros.append((mid, "utility", group, nde, nen, body, note, w))

# ---------------- Spell tab: every active class spell, with what the window may offer for it ----------------
# Class skill lines (category 7) whose class-masked rows all belong to one class; pet, rune and engraving lines are
# not spellbook trees. Talents sit in the same lines with class mask 0.
misc = {r["SpellID"]: r for r in rows("SpellMisc.csv") if r["DifficultyID"] == "0"}
effects = {}
for r in rows("SpellEffect.csv"):
    if r["DifficultyID"] == "0": effects.setdefault(r["SpellID"], []).append(r)
shapeshift = {r["SpellID"]: int(r["ShapeshiftMask_0"]) for r in rows("SpellShapeshift.csv")}
line_rows = {r["ID"]: r for r in rows("SkillLine.csv")}
line_de = {r["ID"]: r["DisplayName_lang"] for r in rows("SkillLine_deDE.csv")}
NOT_TREES = {"261", "777", "778", "2851", "2853", "2898"}   # Beast Training, Mounts, Companions, Engraving, Runes, Explorer Imp
line_class = {}
for r in rows("SkillLineAbility.csv"):
    l = line_rows.get(r["SkillLine"]); mask = int(r["ClassMask"])
    if not l or l["CategoryID"] != "7" or l["ID"] in NOT_TREES or l["DisplayName_lang"].startswith("Pet - "): continue
    if mask not in (0, -1): line_class.setdefault(l["ID"], set()).add(mask)
CLASS_OF_BIT = {1 << (i - 1): c for c, i in CLASS_ID.items()}
line_class = {l: CLASS_OF_BIT[next(iter(m))] for l, m in line_class.items() if len(m) == 1 and next(iter(m)) in CLASS_OF_BIT}

book = {}   # class -> name -> (line, ids)
for r in rows("SkillLineAbility.csv"):
    cls = line_class.get(r["SkillLine"]); sid = r["Spell"]; mask = int(r["ClassMask"])
    if not cls or (mask not in (0, -1) and not mask & (1 << (CLASS_ID[cls] - 1))): continue
    m = misc.get(sid); effs = effects.get(sid, [])
    if not m or int(m["Attributes_0"]) & 0x40 or not effs: continue                   # passive or no effect
    if all(int(e["Effect"]) in (36, 47) for e in effs): continue                       # only teaches spells
    n = spell_en.get(sid)
    if not n or n.endswith(" Effect"): continue
    line, idl = book.setdefault(cls, {}).setdefault(n, (r["SkillLine"], []))
    idl.append(int(sid))

FORM_CASTER = 0x40000002      # Moonkin / Tree of Life: forms that still cast caster spells
FORM_CAT, FORM_BEAR = 0x1, 0x90
STANCES = [(0x10000, "1", "Battle Stance"), (0x20000, "2", "Defensive Stance"), (0x40000, "3", "Berserker Stance")]


def spell_kind(sid):
    effs = effects[str(sid)]
    tg = {int(e[k]) for e in effs for k in ("ImplicitTarget_0", "ImplicitTarget_1")} - {0}
    codes = {int(e["Effect"]) for e in effs}
    if codes & {18, 113, 329} or 121 in tg: return "dead"
    if tg & {16, 87}: return "ground"
    if 6 in tg: return "harm"
    if tg & {21, 56, 57, 31, 132}: return "help"
    if 25 in tg: return "any"
    return None


def spell_flags(cls, name, sid):
    """c = channelled, t = toggles off when cast again, f/b = needs Cat/Bear Form, x = caster spell (druid),
    s<digits> = warrior stances it allows."""
    m, effs = misc[str(sid)], effects[str(sid)]
    auras = {int(e["EffectAura"]) for e in effs}
    flags = ""
    if int(m["Attributes_1"]) & 0x44: flags += "c"
    if auras & {16, 36} or int(m["Attributes_2"]) & 0x20 or name.startswith("Aspect of"): flags += "t"
    mask = shapeshift.get(str(sid), 0)
    if cls == "DRUID" and 36 not in auras:
        if mask & FORM_CASTER == 0 and mask & FORM_CAT and not mask & FORM_BEAR: flags += "f"
        elif mask & FORM_CASTER == 0 and mask & FORM_BEAR and not mask & FORM_CAT: flags += "b"
        elif mask & ~FORM_CASTER == 0: flags += "x"
    if cls == "WARRIOR":
        allowed = [idx for bit, idx, _ in STANCES if mask & bit]
        if 0 < len(allowed) < 3: flags += "s" + "".join(allowed)
    return flags


def cut16(s):
    b = s.encode()[:16]
    while True:
        try: return b.decode()
        except UnicodeDecodeError: b = b[:-1]


def macro_name(s, protect=()):
    """Spell name as a 16-byte macro name: the longest words shrink to initials first ("Fire R. Aura"), the last
    word and the words in protect (those that tell colliding names apart) last."""
    if len(s.encode()) <= 18 and not protect: return cut16(s)   # losing a letter or two reads better
    words = s.split(" ")
    order = sorted(range(len(words)), key=lambda i: (words[i] in protect, i == len(words) - 1, -len(words[i]), i))
    for i in order:
        full = [w for w in words if len(w) > 2 and not w.endswith(".")]
        if len(" ".join(words).encode()) <= 16 or len(full) <= 1: break   # keep at least one word whole
        if len(words[i]) > 2: words[i] = words[i][0] + "."
    return cut16(" ".join(words))


def macro_names(full):
    """key -> full name  =>  key -> macro name; names that still collide keep the words that differ."""
    names = {k: macro_name(n) for k, n in full.items()}
    groups = {}
    for k, n in names.items(): groups.setdefault(n, []).append(k)
    for keys in groups.values():
        if len(keys) < 2: continue
        word_sets = [set(full[k].split(" ")) for k in keys]
        common = set.intersection(*word_sets)
        for k in keys: names[k] = macro_name(full[k], set(full[k].split(" ")) - common)
    return names


spellbook, lines_used = {}, set()
for cls in sorted(book):
    entries, full_de, full_en = [], {}, {}
    for name, (line, idl) in sorted(book[cls].items()):
        idl = sorted(set(idl)); top = max(idl)
        key = f"{cls}:{name}"
        if key in spells and spells[key] != idl: spells[key] = sorted(set(spells[key]) | set(idl))
        else: spells.setdefault(key, idl)
        flags = spell_flags(cls, name, top)
        if "f" in flags or "b" in flags:
            form = "Cat Form" if "f" in flags else "Bear Form"
            spells.setdefault(f"DRUID:{form}", sorted(book["DRUID"][form][1]))
            if form == "Bear Form": spells.setdefault("DRUID:Dire Bear Form", sorted(book["DRUID"]["Dire Bear Form"][1]))
        if "s" in flags:
            for _, idx, stance in STANCES: spells.setdefault(f"WARRIOR:{stance}", sorted(book["WARRIOR"][stance][1]))
        full_de[key], full_en[key] = spell_de.get(str(top)) or name, name
        entries.append((key, line, spell_kind(top), flags)); lines_used.add(line)
    names_de, names_en = macro_names(full_de), macro_names(full_en)
    for names in (names_de, names_en):
        seen = {}
        for k, n in sorted(names.items()):
            if n in seen: warnings.append(f"{cls}: spells {seen[n]!r} and {k!r} share the macro name {n!r} (window shows the first)")
            seen.setdefault(n, k)
    spellbook[cls] = [(k, l, kind, fl, names_de[k] if names_de[k] != full_de[k] else None,
                       names_en[k] if names_en[k] != full_en[k] else None) for k, l, kind, fl in entries]
    # a ready-made class macro named like a spell would fight over the same character-tab slot
    for m in out_macros:
        if m[1] == "class" and m[2] == cls and (m[3] in names_de.values() or m[4] in names_en.values()):
            errors.append(f"{m[0]}: name {m[3]!r}/{m[4]!r} equals a {cls} spell macro name")

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
for mid, rbody, _ in RACIALS:
    spell = re.search(r"\{([^{}|=]+)\}", rbody).group(1)
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
                + f"body = {lua_str(tb)}"
                + (f", target = {lua_str(TARGET.search(body).group(1))}" if TARGET.search(body) else "") + (f", note = {lua_str(note)}" if note else "") + " },\n")
    f.write("}\n\n-- spell tab: skill line id -> German name, English name\nns.LINES = {\n")
    for l in sorted(lines_used, key=int):
        f.write(f"\t[{l}] = {{ {lua_str(line_de.get(l) or line_rows[l]['DisplayName_lang'])}, {lua_str(line_rows[l]['DisplayName_lang'])} }},\n")
    f.write("}\n\n-- spell tab: class -> { spell key, skill line, target kind or false, flags (see build.py spell_flags)[, German and\n-- English macro name where the spell name is over 16 bytes] }\nns.SPELLBOOK = {\n")
    for cls in sorted(spellbook):
        f.write(f"\t{cls} = {{\n")
        for key, line, kind, flags, nde, nen in spellbook[cls]:
            names = f", {lua_str(nde) if nde else 'false'}, {lua_str(nen) if nen else 'false'}" if nde or nen else ""
            f.write(f"\t\t{{ {lua_str(key)}, {line}, {lua_str(kind) if kind else 'false'}, {lua_str(flags)}{names} }},\n")
        f.write("\t},\n")
    f.write("}\n")
print(f"OK: {len(out_macros)} macros, {sum(len(v) for v in spellbook.values())} spell-tab spells, {len(spells)} spells, {len(items)} items; longest worst case "
      f"{max(m[7] for m in out_macros)} bytes ({max(out_macros, key=lambda m: m[7])[0]})")
