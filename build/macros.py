# Macro library for ForeverMacros. {Spell} = spell (localized, raised to the highest known rank), {=Spell} = spell name
# without rank (for /cancelaura), {A|B} = first of A, B the character knows, <Item> = item (localized by item ID).
# Sources: classicwowforever.com macro pages (CC BY 4.0), zockify.com/forever druid macros, own adaptations.
# Fields: id, cat, name_de, name_en, body, (optional) note_de

DRUID = "DRUID"; WARRIOR = "WARRIOR"; PALADIN = "PALADIN"; HUNTER = "HUNTER"; ROGUE = "ROGUE"
PRIEST = "PRIEST"; SHAMAN = "SHAMAN"; MAGE = "MAGE"; WARLOCK = "WARLOCK"

MO_HELP = "[@mouseover,help,nodead][help,nodead][@player]"

MACROS = [
    # ---------------- Druid ----------------
    ("dru_shred", DRUID, "Schreddern/Shift", "Shred/Shift", "#showtooltip\n/startattack [nomod:shift,harm,nodead]\n/cast [mod:shift] {Shifting Power}; [harm,nodead] {Shred}", "Shred; Shift: Shifting Power (Mana in Energie)"),
    ("dru_prowl", DRUID, "Schleichen", "Prowl", "#showtooltip {Prowl}\n/cast !{Cat Form}\n/cast !{Prowl}", "Katzengestalt falls nötig, dann Schleichen (bricht es nicht ab)"),
    ("dru_dash", DRUID, "Spurt", "Dash", "#showtooltip {Dash}\n/cast !{Cat Form}\n/cast {Dash}", "Katzengestalt falls nötig, dann Spurt"),
    ("dru_catbear", DRUID, "Katze/Bär", "Cat/Bear", "#showtooltip [mod:shift] {Dire Bear Form|Bear Form}; {Cat Form}\n/dismount\n/cast [mod:shift] {Dire Bear Form|Bear Form}; {Cat Form}", "Katze; Shift: Bär (Terrorbär sobald gelernt)"),
    ("dru_travel", DRUID, "Reisen", "Travel", "#showtooltip\n/dismount\n/cast [swimming] {Aquatic Form}; [outdoors] {Travel Form}; {Cat Form}", "Wasser: Wassergestalt, draußen: Reisegestalt, drinnen: Katze"),
    ("dru_ff", DRUID, "Feenfeuer", "Faerie Fire", "#showtooltip {Faerie Fire}\n/cast [@mouseover,harm,nodead][harm,nodead] {Faerie Fire}", "Mouseover, sonst Ziel"),
    ("dru_charge", DRUID, "Wilde Attacke", "Feral Charge", "#showtooltip {Feral Charge}\n/cast [@mouseover,harm,nodead][harm,nodead] {Feral Charge}", "Mouseover, sonst Ziel (Talent)"),
    ("dru_berserk", DRUID, "Berserk (Druide)", "Berserk (Druid)", "#showtooltip {Berserk}\n/cast {Berserk}", "Talent ab 40"),
    ("dru_bark", DRUID, "Baumrinde/NG", "Barkskin/NG", "#showtooltip [mod:shift] {Nature's Grasp}; {Barkskin}\n/cast [mod:shift] {Nature's Grasp}; {Barkskin}", "Baumrinde; Shift: Griff der Natur (ohne Formwechsel)"),
    ("dru_primal", DRUID, "Urbiss", "Primal Bite", "#showtooltip {Primal Bite}\n/startattack [harm,nodead]\n/cast [harm,nodead] {Primal Bite}", "Bär, Talent ab 25"),
    ("dru_lacerate", DRUID, "Aufschlitzen", "Lacerate", "#showtooltip {Lacerate}\n/cast [@mouseover,harm,nodead][harm,nodead] {Lacerate}", "Terrorbär ab 42"),
    ("dru_growl", DRUID, "Knurren", "Growl", "#showtooltip {Growl}\n/cast [@mouseover,harm,nodead][harm,nodead] {Growl}", "Spott auf Mouseover/Ziel (Bär)"),
    ("dru_rejuv", DRUID, "Verjüngung MO", "Rejuv MO", "#showtooltip {Rejuvenation}\n/cancelform\n/cast " + MO_HELP + " {Rejuvenation}", None),
    ("dru_regrowth", DRUID, "Nachwachsen MO", "Regrowth MO", "#showtooltip {Regrowth}\n/cancelform\n/cast " + MO_HELP + " {Regrowth}", None),
    ("dru_heal", DRUID, "Heilen", "Heal", "#showtooltip {Healing Touch}\n/cancelform\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] {Regrowth}; [@mouseover,help,nodead][@player] {Healing Touch}", "Heilende Berührung; Shift: Nachwachsen (Mouseover/selbst)"),
    ("dru_ns", DRUID, "NS + Heilen", "NS + Heal", "#showtooltip {Nature's Swiftness}\n/stopcasting\n/cancelform\n/cast {Nature's Swiftness}\n/cast " + MO_HELP + " {Healing Touch}", "Schnelligkeit der Natur + sofortige Heilende Berührung"),
    ("dru_swiftmend", DRUID, "Rasche Heilung", "Swiftmend", "#showtooltip {Swiftmend}\n/cancelform\n/cast " + MO_HELP + " {Swiftmend}", "Talent"),
    ("dru_wildgrowth", DRUID, "Wildwuchs", "Wild Growth", "#showtooltip {Wild Growth}\n/cancelform\n/cast " + MO_HELP + " {Wild Growth}", "Talent"),
    ("dru_curse", DRUID, "Fluch aufheben", "Remove Curse", "#showtooltip {Remove Curse}\n/cancelform\n/cast " + MO_HELP + " {Remove Curse}", None),
    ("dru_poison", DRUID, "Gift heilen", "Cure Poison", "#showtooltip {Cure Poison}\n/cancelform\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] {Abolish Poison}; " + MO_HELP + " {Cure Poison}", "Shift: Vergiftung aufheben"),
    ("dru_innervate", DRUID, "Anregen MO", "Innervate MO", "#showtooltip {Innervate}\n/cast " + MO_HELP + " {Innervate}", None),
    ("dru_rez", DRUID, "Wiederbeleben", "Rebirth/Revive", "#showtooltip [combat] {Rebirth}; {Revive}\n/cast [@mouseover,help,dead,combat][help,dead,combat] {Rebirth}\n/cast [@mouseover,help,dead,nocombat][help,dead,nocombat] {Revive}", "Kampf: Wiedergeburt, sonst Wiederbeleben"),
    ("dru_motw", DRUID, "Mal/Dornen", "MotW/Thorns", "#showtooltip [mod:shift] {Thorns}; {Mark of the Wild}\n/cancelform\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] {Thorns}; " + MO_HELP + " {Mark of the Wild}", "Mal der Wildnis; Shift: Dornen"),
    ("dru_roots", DRUID, "Wurzeln MO", "Roots MO", "#showtooltip {Entangling Roots}\n/cancelform\n/cast [@mouseover,harm,nodead][harm,nodead] {Entangling Roots}", None),
    ("dru_hurricane", DRUID, "Hurrikan", "Hurricane", "#showtooltip {Hurricane}\n/cancelform\n/cast [@cursor] {Hurricane}", "Direkt an der Mausposition"),
    ("dru_noform", DRUID, "Form weg", "Drop form", "/stopcasting\n/cancelform\n/dismount", "Zauber abbrechen, Gestalt verlassen, absitzen"),

    # ---------------- Warrior ----------------
    ("war_charge", WARRIOR, "Sturmangriff", "Charge", "#showtooltip {Charge}\n/dismount\n/startattack\n/cast {Charge}", None),
    ("war_chargeint", WARRIOR, "Charge/Abfangen", "Charge/Intercept", "#show [combat] {Intercept}; {Charge}\n/startattack\n/cast [nocombat,stance:1] {Charge}; [combat,stance:3] {Intercept}; [nocombat,nostance:1] {Battle Stance}; [combat,nostance:3] {Berserker Stance}", "Außerhalb Kampf Sturmangriff, im Kampf Abfangen (mit Haltungswechsel)"),
    ("war_vr", WARRIOR, "Siegesrausch", "Victory Rush", "#showtooltip {Victory Rush}\n/startattack\n/cast {Victory Rush}", None),
    ("war_rage", WARRIOR, "Berserkerwut", "Berserker Rage", "#showtooltip {Berserker Rage}\n/cast [nostance:3] {Berserker Stance}\n/cast {Berserker Rage}", None),
    ("war_execute", WARRIOR, "Hinrichten", "Execute", "#showtooltip {Execute}\n/startattack\n/cast [stance:2] {Battle Stance}\n/cast [mod:shift,@mouseover,harm,nodead] {Execute}; {Execute}", "Shift: auf Mouseover"),
    ("war_hs", WARRIOR, "HS/Spalten", "HS/Cleave", "#show [mod:shift] {Cleave}; {Heroic Strike}\n/startattack\n/cast [mod:shift] {Cleave}; {Heroic Strike}", "Heldenhafter Stoß; Shift: Spalten"),
    ("war_bloodrage", WARRIOR, "Blutrausch+Trank", "Bloodrage+Pot", "#showtooltip {Bloodrage}\n/cast {Bloodrage}\n/use <Mighty Rage Potion>\n/use <Great Rage Potion>\n/use <Rage Potion>", "Blutrausch und bester Wuttrank"),
    ("war_shout", WARRIOR, "Rufe", "Shouts", "#showtooltip [mod:shift] {Demoralizing Shout}; {Battle Shout}\n/cast [mod:shift] {Demoralizing Shout}; {Battle Shout}", "Schlachtruf; Shift: Demoralisierender Ruf"),

    # ---------------- Paladin ----------------
    ("pal_hs", PALADIN, "Heiliger Stoß", "Holy Strike", "#showtooltip {Holy Strike}\n/startattack\n/cast {Holy Strike}", None),
    ("pal_bop", PALADIN, "Schutz MO", "BoP MO", "#showtooltip [mod:alt] {Divine Protection}; {Blessing of Protection}\n/cast [mod:alt] {Divine Protection}; [@mouseover,help,nodead][help,nodead][@targettarget,help,nodead] {Blessing of Protection}", "Alt: Göttlicher Schutz auf dich"),
    ("pal_bless", PALADIN, "Segen", "Blessings", "#showtooltip\n/cast [mod:shift,@mouseover,help,nodead][mod:shift] {Blessing of Wisdom}; [mod:ctrl,@mouseover,help,nodead][mod:ctrl] {Blessing of Kings}; [@mouseover,help,nodead][] {Blessing of Might}", "Macht; Shift: Weisheit; Strg: Könige"),
    ("pal_aura", PALADIN, "Auren", "Auras", "#showtooltip [mod:shift] {Concentration Aura}; [mod:ctrl] {Retribution Aura}; {Devotion Aura}\n/cast [mod:shift] {Concentration Aura}; [mod:ctrl] {Retribution Aura}; {Devotion Aura}", "Hingabe; Shift: Konzentration; Strg: Vergeltung"),
    ("pal_resaura", PALADIN, "Resi-Auren", "Resist Auras", "#showtooltip\n/cast [mod:shift] {Frost Resistance Aura}; [mod:ctrl] {Shadow Resistance Aura}; {Fire Resistance Aura}", "Feuer; Shift: Frost; Strg: Schatten"),
    ("pal_loh", PALADIN, "Handauflegung MO", "LoH MO", "#showtooltip {Lay on Hands}\n/cast " + MO_HELP + " {Lay on Hands}", None),
    ("pal_bubble", PALADIN, "Gottesschild", "Divine Shield", "#showtooltip {Divine Shield}\n/cancelaura {=Divine Shield}\n/cancelaura {=Divine Protection}\n/cancelaura {=Blessing of Protection}\n/cast {Divine Shield}", "Nochmal drücken: Schild beenden"),
    ("pal_rez", PALADIN, "Erlösung MO", "Redemption MO", "#showtooltip {Redemption}\n/cast [@mouseover,help,dead][help,dead] {Redemption}", None),
    ("pal_exo", PALADIN, "Exorzismus", "Exorcism", "#showtooltip [mod:shift] {Turn Undead}; {Exorcism}\n/cast [mod:shift,harm,nodead] {Turn Undead}; [harm,nodead] {Exorcism}", "Shift: Untote vertreiben"),

    # ---------------- Hunter ----------------
    ("hun_mark", HUNTER, "Mal + Pet", "Mark + Pet", "#showtooltip {Hunter's Mark}\n/petattack\n/cast {Hunter's Mark}", None),
    ("hun_mend", HUNTER, "Tier heilen", "Mend Pet", "#showtooltip {Mend Pet}\n/cast [@pet,exists,nodead] {Mend Pet}", None),
    ("hun_petmo", HUNTER, "Pet Mouseover", "Pet Mouseover", "/petattack [@mouseover,harm,nodead][]", "Begleiter greift Mouseover an, sonst Ziel"),
    ("hun_petatt", HUNTER, "Pet Angriff", "Pet Attack", "/petattack [nomod:shift,harm,nodead]\n/petpassive [mod:shift]\n/petfollow [mod:shift]", "Shift: passiv + zurückrufen"),
    ("hun_pet", HUNTER, "Tier", "Pet", "#showtooltip\n/cast [@pet,dead][mod:shift] {Revive Pet}; [nopet] {Call Pet}; {Mend Pet}", "Rufen / heilen / wiederbeleben"),
    ("hun_feed", HUNTER, "Füttern", "Feed Pet", "#showtooltip {Feed Pet}\n/cast [pet,nocombat] {Feed Pet}\n/use [pet,nocombat] <Chunk of Boar Meat>", "Essen ggf. im Makro anpassen"),
    ("hun_hawk", HUNTER, "Falke", "Hawk", "#showtooltip {Aspect of the Hawk}\n/cancelaura {=Aspect of the Cheetah}\n/cast !{Aspect of the Hawk}", None),
    ("hun_cheetah", HUNTER, "Gepard/Rudel", "Cheetah/Pack", "#showtooltip {Aspect of the Cheetah}\n/cast [button:2] !{Aspect of the Pack}; !{Aspect of the Cheetah}", "Rechtsklick: Rudel"),
    ("hun_track", HUNTER, "Fährten", "Tracking", "#showtooltip\n/cast [mod:shift] {Track Beasts}; [mod:ctrl] {Track Undead}; [mod:alt] {Track Hidden}; {Track Humanoids}", None),
    ("hun_fd", HUNTER, "Totstellen", "Feign Death", "#showtooltip {Feign Death}\n/petpassive\n/petfollow\n/stopattack\n/stopcasting\n/cast [combat] {Feign Death}", None),
    ("hun_noaspect", HUNTER, "Aspekt weg", "Cancel Aspect", "/cancelaura {=Aspect of the Cheetah}\n/cancelaura {=Aspect of the Pack}", None),
    ("hun_eagle", HUNTER, "Adlerauge", "Eagle Eye", "#showtooltip {Eagle Eye}\n/cast !{Eagle Eye}", None),

    # ---------------- Rogue ----------------
    ("rog_kick", ROGUE, "Tritt MO", "Kick MO", "#showtooltip {Kick}\n/cast [@mouseover,harm,nodead][] {Kick}", None),
    ("rog_sap", ROGUE, "Kopfnuss MO", "Sap MO", "#showtooltip {Sap}\n/cast [@mouseover,harm,nodead][] {Sap}", None),
    ("rog_stealth", ROGUE, "Verstohlenheit", "Stealth", "#showtooltip {Stealth}\n/dismount\n/cast [nostealth,nocombat] {Stealth}", "Schaltet sich nicht selbst ab"),
    ("rog_pp", ROGUE, "Taschendieb MO", "Pick Pocket MO", "#showtooltip {Pick Pocket}\n/cast [@mouseover,harm,nodead][] {Pick Pocket}", None),
    ("rog_opener", ROGUE, "Opener", "Opener", "#showtooltip\n/cast [stealth] {Pick Pocket}\n/cast [nostealth] {Stealth}; [mod:shift] {Garrote}; [mod:ctrl] {Ambush}; {Cheap Shot}", "Taschendiebstahl + Fieser Trick; Shift: Erdrosseln; Strg: Hinterhalt"),
    ("rog_evasion", ROGUE, "Entrinnen+Sprint", "Evasion+Sprint", "#showtooltip {Evasion}\n/cast {Evasion}\n/cast {Sprint}", None),
    ("rog_poison", ROGUE, "Gift auftragen", "Apply Poison", "#showtooltip\n/use [mod:shift] <Deadly Poison>; <Instant Poison>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Sofort-Gift; Shift: tödliches Gift; Alt: Nebenhand"),
    ("rog_stone", ROGUE, "Wetzstein", "Sharpen", "#showtooltip\n/use [mod:shift] <Heavy Weightstone>; <Heavy Sharpening Stone>\n/use [mod:alt] 17; 16\n/click StaticPopup1Button1", "Shift: Gewichtsstein; Alt: Nebenhand"),
    ("rog_vanish", ROGUE, "Stealth/Vanish", "Stealth/Vanish", "#showtooltip [nocombat] {Stealth}; {Vanish}\n/stopattack [combat]\n/cast [nocombat] !{Stealth}; {Vanish}", None),

    # ---------------- Priest ----------------
    ("pri_dispel", PRIEST, "Magiebannung MO", "Dispel MO", "#showtooltip {Dispel Magic}\n/cast [@mouseover,exists,nodead][] {Dispel Magic}", None),
    ("pri_fort", PRIEST, "Seelenstärke MO", "Fortitude MO", "#showtooltip {Power Word: Fortitude}\n/cast " + MO_HELP + " {Power Word: Fortitude}", None),
    ("pri_fearward", PRIEST, "Furchtzauber MO", "Fear Ward MO", "#showtooltip {Fear Ward}\n/cast " + MO_HELP + " {Fear Ward}", None),
    ("pri_shackle", PRIEST, "Fesseln MO", "Shackle MO", "#showtooltip {Shackle Undead}\n/cast [@mouseover,harm,nodead][harm,nodead] {Shackle Undead}", None),
    ("pri_wand", PRIEST, "Zauberstab", "Wand", "#showtooltip {Shoot}\n/cast !{Shoot}", None),
    ("pri_rez", PRIEST, "Auferstehung MO", "Resurrect MO", "#showtooltip {Resurrection}\n/cast [@mouseover,help,dead][help,dead] {Resurrection}", None),
    ("pri_levitate", PRIEST, "Levitieren", "Levitate", "#showtooltip {Levitate}\n/dismount\n/cancelaura [mod:shift] {=Levitate}\n/cast [nomod] {Levitate}", "Shift: abbrechen"),
    ("pri_buffs", PRIEST, "Selbstbuffs", "Self Buffs", "#showtooltip\n/castsequence [@player] reset=15 {Inner Fire}, {Power Word: Fortitude}, {Divine Spirit}", None),
    ("pri_healsmite", PRIEST, "Heilen/Peinigen", "Heal/Smite", "#showtooltip\n/cast [@mouseover,help,nodead] {Lesser Heal}; [harm,nodead] {Smite}; [help,nodead][@player] {Lesser Heal}", None),

    # ---------------- Shaman ----------------
    ("sha_es", SHAMAN, "Erdschock MO", "Earth Shock MO", "#showtooltip {Earth Shock}\n/stopcasting\n/cast [@mouseover,harm,nodead][] {Earth Shock}", "Bricht eigenen Zauber für den Kick ab"),
    ("sha_totems", SHAMAN, "Totems", "Totems", "#showtooltip [mod:shift] {Totemic Recall}; {Call of the Elements}\n/cast [mod:shift] {Totemic Recall}; {Call of the Elements}", "Shift: zurückrufen"),
    ("sha_totems3", SHAMAN, "Totem-Sets", "Totem Sets", "#showtooltip\n/cast [mod:ctrl] {Call of the Ancestors}; [mod:alt] {Call of the Spirits}; [mod:shift] {Totemic Recall}; {Call of the Elements}", "Strg/Alt: andere Sets; Shift: zurückrufen"),
    ("sha_shield", SHAMAN, "Schild", "Shield", "#showtooltip [mod:shift] {Water Shield}; {Lightning Shield}\n/cast [mod:shift] {Water Shield}; {Lightning Shield}", "Shift: Wasserschild"),
    ("sha_wolf", SHAMAN, "Geisterwolf", "Ghost Wolf", "#showtooltip {Ghost Wolf}\n/cast {Ghost Wolf}", None),
    ("sha_purge", SHAMAN, "Reinigen MO", "Purge MO", "#showtooltip {Purge}\n/cast [@mouseover,harm,nodead][] {Purge}", None),
    ("sha_shocks", SHAMAN, "Schocks", "Shocks", "#showtooltip [mod:shift] {Flame Shock}; [mod:ctrl] {Frost Shock}; {Earth Shock}\n/cast [mod:shift] {Flame Shock}; [mod:ctrl] {Frost Shock}; {Earth Shock}", "Shift: Flamme; Strg: Frost"),
    ("sha_cure", SHAMAN, "Heilung Gift", "Cure", "#showtooltip\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] {Cure Disease}; " + MO_HELP + " {Cure Poison}", "Shift: Krankheit"),
    ("sha_ankh", SHAMAN, "Reinkarnation", "Reincarnation", "#showtooltip {Reincarnation}", "Zeigt nur die Abklingzeit"),
    ("sha_selfheal", SHAMAN, "Selbst heilen", "Self Heal", "#showtooltip [mod:shift] {Lesser Healing Wave}; {Healing Wave}\n/cast [mod:shift,@player] {Lesser Healing Wave}; [@player] {Healing Wave}", None),
    ("sha_water", SHAMAN, "Wasserwandeln", "Water Walk", "#showtooltip\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] {Water Breathing}; " + MO_HELP + " {Water Walking}", "Shift: Wasseratmung"),

    # ---------------- Mage ----------------
    ("mag_cs", MAGE, "Gegenzauber", "Counterspell", "#showtooltip {Counterspell}\n/stopcasting\n/cast {Counterspell}", None),
    ("mag_poly", MAGE, "Verwandlung MO", "Polymorph MO", "#showtooltip {Polymorph}\n/cast [@mouseover,harm,nodead][] {Polymorph}", None),
    ("mag_ai", MAGE, "Intelligenz", "Intellect", "#showtooltip\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] {Arcane Brilliance}; " + MO_HELP + " {Arcane Intellect}", "Shift: Arkane Brillanz"),
    ("mag_dampen", MAGE, "Magie dämpfen", "Dampen Magic", "#showtooltip\n/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] {Amplify Magic}; " + MO_HELP + " {Dampen Magic}", "Shift: Magie verstärken"),
    ("mag_decurse", MAGE, "Fluch aufheben", "Decurse", "#showtooltip {Remove Lesser Curse}\n/cast [mod:shift,@player][@mouseover,help,nodead][help,nodead][@player] {Remove Lesser Curse}", "Shift: auf dich"),
    ("mag_conjure", MAGE, "Herbeizaubern", "Conjure", "#showtooltip [mod:shift] {Conjure Food}; {Conjure Water}\n/cast [mod:shift] {Conjure Food}; {Conjure Water}", "Wasser; Shift: Essen"),
    ("mag_gem", MAGE, "Manastein", "Mana Gem", "#showtooltip\n/use <Mana Ruby>\n/use <Mana Citrine>\n/use <Mana Jade>\n/use <Mana Agate>", "Nimmt den besten vorhandenen"),
    ("mag_armor", MAGE, "Rüstung", "Armor", "#showtooltip [mod:shift] {Mage Armor}; [mod:ctrl] {Frost Armor}; {Ice Armor}\n/cast [mod:shift] {Mage Armor}; [mod:ctrl] {Frost Armor}; {Ice Armor}", "Eisrüstung; Shift: Magier; Strg: Frost"),
    ("mag_tele_a", MAGE, "Teleport (A)", "Teleport (A)", "#showtooltip\n/cast [mod:shift] {Teleport: Ironforge}; [mod:ctrl] {Teleport: Darnassus}; [mod:alt] {Teleport: Dalaran}; {Teleport: Stormwind}", "Allianz"),
    ("mag_tele_h", MAGE, "Teleport (H)", "Teleport (H)", "#showtooltip\n/cast [mod:shift] {Teleport: Undercity}; [mod:ctrl] {Teleport: Thunder Bluff}; [mod:alt] {Teleport: Dalaran}; {Teleport: Orgrimmar}", "Horde"),
    ("mag_portal_a", MAGE, "Portal (A)", "Portal (A)", "#showtooltip\n/cast [mod:shift] {Portal: Ironforge}; [mod:ctrl] {Portal: Darnassus}; {Portal: Stormwind}", "Allianz"),
    ("mag_portal_h", MAGE, "Portal (H)", "Portal (H)", "#showtooltip\n/cast [mod:shift] {Portal: Undercity}; [mod:ctrl] {Portal: Thunder Bluff}; {Portal: Orgrimmar}", "Horde"),
    ("mag_slowfall", MAGE, "Langsamer Fall", "Slow Fall", "#showtooltip {Slow Fall}\n/dismount [nomod:shift]\n/cancelaura [mod:shift] {=Slow Fall}\n/cast [nomod:shift,@player] {Slow Fall}", "Shift: abbrechen"),

    # ---------------- Warlock ----------------
    ("wlk_fear", WARLOCK, "Furcht MO", "Fear MO", "#showtooltip {Fear}\n/cast [@mouseover,harm,nodead][] {Fear}", None),
    ("wlk_petback", WARLOCK, "Dämon zurück", "Pet Back", "/petpassive\n/petfollow", None),
    ("wlk_summon", WARLOCK, "Dämon rufen", "Summon Demon", "#showtooltip\n/cast [mod:shift] {Summon Imp}; [mod:ctrl] {Summon Succubus}; [mod:alt] {Summon Felhunter}; {Summon Voidwalker}", "Leerwandler; Shift: Wichtel; Strg: Sukkubus; Alt: Teufelsjäger"),
    ("wlk_curse", WARLOCK, "Flüche", "Curses", "#showtooltip\n/cast [mod:shift] {Curse of Weakness}; [mod:ctrl] {Curse of Recklessness}; [mod:alt] {Curse of Tongues}; [@mouseover,harm,nodead][] {Curse of the Elements}", "Elemente (Mouseover); Shift: Schwäche; Strg: Tollkühnheit; Alt: Sprachen"),
    ("wlk_dots", WARLOCK, "DoT-Folge", "DoT Sequence", "#showtooltip\n/petattack [harm,nodead]\n/castsequence reset=target {Immolate}, {Bane of Agony}, {Corruption}, !{Shoot}", "Leveln: Opfern, Pein, Verderbnis, Zauberstab"),
    ("wlk_wand", WARLOCK, "Zauberstab", "Wand", "#showtooltip {Shoot}\n/cast !{Shoot}", None),
    ("wlk_hs", WARLOCK, "Gesundheitsstein", "Healthstone", "#showtooltip\n/use <Major Healthstone>\n/use <Greater Healthstone>\n/use <Healthstone>\n/use <Lesser Healthstone>\n/use <Minor Healthstone>\n/cast [mod:shift] {Drain Life}", "Shift: zusätzlich Lebensentzug"),
    ("wlk_ss", WARLOCK, "Seelenstein MO", "Soulstone MO", "#showtooltip\n/use [@mouseover,help][] <Major Soulstone>\n/use [@mouseover,help][] <Greater Soulstone>\n/use [@mouseover,help][] <Soulstone>\n/use [@mouseover,help][] <Lesser Soulstone>\n/use [@mouseover,help][] <Minor Soulstone>", None),
    ("wlk_stones", WARLOCK, "Steine erstellen", "Create Stones", "#showtooltip\n/cast [mod:shift] {Create Soulstone}; [mod:ctrl] {Create Spellstone}; [mod:alt] {Create Firestone}; {Create Healthstone}", None),
    ("wlk_ritual", WARLOCK, "Beschwörung", "Summoning", "#showtooltip {Ritual of Summoning}\n/party Beschwöre %t, bitte Portal anklicken\n/cast {Ritual of Summoning}", "Kündigt die Beschwörung in der Gruppe an"),
    ("wlk_armor", WARLOCK, "Dämonenrüstung", "Demon Armor", "#showtooltip [mod:shift] {Shadow Ward}; {Demon Armor}\n/cast [mod:shift] {Shadow Ward}; {Demon Armor}", "Shift: Schattenzauberschutz"),
]

