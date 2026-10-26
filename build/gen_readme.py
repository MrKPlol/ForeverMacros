"""Writes README.md (usage + every macro in the addon) from macros.py. Usage: python3 -I build/gen_readme.py README.md"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from macros import MACROS, RACIALS, RACIAL_NAMES, UTILITY

CLASSES = [("DRUID", "Druide / Druid"), ("WARRIOR", "Krieger / Warrior"), ("PALADIN", "Paladin"), ("HUNTER", "Jäger / Hunter"),
           ("ROGUE", "Schurke / Rogue"), ("PRIEST", "Priester / Priest"), ("SHAMAN", "Schamane / Shaman"),
           ("MAGE", "Magier / Mage"), ("WARLOCK", "Hexenmeister / Warlock")]
GROUPS = [("general", "Allgemein / General"), ("equip", "Ausrüstung / Equipment"), ("items", "Gegenstände / Items"),
          ("quests", "Quests"), ("professions", "Berufe / Professions")]


def plain(body):
    body = re.sub(r"\{=?([^{}|]+)(\|[^{}]*)?\}", r"\1", body)   # {A|B} -> A (the addon takes the first one you know)
    return re.sub(r"<([^<>]+)>", r"\1", body)


def entry(name_de, name_en, body, note):
    title = name_de if name_de == name_en else f"{name_de} / {name_en}"
    out = [f"**{title}**" + (f" – {note}" if note else ""), "", "```", plain(body), "```", ""]
    return "\n".join(out)


lines = []
add = lines.append
total = len(MACROS) + len(RACIALS) + len(UTILITY)
add("# ForeverMacros")
add("")
add("Fertige Klassen-, Rassen- und Utility-Makros für **WoW Forever (1.60.1)**, mit einem Klick eingebaut.  ")
add("Ready-made class, race and utility macros for **WoW Forever (1.60.1)**, installed with one click.")
add("")
add("## Installation")
add("")
add("1. [ZIP aus den Releases laden](https://github.com/MrKPlol/ForeverMacros/releases/latest) / download the ZIP from the releases.")
add("2. Entpacken nach / unzip into `World of Warcraft/_forever_/Interface/AddOns/` (danach gibt es dort den Ordner `ForeverMacros`).")
add("3. Ingame `/macros` eingeben oder das AddOn-Menü an der Minimap nutzen / type `/macros` or use the addon menu at the minimap.")
add("")
add("## Was es macht / What it does")
add("")
add("- Makros anhaken, mit der Maus drüberfahren zeigt das fertige Makro, **Einbauen** legt sie an.")
add("- Klassen-, Rassen- und Ausrüstungsset-Makros kommen in den **Charakter-Tab**, alles andere in den **allgemeinen Tab** (für alle Charaktere).")
add("- Zauber- und Gegenstandsnamen werden in der **Sprache deines Clients** eingesetzt (Deutsch, Englisch, …).")
add("- Forever hat die Zauberränge neu angelegt: ein Name ohne Rang kann auf einen Rang zeigen, den du noch nicht kannst. "
    "Das Addon setzt den **höchsten Rang ein, den du kennst** (z. B. `Charge(Rank 1)`) und zieht ihn beim Leveln automatisch nach.")
add("- Überschreibt **nie** Makros, die du selbst angelegt oder geändert hast, und ändert nichts im Kampf.")
add("- `A|B` in der Liste unten heißt: das Addon nimmt den ersten Zauber, den du kannst (z. B. Terrorbärgestalt, sonst Bärengestalt). "
    "In der Liste steht jeweils der erste.")
add("")
add(f"## Alle {total} Makros / All {total} macros")
add("")
add("Die Liste zeigt die englischen Namen; im Spiel stehen die Namen deines Clients.  ")
add("The list shows English spell names; in game the addon uses your client's language.")
add("")
add("### Klassen / Classes")
add("")
for token, title in CLASSES:
    macros = [m for m in MACROS if m[1] == token]
    add(f"<details><summary><b>{title}</b> ({len(macros)})</summary>")
    add("")
    for mid, cls, nde, nen, body, note in macros: add(entry(nde, nen, body, note))
    add("</details>")
    add("")
add("### Rassen / Races")
add("")
add(f"<details><summary><b>Rassenfähigkeiten / Racial abilities</b> ({len(RACIALS)})</summary>")
add("")
add("Im Fenster erscheinen nur die Fähigkeiten, die dein Charakter hat. Jedes Makro: `#showtooltip <Fähigkeit>` + `/cast <Fähigkeit>`.")
add("")
for mid, spell in RACIALS:
    nde, nen = RACIAL_NAMES.get(mid, (None, None))
    add(f"- {spell}" + (f" (Makroname / macro name: {nde} / {nen})" if nde else ""))
add("")
add("</details>")
add("")
add("### Utility (allgemeiner Tab / general tab)")
add("")
for group, title in GROUPS:
    macros = [m for m in UTILITY if m[1] == group]
    add(f"<details><summary><b>{title}</b> ({len(macros)})</summary>")
    add("")
    for mid, grp, nde, nen, body, note in macros: add(entry(nde, nen, body, note))
    add("</details>")
    add("")
add("<details><summary><b>Ausrüstungssets / Equipment sets</b></summary>")
add("")
add("Für jedes Ausrüstungsset deines Charakters bietet das Fenster ein Makro `/equipset <Setname>` an (Charakter-Tab).  ")
add("For every equipment set of your character the window offers a `/equipset <set name>` macro (character tab).")
add("")
add("</details>")
add("")
add("## Entwicklung / Development")
add("")
add("- `build/macros.py`: die Makros (`{Zauber}`, `{=Zauber}` ohne Rang, `{A|B}` erster bekannter, `<Gegenstand>`).")
add("- `python3 -I build/build.py db ForeverMacros/Data.lua`: prüft jeden Namen gegen die Client-Tabellen von 1.60.1.70532 "
    "(CSV von wago.tools in `db/`) und jede Länge (255 Zeichen im ungünstigsten Fall) und schreibt `Data.lua`.")
add("- `python3 -I build/gen_readme.py README.md`: erzeugt diese README.")
add("- `cd test && luajit test.lua ../ForeverMacros`: Test mit nachgebauter WoW-API (alle Klassen, Deutsch/Englisch, niedrige/hohe Ränge).")
add("")
add("## Quellen / Credits")
add("")
add("Makrotexte angepasst nach / macro texts adapted from [Classic WoW Forever](https://classicwowforever.com/macros/) "
    "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) und [Zockify](https://www.zockify.com/forever/druid/macros/). "
    "Änderungen: Namen aus IDs lokalisiert, Ränge automatisch, einige Makros gekürzt. Details: `ForeverMacros/CREDITS.txt`.")
add("")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines))
print("README:", total, "macros,", len(lines), "lines")
