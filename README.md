# ForeverMacros

Fertige Klassen-, Rassen- und Utility-Makros für **WoW Forever (1.60.1)**, mit einem Klick eingebaut.  
Ready-made class, race and utility macros for **WoW Forever (1.60.1)**, installed with one click.

## Installation

1. [ZIP aus den Releases laden](https://github.com/MrKPlol/ForeverMacros/releases/latest) / download the ZIP from the releases.
2. Entpacken nach / unzip into `World of Warcraft/_forever_/Interface/AddOns/` (danach gibt es dort den Ordner `ForeverMacros`).
3. Ingame `/macros` eingeben oder das AddOn-Menü an der Minimap nutzen / type `/macros` or use the addon menu at the minimap.

## Was es macht / What it does

- Makros anhaken, mit der Maus drüberfahren zeigt das fertige Makro, **Einbauen** legt sie an.
- Klassen-, Rassen- und Ausrüstungsset-Makros kommen in den **Charakter-Tab**, alles andere in den **allgemeinen Tab** (für alle Charaktere).
- Zauber- und Gegenstandsnamen werden in der **Sprache deines Clients** eingesetzt (Deutsch, Englisch, …).
- Forever hat die Zauberränge neu angelegt: ein Name ohne Rang kann auf einen Rang zeigen, den du noch nicht kannst. Das Addon setzt den **höchsten Rang ein, den du kennst** (z. B. `Charge(Rank 1)`) und zieht ihn beim Leveln automatisch nach.
- Überschreibt **nie** Makros, die du selbst angelegt oder geändert hast, und ändert nichts im Kampf.
- `A|B` in der Liste unten heißt: das Addon nimmt den ersten Zauber, den du kannst (z. B. Terrorbärgestalt, sonst Bärengestalt). In der Liste steht jeweils der erste.

## Alle 154 Makros / All 154 macros

Die Liste zeigt die englischen Namen; im Spiel stehen die Namen deines Clients.  
The list shows English spell names; in game the addon uses your client's language.

### Klassen / Classes

<details><summary><b>Druide / Druid</b> (26)</summary>

**Schreddern/Shift / Shred/Shift** – Shred; Shift: Shifting Power (Mana in Energie)

```
#showtooltip
/startattack [nomod:shift,harm,nodead]
/cast [mod:shift] Shifting Power; [harm,nodead] Shred
```

**Schleichen / Prowl** – Katzengestalt falls nötig, dann Schleichen (bricht es nicht ab)

```
#showtooltip Prowl
/cast !Cat Form
/cast !Prowl
```

**Spurt / Dash** – Katzengestalt falls nötig, dann Spurt

```
#showtooltip Dash
/cast !Cat Form
/cast Dash
```

**Katze/Bär / Cat/Bear** – Katze; Shift: Bär (Terrorbär sobald gelernt)

```
#showtooltip [mod:shift] Dire Bear Form; Cat Form
/dismount
/cast [mod:shift] Dire Bear Form; Cat Form
```

**Reisen / Travel** – Wasser: Wassergestalt, draußen: Reisegestalt, drinnen: Katze

```
#showtooltip
/dismount
/cast [swimming] Aquatic Form; [outdoors] Travel Form; Cat Form
```

**Feenfeuer / Faerie Fire** – Mouseover, sonst Ziel

```
#showtooltip Faerie Fire
/cast [@mouseover,harm,nodead][harm,nodead] Faerie Fire
```

**Wilde Attacke / Feral Charge** – Mouseover, sonst Ziel (Talent)

```
#showtooltip Feral Charge
/cast [@mouseover,harm,nodead][harm,nodead] Feral Charge
```

**Berserk (Druide) / Berserk (Druid)** – Talent ab 40

```
#showtooltip Berserk
/cast Berserk
```

**Baumrinde/NG / Barkskin/NG** – Baumrinde; Shift: Griff der Natur (ohne Formwechsel)

```
#showtooltip [mod:shift] Nature's Grasp; Barkskin
/cast [mod:shift] Nature's Grasp; Barkskin
```

**Urbiss / Primal Bite** – Bär, Talent ab 25

```
#showtooltip Primal Bite
/startattack [harm,nodead]
/cast [harm,nodead] Primal Bite
```

**Aufschlitzen / Lacerate** – Terrorbär ab 42

```
#showtooltip Lacerate
/cast [@mouseover,harm,nodead][harm,nodead] Lacerate
```

**Knurren / Growl** – Spott auf Mouseover/Ziel (Bär)

```
#showtooltip Growl
/cast [@mouseover,harm,nodead][harm,nodead] Growl
```

**Verjüngung MO / Rejuv MO**

```
#showtooltip Rejuvenation
/cancelform
/cast [@mouseover,help,nodead][help,nodead][@player] Rejuvenation
```

**Nachwachsen MO / Regrowth MO**

```
#showtooltip Regrowth
/cancelform
/cast [@mouseover,help,nodead][help,nodead][@player] Regrowth
```

**Heilen / Heal** – Heilende Berührung; Shift: Nachwachsen (Mouseover/selbst)

```
#showtooltip Healing Touch
/cancelform
/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] Regrowth; [@mouseover,help,nodead][@player] Healing Touch
```

**NS + Heilen / NS + Heal** – Schnelligkeit der Natur + sofortige Heilende Berührung

```
#showtooltip Nature's Swiftness
/stopcasting
/cancelform
/cast Nature's Swiftness
/cast [@mouseover,help,nodead][help,nodead][@player] Healing Touch
```

**Rasche Heilung / Swiftmend** – Talent

```
#showtooltip Swiftmend
/cancelform
/cast [@mouseover,help,nodead][help,nodead][@player] Swiftmend
```

**Wildwuchs / Wild Growth** – Talent

```
#showtooltip Wild Growth
/cancelform
/cast [@mouseover,help,nodead][help,nodead][@player] Wild Growth
```

**Fluch aufheben / Remove Curse**

```
#showtooltip Remove Curse
/cancelform
/cast [@mouseover,help,nodead][help,nodead][@player] Remove Curse
```

**Gift heilen / Cure Poison** – Shift: Vergiftung aufheben

```
#showtooltip Cure Poison
/cancelform
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Abolish Poison; [@mouseover,help,nodead][help,nodead][@player] Cure Poison
```

**Anregen MO / Innervate MO**

```
#showtooltip Innervate
/cast [@mouseover,help,nodead][help,nodead][@player] Innervate
```

**Wiederbeleben / Rebirth/Revive** – Kampf: Wiedergeburt, sonst Wiederbeleben

```
#showtooltip [combat] Rebirth; Revive
/cast [@mouseover,help,dead,combat][help,dead,combat] Rebirth
/cast [@mouseover,help,dead,nocombat][help,dead,nocombat] Revive
```

**Mal/Dornen / MotW/Thorns** – Mal der Wildnis; Shift: Dornen

```
#showtooltip [mod:shift] Thorns; Mark of the Wild
/cancelform
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Thorns; [@mouseover,help,nodead][help,nodead][@player] Mark of the Wild
```

**Wurzeln MO / Roots MO**

```
#showtooltip Entangling Roots
/cancelform
/cast [@mouseover,harm,nodead][harm,nodead] Entangling Roots
```

**Hurrikan / Hurricane** – Direkt an der Mausposition

```
#showtooltip Hurricane
/cancelform
/cast [@cursor] Hurricane
```

**Form weg / Drop form** – Zauber abbrechen, Gestalt verlassen, absitzen

```
/stopcasting
/cancelform
/dismount
```

</details>

<details><summary><b>Krieger / Warrior</b> (8)</summary>

**Sturmangriff / Charge**

```
#showtooltip Charge
/dismount
/startattack
/cast Charge
```

**Charge/Abfangen / Charge/Intercept** – Außerhalb Kampf Sturmangriff, im Kampf Abfangen (mit Haltungswechsel)

```
#show [combat] Intercept; Charge
/startattack
/cast [nocombat,stance:1] Charge; [combat,stance:3] Intercept; [nocombat,nostance:1] Battle Stance; [combat,nostance:3] Berserker Stance
```

**Siegesrausch / Victory Rush**

```
#showtooltip Victory Rush
/startattack
/cast Victory Rush
```

**Berserkerwut / Berserker Rage**

```
#showtooltip Berserker Rage
/cast [nostance:3] Berserker Stance
/cast Berserker Rage
```

**Hinrichten / Execute** – Shift: auf Mouseover

```
#showtooltip Execute
/startattack
/cast [stance:2] Battle Stance
/cast [mod:shift,@mouseover,harm,nodead] Execute; Execute
```

**HS/Spalten / HS/Cleave** – Heldenhafter Stoß; Shift: Spalten

```
#show [mod:shift] Cleave; Heroic Strike
/startattack
/cast [mod:shift] Cleave; Heroic Strike
```

**Blutrausch+Trank / Bloodrage+Pot** – Blutrausch und bester Wuttrank

```
#showtooltip Bloodrage
/cast Bloodrage
/use Mighty Rage Potion
/use Great Rage Potion
/use Rage Potion
```

**Rufe / Shouts** – Schlachtruf; Shift: Demoralisierender Ruf

```
#showtooltip [mod:shift] Demoralizing Shout; Battle Shout
/cast [mod:shift] Demoralizing Shout; Battle Shout
```

</details>

<details><summary><b>Paladin</b> (9)</summary>

**Heiliger Stoß / Holy Strike**

```
#showtooltip Holy Strike
/startattack
/cast Holy Strike
```

**Schutz MO / BoP MO** – Alt: Göttlicher Schutz auf dich

```
#showtooltip [mod:alt] Divine Protection; Blessing of Protection
/cast [mod:alt] Divine Protection; [@mouseover,help,nodead][help,nodead][@targettarget,help,nodead] Blessing of Protection
```

**Segen / Blessings** – Macht; Shift: Weisheit; Strg: Könige

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift] Blessing of Wisdom; [mod:ctrl,@mouseover,help,nodead][mod:ctrl] Blessing of Kings; [@mouseover,help,nodead][] Blessing of Might
```

**Auren / Auras** – Hingabe; Shift: Konzentration; Strg: Vergeltung

```
#showtooltip [mod:shift] Concentration Aura; [mod:ctrl] Retribution Aura; Devotion Aura
/cast [mod:shift] Concentration Aura; [mod:ctrl] Retribution Aura; Devotion Aura
```

**Resi-Auren / Resist Auras** – Feuer; Shift: Frost; Strg: Schatten

```
#showtooltip
/cast [mod:shift] Frost Resistance Aura; [mod:ctrl] Shadow Resistance Aura; Fire Resistance Aura
```

**Handauflegung MO / LoH MO**

```
#showtooltip Lay on Hands
/cast [@mouseover,help,nodead][help,nodead][@player] Lay on Hands
```

**Gottesschild / Divine Shield** – Nochmal drücken: Schild beenden

```
#showtooltip Divine Shield
/cancelaura Divine Shield
/cancelaura Divine Protection
/cancelaura Blessing of Protection
/cast Divine Shield
```

**Erlösung MO / Redemption MO**

```
#showtooltip Redemption
/cast [@mouseover,help,dead][help,dead] Redemption
```

**Exorzismus / Exorcism** – Shift: Untote vertreiben

```
#showtooltip [mod:shift] Turn Undead; Exorcism
/cast [mod:shift,harm,nodead] Turn Undead; [harm,nodead] Exorcism
```

</details>

<details><summary><b>Jäger / Hunter</b> (12)</summary>

**Mal + Pet / Mark + Pet**

```
#showtooltip Hunter's Mark
/petattack
/cast Hunter's Mark
```

**Tier heilen / Mend Pet**

```
#showtooltip Mend Pet
/cast [@pet,exists,nodead] Mend Pet
```

**Pet Mouseover** – Begleiter greift Mouseover an, sonst Ziel

```
/petattack [@mouseover,harm,nodead][]
```

**Pet Angriff / Pet Attack** – Shift: passiv + zurückrufen

```
/petattack [nomod:shift,harm,nodead]
/petpassive [mod:shift]
/petfollow [mod:shift]
```

**Tier / Pet** – Rufen / heilen / wiederbeleben

```
#showtooltip
/cast [@pet,dead][mod:shift] Revive Pet; [nopet] Call Pet; Mend Pet
```

**Füttern / Feed Pet** – Essen ggf. im Makro anpassen

```
#showtooltip Feed Pet
/cast [pet,nocombat] Feed Pet
/use [pet,nocombat] Chunk of Boar Meat
```

**Falke / Hawk**

```
#showtooltip Aspect of the Hawk
/cancelaura Aspect of the Cheetah
/cast !Aspect of the Hawk
```

**Gepard/Rudel / Cheetah/Pack** – Rechtsklick: Rudel

```
#showtooltip Aspect of the Cheetah
/cast [button:2] !Aspect of the Pack; !Aspect of the Cheetah
```

**Fährten / Tracking**

```
#showtooltip
/cast [mod:shift] Track Beasts; [mod:ctrl] Track Undead; [mod:alt] Track Hidden; Track Humanoids
```

**Totstellen / Feign Death**

```
#showtooltip Feign Death
/petpassive
/petfollow
/stopattack
/stopcasting
/cast [combat] Feign Death
```

**Aspekt weg / Cancel Aspect**

```
/cancelaura Aspect of the Cheetah
/cancelaura Aspect of the Pack
```

**Adlerauge / Eagle Eye**

```
#showtooltip Eagle Eye
/cast !Eagle Eye
```

</details>

<details><summary><b>Schurke / Rogue</b> (9)</summary>

**Tritt MO / Kick MO**

```
#showtooltip Kick
/cast [@mouseover,harm,nodead][] Kick
```

**Kopfnuss MO / Sap MO**

```
#showtooltip Sap
/cast [@mouseover,harm,nodead][] Sap
```

**Verstohlenheit / Stealth** – Schaltet sich nicht selbst ab

```
#showtooltip Stealth
/dismount
/cast [nostealth,nocombat] Stealth
```

**Taschendieb MO / Pick Pocket MO**

```
#showtooltip Pick Pocket
/cast [@mouseover,harm,nodead][] Pick Pocket
```

**Opener** – Taschendiebstahl + Fieser Trick; Shift: Erdrosseln; Strg: Hinterhalt

```
#showtooltip
/cast [stealth] Pick Pocket
/cast [nostealth] Stealth; [mod:shift] Garrote; [mod:ctrl] Ambush; Cheap Shot
```

**Entrinnen+Sprint / Evasion+Sprint**

```
#showtooltip Evasion
/cast Evasion
/cast Sprint
```

**Gift auftragen / Apply Poison** – Sofort-Gift; Shift: tödliches Gift; Alt: Nebenhand

```
#showtooltip
/use [mod:shift] Deadly Poison; Instant Poison
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Wetzstein / Sharpen** – Shift: Gewichtsstein; Alt: Nebenhand