# Racial macros: one per active racial (filtered in game by whether the character knows it).
RACIAL_NAMES = {
    "rac_wotf": ("Wille Verlassene", "WotF"), "rac_regen": ("Rasche Regen.", "Rapid Regen"),
}
RACIALS = [
    ("rac_wotf", "Will of the Forsaken"), ("rac_stomp", "War Stomp"), ("rac_berserking", "Berserking"),
    ("rac_bloodfury", "Blood Fury"), ("rac_cannibalize", "Cannibalize"), ("rac_meld", "Shadowmeld"),
    ("rac_escape", "Escape Artist"), ("rac_stoneform", "Stoneform"), ("rac_treasure", "Find Treasure"),
    ("rac_perception", "Perception"), ("rac_leyline", "Read Leyline"), ("rac_walkair", "Walk on Air"),
    ("rac_skysight", "Skysight"), ("rac_survive", "Will to Survive"), ("rac_elune", "Elune's Light"),
    ("rac_eureka", "Eureka!"), ("rac_shatter", "Shatter Curse"), ("rac_regen", "Rapid Regeneration"),
    ("rac_cultivation", "Cultivation"),
]

# Utility macros (general tab, for all characters): (id, group, name_de, name_en, body, note_de)
UTILITY = [
    ("u_hearth", "general", "Ruhestein", "Hearthstone", "#showtooltip <Hearthstone>\n/use <Hearthstone>", None),
    ("u_trinkets", "equip", "Schmuck 1+2", "Trinkets", "#showtooltip\n/use 13\n/use 14", "Beide Schmuckstücke"),
    ("u_trinket1", "equip", "Schmuck oben", "Trinket 1", "#showtooltip 13\n/use 13", None),
    ("u_trinket2", "equip", "Schmuck unten", "Trinket 2", "#showtooltip 14\n/use 14", None),
    ("u_hppot", "items", "Heiltrank", "Healing Potion", "#showtooltip\n/use <Major Healing Potion>\n/use <Superior Healing Potion>\n/use <Greater Healing Potion>\n/use <Healing Potion>\n/use <Lesser Healing Potion>\n/use <Minor Healing Potion>", "Nimmt den besten vorhandenen"),
    ("u_manapot", "items", "Manatrank", "Mana Potion", "#showtooltip\n/use <Major Mana Potion>\n/use <Superior Mana Potion>\n/use <Greater Mana Potion>\n/use <Mana Potion>\n/use <Lesser Mana Potion>\n/use <Minor Mana Potion>", "Nimmt den besten vorhandenen"),
    ("u_bandage", "items", "Verband", "Bandage", "#showtooltip\n/use [@player] <Heavy Runecloth Bandage>\n/use [@player] <Runecloth Bandage>\n/use [@player] <Heavy Mageweave Bandage>\n/use [@player] <Mageweave Bandage>\n/use [@player] <Heavy Silk Bandage>", "Bester Verband auf dich (Seide bis Runenstoff)"),
    ("u_bandage_low", "items", "Verband (klein)", "Bandage (low)", "#showtooltip\n/use [@player] <Silk Bandage>\n/use [@player] <Heavy Wool Bandage>\n/use [@player] <Wool Bandage>\n/use [@player] <Heavy Linen Bandage>\n/use [@player] <Linen Bandage>", "Bester Verband auf dich (Leinen bis Seide)"),
    ("u_focus", "general", "Fokus MO", "Focus MO", "/focus [@mouseover,exists,nodead][]", "Mouseover, sonst Ziel als Fokus"),
    ("u_clearfocus", "general", "Fokus weg", "Clear Focus", "/clearfocus", None),
    ("u_skull", "general", "Totenkopf", "Skull", "/tm 8", "Totenkopf aufs Ziel"),
    ("u_nomark", "general", "Marker weg", "Clear Mark", "/tm 0", "Zielmarkierung entfernen"),
    ("u_accept", "general", "Bestätigen", "Confirm", "/click StaticPopup1Button1", "Klickt 'Annehmen' im obersten Dialog"),
    ("u_release", "general", "Geist freilassen", "Release Spirit", "/run RepopMe()", None),
    ("u_reset", "general", "Instanz-Reset", "Reset Instances", "/run ResetInstances()", None),
    ("u_leave", "general", "Gruppe verlassen", "Leave Group", "/run C_PartyInfo.LeaveParty()", None),
    ("u_reload", "general", "UI neu laden", "Reload UI", "/reload", None),
    ("u_dismount", "general", "Absitzen", "Dismount", "/dismount", None),
    ("u_quest", "quests", "Quest an/ab", "Quest Accept", "/click QuestFrameAcceptButton\n/click QuestFrameCompleteButton\n/click QuestFrameCompleteQuestButton", "Nimmt an / gibt ab im offenen Questfenster"),
    ("u_share", "quests", "Quest teilen", "Share Quest", "/run local q=C_QuestLog.GetSelectedQuest() if q and q>0 then QuestLogPushQuest(C_QuestLog.GetLogIndexForQuestID(q)) end", "Teilt die im Questlog ausgewählte Quest"),
    ("u_find", "professions", "Kräuter/Erze", "Herbs/Ore", "#showtooltip\n/cast [mod:shift] {Find Minerals}; {Find Herbs}", "Kräutersuche; Shift: Mineraliensuche"),
    ("u_fish", "professions", "Angeln", "Fishing", "#showtooltip {Fishing}\n/cast {Fishing}", None),
    ("u_fire", "professions", "Kochfeuer", "Campfire", "#showtooltip {Basic Campfire}\n/cast {Basic Campfire}", None),
    ("u_cook", "professions", "Kochen", "Cooking", "#showtooltip {Cooking}\n/cast {Cooking}", None),
    ("u_firstaid", "professions", "Erste Hilfe", "First Aid", "#showtooltip {First Aid}\n/cast {First Aid}", None),
    ("u_disenchant", "professions", "Entzaubern", "Disenchant", "#showtooltip {Disenchant}\n/cast {Disenchant}", None),
    ("u_smelt", "professions", "Verhütten", "Smelting", "#showtooltip {Smelting}\n/cast {Smelting}", None),
]
