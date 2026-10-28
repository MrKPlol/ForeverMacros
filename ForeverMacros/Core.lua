-- ForeverMacros: installs ready-made macros into the macro book (class/race macros per character, utility macros
-- for all characters), and one macro per learned spell with the options the player ticks (spell tab). Every spell name comes from its spell ID in the client's own language; items load first.
-- On WoW Forever an unranked spell name can resolve to a rank the character has not learned (e.g. a level-46
-- remake of Charge), so a name the character does not know is written with the highest rank it does know.
local ADDON, ns = ...

local DE = GetLocale() == "deDE"
local EN = GetLocale():find("^en") ~= nil
local L = DE and {
	combat = "Im Kampf können keine Makros geändert werden.",
	macroFrame = "Bitte erst Blizzards Makrofenster (/macro) schließen.",
	itemsLate = "Einige Gegenstände sind noch nicht geladen; sie stehen mit englischem Namen im Makro:",
	created = "%d neu, %d aktualisiert, %d unverändert.",
	skipped = "Übersprungen (Name schon vergeben, nicht von ForeverMacros oder von dir geändert): %s",
	full = "Kein Platz mehr (%s): %s",
	charTab = "Charakter", accountTab = "Allgemein",
	failed = "Konnte nicht angelegt werden: %s",
	synced = "Ränge aktualisiert: %s",
} or {
	combat = "Macros cannot be changed in combat.",
	macroFrame = "Please close Blizzard's macro window (/macro) first.",
	itemsLate = "Some items have not loaded yet; they are in the macro with their English name:",
	created = "%d created, %d updated, %d unchanged.",
	skipped = "Skipped (name already taken, not made by ForeverMacros or edited by you): %s",
	full = "No free slot (%s): %s",
	charTab = "Character", accountTab = "General",
	failed = "Could not be created: %s",
	synced = "Ranks updated: %s",
}
ns.L, ns.DE = L, DE

local QUESTION_MARK = 134400   -- INV_Misc_QuestionMark: shows the live spell icon for #showtooltip macros

function ns.Print(msg) DEFAULT_CHAT_FRAME:AddMessage("|cff66ccffForeverMacros|r: " .. msg) end

function ns.Limits()
	local consts = Constants and Constants.MacroConsts
	local maxAccount = (consts and consts.MAX_ACCOUNT_MACROS) or MAX_ACCOUNT_MACROS or 120
	local maxChar = (consts and consts.MAX_CHARACTER_MACROS) or MAX_CHARACTER_MACROS or 30
	local numAccount, numChar = GetNumMacros()
	return numAccount or 0, maxAccount, numChar or 0, maxChar
end

-- ---------------------------------------------------------------------------------------------------------
-- Spells
-- ---------------------------------------------------------------------------------------------------------

local function Known(id)
	if not id then return false end
	if C_SpellBook and C_SpellBook.IsSpellKnown then
		local ok, known = pcall(C_SpellBook.IsSpellKnown, id)
		if ok and known then return true end
	end
	if IsPlayerSpell then
		local ok, known = pcall(IsPlayerSpell, id)
		if ok and known then return true end
	end
	return false
end

local function RankNumber(id)
	local sub = C_Spell.GetSpellSubtext(id)
	return tonumber(sub and sub:match("(%d+)")) or 0, sub
end

-- The text for one spell key: localized name, raised to the highest known rank when the plain name points at a
-- rank this character lacks. Second return: whether the character knows the spell at all.
local function SpellKeyText(key, plain)
	local ids = ns.SPELLS[key]
	if not ids then return nil, false end
	local name = C_Spell.GetSpellName(ids[1])
	if not name then return nil, false end
	local best, bestRank
	for _, id in ipairs(ids) do
		if Known(id) then
			local rank = RankNumber(id)
			if not best or rank > bestRank then best, bestRank = id, rank end
		end
	end
	local info = C_Spell.GetSpellInfo(name)
	local nameKnown = info and Known(info.spellID)
	if plain or nameKnown or not best then return name, (nameKnown or best ~= nil) end
	local _, sub = RankNumber(best)
	if sub and sub ~= "" then return name .. "(" .. sub .. ")", true end
	return name, true