```
#showtooltip
/use [mod:shift] Heavy Weightstone; Heavy Sharpening Stone
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Stealth/Vanish**

```
#showtooltip [nocombat] Stealth; Vanish
/stopattack [combat]
/cast [nocombat] !Stealth; Vanish
```

</details>

<details><summary><b>Priester / Priest</b> (9)</summary>

**Magiebannung MO / Dispel MO**

```
#showtooltip Dispel Magic
/cast [@mouseover,exists,nodead][] Dispel Magic
```

**Seelenstärke MO / Fortitude MO**

```
#showtooltip Power Word: Fortitude
/cast [@mouseover,help,nodead][help,nodead][@player] Power Word: Fortitude
```

**Furchtzauber MO / Fear Ward MO**

```
#showtooltip Fear Ward
/cast [@mouseover,help,nodead][help,nodead][@player] Fear Ward
```

**Fesseln MO / Shackle MO**

```
#showtooltip Shackle Undead
/cast [@mouseover,harm,nodead][harm,nodead] Shackle Undead
```

**Zauberstab / Wand**

```
#showtooltip Shoot
/cast !Shoot
```

**Auferstehung MO / Resurrect MO**

```
#showtooltip Resurrection
/cast [@mouseover,help,dead][help,dead] Resurrection
```

**Levitieren / Levitate** – Shift: abbrechen

```
#showtooltip Levitate
/dismount
/cancelaura [mod:shift] Levitate
/cast [nomod] Levitate
```

**Selbstbuffs / Self Buffs**

```
#showtooltip
/castsequence [@player] reset=15 Inner Fire, Power Word: Fortitude, Divine Spirit
```

**Heilen/Peinigen / Heal/Smite**

```
#showtooltip
/cast [@mouseover,help,nodead] Lesser Heal; [harm,nodead] Smite; [help,nodead][@player] Lesser Heal
```

</details>

<details><summary><b>Schamane / Shaman</b> (11)</summary>

**Erdschock MO / Earth Shock MO** – Bricht eigenen Zauber für den Kick ab

```
#showtooltip Earth Shock
/stopcasting
/cast [@mouseover,harm,nodead][] Earth Shock
```

**Totems** – Shift: zurückrufen

```
#showtooltip [mod:shift] Totemic Recall; Call of the Elements
/cast [mod:shift] Totemic Recall; Call of the Elements
```

**Totem-Sets / Totem Sets** – Strg/Alt: andere Sets; Shift: zurückrufen

```
#showtooltip
/cast [mod:ctrl] Call of the Ancestors; [mod:alt] Call of the Spirits; [mod:shift] Totemic Recall; Call of the Elements
```

**Schild / Shield** – Shift: Wasserschild

```
#showtooltip [mod:shift] Water Shield; Lightning Shield
/cast [mod:shift] Water Shield; Lightning Shield
```

**Geisterwolf / Ghost Wolf**

```
#showtooltip Ghost Wolf
/cast Ghost Wolf
```

**Reinigen MO / Purge MO**

```
#showtooltip Purge
/cast [@mouseover,harm,nodead][] Purge
```

**Schocks / Shocks** – Shift: Flamme; Strg: Frost

```
#showtooltip [mod:shift] Flame Shock; [mod:ctrl] Frost Shock; Earth Shock
/cast [mod:shift] Flame Shock; [mod:ctrl] Frost Shock; Earth Shock
```

**Heilung Gift / Cure** – Shift: Krankheit

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] Cure Disease; [@mouseover,help,nodead][help,nodead][@player] Cure Poison
```

