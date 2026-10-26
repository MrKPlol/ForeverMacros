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
	local def; for _, d in ipairs(ns.MACROS) do if d.id == "u_hearth" then def = d end end
	ns.Install({ def }, nil); runTimers()
	local _, _, body = GetMacroInfo(1)
	print("German hearthstone macro: " .. tostring(body))
	check(body and body:find("Ruhestein"), "item name localized after load")
end

-- scenario: UI opens, lists, selects, installs
do
	reset("deDE", "DRUID"); local ns = loadAddon(); W.known = knownFor(ns, "DRUID", true); W.sets = true
	ns.Toggle()
	local f = _G.ForeverMacrosFrame
	check(f and f:IsShown(), "window shows")
	local cbs = {}
	for _, fr in ipairs(frames) do if fr._kind == "CheckButton" and fr._shown and fr.def then cbs[#cbs + 1] = fr end end
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
	SlashCmdList.FOREVERMACROS(""); check(not f:IsShown(), "/macros toggles")
	fire("PLAYER_REGEN_DISABLED")
end

print(("%d checks, %d failures"):format(checks, failures))
os.exit(failures == 0 and 0 or 1)
