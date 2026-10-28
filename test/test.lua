-- Headless test of ForeverMacros against a mocked WoW Forever API (macro rules as the real client enforces them).
-- Usage: luajit test.lua <addon dir>
local DIR = arg[1]
dofile((arg[0]:match("(.*/)") or "./") .. "fixtures.lua")

local failures, checks = 0, 0
local function check(cond, msg) checks = checks + 1; if not cond then failures = failures + 1; print("FAIL: " .. msg) end end

-- ------------------------------------------------------------------------------------------------ world state
local W
local function reset(locale, class, known, combat)
	W = { locale = locale, class = class, known = known or {}, combat = combat or false, timers = {},
		account = {}, char = {}, events = {}, printed = {}, itemLoaded = {} }
end

-- ------------------------------------------------------------------------------------------------ generic mock objects
local Mock = {}
local function mock(kind)
	local o = { _kind = kind, _shown = true, _scripts = {}, _text = "", _checked = false, _enabled = true, _events = {} }
	return setmetatable(o, Mock)
end
local methods = {
	Show = function(s) s._shown = true; if s._scripts.OnShow then s._scripts.OnShow(s) end end,
	Hide = function(s) s._shown = false end,
	IsShown = function(s) return s._shown end,
	SetShown = function(s, v) if v then s:Show() else s:Hide() end end,
	SetScript = function(s, k, f) s._scripts[k] = f end,
	GetScript = function(s, k) return s._scripts[k] end,
	SetText = function(s, t) s._text = t end,
	GetText = function(s) return s._text end,
	SetChecked = function(s, v) s._checked = v and true or false end,
	GetChecked = function(s) return s._checked end,
	Enable = function(s) s._enabled = true end,
	Disable = function(s) s._enabled = false end,
	SetEnabled = function(s, v) s._enabled = v and true or false end,
	IsEnabled = function(s) return s._enabled end,
	RegisterEvent = function(s, e) s._events[e] = true; W.events[#W.events + 1] = s end,
	UnregisterEvent = function(s, e) s._events[e] = nil end,
	CreateFontString = function(s) return mock("FontString") end,
	Click = function(s) if s._kind == "CheckButton" then s._checked = not s._checked end; if s._scripts.OnClick then s._scripts.OnClick(s) end end,
}
Mock.__index = function(t, k)
	if methods[k] then return methods[k] end
	if k == "Text" or k == "TitleText" then local child = mock("FontString"); rawset(t, k, child); return child end
	return function() return nil end
end

local frames = {}
function CreateFrame(kind, name, parent, template)
	local f = mock(kind)
	if kind ~= "CheckButton" and kind ~= "Button" and kind ~= "ScrollFrame" then f._shown = true end
	if name then _G[name] = f end
	frames[#frames + 1] = f
	return f
end
local function fire(event, ...)
	for _, f in ipairs(frames) do
		if f._events[event] and f._scripts.OnEvent then f._scripts.OnEvent(f, event, ...) end
	end
end

-- ------------------------------------------------------------------------------------------------ WoW API mocks
function GetLocale() return W.locale end
local CLASS_NAMES = { DRUID = "Druide", WARRIOR = "Krieger", PALADIN = "Paladin", HUNTER = "Jäger", ROGUE = "Schurke",
	PRIEST = "Priester", SHAMAN = "Schamane", MAGE = "Magier", WARLOCK = "Hexenmeister" }
function UnitClass() return CLASS_NAMES[W.class], W.class end
function InCombatLockdown() return W.combat end
DEFAULT_CHAT_FRAME = { AddMessage = function(_, m) W.printed[#W.printed + 1] = m end }
UISpecialFrames = {}
GameTooltip = mock("GameTooltip")
SlashCmdList = {}
function wipe(t) for k in pairs(t) do t[k] = nil end return t end
tinsert = table.insert
Constants = { MacroConsts = { MAX_ACCOUNT_MACROS = 120, MAX_CHARACTER_MACROS = 30 } }
C_Timer = { After = function(s, f) W.timers[#W.timers + 1] = f end }
local function runTimers() while #W.timers > 0 do local f = table.remove(W.timers, 1); f() end end

local function spellFix(id) return FIX.spell[W.locale][id] end
C_Spell = {
	GetSpellName = function(id) local s = spellFix(id); return s and s[1] ~= "" and s[1] or nil end,
	GetSpellSubtext = function(id) local s = spellFix(id); return s and s[2] or nil end,
	GetSpellTexture = function(id) return spellFix(id) and 135000 + (id % 1000) or nil end,
	-- like the client: a bare name resolves to the highest spell id with that name (Forever's remade ranks)
	GetSpellInfo = function(name)
		local best
		for id, s in pairs(FIX.spell[W.locale]) do if s[1] == name and (not best or id > best) then best = id end end
		return best and { spellID = best, name = name } or nil
	end,
}
C_SpellBook = { IsSpellKnown = function(id) return W.known[id] == true end }
C_Item = {
	GetItemNameByID = function(id) return W.itemLoaded[id] and FIX.item[W.locale][id] or nil end,
	GetItemIconByID = function(id) return 133000 + id % 1000 end,
	RequestLoadItemDataByID = function(id) W.requested = (W.requested or 0) + 1 end,
}
Item = { CreateFromItemID = function(_, id)
	return { IsItemEmpty = function() return FIX.item.enUS[id] == nil end,
		ContinueOnItemLoad = function(_, cb) C_Timer.After(0, function() W.itemLoaded[id] = true; cb() end) end }
end }
C_EquipmentSet = { GetEquipmentSetIDs = function() return W.sets and { 1 } or {} end,
	GetEquipmentSetInfo = function() return "Tank", 132000 end }

-- macro book with the client's rules
local function tab(perChar) return perChar and W.char or W.account end
local function sortTab(t) table.sort(t, function(a, b) return a.name < b.name end) end
function GetNumMacros() return #W.account, #W.char end
function GetMacroInfo(index)
	local m
	if index > 120 then m = W.char[index - 120] else m = W.account[index] end
	if m then return m.name, m.icon, m.body end
end
function CreateMacro(name, icon, body, perChar)
	assert(not W.combat, "CreateMacro in combat")
	assert(type(name) == "string" and #name > 0 and #name <= 16, "bad name " .. tostring(name))
	assert(type(body) == "string" and #body <= 255, "body too long: " .. #body)
	assert(icon ~= nil, "nil icon")
	local t = tab(perChar)
	assert(#t < (perChar and 30 or 120), "tab full")
	t[#t + 1] = { name = name, icon = icon, body = body }; sortTab(t)
	for i, m in ipairs(t) do if m.name == name then return perChar and 120 + i or i end end
end
function EditMacro(index, name, icon, body)
	assert(not W.combat, "EditMacro in combat")
	local t, i = W.account, index
	if index > 120 then t, i = W.char, index - 120 end
	local m = assert(t[i], "EditMacro: no macro at " .. index)
	if name then assert(#name <= 16); m.name = name end
	if icon then m.icon = icon end
	if body then assert(#body <= 255, "edit body too long"); m.body = body end
	sortTab(t)
	return index
end
_G.MacroFrame = nil

-- ------------------------------------------------------------------------------------------------ load addon
local function loadAddon()
	frames = {}
	ForeverMacrosDB, ForeverMacrosCharDB = nil, nil
	local ns = {}
	for _, file in ipairs({ "Data.lua", "Core.lua", "UI.lua" }) do
		local chunk = assert(loadfile(DIR .. "/" .. file))
		chunk("ForeverMacros", ns)
	end
	fire("ADDON_LOADED", "ForeverMacros")
	return ns
end

-- known spells for a character: the lowest rank (low level) or every rank (max level) of each spell of its class
local function knownFor(ns, class, everyRank)
	local known = {}
	for key, ids in pairs(ns.SPELLS) do
		if key:find("^" .. class .. ":") or key:find("^UTILITY:") or key:find("^RACE:") then
			if everyRank then for _, id in ipairs(ids) do known[id] = true end
			else
				-- the lowest rank by its rank text (ids are not in rank order)
				local low, lowRank
				for _, id in ipairs(ids) do
					local s = FIX.spell.enUS[id]
					local r = tonumber(s and s[2]:match("(%d+)")) or 0
					if not low or r < lowRank then low, lowRank = id, r end
				end
				known[low] = true
			end
		end
	end
	return known
end

-- ------------------------------------------------------------------------------------------------ tests
local CLASSES = { "DRUID", "WARRIOR", "PALADIN", "HUNTER", "ROGUE", "PRIEST", "SHAMAN", "MAGE", "WARLOCK" }

for _, locale in ipairs({ "deDE", "enUS" }) do
	for _, class in ipairs(CLASSES) do
		for _, everyRank in ipairs({ false, true }) do
			reset(locale, class); local ns = loadAddon(); W.known = knownFor(ns, class, everyRank)
			for id in pairs(FIX.item.enUS) do W.itemLoaded[id] = true end
			local tag = locale .. "/" .. class .. (everyRank and "/max" or "/low")
			local defs = ns.Definitions()
			local n = 0
			for _, def in ipairs(defs) do
				local body, icon = ns.Render(def)
				check(body ~= nil, tag .. ": render failed " .. def.id)
				if body then
					n = n + 1
					check(#body <= 255, tag .. ": " .. def.id .. " too long " .. #body)
					check(not body:find("[{}]"), tag .. ": unreplaced token in " .. def.id .. ": " .. body)
					check(not body:find("item:"), tag .. ": item not localized in " .. def.id)
					for line in body:gmatch("[^\n]+") do
						if line:find("^/cast") or line:find("^#show") then check(not line:find("%(%)"), tag .. ": empty rank in " .. def.id) end
					end
					check(icon ~= nil, tag .. ": no icon " .. def.id)
					if not everyRank then
						-- low level: a ranked name must name a rank the character knows
						for rank in body:gmatch("%(([^)]*%d+)%)") do check(rank:find("1"), tag .. ": " .. def.id .. " uses rank " .. rank) end
					end
				end
				local name = ns.MacroName(def)
				check(#name >= 1 and #name <= 16, tag .. ": bad name " .. tostring(name))
			end
			-- install everything that fits
			local done
			ns.Install(defs, function(r) done = r end); runTimers()
			check(done ~= nil, tag .. ": install did not finish")
			if done then
				local numA, numC = GetNumMacros()
				check(#done.failed == 0, tag .. ": failed " .. table.concat(done.failed, ","))
				check(done.created + #done.full == #defs, tag .. ": created " .. done.created .. " + full " .. #done.full .. " ~= " .. #defs)
				check(numC <= 30 and numA <= 120, tag .. ": over limits")
				for _, m in ipairs(W.account) do check(not m.name:find("^ ") , "x") end
				-- second run: nothing changes
				local again; ns.Install(defs, function(r) again = r end); runTimers()
				check(again and again.created == 0 and again.updated == 0 and #again.skipped == 0, tag .. ": reinstall not idempotent")
			end
		end
	end
end

-- scenario: Charge on a low-level warrior gets a rank, learning rank 2 upgrades it, player edits are respected
do
	reset("enUS", "WARRIOR"); local ns = loadAddon()
	local ids = ns.SPELLS["WARRIOR:Charge"]
	table.sort(ids)
	W.known = { [ids[1]] = true }
	local def; for _, d in ipairs(ns.MACROS) do if d.id == "war_charge" then def = d end end
	local body = ns.Render(def)
	print("low-level Charge macro:\n" .. body)
	check(body:find("Charge%(Rank 1%)"), "Charge should be ranked for a low-level warrior")
	ns.Install({ def }, nil); runTimers()
	W.known[ids[2]] = true
	fire("SPELLS_CHANGED"); runTimers()
	local _, _, now = GetMacroInfo(121)
	check(now and now:find("Charge%(Rank 2%)"), "rank sync should raise to Rank 2, got " .. tostring(now))
	-- player edits the macro: never touched again
	W.char[1].body = "/say mine"
	for _, id in ipairs(ids) do W.known[id] = true end
	fire("SPELLS_CHANGED"); runTimers()
	check(W.char[1].body == "/say mine", "edited macro must not be synced")
	local r; ns.Install({ def }, function(x) r = x end); runTimers()
	check(r and #r.skipped == 1, "edited macro must be skipped on install")
	-- foreign macro with the same name in the general tab does not block the character tab
	check(#W.account == 0, "nothing in the general tab")
end

-- scenario: Blizzard's macro window is open -> nothing is written, callback still fires
do
	reset("deDE", "DRUID"); local ns = loadAddon(); W.known = knownFor(ns, "DRUID", true)
	_G.MacroFrame = mock("Frame"); _G.MacroFrame._shown = true
	local called = false
	ns.Install(ns.Definitions(), function() called = true end); runTimers()
	check(#W.char == 0 and #W.account == 0, "no writes while MacroFrame is open")
	check(called, "onDone fires so the button re-enables")
	check(W.printed[#W.printed]:find("Makrofenster"), "macro window message")
	_G.MacroFrame._shown = false
	ns.Install(ns.Definitions(), nil); runTimers()
	check(#W.char > 0, "installs once the macro window is closed")
	_G.MacroFrame = nil
end

-- scenario: general-tab macros never carry a rank; rank sync only edits the character tab
do
	reset("enUS", "WARRIOR"); local ns = loadAddon()
	for _, ids in pairs(ns.SPELLS) do for _, id in ipairs(ids) do W.known[id] = false end end
	-- know only the lowest Fishing / Find Herbs rank: a character macro would be ranked, a general one must not be
	for _, key in ipairs({ "UTILITY:Fishing", "UTILITY:Find Herbs" }) do
		local low, lowRank
		for _, id in ipairs(ns.SPELLS[key]) do
			local r = tonumber((FIX.spell.enUS[id] or { "", "" })[2]:match("(%d+)")) or 0
			if not low or r < lowRank then low, lowRank = id, r end
		end
		W.known[low] = true
	end
	local util = {}
	for _, d in ipairs(ns.MACROS) do if d.scope == "utility" then util[#util + 1] = d end end
	for id in pairs(FIX.item.enUS) do W.itemLoaded[id] = true end
	ns.Install(util, nil); runTimers()
	for _, m in ipairs(W.account) do check(not m.body:find("%(Rank"), "general macro has a rank: " .. m.name .. " " .. m.body) end
	local before = {}
	for i, m in ipairs(W.account) do before[i] = m.body end
	for _, ids in pairs(ns.SPELLS) do for _, id in ipairs(ids) do W.known[id] = true end end
	fire("SPELLS_CHANGED"); runTimers()
	for i, m in ipairs(W.account) do check(m.body == before[i], "sync changed a general macro: " .. m.name) end
end

-- scenario: combat
do
	reset("deDE", "DRUID", nil, true); local ns = loadAddon()
	local r; ns.Install(ns.Definitions(), function(x) r = x end); runTimers()
	check(r == nil and #W.char == 0, "no writes in combat")
	check(W.printed[#W.printed]:find("Kampf"), "combat message")
end

-- scenario: items not loaded yet -> English fallback announced, no failure
do
	reset("deDE", "WARRIOR"); local ns = loadAddon()
	local def; for _, d in ipairs(ns.MACROS) do if d.id == "u_bomb" then def = d end end
	ns.Install({ def }, nil); runTimers()
	local _, _, body = GetMacroInfo(1)
	print("German bomb macro: " .. tostring(body))
	check(body and body:find("Thoriumgranate", 1, true) and body:find("[@cursor]", 1, true), "item name localized after load")
end

-- scenario: UI opens, lists, selects, installs
do
	reset("deDE", "DRUID"); local ns = loadAddon(); W.known = knownFor(ns, "DRUID", true); W.sets = true
	ns.Toggle()
	check((W.requested or 0) > 0, "item data requested when the window opens")
	local f = _G.ForeverMacrosFrame
	check(f and f:IsShown(), "window shows")
	local cbs = {}
	for _, fr in ipairs(frames) do if fr._kind == "CheckButton" and fr._shown and type(rawget(fr, "def")) == "table" then cbs[#cbs + 1] = fr end end
	check(#cbs > 30, "rows listed: " .. #cbs)
	local seenSet = false
	for _, cb in ipairs(cbs) do if cb.def.scope == "set" then seenSet = true end end
	check(seenSet, "equipment set row listed")
	for i = 1, 5 do cbs[i]:Click() end
	local install
	for _, fr in ipairs(frames) do if fr._kind == "Button" and fr._scripts.OnClick and (fr._text or ""):find("Einbauen") then install = fr end end
	check(install and install:IsEnabled(), "install button enabled: " .. tostring(install and install._text))
	install._scripts.OnClick(install); runTimers()
	check(#W.char + #W.account == 5, "5 macros installed, got " .. (#W.char + #W.account))
	check(install:IsEnabled(), "install button enabled again after installing")
	for _ = 1, 50 do fire("UPDATE_MACROS") end
	local queued = #W.timers
	check(queued == 1, "50 UPDATE_MACROS coalesce into one refresh, got " .. queued)
	runTimers()
	-- target option boxes: Rejuvenation/Regrowth (help) shows MO/Focus/Target/Self, ticking Focus changes the body
	local hots, hotsDef
	for _, cb in ipairs(cbs) do if cb.def.id == "dru_hots" then hots, hotsDef = cb, cb.def end end
	local boxes = {}
	for _, b in ipairs(hots.options) do if b:IsShown() then boxes[b.option] = b end end
	check(boxes.mo and boxes.focus and boxes.tgt and boxes.self and not boxes.cursor, "help macro offers mo/focus/target/self")
	check(boxes.mo:GetChecked() and not boxes.focus:GetChecked(), "help default: mouseover on, focus off")
	check(ns.Render(hotsDef):find("; [@mouseover,help,nodead][help,nodead][@player] ", 1, true), "default help body: " .. ns.Render(hotsDef))
	boxes.focus:Click(); boxes.mo:Click(); boxes.self:Click()
	local b = ns.Render(hotsDef)
	check(b:find("; [@focus,help,nodead][help,nodead] ", 1, true) and b:find("[mod:shift,@focus,help,nodead]", 1, true), "focus+target body: " .. b)
	check(ForeverMacrosCharDB.selected.dru_hots == true, "changed macro gets selected")
	boxes.focus:Click(); boxes.tgt:Click()
	check(ns.Render(hotsDef):find("/cast [mod:shift] Nachwachsen; Verjüngung", 1, true), "no option: plain casts: " .. ns.Render(hotsDef))
	check(not ns.Render(hotsDef):find("  "), "no double space")
	-- category box selects the whole group
	local header
	for _, fr in ipairs(frames) do if rawget(fr, "group") == "engineering" and fr._shown then header = fr end end
	check(header ~= nil, "engineering header box")
	if header then
		header:Click()
		local all = true
		for _, d in ipairs(ns.Definitions()) do if d.group == "engineering" and not ForeverMacrosCharDB.selected[d.id] then all = false end end
		check(all, "header selects every engineering macro")
		check(header:GetChecked(), "header shows checked")
		header:Click()
		for _, d in ipairs(ns.Definitions()) do if d.group == "engineering" then check(not ForeverMacrosCharDB.selected[d.id], "header clears " .. d.id) end end
	end
	SlashCmdList.FOREVERMACROS(""); check(not f:IsShown(), "/macros toggles")
	fire("PLAYER_REGEN_DISABLED")
end

-- ------------------------------------------------------------------------------------------------ spell tab
local ALL_TARGETS = { mo = true, focus = true, tgt = true, self = true }

-- every spell of every class, with every target option and every extra on, fits and renders cleanly
for _, locale in ipairs({ "deDE", "enUS" }) do
	for _, class in ipairs(CLASSES) do
		for _, everyRank in ipairs({ false, true }) do
			reset(locale, class); local ns = loadAddon(); W.known = knownFor(ns, class, everyRank)
			local tag = locale .. "/" .. class .. (everyRank and "/max" or "/low") .. "/spell"
			local defs, names = ns.SpellDefinitions(), {}
			check(#defs > 20, tag .. ": spell rows " .. #defs)
			for _, def in ipairs(defs) do
				local name = ns.MacroName(def)
				check(#name >= 1 and #name <= 16, tag .. ": bad name " .. name)
				check(not names[name], tag .. ": duplicate name " .. name); names[name] = true
				for _, groundOption in ipairs({ "cursor", "self" }) do
					ForeverMacrosCharDB.targets[def.id] = def.target == "ground" and { [groundOption] = true } or ALL_TARGETS
					for _, option in ipairs(ns.EXTRAS) do if ns.Offers(def, option) then ns.SetExtra(def, option, true) end end
					local body = ns.Render(def)
					check(body ~= nil, tag .. ": render failed with everything on: " .. def.id)
					if body then
						check(#body <= 255, tag .. ": " .. def.id .. " too long " .. #body)
						check(not body:find("[{}]"), tag .. ": unreplaced token in " .. def.id .. ": " .. body)
						check(not body:find("  ") and not body:find("%[%]"), tag .. ": bad spacing in " .. def.id .. ": " .. body)
					end
				end
				ForeverMacrosCharDB.targets[def.id] = nil; ForeverMacrosCharDB.extras[def.id] = nil
				local plain = ns.Render(def)
				check(plain and plain:find("^#showtooltip\n/cast "), tag .. ": plain spell macro " .. def.id .. ": " .. tostring(plain))
			end
			-- installing more than fits fills the character tab and reports the rest
			local done; ns.Install(defs, function(r) done = r end); runTimers()
			check(done and #done.failed == 0 and done.created == math.min(#defs, 30) and #W.char <= 30, tag .. ": spell install")
		end
	end
end

local function spellDef(ns, key) for _, d in ipairs(ns.SpellDefinitions()) do if d.key == key then return d end end end

-- what the extras write
do
	reset("deDE", "DRUID"); local ns = loadAddon(); W.known = knownFor(ns, "DRUID", true)
	local shred = spellDef(ns, "DRUID:Shred")
	check(shred and ns.Offers(shred, "form") and ns.Offers(shred, "attack") and not ns.Offers(shred, "spam"), "Shred offers form/attack, no spam")
	ns.SetExtra(shred, "form", true); ns.SetExtra(shred, "attack", true)
	local b = ns.Render(shred)
	check(b:find("^#showtooltip\n/cast !Katzengestalt\n/cast %[@mouseover,harm,nodead%]%[harm,nodead%] Schreddern\n/startattack$"), "Shred with form+attack: " .. b)
	local hur = spellDef(ns, "DRUID:Hurricane")
	ns.SetExtra(hur, "spam", true); ns.SetExtra(hur, "form", true)
	b = ns.Render(hur)
	check(b:find("/cancelform\n/cast [nochanneling,@cursor] Hurrikan", 1, true), "Hurricane spam+cancelform: " .. b)
	ns.SetExtra(hur, "stop", true)
	check(ns.Render(hur):find("/stopcasting [nochanneling]\n", 1, true), "stop never cuts the spammed channel: " .. ns.Render(hur))
	local prowl = spellDef(ns, "DRUID:Prowl")
	ns.SetExtra(prowl, "spam", true); ns.SetExtra(prowl, "form", true)
	check(ns.Render(prowl):find("/cast !Katzengestalt\n/cast !Schleichen", 1, true), "Prowl spam-safe: " .. ns.Render(prowl))
	local bash = spellDef(ns, "DRUID:Bash")
	ns.SetExtra(bash, "form", true)
	check(ns.Render(bash):find("/cast !Terrorbärengestalt\n", 1, true), "Bash shifts into Dire Bear Form: " .. ns.Render(bash))

	reset("enUS", "WARRIOR"); ns = loadAddon(); W.known = knownFor(ns, "WARRIOR", true)
	local execute = spellDef(ns, "WARRIOR:Execute")
	check(not ns.Offers(execute, "stop"), "warriors get no stopcasting")
	ns.SetExtra(execute, "stance", true); ns.SetExtra(execute, "trinket", true)
	b = ns.Render(execute)
	check(b:find("^#showtooltip\n/cast %[nostance:1/3%] Battle Stance\n/use 13\n/use 14\n/cast "), "Execute with stance+trinkets: " .. b)
	local overpower = spellDef(ns, "WARRIOR:Overpower")
	ns.SetExtra(overpower, "stance", true)
	check(ns.Render(overpower):find("[nostance:1] Battle Stance", 1, true), "Overpower: battle only")

	reset("enUS", "MAGE"); ns = loadAddon(); W.known = knownFor(ns, "MAGE", true)
	for _, d in ipairs(ns.SpellDefinitions()) do check(not ns.Offers(d, "attack") and not ns.Offers(d, "form"), "mage has no attack/form: " .. d.id) end
end

-- spell tab in the window: switch tabs, tick, install, rank upkeep
do
	reset("deDE", "DRUID"); local ns = loadAddon()
	local ids = ns.SPELLS["DRUID:Shred"]; table.sort(ids)
	W.known = knownFor(ns, "DRUID", false)
	ns.Toggle()
	local f = _G.ForeverMacrosFrame
	local tabSpell, install
	for _, fr in ipairs(frames) do
		if fr._kind == "Button" and rawget(fr, "tab") == "spell" then tabSpell = fr end
		if fr._kind == "Button" and (fr._text or ""):find("Einbauen") then install = fr end
	end
	check(tabSpell and tabSpell:IsEnabled(), "spell tab button")
	tabSpell:Click()
	check(ForeverMacrosCharDB.tab == "spell" and not tabSpell:IsEnabled(), "spell tab active")
	local row
	for _, fr in ipairs(frames) do if fr._kind == "CheckButton" and fr._shown and type(rawget(fr, "def")) == "table" and fr.def.id == "sp:DRUID:Shred" then row = fr end end
	check(row ~= nil, "Shred row in the spell tab")
	if row then
		check(row.extras.form and row.extras.form:IsShown() and not (row.extras.stop and row.extras.stop:IsShown()), "Shred row: form box shown, no stop box")
		row.extras.form:Click()
		check(ForeverMacrosCharDB.extras["sp:DRUID:Shred"].form and ForeverMacrosCharDB.selected["sp:DRUID:Shred"], "form ticked, row selected")
		install._scripts.OnClick(install); runTimers()
		local made
		for _, m in ipairs(W.char) do if m.name == "Schreddern" then made = m end end
		check(made and made.body:find("Schreddern%(Rang 1%)"), "Shred installed with rank 1: " .. tostring(made and made.body))
		check(row.status:GetText():find("eingebaut"), "installed status: " .. tostring(row.status:GetText()))
		for _, id in ipairs(ids) do W.known[id] = true end
		fire("SPELLS_CHANGED"); runTimers()
		check(made.body:find("/cast !Katzengestalt\n", 1, true) and not made.body:find("Rang"), "rank upkeep raises the spell macro: " .. made.body)
	end
	local tabReady
	for _, fr in ipairs(frames) do if fr._kind == "Button" and rawget(fr, "tab") == "ready" then tabReady = fr end end
	tabReady:Click()
	check(ForeverMacrosCharDB.tab == nil, "back to ready-made tab")
	local stillSpell = false
	for _, fr in ipairs(frames) do if fr._kind == "CheckButton" and fr._shown and type(rawget(fr, "def")) == "table" and fr.def.scope == "spell" then stillSpell = true end end
	check(not stillSpell, "ready-made tab lists no spell rows")
	f:Hide()
end

print(("%d checks, %d failures"):format(checks, failures))
os.exit(failures == 0 and 0 or 1)