**Reinkarnation / Reincarnation** – Zeigt nur die Abklingzeit

```
#showtooltip Reincarnation
```

**Selbst heilen / Self Heal**

```
#showtooltip [mod:shift] Lesser Healing Wave; Healing Wave
/cast [mod:shift,@player] Lesser Healing Wave; [@player] Healing Wave
```

**Wasserwandeln / Water Walk** – Shift: Wasseratmung

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Water Breathing; [@mouseover,help,nodead][help,nodead][@player] Water Walking
```

</details>

<details><summary><b>Magier / Mage</b> (13)</summary>

**Gegenzauber / Counterspell**

```
#showtooltip Counterspell
/stopcasting
/cast Counterspell
```

**Verwandlung MO / Polymorph MO**

```
#showtooltip Polymorph
/cast [@mouseover,harm,nodead][] Polymorph
```

**Intelligenz / Intellect** – Shift: Arkane Brillanz

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Arcane Brilliance; [@mouseover,help,nodead][help,nodead][@player] Arcane Intellect
```

**Magie dämpfen / Dampen Magic** – Shift: Magie verstärken

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] Amplify Magic; [@mouseover,help,nodead][help,nodead][@player] Dampen Magic
```

**Fluch aufheben / Decurse** – Shift: auf dich

```
#showtooltip Remove Lesser Curse
/cast [mod:shift,@player][@mouseover,help,nodead][help,nodead][@player] Remove Lesser Curse
```

**Herbeizaubern / Conjure** – Wasser; Shift: Essen

```
#showtooltip [mod:shift] Conjure Food; Conjure Water
/cast [mod:shift] Conjure Food; Conjure Water
```

**Manastein / Mana Gem** – Nimmt den besten vorhandenen

```
#showtooltip
/use Mana Ruby
/use Mana Citrine
/use Mana Jade
/use Mana Agate
```

**Rüstung / Armor** – Eisrüstung; Shift: Magier; Strg: Frost

```
#showtooltip [mod:shift] Mage Armor; [mod:ctrl] Frost Armor; Ice Armor
/cast [mod:shift] Mage Armor; [mod:ctrl] Frost Armor; Ice Armor
```

**Teleport (A)** – Allianz

```
#showtooltip
/cast [mod:shift] Teleport: Ironforge; [mod:ctrl] Teleport: Darnassus; [mod:alt] Teleport: Dalaran; Teleport: Stormwind
```

**Teleport (H)** – Horde

```
#showtooltip
/cast [mod:shift] Teleport: Undercity; [mod:ctrl] Teleport: Thunder Bluff; [mod:alt] Teleport: Dalaran; Teleport: Orgrimmar
```

**Portal (A)** – Allianz

```
#showtooltip
/cast [mod:shift] Portal: Ironforge; [mod:ctrl] Portal: Darnassus; Portal: Stormwind
```

**Portal (H)** – Horde

```
#showtooltip
/cast [mod:shift] Portal: Undercity; [mod:ctrl] Portal: Thunder Bluff; Portal: Orgrimmar
```

**Langsamer Fall / Slow Fall** – Shift: abbrechen

```
#showtooltip Slow Fall
/dismount [nomod:shift]
/cancelaura [mod:shift] Slow Fall
/cast [nomod:shift,@player] Slow Fall
```

</details>

<details><summary><b>Hexenmeister / Warlock</b> (11)</summary>

**Furcht MO / Fear MO**

```
#showtooltip Fear
/cast [@mouseover,harm,nodead][] Fear
```

**Dämon zurück / Pet Back**

```
/petpassive
/petfollow
```

**Dämon rufen / Summon Demon** – Leerwandler; Shift: Wichtel; Strg: Sukkubus; Alt: Teufelsjäger

```
#showtooltip
/cast [mod:shift] Summon Imp; [mod:ctrl] Summon Succubus; [mod:alt] Summon Felhunter; Summon Voidwalker
```

**Flüche / Curses** – Elemente (Mouseover); Shift: Schwäche; Strg: Tollkühnheit; Alt: Sprachen

```
#showtooltip
/cast [mod:shift] Curse of Weakness; [mod:ctrl] Curse of Recklessness; [mod:alt] Curse of Tongues; [@mouseover,harm,nodead][] Curse of the Elements
```

**DoT-Folge / DoT Sequence** – Leveln: Opfern, Pein, Verderbnis, Zauberstab

```
#showtooltip
/petattack [harm,nodead]
/castsequence reset=target Immolate, Bane of Agony, Corruption, !Shoot
```

**Zauberstab / Wand**

```
#showtooltip Shoot
/cast !Shoot
```

**Gesundheitsstein / Healthstone** – Shift: zusätzlich Lebensentzug

```
#showtooltip
/use Major Healthstone
/use Greater Healthstone
/use Healthstone
/use Lesser Healthstone
/use Minor Healthstone
/cast [mod:shift] Drain Life
```

**Seelenstein MO / Soulstone MO**

```
#showtooltip
/use [@mouseover,help][] Major Soulstone
/use [@mouseover,help][] Greater Soulstone
/use [@mouseover,help][] Soulstone
/use [@mouseover,help][] Lesser Soulstone
/use [@mouseover,help][] Minor Soulstone
```

**Steine erstellen / Create Stones**

```
#showtooltip
/cast [mod:shift] Create Soulstone; [mod:ctrl] Create Spellstone; [mod:alt] Create Firestone; Create Healthstone
```

**Beschwörung / Summoning** – Kündigt die Beschwörung in der Gruppe an

```
#showtooltip Ritual of Summoning
/party Beschwöre %t, bitte Portal anklicken
/cast Ritual of Summoning
```

**Dämonenrüstung / Demon Armor** – Shift: Schattenzauberschutz

```
#showtooltip [mod:shift] Shadow Ward; Demon Armor
/cast [mod:shift] Shadow Ward; Demon Armor
```

</details>

### Rassen / Races

<details><summary><b>Rassenfähigkeiten / Racial abilities</b> (19)</summary>

Im Fenster erscheinen nur die Fähigkeiten, die dein Charakter hat. Jedes Makro: `#showtooltip <Fähigkeit>` + `/cast <Fähigkeit>`.

