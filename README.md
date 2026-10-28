# ForeverMacros

Fertige Klassen-, Rassen- und Utility-Makros für **WoW Forever (1.60.1)**, mit einem Klick eingebaut, dazu ein Makro pro gelerntem Zauber mit Ziel- und Extra-Haken.  
Ready-made class, race and utility macros for **WoW Forever (1.60.1)**, installed with one click, plus one macro per learned spell built from target and extra boxes.

## Installation

1. [ZIP aus den Releases laden](https://github.com/MrKPlol/ForeverMacros/releases/latest) / download the ZIP from the releases.
2. Entpacken nach / unzip into `World of Warcraft/_forever_/Interface/AddOns/` (danach gibt es dort den Ordner `ForeverMacros`).
3. Ingame `/macros` eingeben oder das AddOn-Menü an der Minimap nutzen / type `/macros` or use the addon menu at the minimap.

## Was es macht / What it does

- Makros anhaken, mit der Maus drüberfahren zeigt das fertige Makro, **Einbauen** legt sie an.
- Klassen-, Rassen- und Ausrüstungsset-Makros kommen in den **Charakter-Tab**, alles andere in den **allgemeinen Tab** (für alle Charaktere).
- Zauber- und Gegenstandsnamen werden in der **Sprache deines Clients** eingesetzt (Deutsch, Englisch, …).
- Forever hat die Zauberränge neu angelegt: ein Name ohne Rang kann auf einen Rang zeigen, den du noch nicht kannst. Das Addon setzt den **höchsten Rang ein, den du kennst** (z. B. `Charge(Rank 1)`) und zieht ihn beim Leveln automatisch nach.
- **Ziel-Optionen:** hinter vielen Makros sitzen kleine Kästchen: **MO** (Mouseover), **Fokus**, **Ziel**, **Ich** bzw. bei Boden-Zaubern und Bomben **Maus** (sofort an der Mausposition) oder **Ich** (unter dir). Es gibt nur die Optionen, die der Zauber oder Gegenstand in Forever zulässt. Die Liste unten zeigt die Standard-Auswahl.
- Kästchen am **Gruppenkopf** hakt die ganze Kategorie an oder ab.
- **Zwei Reiter:** **Fertige Makros** (die Liste unten: nur Makros, die mehr als einen Zauber kombinieren) und **Zauber-Makros**: ein Makro pro gelerntem Zauber deiner Klasse, sortiert nach Talentbaum. Dahinter dieselben Ziel-Kästchen und, je nachdem was der Zauber in Forever kann:
  - **Haltung** (Krieger): wechselt erst in eine passende Haltung, z. B. `/cast [nostance:1/3] Battle Stance` vor Hinrichten.
  - **Gestalt** (Druide): Katzen-/Bärenfähigkeiten gehen erst in die Gestalt (`/cast !Cat Form`), Zauber verlassen sie (`/cancelform`).
  - **Stop** (`/stopcasting`), **Schmuck** (`/use 13`, `/use 14`), **Angriff** (`/startattack`, Nahkampfklassen).
  - **Spam:** kanalisierte Zauber bekommen `[nochanneling]`, Umschalt-Zauber (Gestalten, Schleichen, Aspekte, Auto Shot) ein `!`, damit wiederholtes Drücken nichts abbricht.
  - Haltung und Gestalt lösen die globale Abklingzeit aus: danach die Taste ein zweites Mal drücken.
  - Zauber-Makros liegen im Charakter-Tab (max. 30 Plätze) und bekommen ihren Rang genauso automatisch nachgezogen.
- **Ingenieurskunst:** alle Gegenstände mit Benutzen-Effekt aus den Forever-Tabellen geprüft, dazu die neuen Gürtel-Tinker (Teleport, Nitro Boosts, Magnetic Displacement) über `/use 6`.
- Überschreibt **nie** Makros, die du selbst angelegt oder geändert hast, und ändert nichts im Kampf.
- `A|B` in der Liste unten heißt: das Addon nimmt den ersten Zauber, den du kannst (z. B. Terrorbärgestalt, sonst Bärengestalt). In der Liste steht jeweils der erste.

## Alle 124 Makros / All 124 macros

Die Liste zeigt die englischen Namen; im Spiel stehen die Namen deines Clients.  
The list shows English spell names; in game the addon uses your client's language.

### Klassen / Classes

<details><summary><b>Druide / Druid</b> (14)</summary>

**Schreddern/Shift / Shred/Shift** – Shred; Shift: Shifting Power (Mana in Energie)

```
#showtooltip
/startattack [nomod:shift,harm,nodead]
/cast [mod:shift] Shifting Power; [harm,nodead] Shred
```

**Powershift** – Gestalt neu betreten (Furor: Energie/Wut, löst Verlangsamungen); Shift: Bär. Steht man danach in Normalgestalt: nochmal drücken

```
#showtooltip
/cancelform
/cast [mod:shift] !Dire Bear Form; !Cat Form
```

**Katze+Schleichen / Cat+Prowl** – Katzengestalt falls nötig, dann Schleichen (bricht es nicht ab)

```
#showtooltip Prowl
/cast !Cat Form
/cast !Prowl
```

**Katze+Spurt / Cat+Dash** – Katzengestalt falls nötig, dann Spurt

```
#showtooltip Dash
/cast !Cat Form
/cast Dash
```

**Katze/Bär / Cat/Bear** – Katze; Shift: Bär (Terrorbär sobald gelernt). Nochmal drücken wirft dich nicht aus der Gestalt

```
#showtooltip [mod:shift] Dire Bear Form; Cat Form
/dismount
/cast [mod:shift] !Dire Bear Form; !Cat Form
```

**Reisen / Travel** – Wasser: Wassergestalt, draußen: Reisegestalt, drinnen: Katze

```
#showtooltip
/dismount
/cast [swimming] Aquatic Form; [outdoors] Travel Form; Cat Form
```

**Baumrinde/NG / Barkskin/NG** – Baumrinde; Shift: Griff der Natur (ohne Formwechsel)

```
#showtooltip [mod:shift] Nature's Grasp; Barkskin
/cast [mod:shift] Nature's Grasp; Barkskin
```

**Verjüng/Nachw. / Rejuv/Regrowth** – Verjüngung; Shift: Nachwachsen (verlässt die Gestalt)

```
#showtooltip
/cancelform
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Regrowth; [@mouseover,help,nodead][help,nodead][@player] Rejuvenation
```

**Fluch/Gift / Curse/Poison** – Fluch aufheben; Shift: Gift (Vergiftung aufheben, sobald gelernt)

```
#showtooltip
/cancelform
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Abolish Poison; [@mouseover,help,nodead][help,nodead][@player] Remove Curse
```

**NS + Heilen / NS + Heal** – Schnelligkeit der Natur + sofortige Heilende Berührung

```
#showtooltip Nature's Swiftness
/stopcasting
/cancelform
/cast Nature's Swiftness
/cast [@mouseover,help,nodead][help,nodead][@player] Healing Touch
```

**Wiedergeb./Bel. / Rebirth/Revive** – Kampf: Wiedergeburt, sonst Wiederbeleben

```
#showtooltip
/cast [combat,@mouseover,help,dead][combat,help,dead] Rebirth
/cast [nocombat,@mouseover,help,dead][nocombat,help,dead] Revive
```

**Form weg / Drop form** – Zauber abbrechen, Gestalt verlassen, absitzen

```
/stopcasting
/cancelform
/dismount
```

**Urbiss+Zermalmen / Bite+Maul** – Bär: Urbiss und Zermalmen auf den nächsten Schlag; Strg: Wut sparen (ohne Zermalmen)

```
#showtooltip Primal Bite
/startattack
/cast Primal Bite
/cast [nomod:ctrl] Maul
```

**Knurren/Gebrüll / Growl/Roar** – Knurren; Strg: Herausforderndes Gebrüll

```
#showtooltip
/cast [mod:ctrl] Challenging Roar; [@mouseover,harm,nodead][harm,nodead] Growl
```

</details>

<details><summary><b>Krieger / Warrior</b> (8)</summary>

**Sturm+Angriff / Charge+Attack**

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

**Haltung+Wut / Stance+Rage**

```
#showtooltip Berserker Rage
/cast [nostance:3] Berserker Stance
/cast Berserker Rage
```

**Haltung+Hinricht / Stance+Execute**

```
#showtooltip Execute
/startattack
/cast [stance:2] Battle Stance
/cast [@mouseover,harm,nodead][harm,nodead] Execute
```

**HS/Spalten / HS/Cleave** – Heldenhafter Stoß; Shift: Spalten

```
#show [mod:shift] Cleave; Heroic Strike
/startattack
/cast [mod:shift] Cleave; Heroic Strike
```

**Rufe / Shouts** – Schlachtruf; Shift: Demoralisierender Ruf

```
#showtooltip [mod:shift] Demoralizing Shout; Battle Shout
/cast [mod:shift] Demoralizing Shout; Battle Shout
```

**Unterbrechen / Interrupt** – Berserkerhaltung: Zuschlagen, sonst Schildhieb (Schild nötig)

```
#showtooltip
/cast [stance:3,@mouseover,harm,nodead][stance:3,harm,nodead] Pummel; [@mouseover,harm,nodead][harm,nodead] Shield Bash
```

**Spott/Ruf / Taunt/Shout** – Spott; Strg: Herausforderungsruf

```
#showtooltip
/cast [mod:ctrl] Challenging Shout; [@mouseover,harm,nodead][harm,nodead] Taunt
```

</details>

<details><summary><b>Paladin</b> (4)</summary>

**Schutz / BoP** – Alt: Göttlicher Schutz auf dich

```
#showtooltip [mod:alt] Divine Protection; Blessing of Protection
/cast [mod:alt] Divine Protection; [@mouseover,help,nodead][help,nodead][@player] Blessing of Protection
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

**Gottesschild+Weg / Bubble+Cancel** – Nochmal drücken: Schild beenden

```
#showtooltip Divine Shield
/cancelaura Divine Shield
/cancelaura Divine Protection
/cancelaura Blessing of Protection
/cast Divine Shield
```

</details>

<details><summary><b>Jäger / Hunter</b> (10)</summary>

**Mal + Pet / Mark + Pet**

```
#showtooltip Hunter's Mark
/petattack [@mouseover,harm,nodead][harm,nodead] 
/cast [@mouseover,harm,nodead][harm,nodead] Hunter's Mark
```

**Pet Angriff Ziel / Pet Attack Unit** – Begleiter greift die gewählte Einheit an

```
/petattack [@mouseover,harm,nodead][harm,nodead] 
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

**Totstellen+Stop / Feign+Stop**

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

**Totst.+Falle / Feign+Trap** – Im Kampf: Totstellen, nochmal drücken: Eiskältefalle

```
#showtooltip Freezing Trap
/petpassive
/petfollow
/stopattack
/cast [combat] Feign Death
/cast [nocombat] Freezing Trap
```

</details>

<details><summary><b>Schurke / Rogue</b> (5)</summary>

**Verstohl. sicher / Stealth (safe)** – Schaltet sich nicht selbst ab

```
#showtooltip Stealth
/dismount
/cast [nostealth,nocombat] Stealth
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

**Stealth/Vanish**

```
#showtooltip [nocombat] Stealth; Vanish
/stopattack [combat]
/cast [nocombat] !Stealth; Vanish
```

</details>

<details><summary><b>Priester / Priest</b> (5)</summary>

**Zauberstab / Wand**

```
#showtooltip Shoot
/cast !Shoot
```

**Levitieren+Weg / Levitate+Off** – Shift: abbrechen

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

**Innerer Fokus+ / Inner Focus+** – Innerer Fokus + Große Heilung; Shift: + Gedankenschlag

```
#showtooltip
/cast Inner Focus
/cast [mod:shift] Mind Blast; [@mouseover,help,nodead][help,nodead][@player] Greater Heal
```

</details>

<details><summary><b>Schamane / Shaman</b> (8)</summary>

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

**Schocks / Shocks** – Shift: Flamme; Strg: Frost

```
#showtooltip [mod:shift] Flame Shock; [mod:ctrl] Frost Shock; Earth Shock
/cast [mod:shift] Flame Shock; [mod:ctrl] Frost Shock; Earth Shock
```

**Heilung Gift / Cure** – Shift: Krankheit

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Cure Disease; [@mouseover,help,nodead][help,nodead][@player] Cure Poison
```

**Selbst heilen / Self Heal**

```
#showtooltip [mod:shift] Lesser Healing Wave; Healing Wave
/cast [mod:shift,@player] Lesser Healing Wave; [@player] Healing Wave
```

**Wasserw./Atmung / WaterWalk/Breath** – Shift: Wasseratmung

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Water Breathing; [@mouseover,help,nodead][help,nodead][@player] Water Walking
```

**NS + Heilen / NS + Heal** – Schnelligkeit der Natur + sofortige Welle der Heilung

```
#showtooltip Nature's Swiftness
/stopcasting
/cast Nature's Swiftness
/cast [@mouseover,help,nodead][help,nodead][@player] Healing Wave
```

</details>

<details><summary><b>Magier / Mage</b> (11)</summary>

**Intelligenz / Intellect** – Shift: Arkane Brillanz

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Arcane Brilliance; [@mouseover,help,nodead][help,nodead][@player] Arcane Intellect
```

**Dämpfen/Verst. / Dampen/Amplify** – Shift: Magie verstärken

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Amplify Magic; [@mouseover,help,nodead][help,nodead][@player] Dampen Magic
```

**Herbeizaubern / Conjure** – Wasser; Shift: Essen

```
#showtooltip [mod:shift] Conjure Food; Conjure Water
/cast [mod:shift] Conjure Food; Conjure Water
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

**Langs. Fall+Weg / Slow Fall+Off** – Shift: abbrechen

```
#showtooltip Slow Fall
/dismount [nomod:shift]
/cancelaura [mod:shift] Slow Fall
/cast [nomod:shift,@player] Slow Fall
```

**Eisblock+Weg / Ice Block+Off** – Nochmal drücken: Eisblock beenden

```
#showtooltip Ice Block
/cancelaura Ice Block
/cast Ice Block
```

**GG+AM+Pyro / PoM+AP+Pyro** – Geistesgegenwart + Arkane Macht + Pyroschlag (sonst Feuerball)

```
#showtooltip
/cast Presence of Mind
/cast Arcane Power
/cast [@mouseover,harm,nodead][harm,nodead] Pyroblast
```

</details>

<details><summary><b>Hexenmeister / Warlock</b> (12)</summary>

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

**Teufelsb.+Dämon / FelDom+Summon** – Teufelsbeherrschung, dann Dämon (Tasten wie Dämon rufen)

```
#showtooltip
/cast Fel Domination
/cast [mod:shift] Summon Imp; [mod:ctrl] Summon Succubus; [mod:alt] Summon Felhunter; Summon Voidwalker
```

**Zaubersperre / Spell Lock** – Teufelsjäger: Unterbrechen (Fokus/Mouseover)

```
#showtooltip
/cast [@mouseover,harm,nodead][harm,nodead] Spell Lock
```

**Magie verschl. / Devour Magic** – Teufelsjäger: Magie bannen, Freund oder Feind

```
#showtooltip
/cast [@mouseover,exists,nodead][exists,nodead] Devour Magic
```

**Flüche / Curses** – Elemente; Shift: Schwäche; Strg: Tollkühnheit; Alt: Sprachen

```
#showtooltip
/cast [mod:shift] Curse of Weakness; [mod:ctrl] Curse of Recklessness; [mod:alt] Curse of Tongues; [@mouseover,harm,nodead][harm,nodead] Curse of the Elements
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

**Seelenstein / Soulstone**

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

**Rüstung/Schutz / Armor/Ward** – Shift: Schattenzauberschutz

```
#showtooltip [mod:shift] Shadow Ward; Demon Armor
/cast [mod:shift] Shadow Ward; Demon Armor
```

</details>

### Rassen / Races

<details><summary><b>Rassenfähigkeiten / Racial abilities</b> (4)</summary>

Im Fenster erscheinen nur die, die dein Charakter hat. Nur Kombinationen, die mehr können als die Fähigkeit allein.

**Shadowmeld** – Kampf/Zauber stoppen, dann Schattenmimik (sonst bricht sie sofort)

```
#showtooltip Shadowmeld
/stopattack
/stopcasting
/cast Shadowmeld
```

**Blood Fury** – Kochendes Blut + beide Schmuckstücke

```
#showtooltip Blood Fury
/cast Blood Fury
/use 13
/use 14
```

**Berserking** – Berserker + beide Schmuckstücke

```
#showtooltip Berserking
/cast Berserking
/use 13
/use 14
```

**Walk on Air** – Absitzen und sofort gleiten (auch mitten im Flug)

```
#showtooltip Walk on Air
/dismount
/cast Walk on Air
```

</details>

### Utility (allgemeiner Tab / general tab)

<details><summary><b>Allgemein / General</b> (9)</summary>

**Fokus setzen / Set Focus** – Mouseover, sonst Ziel als Fokus

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

</details>

<details><summary><b>Ausrüstung / Equipment</b> (3)</summary>

**Schmuck 1+2 / Trinkets** – Beide Schmuckstücke (Ziel-Optionen für Netz, Schrumpfstrahl & Co.)

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

<details><summary><b>Ingenieurskunst / Engineering</b> (22)</summary>

**Gürtel-Tinker / Belt Tinker** – Ingi-Verzauberung am Gürtel: Teleport, Nitro Boosts oder Magnetic Displacement (Ziel-Optionen nur für Letzteres nötig)

```
#showtooltip 6
/use 6
```

**Ingi-Slots / Engi Slots** – Stiefel; Shift: Helm; Strg: Gürtel; Alt: Umhang (Raketenstiefel, Kappe, Fallschirm …) – egal welches Teil angelegt ist

```
#showtooltip
/use [mod:shift] 1; [mod:ctrl] 6; [mod:alt] 15; 8
```

**Net-o-Matik / Net-o-Matic**

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Gnomish Net-o-Matic Projector
```

**Schrumpfstrahl / Shrink Ray**

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Gnomish Shrink Ray
```

**Geflügelisierer / Poultryizer**

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Gnomish Poultryizer
```

**Todesstrahl / Death Ray**

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Gnomish Death Ray
```

**Diskombobulator / Discombobulator**

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Discombobulator Ray
```

**Gedankenkappe / Mind Control Cap** – Kopf

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Gnomish Mind Control Cap
```

**Raketenhelm / Rocket Helmet** – Kopf: Ansturm aufs Ziel

```
#showtooltip
/use [@mouseover,harm,nodead][harm,nodead] Goblin Rocket Helmet
```

**Rekombobulator / Recombobulator** – Hebt Verwandlung auf, großer zuerst

```
#showtooltip
/use [@mouseover,help,nodead][help,nodead][@player] Major Recombobulator
/use [@mouseover,help,nodead][help,nodead][@player] Minor Recombobulator
```

**Reflektor / Reflector** – Feuer; Shift: Frost; Strg: Schatten

```
#showtooltip
/use [mod:shift] Gyrofreeze Ice Reflector; [mod:ctrl] Ultra-Flash Shadow Reflector; Hyper-Radiant Flame Reflector
```

**Tarnung / Cloaking** – Kampf/Zauber stoppen, dann Tarnung

```
#showtooltip
/stopattack
/stopcasting
/use Emergency Field Cloak
/use Gnomish Cloaking Device
/use Stealthman 52
```

**Bombe / Bomb** – Beste vorhandene Bombe/Granate

```
#showtooltip
/use [@cursor] EZ-Thro Dark Bomb
/use [@cursor] EZ-Thro Thorium Grenade
/use [@cursor] Dark Iron Bomb
/use [@cursor] Thorium Grenade
/use [@cursor] Tru-Trigger Frag Bomb
/use [@cursor] SAF-T Bomb
```

**Bombe (klein) / Bomb (low)** – Wie Bombe, für niedrigere Stufen

```
#showtooltip
/use [@cursor] Hi-Explosive Bomb
/use [@cursor] Mithril Frag Bomb
/use [@cursor] Big Iron Bomb
/use [@cursor] EZ-Thro Grenade
/use [@cursor] Iron Grenade
/use [@cursor] SAF-T Bronze Bomb
```

**Manabombe / Mana Bomb** – Entzieht Mana

```
#showtooltip
/use [@cursor] EZ-Thro Mana Bomb
/use [@cursor] Arcane Bomb
```

**Dynamit / Dynamite** – Bestes vorhandenes Dynamit

```
#showtooltip
/use [@cursor] SAF-T Clever Dynamite
/use [@cursor] Dense Dynamite
/use [@cursor] Ez-Thro Dynamite II
/use [@cursor] SAF-T Jumbo Dynamite
/use [@cursor] Solid Dynamite
/use [@cursor] Heavy Dynamite
```

**Dynamit (klein) / Dynamite (low)** – Wie Dynamit, für niedrige Stufen

```
#showtooltip
/use [@cursor] Ez-Thro Dynamite
/use [@cursor] SAF-T Dynamite
/use [@cursor] Coarse Dynamite
/use [@cursor] Rough Dynamite
```

**Mörser / Mortar** – Goblinmörser (Schmuck) oder Bronzemörser

```
#showtooltip
/use [@cursor] Goblin Mortar
/use [@cursor] EZ-Thro Bronze Mortar
/use [@cursor] Portable Bronze Mortar
```

**Ingi-Teleport / Engi Teleport** – Gadgetzan; Shift: Everlook (Gnom- oder Goblin-Version)

```
#showtooltip
/use [nomod] Ultrasafe Transporter: Gadgetzan
/use [nomod] EZ-Thro Field Transporter: Gadgetzan
/use [mod:shift] Dimensional Ripper - Everlook
/use [mod:shift] SAF-T Emergency Ripper: Everlook
```

**Teleport Hyjal** – Hyjal-Transporter, welche Version du hast

```
#showtooltip
/use Dimensional Transporter - Mt. Hyjal
/use EZ and SAF Field Transporter: Mt. Hyjal
```

**Zielattrappe / Target Dummy** – Beste vorhandene Zielattrappe

```
#showtooltip
/use Masterwork Target Dummy
/use Advanced Target Dummy
/use Target Dummy
```

**Reparaturbot / Repair Bot**

```
#showtooltip
/use Field Repair Bot 74A
/use Repair Bot
```

</details>

<details><summary><b>Berufe / Professions</b> (7)</summary>

**Schleifstein / Sharpen** – Bester Wetzstein auf die Haupthand und bestätigen; Alt: Nebenhand

```
#showtooltip
/use Elemental Sharpening Stone
/use Dense Sharpening Stone
/use Solid Sharpening Stone
/use Heavy Sharpening Stone
/use Coarse Sharpening Stone
/use Rough Sharpening Stone
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Gewichtsstein / Weightstone** – Bester Gewichtsstein auf die Haupthand und bestätigen; Alt: Nebenhand

```
#showtooltip
/use Dense Weightstone
/use Solid Weightstone
/use Heavy Weightstone
/use Coarse Weightstone
/use Rough Weightstone
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Zauberöl / Wizard Oil** – Bestes Zauberöl auf die Haupthand und bestätigen; Alt: Nebenhand

```
#showtooltip
/use Brilliant Wizard Oil
/use Wizard Oil
/use Lesser Wizard Oil
/use Minor Wizard Oil
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Manaöl / Mana Oil** – Bestes Manaöl auf die Haupthand und bestätigen; Alt: Nebenhand

```
#showtooltip
/use Brilliant Mana Oil
/use Lesser Mana Oil
/use Minor Mana Oil
/use [mod:alt] 17; 16
/click StaticPopup1Button1
```

**Angeln+Köder / Fish + Lure** – Angeln; Shift: besten Köder an die Angel

```
#showtooltip
/use [mod:shift] Flesh Eating Worm
/use [mod:shift] Bright Baubles
/use [mod:shift] Aquadynamic Fish Attractor
/use [mod:shift] Nightcrawlers
/use [mod:shift] 16
/cast [nomod] Fishing
```

**Lagerfeuer / Campfire** – Bestes Lagerfeuer-Set, sonst normales Kochfeuer

```
#showtooltip
/use [@cursor] Expert Campfire Kit
/use [@cursor] Journeyman Campfire Kit
/use [@cursor] Basic Campfire Kit
/cast Basic Campfire
```

**Kräuter/Erze / Herbs/Ore** – Kräutersuche; Shift: Mineraliensuche

```
#showtooltip
/cast [mod:shift] Find Minerals; Find Herbs
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
- `python3 -I build/gen_fixtures.py db ForeverMacros/Data.lua test/fixtures.lua`: Zauber- und Gegenstandsnamen (en/de) für den Test.
- `cd test && luajit test.lua ../ForeverMacros`: Test mit nachgebauter WoW-API (alle Klassen, Deutsch/Englisch, niedrige/hohe Ränge).

## Quellen / Credits

Makrotexte angepasst nach / macro texts adapted from [Classic WoW Forever](https://classicwowforever.com/macros/) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) und [Zockify](https://www.zockify.com/forever/druid/macros/). Änderungen: Namen aus IDs lokalisiert, Ränge automatisch, einige Makros gekürzt. Details: `ForeverMacros/CREDITS.txt`.  
Idee des Zauber-Reiters nach / spell tab idea from [Macro Spellbook](https://github.com/notstraws/MacroSpellbook) (MIT); eigener Code, nichts übernommen.
