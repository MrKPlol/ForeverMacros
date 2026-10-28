# Macro library for ForeverMacros. {Spell} = spell (localized, raised to the highest known rank), {=Spell} = spell name
# without rank (for /cancelaura), {A|B} = first of A, B the character knows, <Item> = item (localized by item ID).
# {T:kind} / {T:kind:cond} = unit conditions the player picks per macro in the window (mouseover, focus, target, self,
# cursor); cond is put in front of every clause. Kinds: help, harm, any, dead, unit (always falls back to plain), ground
# (spell or item with a ground reticle, verified in SpellEffect: implicit target 16/87). One kind per macro.
# Only macros that do more than one spell with target options: single spells are built in the window's spell tab.
# Sources: classicwowforever.com macro pages (CC BY 4.0), zockify.com/forever druid macros, own adaptations.
# Fields: id, cat, name_de, name_en, body, (optional) note_de

DRUID = "DRUID"; WARRIOR = "WARRIOR"; PALADIN = "PALADIN"; HUNTER = "HUNTER"; ROGUE = "ROGUE"
PRIEST = "PRIEST"; SHAMAN = "SHAMAN"; MAGE = "MAGE"; WARLOCK = "WARLOCK"

MACROS = [
    # ---------------- Druid ----------------
    ("dru_shred", DRUID, "Schreddern/Shift", "Shred/Shift", "#showtooltip\n/startattack [nomod:shift,harm,nodead]\n/cast [mod:shift] {Shifting Power}; [harm,nodead] {Shred}", "Shred; Shift: Shifting Power (Mana in Energie)"),
    ("dru_powershift", DRUID, "Powershift", "Powershift", "#showtooltip\n/cancelform\n/cast [mod:shift] !{Dire Bear Form|Bear Form}; !{Cat Form}", "Gestalt neu betreten (Furor: Energie/Wut, löst Verlangsamungen); Shift: Bär. Steht man danach in Normalgestalt: nochmal drücken"),
    ("dru_prowl", DRUID, "Katze+Schleichen", "Cat+Prowl", "#showtooltip {Prowl}\n/cast !{Cat Form}\n/cast !{Prowl}", "Katzengestalt falls nötig, dann Schleichen (bricht es nicht ab)"),
    ("dru_dash", DRUID, "Katze+Spurt", "Cat+Dash", "#showtooltip {Dash}\n/cast !{Cat Form}\n/cast {Dash}", "Katzengestalt falls nötig, dann Spurt"),
    ("dru_catbear", DRUID, "Katze/Bär", "Cat/Bear", "#showtooltip [mod:shift] {Dire Bear Form|Bear Form}; {Cat Form}\n/dismount\n/cast [mod:shift] !{Dire Bear Form|Bear Form}; !{Cat Form}", "Katze; Shift: Bär (Terrorbär sobald gelernt). Nochmal drücken wirft dich nicht aus der Gestalt"),
    ("dru_travel", DRUID, "Reisen", "Travel", "#showtooltip\n/dismount\n/cast [swimming] {Aquatic Form}; [outdoors] {Travel Form}; {Cat Form}", "Wasser: Wassergestalt, draußen: Reisegestalt, drinnen: Katze"),
    ("dru_bark", DRUID, "Baumrinde/NG", "Barkskin/NG", "#showtooltip [mod:shift] {Nature's Grasp}; {Barkskin}\n/cast [mod:shift] {Nature's Grasp}; {Barkskin}", "Baumrinde; Shift: Griff der Natur (ohne Formwechsel)"),
    ("dru_hots", DRUID, "Verjüng/Nachw.", "Rejuv/Regrowth", "#showtooltip\n/cancelform\n/cast {T:help:mod:shift} {Regrowth}; {T:help} {Rejuvenation}", "Verjüngung; Shift: Nachwachsen (verlässt die Gestalt)"),
    ("dru_cleanse", DRUID, "Fluch/Gift", "Curse/Poison", "#showtooltip\n/cancelform\n/cast {T:help:mod:shift} {=Abolish Poison|Cure Poison}; {T:help} {=Remove Curse}", "Fluch aufheben; Shift: Gift (Vergiftung aufheben, sobald gelernt)"),
    ("dru_ns", DRUID, "NS + Heilen", "NS + Heal", "#showtooltip {Nature's Swiftness}\n/stopcasting\n/cancelform\n/cast {Nature's Swiftness}\n/cast {T:help} {Healing Touch}", "Schnelligkeit der Natur + sofortige Heilende Berührung"),
    ("dru_rez", DRUID, "Wiedergeb./Bel.", "Rebirth/Revive", "#showtooltip\n/cast {T:dead:combat} {Rebirth}\n/cast {T:dead:nocombat} {Revive}", "Kampf: Wiedergeburt, sonst Wiederbeleben"),
    ("dru_noform", DRUID, "Form weg", "Drop form", "/stopcasting\n/cancelform\n/dismount", "Zauber abbrechen, Gestalt verlassen, absitzen"),
    ("dru_maul", DRUID, "Urbiss+Zermalmen", "Bite+Maul", "#showtooltip {Primal Bite}\n/startattack\n/cast {Primal Bite}\n/cast [nomod:ctrl] {Maul}", "Bär: Urbiss und Zermalmen auf den nächsten Schlag; Strg: Wut sparen (ohne Zermalmen)"),
    ("dru_growl", DRUID, "Knurren/Gebrüll", "Growl/Roar", "#showtooltip\n/cast [mod:ctrl] {Challenging Roar}; {T:harm} {Growl}", "Knurren; Strg: Herausforderndes Gebrüll"),

    # ---------------- Warrior ----------------
    ("war_charge", WARRIOR, "Sturm+Angriff", "Charge+Attack", "#showtooltip {Charge}\n/dismount\n/startattack\n/cast {Charge}", None),
    ("war_chargeint", WARRIOR, "Charge/Abfangen", "Charge/Intercept", "#show [combat] {Intercept}; {Charge}\n/startattack\n/cast [nocombat,stance:1] {Charge}; [combat,stance:3] {Intercept}; [nocombat,nostance:1] {Battle Stance}; [combat,nostance:3] {Berserker Stance}", "Außerhalb Kampf Sturmangriff, im Kampf Abfangen (mit Haltungswechsel)"),
    ("war_rage", WARRIOR, "Haltung+Wut", "Stance+Rage", "#showtooltip {Berserker Rage}\n/cast [nostance:3] {Berserker Stance}\n/cast {Berserker Rage}", None),
    ("war_execute", WARRIOR, "Haltung+Hinricht", "Stance+Execute", "#showtooltip {Execute}\n/startattack\n/cast [stance:2] {Battle Stance}\n/cast {T:harm} {Execute}", None),
    ("war_hs", WARRIOR, "HS/Spalten", "HS/Cleave", "#show [mod:shift] {Cleave}; {Heroic Strike}\n/startattack\n/cast [mod:shift] {Cleave}; {Heroic Strike}", "Heldenhafter Stoß; Shift: Spalten"),
    ("war_shout", WARRIOR, "Rufe", "Shouts", "#showtooltip [mod:shift] {Demoralizing Shout}; {Battle Shout}\n/cast [mod:shift] {Demoralizing Shout}; {Battle Shout}", "Schlachtruf; Shift: Demoralisierender Ruf"),
    ("war_kick", WARRIOR, "Unterbrechen", "Interrupt", "#showtooltip\n/cast {T:harm:stance:3} {Pummel}; {T:harm} {Shield Bash}", "Berserkerhaltung: Zuschlagen, sonst Schildhieb (Schild nötig)"),
    ("war_taunt", WARRIOR, "Spott/Ruf", "Taunt/Shout", "#showtooltip\n/cast [mod:ctrl] {Challenging Shout}; {T:harm} {Taunt}", "Spott; Strg: Herausforderungsruf"),

    # ---------------- Paladin ----------------
    ("pal_bop", PALADIN, "Schutz", "BoP", "#showtooltip [mod:alt] {Divine Protection}; {Blessing of Protection}\n/cast [mod:alt] {Divine Protection}; {T:help} {Blessing of Protection}", "Alt: Göttlicher Schutz auf dich"),
    ("pal_aura", PALADIN, "Auren", "Auras", "#showtooltip [mod:shift] {Concentration Aura}; [mod:ctrl] {Retribution Aura}; {Devotion Aura}\n/cast [mod:shift] {Concentration Aura}; [mod:ctrl] {Retribution Aura}; {Devotion Aura}", "Hingabe; Shift: Konzentration; Strg: Vergeltung"),
    ("pal_resaura", PALADIN, "Resi-Auren", "Resist Auras", "#showtooltip\n/cast [mod:shift] {Frost Resistance Aura}; [mod:ctrl] {Shadow Resistance Aura}; {Fire Resistance Aura}", "Feuer; Shift: Frost; Strg: Schatten"),
    ("pal_bubble", PALADIN, "Gottesschild+Weg", "Bubble+Cancel", "#showtooltip {Divine Shield}\n/cancelaura {=Divine Shield}\n/cancelaura {=Divine Protection}\n/cancelaura {=Blessing of Protection}\n/cast {Divine Shield}", "Nochmal drücken: Schild beenden"),

    # ---------------- Hunter ----------------
    ("hun_mark", HUNTER, "Mal + Pet", "Mark + Pet", "#showtooltip {Hunter's Mark}\n/petattack {T:harm}\n/cast {T:harm} {Hunter's Mark}", None),
    ("hun_petmo", HUNTER, "Pet Angriff Ziel", "Pet Attack Unit", "/petattack {T:harm}", "Begleiter greift die gewählte Einheit an"),
    ("hun_petatt", HUNTER, "Pet Angriff", "Pet Attack", "/petattack [nomod:shift,harm,nodead]\n/petpassive [mod:shift]\n/petfollow [mod:shift]", "Shift: passiv + zurückrufen"),
    ("hun_pet", HUNTER, "Tier", "Pet", "#showtooltip\n/cast [@pet,dead][mod:shift] {Revive Pet}; [nopet] {Call Pet}; {Mend Pet}", "Rufen / heilen / wiederbeleben"),
    ("hun_hawk", HUNTER, "Falke", "Hawk", "#showtooltip {Aspect of the Hawk}\n/cancelaura {=Aspect of the Cheetah}\n/cast !{Aspect of the Hawk}", None),
    ("hun_cheetah", HUNTER, "Gepard/Rudel", "Cheetah/Pack", "#showtooltip {Aspect of the Cheetah}\n/cast [button:2] !{Aspect of the Pack}; !{Aspect of the Cheetah}", "Rechtsklick: Rudel"),
    ("hun_track", HUNTER, "Fährten", "Tracking", "#showtooltip\n/cast [mod:shift] {Track Beasts}; [mod:ctrl] {Track Undead}; [mod:alt] {Track Hidden}; {Track Humanoids}", None),
    ("hun_fd", HUNTER, "Totstellen+Stop", "Feign+Stop", "#showtooltip {Feign Death}\n/petpassive\n/petfollow\n/stopattack\n/stopcasting\n/cast [combat] {Feign Death}", None),
    ("hun_noaspect", HUNTER, "Aspekt weg", "Cancel Aspect", "/cancelaura {=Aspect of the Cheetah}\n/cancelaura {=Aspect of the Pack}", None),
    ("hun_trap", HUNTER, "Totst.+Falle", "Feign+Trap", "#showtooltip {Freezing Trap}\n/petpassive\n/petfollow\n/stopattack\n/cast [combat] {Feign Death}\n/cast [nocombat] {Freezing Trap}", "Im Kampf: Totstellen, nochmal drücken: Eiskältefalle"),

    # ---------------- Rogue ----------------
    ("rog_stealth", ROGUE, "Verstohl. sicher", "Stealth (safe)", "#showtooltip {Stealth}\n/dismount\n/cast [nostealth,nocombat] {Stealth}", "Schaltet sich nicht selbst ab"),
    ("rog_opener", ROGUE, "Opener", "Opener", "#showtooltip\n/cast [stealth] {Pick Pocket}\n/cast [nostealth] {Stealth}; [mod:shift] {Garrote}; [mod:ctrl] {Ambush}; {Cheap Shot}", "Taschendiebstahl + Fieser Trick; Shift: Erdrosseln; Strg: Hinterhalt"),
    ("rog_evasion", ROGUE, "Entrinnen+Sprint", "Evasion+Sprint", "#showtooltip {Evasion}\n/cast {Evasion}\n/cast {Sprint}", None),
    ("rog_poison", ROGUE, "Gift auftragen", "Apply Poison", "#showtooltip\n/use [mod:shift] <Deadly Poison>; <Instant Poison>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Sofort-Gift; Shift: tödliches Gift; Alt: Nebenhand"),
    ("rog_vanish", ROGUE, "Stealth/Vanish", "Stealth/Vanish", "#showtooltip [nocombat] {Stealth}; {Vanish}\n/stopattack [combat]\n/cast [nocombat] !{Stealth}; {Vanish}", None),

    # ---------------- Priest ----------------
    ("pri_wand", PRIEST, "Zauberstab", "Wand", "#showtooltip {Shoot}\n/cast !{Shoot}", None),
    ("pri_levitate", PRIEST, "Levitieren+Weg", "Levitate+Off", "#showtooltip {Levitate}\n/dismount\n/cancelaura [mod:shift] {=Levitate}\n/cast [nomod] {Levitate}", "Shift: abbrechen"),
    ("pri_buffs", PRIEST, "Selbstbuffs", "Self Buffs", "#showtooltip\n/castsequence [@player] reset=15 {Inner Fire}, {Power Word: Fortitude}, {Divine Spirit}", None),
    ("pri_healsmite", PRIEST, "Heilen/Peinigen", "Heal/Smite", "#showtooltip\n/cast [@mouseover,help,nodead] {Lesser Heal}; [harm,nodead] {Smite}; [help,nodead][@player] {Lesser Heal}", None),
    ("pri_inner", PRIEST, "Innerer Fokus+", "Inner Focus+", "#showtooltip\n/cast {Inner Focus}\n/cast [mod:shift] {Mind Blast}; {T:help} {Greater Heal|Heal}", "Innerer Fokus + Große Heilung; Shift: + Gedankenschlag"),

    # ---------------- Shaman ----------------
    ("sha_totems", SHAMAN, "Totems", "Totems", "#showtooltip [mod:shift] {Totemic Recall}; {Call of the Elements}\n/cast [mod:shift] {Totemic Recall}; {Call of the Elements}", "Shift: zurückrufen"),
    ("sha_totems3", SHAMAN, "Totem-Sets", "Totem Sets", "#showtooltip\n/cast [mod:ctrl] {Call of the Ancestors}; [mod:alt] {Call of the Spirits}; [mod:shift] {Totemic Recall}; {Call of the Elements}", "Strg/Alt: andere Sets; Shift: zurückrufen"),
    ("sha_shield", SHAMAN, "Schild", "Shield", "#showtooltip [mod:shift] {Water Shield}; {Lightning Shield}\n/cast [mod:shift] {Water Shield}; {Lightning Shield}", "Shift: Wasserschild"),
    ("sha_shocks", SHAMAN, "Schocks", "Shocks", "#showtooltip [mod:shift] {Flame Shock}; [mod:ctrl] {Frost Shock}; {Earth Shock}\n/cast [mod:shift] {Flame Shock}; [mod:ctrl] {Frost Shock}; {Earth Shock}", "Shift: Flamme; Strg: Frost"),
    ("sha_cure", SHAMAN, "Heilung Gift", "Cure", "#showtooltip\n/cast {T:help:mod:shift} {Cure Disease}; {T:help} {Cure Poison}", "Shift: Krankheit"),
    ("sha_selfheal", SHAMAN, "Selbst heilen", "Self Heal", "#showtooltip [mod:shift] {Lesser Healing Wave}; {Healing Wave}\n/cast [mod:shift,@player] {Lesser Healing Wave}; [@player] {Healing Wave}", None),
    ("sha_water", SHAMAN, "Wasserw./Atmung", "WaterWalk/Breath", "#showtooltip\n/cast {T:help:mod:shift} {Water Breathing}; {T:help} {Water Walking}", "Shift: Wasseratmung"),
    ("sha_ns", SHAMAN, "NS + Heilen", "NS + Heal", "#showtooltip {Nature's Swiftness}\n/stopcasting\n/cast {Nature's Swiftness}\n/cast {T:help} {Healing Wave}", "Schnelligkeit der Natur + sofortige Welle der Heilung"),

    # ---------------- Mage ----------------
    ("mag_ai", MAGE, "Intelligenz", "Intellect", "#showtooltip\n/cast {T:help:mod:shift} {Arcane Brilliance}; {T:help} {Arcane Intellect}", "Shift: Arkane Brillanz"),
    ("mag_dampen", MAGE, "Dämpfen/Verst.", "Dampen/Amplify", "#showtooltip\n/cast {T:help:mod:shift} {Amplify Magic}; {T:help} {Dampen Magic}", "Shift: Magie verstärken"),
    ("mag_conjure", MAGE, "Herbeizaubern", "Conjure", "#showtooltip [mod:shift] {Conjure Food}; {Conjure Water}\n/cast [mod:shift] {Conjure Food}; {Conjure Water}", "Wasser; Shift: Essen"),
    ("mag_armor", MAGE, "Rüstung", "Armor", "#showtooltip [mod:shift] {Mage Armor}; [mod:ctrl] {Frost Armor}; {Ice Armor}\n/cast [mod:shift] {Mage Armor}; [mod:ctrl] {Frost Armor}; {Ice Armor}", "Eisrüstung; Shift: Magier; Strg: Frost"),
    ("mag_tele_a", MAGE, "Teleport (A)", "Teleport (A)", "#showtooltip\n/cast [mod:shift] {Teleport: Ironforge}; [mod:ctrl] {Teleport: Darnassus}; [mod:alt] {Teleport: Dalaran}; {Teleport: Stormwind}", "Allianz"),
    ("mag_tele_h", MAGE, "Teleport (H)", "Teleport (H)", "#showtooltip\n/cast [mod:shift] {Teleport: Undercity}; [mod:ctrl] {Teleport: Thunder Bluff}; [mod:alt] {Teleport: Dalaran}; {Teleport: Orgrimmar}", "Horde"),
    ("mag_portal_a", MAGE, "Portal (A)", "Portal (A)", "#showtooltip\n/cast [mod:shift] {Portal: Ironforge}; [mod:ctrl] {Portal: Darnassus}; {Portal: Stormwind}", "Allianz"),
    ("mag_portal_h", MAGE, "Portal (H)", "Portal (H)", "#showtooltip\n/cast [mod:shift] {Portal: Undercity}; [mod:ctrl] {Portal: Thunder Bluff}; {Portal: Orgrimmar}", "Horde"),
    ("mag_slowfall", MAGE, "Langs. Fall+Weg", "Slow Fall+Off", "#showtooltip {Slow Fall}\n/dismount [nomod:shift]\n/cancelaura [mod:shift] {=Slow Fall}\n/cast [nomod:shift,@player] {Slow Fall}", "Shift: abbrechen"),
    ("mag_iceblock", MAGE, "Eisblock+Weg", "Ice Block+Off", "#showtooltip {Ice Block}\n/cancelaura {=Ice Block}\n/cast {Ice Block}", "Nochmal drücken: Eisblock beenden"),
    ("mag_burst", MAGE, "GG+AM+Pyro", "PoM+AP+Pyro", "#showtooltip\n/cast {Presence of Mind}\n/cast {Arcane Power}\n/cast {T:harm} {Pyroblast|Fireball}", "Geistesgegenwart + Arkane Macht + Pyroschlag (sonst Feuerball)"),

    # ---------------- Warlock ----------------
    ("wlk_petback", WARLOCK, "Dämon zurück", "Pet Back", "/petpassive\n/petfollow", None),
    ("wlk_summon", WARLOCK, "Dämon rufen", "Summon Demon", "#showtooltip\n/cast [mod:shift] {Summon Imp}; [mod:ctrl] {Summon Succubus}; [mod:alt] {Summon Felhunter}; {Summon Voidwalker}", "Leerwandler; Shift: Wichtel; Strg: Sukkubus; Alt: Teufelsjäger"),
    ("wlk_feldom", WARLOCK, "Teufelsb.+Dämon", "FelDom+Summon", "#showtooltip\n/cast {Fel Domination}\n/cast [mod:shift] {Summon Imp}; [mod:ctrl] {Summon Succubus}; [mod:alt] {Summon Felhunter}; {Summon Voidwalker}", "Teufelsbeherrschung, dann Dämon (Tasten wie Dämon rufen)"),
    ("wlk_lock", WARLOCK, "Zaubersperre", "Spell Lock", "#showtooltip\n/cast {T:harm} {=Spell Lock}", "Teufelsjäger: Unterbrechen (Fokus/Mouseover)"),
    ("wlk_devour", WARLOCK, "Magie verschl.", "Devour Magic", "#showtooltip\n/cast {T:any} {=Devour Magic}", "Teufelsjäger: Magie bannen, Freund oder Feind"),
    ("wlk_curse", WARLOCK, "Flüche", "Curses", "#showtooltip\n/cast [mod:shift] {Curse of Weakness}; [mod:ctrl] {Curse of Recklessness}; [mod:alt] {Curse of Tongues}; {T:harm} {Curse of the Elements}", "Elemente; Shift: Schwäche; Strg: Tollkühnheit; Alt: Sprachen"),
    ("wlk_dots", WARLOCK, "DoT-Folge", "DoT Sequence", "#showtooltip\n/petattack [harm,nodead]\n/castsequence reset=target {Immolate}, {Bane of Agony}, {Corruption}, !{Shoot}", "Leveln: Opfern, Pein, Verderbnis, Zauberstab"),
    ("wlk_wand", WARLOCK, "Zauberstab", "Wand", "#showtooltip {Shoot}\n/cast !{Shoot}", None),
    ("wlk_ss", WARLOCK, "Seelenstein", "Soulstone", "#showtooltip\n/use [@mouseover,help][] <Major Soulstone>\n/use [@mouseover,help][] <Greater Soulstone>\n/use [@mouseover,help][] <Soulstone>\n/use [@mouseover,help][] <Lesser Soulstone>\n/use [@mouseover,help][] <Minor Soulstone>", None),
    ("wlk_stones", WARLOCK, "Steine erstellen", "Create Stones", "#showtooltip\n/cast [mod:shift] {Create Soulstone}; [mod:ctrl] {Create Spellstone}; [mod:alt] {Create Firestone}; {Create Healthstone}", None),
    ("wlk_ritual", WARLOCK, "Beschwörung", "Summoning", "#showtooltip {Ritual of Summoning}\n/party Beschwöre %t, bitte Portal anklicken\n/cast {Ritual of Summoning}", "Kündigt die Beschwörung in der Gruppe an"),
    ("wlk_armor", WARLOCK, "Rüstung/Schutz", "Armor/Ward", "#showtooltip [mod:shift] {Shadow Ward}; {Demon Armor}\n/cast [mod:shift] {Shadow Ward}; {Demon Armor}", "Shift: Schattenzauberschutz"),
]