end

-- "{S:a|b}": first alternative the character knows, else the last one.
local function SpellText(keys, plain)
	local text, known
	for key in keys:gmatch("[^|]+") do
		text, known = SpellKeyText(key, plain)
		if known then return text, true end
	end
	return text, false
end

-- ---------------------------------------------------------------------------------------------------------
-- Rendering
-- ---------------------------------------------------------------------------------------------------------

local function ItemText(id)
	return C_Item.GetItemNameByID(id) or ns.ITEMS[id]
end

-- Unit conditions the player picks per macro ({T:kind} or {T:kind:cond} in a body). Clauses in priority order;
-- build.py mirrors these to check the worst-case length. ground options exclude each other (no option = normal
-- reticle); unit always ends with a plain clause so self-targeted gadgets still fire.
ns.TARGETS = {
	help = { order = { "mo", "focus", "tgt", "self" }, default = { mo = true, tgt = true, self = true },
		clause = { mo = "@mouseover,help,nodead", focus = "@focus,help,nodead", tgt = "help,nodead", self = "@player" } },
	harm = { order = { "mo", "focus", "tgt" }, default = { mo = true, tgt = true },
		clause = { mo = "@mouseover,harm,nodead", focus = "@focus,harm,nodead", tgt = "harm,nodead" } },
	any = { order = { "mo", "focus", "tgt" }, default = { mo = true, tgt = true },
		clause = { mo = "@mouseover,exists,nodead", focus = "@focus,exists,nodead", tgt = "exists,nodead" } },
	dead = { order = { "mo", "focus", "tgt" }, default = { mo = true, tgt = true },
		clause = { mo = "@mouseover,help,dead", focus = "@focus,help,dead", tgt = "help,dead" } },
	unit = { order = { "mo", "focus" }, default = {}, fallback = true,
		clause = { mo = "@mouseover,exists,nodead", focus = "@focus,exists,nodead" } },
	ground = { order = { "cursor", "self" }, default = { cursor = true }, exclusive = true,
		clause = { cursor = "@cursor", self = "@player" } },
}

local function TargetStore(def) return def.scope == "utility" and ForeverMacrosDB.targets or ForeverMacrosCharDB.targets end

-- The options in effect for a macro: the player's choice, else the kind's default.
function ns.TargetChoice(def)
	local kind = ns.TARGETS[def.target]
	if not kind then return nil end
	return TargetStore(def)[def.id] or kind.default
end

function ns.SetTargetOption(def, option, value)
	local kind = ns.TARGETS[def.target]
	local choice = {}
	if not kind.exclusive then for k, v in pairs(ns.TargetChoice(def)) do choice[k] = v end end
	choice[option] = value or nil
	TargetStore(def)[def.id] = choice
end