- Will of the Forsaken (Makroname / macro name: Wille Verlassene / WotF)
- War Stomp
- Berserking
- Blood Fury
- Cannibalize
- Shadowmeld
- Escape Artist
- Stoneform
- Find Treasure
- Perception
- Read Leyline
- Walk on Air
- Skysight
- Will to Survive
- Elune's Light
- Eureka!
- Shatter Curse
- Rapid Regeneration (Makroname / macro name: Rasche Regen. / Rapid Regen)
- Cultivation

</details>

### Utility (allgemeiner Tab / general tab)

<details><summary><b>Allgemein / General</b> (11)</summary>

**Ruhestein / Hearthstone**

```
#showtooltip Hearthstone
/use Hearthstone
```

**Fokus MO / Focus MO** – Mouseover, sonst Ziel als Fokus

```
/focus [@mouseover,exists,nodead][]
```

**Fokus weg / Clear Focus**

```
/clearfocus
```

**Totenkopf / Skull** – Totenkopf aufs Ziel

```
/tm 8
```

**Marker weg / Clear Mark** – Zielmarkierung entfernen

```
/tm 0
```

**Bestätigen / Confirm** – Klickt 'Annehmen' im obersten Dialog

```
/click StaticPopup1Button1
```

**Geist freilassen / Release Spirit**