# Racial macros: one per active racial (filtered in game by whether the character knows it).
RACIAL_NAMES = {}
# Racial macros (character tab, listed when the character knows the ability): (id, body). Only combos that add something
# over the ability itself on a bar.
RACIALS = [
    ("rac_meld", "#showtooltip {Shadowmeld}\n/stopattack\n/stopcasting\n/cast {Shadowmeld}", "Kampf/Zauber stoppen, dann Schattenmimik (sonst bricht sie sofort)"),
    ("rac_bloodfury", "#showtooltip {Blood Fury}\n/cast {Blood Fury}\n/use 13\n/use 14", "Kochendes Blut + beide Schmuckstücke"),
    ("rac_berserking", "#showtooltip {Berserking}\n/cast {Berserking}\n/use 13\n/use 14", "Berserker + beide Schmuckstücke"),
    ("rac_walkair", "#showtooltip {Walk on Air}\n/dismount\n/cast {Walk on Air}", "Absitzen und sofort gleiten (auch mitten im Flug)"),
]

# Utility macros (general tab, for all characters): (id, group, name_de, name_en, body, note_de)
# Engineering: every item checked in 1.60.1.70532 (ItemEffect on-use spell, its implicit target, inventory slot).
# Tinkers (Teleport, Nitro Boosts, Magnetic Displacement) are belt enchantments (SpellEquippedItems: waist only).
UTILITY = [
    ("u_trinkets", "equip", "Schmuck 1+2", "Trinkets", "#showtooltip\n/use {T:unit} 13\n/use {T:unit} 14", "Beide Schmuckstücke (Ziel-Optionen für Netz, Schrumpfstrahl & Co.)"),
    ("u_trinket1", "equip", "Schmuck oben", "Trinket 1", "#showtooltip 13\n/use {T:unit} 13", None),
    ("u_trinket2", "equip", "Schmuck unten", "Trinket 2", "#showtooltip 14\n/use {T:unit} 14", None),
    ("u_focus", "general", "Fokus setzen", "Set Focus", "/focus [@mouseover,exists,nodead][]", "Mouseover, sonst Ziel als Fokus"),
    ("u_clearfocus", "general", "Fokus weg", "Clear Focus", "/clearfocus", None),
    ("u_skull", "general", "Totenkopf", "Skull", "/tm 8", "Totenkopf aufs Ziel"),
    ("u_nomark", "general", "Marker weg", "Clear Mark", "/tm 0", "Zielmarkierung entfernen"),
    ("u_accept", "general", "Bestätigen", "Confirm", "/click StaticPopup1Button1", "Klickt 'Annehmen' im obersten Dialog"),
    ("u_release", "general", "Geist freilassen", "Release Spirit", "/run RepopMe()", None),
    ("u_reset", "general", "Instanz-Reset", "Reset Instances", "/run ResetInstances()", None),
    ("u_leave", "general", "Gruppe verlassen", "Leave Group", "/run C_PartyInfo.LeaveParty()", None),
    ("u_reload", "general", "UI neu laden", "Reload UI", "/reload", None),
    ("u_quest", "quests", "Quest an/ab", "Quest Accept", "/click QuestFrameAcceptButton\n/click QuestFrameCompleteButton\n/click QuestFrameCompleteQuestButton", "Nimmt an / gibt ab im offenen Questfenster"),
    ("u_share", "quests", "Quest teilen", "Share Quest", "/run local q=C_QuestLog.GetSelectedQuest() if q and q>0 then QuestLogPushQuest(C_QuestLog.GetLogIndexForQuestID(q)) end", "Teilt die im Questlog ausgewählte Quest"),

    # ---------------- Engineering: equipped gadgets and enchantments ----------------
    ("u_tinker", "engineering", "Gürtel-Tinker", "Belt Tinker", "#showtooltip 6\n/use {T:unit} 6", "Ingi-Verzauberung am Gürtel: Teleport, Nitro Boosts oder Magnetic Displacement (Ziel-Optionen nur für Letzteres nötig)"),
    ("u_engislots", "engineering", "Ingi-Slots", "Engi Slots", "#showtooltip\n/use [mod:shift] 1; [mod:ctrl] 6; [mod:alt] 15; 8", "Stiefel; Shift: Helm; Strg: Gürtel; Alt: Umhang (Raketenstiefel, Kappe, Fallschirm …) – egal welches Teil angelegt ist"),
    ("u_net", "engineering", "Net-o-Matik", "Net-o-Matic", "#showtooltip\n/use {T:harm} <Gnomish Net-o-Matic Projector>", None),
    ("u_shrink", "engineering", "Schrumpfstrahl", "Shrink Ray", "#showtooltip\n/use {T:harm} <Gnomish Shrink Ray>", None),
    ("u_poultry", "engineering", "Geflügelisierer", "Poultryizer", "#showtooltip\n/use {T:harm} <Gnomish Poultryizer>", None),
    ("u_deathray", "engineering", "Todesstrahl", "Death Ray", "#showtooltip\n/use {T:harm} <Gnomish Death Ray>", None),
    ("u_discomb", "engineering", "Diskombobulator", "Discombobulator", "#showtooltip\n/use {T:harm} <Discombobulator Ray>", None),
    ("u_mccap", "engineering", "Gedankenkappe", "Mind Control Cap", "#showtooltip\n/use {T:harm} <Gnomish Mind Control Cap>", "Kopf"),
    ("u_rockethelm", "engineering", "Raketenhelm", "Rocket Helmet", "#showtooltip\n/use {T:harm} <Goblin Rocket Helmet>", "Kopf: Ansturm aufs Ziel"),
    ("u_recomb", "engineering", "Rekombobulator", "Recombobulator", "#showtooltip\n/use {T:help} <Major Recombobulator>\n/use {T:help} <Minor Recombobulator>", "Hebt Verwandlung auf, großer zuerst"),
    ("u_reflect", "engineering", "Reflektor", "Reflector", "#showtooltip\n/use [mod:shift] <Gyrofreeze Ice Reflector>; [mod:ctrl] <Ultra-Flash Shadow Reflector>; <Hyper-Radiant Flame Reflector>", "Feuer; Shift: Frost; Strg: Schatten"),
    ("u_cloak", "engineering", "Tarnung", "Cloaking", "#showtooltip\n/stopattack\n/stopcasting\n/use <Emergency Field Cloak>\n/use <Gnomish Cloaking Device>\n/use <Stealthman 52>", "Kampf/Zauber stoppen, dann Tarnung"),

    # ---------------- Engineering: thrown and placed ----------------
    ("u_bomb", "engineering", "Bombe", "Bomb", "#showtooltip\n/use {T:ground} <EZ-Thro Dark Bomb>\n/use {T:ground} <EZ-Thro Thorium Grenade>\n/use {T:ground} <Dark Iron Bomb>\n/use {T:ground} <Thorium Grenade>\n/use {T:ground} <Tru-Trigger Frag Bomb>\n/use {T:ground} <SAF-T Bomb>", "Beste vorhandene Bombe/Granate"),
    ("u_bomb_low", "engineering", "Bombe (klein)", "Bomb (low)", "#showtooltip\n/use {T:ground} <Hi-Explosive Bomb>\n/use {T:ground} <Mithril Frag Bomb>\n/use {T:ground} <Big Iron Bomb>\n/use {T:ground} <EZ-Thro Grenade>\n/use {T:ground} <Iron Grenade>\n/use {T:ground} <SAF-T Bronze Bomb>", "Wie Bombe, für niedrigere Stufen"),
    ("u_manabomb", "engineering", "Manabombe", "Mana Bomb", "#showtooltip\n/use {T:ground} <EZ-Thro Mana Bomb>\n/use {T:ground} <Arcane Bomb>", "Entzieht Mana"),
    ("u_dynamite", "engineering", "Dynamit", "Dynamite", "#showtooltip\n/use {T:ground} <SAF-T Clever Dynamite>\n/use {T:ground} <Dense Dynamite>\n/use {T:ground} <Ez-Thro Dynamite II>\n/use {T:ground} <SAF-T Jumbo Dynamite>\n/use {T:ground} <Solid Dynamite>\n/use {T:ground} <Heavy Dynamite>", "Bestes vorhandenes Dynamit"),
    ("u_dynamite_low", "engineering", "Dynamit (klein)", "Dynamite (low)", "#showtooltip\n/use {T:ground} <Ez-Thro Dynamite>\n/use {T:ground} <SAF-T Dynamite>\n/use {T:ground} <Coarse Dynamite>\n/use {T:ground} <Rough Dynamite>", "Wie Dynamit, für niedrige Stufen"),
    ("u_mortar", "engineering", "Mörser", "Mortar", "#showtooltip\n/use {T:ground} <Goblin Mortar>\n/use {T:ground} <EZ-Thro Bronze Mortar>\n/use {T:ground} <Portable Bronze Mortar>", "Goblinmörser (Schmuck) oder Bronzemörser"),
    ("u_engiport", "engineering", "Ingi-Teleport", "Engi Teleport", "#showtooltip\n/use [nomod] <Ultrasafe Transporter: Gadgetzan>\n/use [nomod] <EZ-Thro Field Transporter: Gadgetzan>\n/use [mod:shift] <Dimensional Ripper - Everlook>\n/use [mod:shift] <SAF-T Emergency Ripper: Everlook>", "Gadgetzan; Shift: Everlook (Gnom- oder Goblin-Version)"),
    ("u_engihyjal", "engineering", "Teleport Hyjal", "Teleport Hyjal", "#showtooltip\n/use <Dimensional Transporter - Mt. Hyjal>\n/use <EZ and SAF Field Transporter: Mt. Hyjal>", "Hyjal-Transporter, welche Version du hast"),
    ("u_dummy", "engineering", "Zielattrappe", "Target Dummy", "#showtooltip\n/use <Masterwork Target Dummy>\n/use <Advanced Target Dummy>\n/use <Target Dummy>", "Beste vorhandene Zielattrappe"),
    ("u_repairbot", "engineering", "Reparaturbot", "Repair Bot", "#showtooltip\n/use <Field Repair Bot 74A>\n/use <Repair Bot>", None),

    # ---------------- Professions ----------------
    ("u_sharpen", "professions", "Schleifstein", "Sharpen", "#showtooltip\n/use <Elemental Sharpening Stone>\n/use <Dense Sharpening Stone>\n/use <Solid Sharpening Stone>\n/use <Heavy Sharpening Stone>\n/use <Coarse Sharpening Stone>\n/use <Rough Sharpening Stone>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Bester Wetzstein auf die Haupthand und bestätigen; Alt: Nebenhand"),
    ("u_weight", "professions", "Gewichtsstein", "Weightstone", "#showtooltip\n/use <Dense Weightstone>\n/use <Solid Weightstone>\n/use <Heavy Weightstone>\n/use <Coarse Weightstone>\n/use <Rough Weightstone>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Bester Gewichtsstein auf die Haupthand und bestätigen; Alt: Nebenhand"),
    ("u_wizoil", "professions", "Zauberöl", "Wizard Oil", "#showtooltip\n/use <Brilliant Wizard Oil>\n/use <Wizard Oil>\n/use <Lesser Wizard Oil>\n/use <Minor Wizard Oil>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Bestes Zauberöl auf die Haupthand und bestätigen; Alt: Nebenhand"),
    ("u_manaoil", "professions", "Manaöl", "Mana Oil", "#showtooltip\n/use <Brilliant Mana Oil>\n/use <Lesser Mana Oil>\n/use <Minor Mana Oil>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Bestes Manaöl auf die Haupthand und bestätigen; Alt: Nebenhand"),
    ("u_fishing", "professions", "Angeln+Köder", "Fish + Lure", "#showtooltip\n/use [mod:shift] <Flesh Eating Worm>\n/use [mod:shift] <Bright Baubles>\n/use [mod:shift] <Aquadynamic Fish Attractor>\n/use [mod:shift] <Nightcrawlers>\n/use [mod:shift] 16\n/cast [nomod] {Fishing}", "Angeln; Shift: besten Köder an die Angel"),
    ("u_campfire", "professions", "Lagerfeuer", "Campfire", "#showtooltip\n/use {T:ground} <Expert Campfire Kit>\n/use {T:ground} <Journeyman Campfire Kit>\n/use {T:ground} <Basic Campfire Kit>\n/cast {Basic Campfire}", "Bestes Lagerfeuer-Set, sonst normales Kochfeuer"),
    ("u_find", "professions", "Kräuter/Erze", "Herbs/Ore", "#showtooltip\n/cast [mod:shift] {Find Minerals}; {Find Herbs}", "Kräutersuche; Shift: Mineraliensuche"),
]