local function TargetText(def, cond)
	local kind, choice = ns.TARGETS[def.target], ns.TargetChoice(def)
	if not kind then return "" end
	local prefix = cond ~= "" and cond .. "," or ""
	local out = {}
	for _, option in ipairs(kind.order) do
		if choice[option] then out[#out + 1] = "[" .. prefix .. kind.clause[option] .. "]" end
	end
	if (#out > 0 and kind.fallback) or (#out == 0 and cond ~= "") then out[#out + 1] = "[" .. cond .. "]" end
	return table.concat(out)
end

-- ---------------------------------------------------------------------------------------------------------
-- Spell tab: one macro per learned spell, written from the options the player ticks
-- ---------------------------------------------------------------------------------------------------------

-- Extra options in column order. Which a spell offers depends on its class and its flags from build.py:
-- c channelled, t toggles off when cast again, f/b needs Cat/Bear Form, x druid caster spell, s<n> warrior stances.
ns.EXTRAS = { "stance", "form", "stop", "trinket", "spam", "attack" }
local NO_STOP = { WARRIOR = true, ROGUE = true }                                   -- nothing to stop casting
local MELEE = { WARRIOR = true, ROGUE = true, DRUID = true, PALADIN = true, SHAMAN = true }
local STANCE_KEYS = { "WARRIOR:Battle Stance", "WARRIOR:Defensive Stance", "WARRIOR:Berserker Stance" }

function ns.Offers(def, option)
	local flags = def.flags
	if option == "stance" then return flags:find("s%d") ~= nil end
	if option == "form" then return flags:find("[fbx]") ~= nil end
	if option == "stop" then return not NO_STOP[def.class] and not flags:find("[fb]") end   -- feral moves cast nothing
	if option == "trinket" then return true end
	if option == "spam" then return flags:find("[ct]") ~= nil end
	if option == "attack" then return def.target == "harm" and MELEE[def.class] == true end
	return false
end

function ns.ExtraChoice(def) return ForeverMacrosCharDB.extras[def.id] or {} end

function ns.SetExtra(def, option, value)
	local choice = {}
	for k, v in pairs(ns.ExtraChoice(def)) do choice[k] = v end
	choice[option] = value or nil
	ForeverMacrosCharDB.extras[def.id] = next(choice) and choice or nil
end

-- The macro text with tokens ({T:...}, {S:...}) for ns.Render. Lines before the cast need a second press when they
-- change form or stance (the change starts the global cooldown).
local function SpellTemplate(def)
	local on, flags = ns.ExtraChoice(def), def.flags
	local function wants(option) return on[option] and ns.Offers(def, option) end
	local lines = { "#showtooltip" }
	if wants("stance") then
		local allowed = flags:match("s(%d+)")
		lines[#lines + 1] = "/cast [nostance:" .. allowed:gsub("(%d)", "%1/"):sub(1, -2) .. "] {S:" .. STANCE_KEYS[tonumber(allowed:sub(1, 1))] .. "}"
	end
	if wants("form") then
		if flags:find("f") then lines[#lines + 1] = "/cast !{S:DRUID:Cat Form}"
		elseif flags:find("b") then lines[#lines + 1] = "/cast !{S:DRUID:Dire Bear Form|DRUID:Bear Form}"
		else lines[#lines + 1] = "/cancelform" end
	end
	local spam = wants("spam")
	local cond = (spam and flags:find("c")) and "nochanneling" or ""
	-- spam on a channel: stopping would cut the running channel on every press
	if wants("stop") then lines[#lines + 1] = cond ~= "" and "/stopcasting [nochanneling]" or "/stopcasting" end
	if wants("trinket") then lines[#lines + 1] = "/use 13"; lines[#lines + 1] = "/use 14" end
	local spell = ((spam and flags:find("t")) and "!" or "") .. "{S:" .. def.key .. "}"
	if def.target then lines[#lines + 1] = "/cast {T:" .. def.target .. (cond ~= "" and ":" .. cond or "") .. "} " .. spell
	else lines[#lines + 1] = "/cast " .. (cond ~= "" and "[" .. cond .. "] " or "") .. spell end
	if wants("attack") then lines[#lines + 1] = "/startattack" end
	return table.concat(lines, "\n")
end

-- Returns body, icon, missing (spell names the character does not know yet), or nil if a spell is unknown to the client.
function ns.Render(def)
	local missing, broken, icon = {}, false, nil
	local body = (def.scope == "spell" and SpellTemplate(def) or def.body):gsub("{T:(%a+):?([^}]*)} ?", function(_, cond)
		local text = TargetText(def, cond)
		return text ~= "" and text .. " " or ""
	end)
	body = body:gsub("{(%a):([^}]+)}", function(kind, ref)
		if kind == "I" then
			local id = tonumber(ref)
			icon = icon or C_Item.GetItemIconByID(id)
			return ItemText(id) or ("item:" .. ref)
		end
		-- general-tab macros are shared by all characters: never pin a rank there (it would differ per character)
		local text, known = SpellText(ref, kind == "P" or def.scope == "utility")
		if not text then broken = true; return "" end
		if not known then missing[#missing + 1] = text end
		if not icon then
			local first = ns.SPELLS[ref:match("[^|]+")]
			icon = first and C_Spell.GetSpellTexture(first[1])
		end
		return text
	end)
	if broken or #body > 255 then return nil end
	if body:find("^#show") then icon = QUESTION_MARK end
	return body, icon or QUESTION_MARK, missing
end

-- UTF-8 safe cut to the 16-byte macro name limit.
local function Cut(name)
	if #name <= 16 then return name end
	local cut = name:sub(1, 16)
	while #cut > 0 and cut:byte(#cut) >= 0x80 and cut:byte(#cut) < 0xC0 do cut = cut:sub(1, -2) end
	if #cut > 0 and cut:byte(#cut) >= 0xC0 then cut = cut:sub(1, -2) end
	return cut
end
ns.Cut = Cut

function ns.MacroName(def)
	if def.macroName then return def.macroName end
	if def.scope == "spell" then
		-- build.py shortened names over 16 bytes readably for German and English; other clients cut their own
		local name = (DE and def.nameDE) or (EN and def.nameEN) or C_Spell.GetSpellName(ns.SPELLS[def.key][1])
		return Cut(name or def.id)
	end
	local name = DE and def.nameDE or def.nameEN
	if not name and def.scope == "race" then
		local ref = def.body:match("{S:([^}]+)}")
		name = ref and SpellText(ref, true)
	end
	return Cut(name or def.id)
end

function ns.PerCharacter(def) return def.scope ~= "utility" end

-- ---------------------------------------------------------------------------------------------------------
-- Definitions the player can choose from
-- ---------------------------------------------------------------------------------------------------------

function ns.Definitions()
	local _, class = UnitClass("player")
	local list = {}
	for _, def in ipairs(ns.MACROS) do
		if def.scope == "class" and def.group == class then list[#list + 1] = def
		elseif def.scope == "utility" then list[#list + 1] = def
		elseif def.scope == "race" then
			local ref = def.body:match("{S:([^}]+)}")
			local _, known = SpellText(ref, true)
			if known then list[#list + 1] = def end
		end
	end
	-- equipment sets of this character: one /equipset macro each
	if C_EquipmentSet and C_EquipmentSet.GetEquipmentSetIDs then
		for _, setID in ipairs(C_EquipmentSet.GetEquipmentSetIDs() or {}) do
			local name, iconFileID = C_EquipmentSet.GetEquipmentSetInfo(setID)
			if name and #("/equipset " .. name) <= 255 then
				list[#list + 1] = { id = "set:" .. name, scope = "set", group = "sets", macroName = Cut(name),
					body = "/equipset " .. name, icon = iconFileID }
			end
		end
	end
	return list
end

local spellDefs = {}   -- id -> def, shared by the window and rank upkeep

local function SpellDef(class, entry)
	local id = "sp:" .. entry[1]
	local def = spellDefs[id]
	if not def then
		def = { id = id, scope = "spell", class = class, key = entry[1], group = entry[2], target = entry[3] or nil,
			flags = entry[4], nameDE = entry[5] or nil, nameEN = entry[6] or nil }
		spellDefs[id] = def
	end
	return def
end

-- Spell-tab rows: every spell of the class the character knows (any rank), one per macro name.
function ns.SpellDefinitions()
	local _, class = UnitClass("player")
	local list, names = {}, {}
	for _, entry in ipairs(ns.SPELLBOOK[class] or {}) do
		local def = SpellDef(class, entry)
		local _, known = SpellText(def.key, true)
		local name = ns.MacroName(def)
		if known and not names[name] then names[name] = true; list[#list + 1] = def end
	end
	return list
end

-- ---------------------------------------------------------------------------------------------------------
-- Writing (never in combat; never touches a macro the player made or edited)
-- ---------------------------------------------------------------------------------------------------------

local function Store(perChar) return perChar and ForeverMacrosCharDB.made or ForeverMacrosDB.made end

-- Only GetMacroInfo / GetNumMacros / CreateMacro / EditMacro are used (the calls Blizzard's own macro window makes on
-- Forever). General macros are indices 1..n, character macros MAX_ACCOUNT_MACROS+1..+n, as in Blizzard_MacroUI.
-- Returns index, body of the macro called `name` in that tab, or nil.
local function Find(name, perChar)
	local _, maxAccount, _, maxChar = ns.Limits()
	local first, count = 1, maxAccount
	if perChar then first, count = maxAccount + 1, maxChar end
	for index = first, first + count - 1 do
		local macroName, _, body = GetMacroInfo(index)
		if macroName == name then return index, body end
	end
end
ns.Find = Find

local function Remember(name, perChar, defId)
	local index, body = Find(name, perChar)
	if index then Store(perChar)[name] = { id = defId, body = body } end
end

local function WriteOne(def, result)
	local name, perChar = ns.MacroName(def), ns.PerCharacter(def)
	local body, icon
	if def.scope == "set" then body, icon = def.body, def.icon or QUESTION_MARK
	else body, icon = ns.Render(def) end
	if not body then result.failed[#result.failed + 1] = name; return end
	local index, current = Find(name, perChar)
	if index then
		if current == body then result.unchanged = result.unchanged + 1; Remember(name, perChar, def.id); return end
		local record = Store(perChar)[name]
		if not record or record.body ~= current then result.skipped[#result.skipped + 1] = name; return end
		local ok = pcall(EditMacro, index, name, icon, body)
		if ok then result.updated = result.updated + 1; Remember(name, perChar, def.id)
		else result.failed[#result.failed + 1] = name end
		return
	end
	local numAccount, maxAccount, numChar, maxChar = ns.Limits()
	if (perChar and numChar >= maxChar) or (not perChar and numAccount >= maxAccount) then
		result.full[#result.full + 1] = name; return
	end
	local ok = pcall(CreateMacro, name, icon, body, perChar)
	if ok and Find(name, perChar) then result.created = result.created + 1; Remember(name, perChar, def.id)
	else result.failed[#result.failed + 1] = name end
end

-- Loads every item the selection uses (localized names), then calls done(lateItems). Gives up waiting after 5 s.
local function LoadItems(defs, done)
	local pending, late, finished = {}, {}, false
	for _, def in ipairs(defs) do
		for id in (def.body or ""):gmatch("{I:(%d+)}") do pending[tonumber(id)] = true end
	end
	local function finish()
		if finished then return end
		finished = true
		for id in pairs(pending) do late[#late + 1] = ns.ITEMS[id] end
		done(late)
	end
	local count = 0
	for id in pairs(pending) do
		count = count + 1
		local item = Item:CreateFromItemID(id)
		if item:IsItemEmpty() then pending[id] = nil
		else
			item:ContinueOnItemLoad(function()
				pending[id] = nil
				if not next(pending) then finish() end
			end)
		end
	end
	if count == 0 or not next(pending) then finish() else C_Timer.After(5, finish) end
end

-- Blizzard's macro window remembers its selection by position and saves the edit box into that position when it
-- closes; creating macros while it is open re-sorts the list under it, so nothing is written while it is shown.
local function MacroFrameOpen() return MacroFrame and MacroFrame:IsShown() end
ns.MacroFrameOpen = MacroFrameOpen

function ns.Install(defs, onDone)
	if InCombatLockdown() then ns.Print(L.combat); if onDone then onDone() end; return end
	if MacroFrameOpen() then ns.Print(L.macroFrame); if onDone then onDone() end; return end
	LoadItems(defs, function(late)
		if InCombatLockdown() then ns.Print(L.combat); if onDone then onDone() end; return end
		if MacroFrameOpen() then ns.Print(L.macroFrame); if onDone then onDone() end; return end
		local result = { created = 0, updated = 0, unchanged = 0, skipped = {}, full = {}, failed = {} }
		for _, def in ipairs(defs) do WriteOne(def, result) end
		ns.Print(L.created:format(result.created, result.updated, result.unchanged))
		if #late > 0 then ns.Print(L.itemsLate .. " " .. table.concat(late, ", ")) end
		if #result.skipped > 0 then ns.Print(L.skipped:format(table.concat(result.skipped, ", "))) end
		if #result.full > 0 then ns.Print(L.full:format(L.charTab .. "/" .. L.accountTab, table.concat(result.full, ", "))) end
		if #result.failed > 0 then ns.Print(L.failed:format(table.concat(result.failed, ", "))) end
		if onDone then onDone(result) end
	end)
end

-- ---------------------------------------------------------------------------------------------------------
-- Rank upkeep: after learning spells, macros this addon made (and the player left alone) get the new rank.
-- ---------------------------------------------------------------------------------------------------------

local byId = {}
local syncQueued, syncPending = false, false

-- Rank upkeep only rewrites a macro when its item names are available in the client's language (else it would
-- swap localized item names for English ones).
local function ItemsCached(def)
	for id in (def.body or ""):gmatch("{I:(%d+)}") do
		if not C_Item.GetItemNameByID(tonumber(id)) then return false end
	end
	return true
end

local function SyncRanks()
	syncQueued = false
	if InCombatLockdown() then syncPending = true; return end
	if MacroFrameOpen() then return end   -- never edit under the player's open macro window
	-- character tab only (general-tab macros carry no ranks); one pass over the tab, then edits by name
	local _, maxAccount, _, maxChar = ns.Limits()
	local live = {}
	for index = maxAccount + 1, maxAccount + maxChar do
		local name, _, body = GetMacroInfo(index)
		if name then live[name] = body end
	end
	local changed = {}
	for name, record in pairs(Store(true)) do
		local def = byId[record.id]
		if def and live[name] == record.body and ItemsCached(def) then
			local body, icon = ns.Render(def)
			local index = body and body ~= record.body and Find(name, true)
			if index and pcall(EditMacro, index, name, icon, body) then
				Remember(name, true, def.id); changed[#changed + 1] = name
			end
		end
	end
	if #changed > 0 then ns.Print(L.synced:format(table.concat(changed, ", "))) end
end

local events = CreateFrame("Frame")
events:RegisterEvent("ADDON_LOADED")
events:SetScript("OnEvent", function(self, event, arg)
	if event == "ADDON_LOADED" and arg == ADDON then
		ForeverMacrosDB = ForeverMacrosDB or {}
		ForeverMacrosDB.made = ForeverMacrosDB.made or {}
		ForeverMacrosCharDB = ForeverMacrosCharDB or {}
		ForeverMacrosCharDB.made = ForeverMacrosCharDB.made or {}
		ForeverMacrosCharDB.selected = ForeverMacrosCharDB.selected or {}
		ForeverMacrosDB.targets = ForeverMacrosDB.targets or {}
		ForeverMacrosCharDB.targets = ForeverMacrosCharDB.targets or {}
		ForeverMacrosCharDB.extras = ForeverMacrosCharDB.extras or {}
		for _, def in ipairs(ns.MACROS) do byId[def.id] = def end
		local _, class = UnitClass("player")
		for _, entry in ipairs(ns.SPELLBOOK[class] or {}) do local def = SpellDef(class, entry); byId[def.id] = def end
		self:UnregisterEvent("ADDON_LOADED")
		self:RegisterEvent("SPELLS_CHANGED")
		self:RegisterEvent("PLAYER_REGEN_ENABLED")
	elseif event == "SPELLS_CHANGED" then
		if not syncQueued then syncQueued = true; C_Timer.After(3, SyncRanks) end
	elseif event == "PLAYER_REGEN_ENABLED" and syncPending then
		syncPending = false
		if not syncQueued then syncQueued = true; C_Timer.After(1, SyncRanks) end
	end
end)