```
/run RepopMe()
```

**Instanz-Reset / Reset Instances**

```
/run ResetInstances()
```

**Gruppe verlassen / Leave Group**

```
/run C_PartyInfo.LeaveParty()
```

**UI neu laden / Reload UI**

```
/reload
```

**Absitzen / Dismount**

```
/dismount
```

</details>

<details><summary><b>Ausrüstung / Equipment</b> (3)</summary>

**Schmuck 1+2 / Trinkets** – Beide Schmuckstücke

```
#showtooltip
/use 13
/use 14
```

**Schmuck oben / Trinket 1**

```
#showtooltip 13
/use 13
```

**Schmuck unten / Trinket 2**

```
#showtooltip 14
/use 14
```

</details>

<details><summary><b>Gegenstände / Items</b> (4)</summary>

**Heiltrank / Healing Potion** – Nimmt den besten vorhandenen

```
#showtooltip
/use Major Healing Potion
/use Superior Healing Potion
/use Greater Healing Potion
/use Healing Potion
/use Lesser Healing Potion
/use Minor Healing Potion
```

**Manatrank / Mana Potion** – Nimmt den besten vorhandenen

```
#showtooltip
/use Major Mana Potion
/use Superior Mana Potion
/use Greater Mana Potion
/use Mana Potion
/use Lesser Mana Potion
/use Minor Mana Potion
```

**Verband / Bandage** – Bester Verband auf dich (Seide bis Runenstoff)

```
#showtooltip
/use [@player] Heavy Runecloth Bandage
/use [@player] Runecloth Bandage
/use [@player] Heavy Mageweave Bandage
/use [@player] Mageweave Bandage
/use [@player] Heavy Silk Bandage
```

**Verband (klein) / Bandage (low)** – Bester Verband auf dich (Leinen bis Seide)

```
#showtooltip
/use [@player] Silk Bandage
/use [@player] Heavy Wool Bandage
/use [@player] Wool Bandage
/use [@player] Heavy Linen Bandage
/use [@player] Linen Bandage
```

</details>

<details><summary><b>Quests</b> (2)</summary>

**Quest an/ab / Quest Accept** – Nimmt an / gibt ab im offenen Questfenster

```
/click QuestFrameAcceptButton
/click QuestFrameCompleteButton
/click QuestFrameCompleteQuestButton
```

**Quest teilen / Share Quest** – Teilt die im Questlog ausgewählte Quest

```
/run local q=C_QuestLog.GetSelectedQuest() if q and q>0 then QuestLogPushQuest(C_QuestLog.GetLogIndexForQuestID(q)) end
```

</details>

<details><summary><b>Berufe / Professions</b> (7)</summary>

**Kräuter/Erze / Herbs/Ore** – Kräutersuche; Shift: Mineraliensuche

```
#showtooltip
/cast [mod:shift] Find Minerals; Find Herbs
```

**Angeln / Fishing**

```
#showtooltip Fishing
/cast Fishing
```

**Kochfeuer / Campfire**

```
#showtooltip Basic Campfire
/cast Basic Campfire
```

**Kochen / Cooking**

```
#showtooltip Cooking
/cast Cooking
```

**Erste Hilfe / First Aid**

```
#showtooltip First Aid
/cast First Aid
```

**Entzaubern / Disenchant**

```
#showtooltip Disenchant
/cast Disenchant
```

**Verhütten / Smelting**

```
#showtooltip Smelting
/cast Smelting
```

</details>

<details><summary><b>Ausrüstungssets / Equipment sets</b></summary>

Für jedes Ausrüstungsset deines Charakters bietet das Fenster ein Makro `/equipset <Setname>` an (Charakter-Tab).  
For every equipment set of your character the window offers a `/equipset <set name>` macro (character tab).

</details>

## Entwicklung / Development

- `build/macros.py`: die Makros (`{Zauber}`, `{=Zauber}` ohne Rang, `{A|B}` erster bekannter, `<Gegenstand>`).
- `python3 -I build/build.py db ForeverMacros/Data.lua`: prüft jeden Namen gegen die Client-Tabellen von 1.60.1.70532 (CSV von wago.tools in `db/`) und jede Länge (255 Zeichen im ungünstigsten Fall) und schreibt `Data.lua`.
- `python3 -I build/gen_readme.py README.md`: erzeugt diese README.
- `cd test && luajit test.lua ../ForeverMacros`: Test mit nachgebauter WoW-API (alle Klassen, Deutsch/Englisch, niedrige/hohe Ränge).

## Quellen / Credits

Makrotexte angepasst nach / macro texts adapted from [Classic WoW Forever](https://classicwowforever.com/macros/) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) und [Zockify](https://www.zockify.com/forever/druid/macros/). Änderungen: Namen aus IDs lokalisiert, Ränge automatisch, einige Makros gekürzt. Details: `ForeverMacros/CREDITS.txt`.
