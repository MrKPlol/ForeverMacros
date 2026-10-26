-- ForeverMacros window: pick macros, see what each one will be, install the selection with one click.
local ADDON, ns = ...

local T = ns.DE and {
	title = "ForeverMacros", all = "Alle", none = "Keine", install = "Einbauen (%d)",
	class = "Klasse: %s", race = "Rasse", general = "Allgemein", equip = "Ausrüstung", items = "Gegenstände",
	quests = "Quests", professions = "Berufe", sets = "Ausrüstungssets",
	installed = "eingebaut", taken = "Name belegt", unlearned = "noch nicht gelernt",
	slots = "Charakter %d/%d   Allgemein %d/%d", charTab = "Tab: Charakter", accountTab = "Tab: Allgemein (alle Charaktere)",
	combat = "Im Kampf gesperrt", empty = "Nichts ausgewählt.",
	hint = "Klasse, Rasse und Sets landen im Charakter-Tab, alles andere im allgemeinen Tab.",
} or {
	title = "ForeverMacros", all = "All", none = "None", install = "Install (%d)",
	class = "Class: %s", race = "Race", general = "General", equip = "Equipment", items = "Items",
	quests = "Quests", professions = "Professions", sets = "Equipment sets",
	installed = "installed", taken = "name taken", unlearned = "not learned yet",
	slots = "Character %d/%d   General %d/%d", charTab = "Tab: Character", accountTab = "Tab: General (all characters)",
	combat = "Locked in combat", empty = "Nothing selected.",
	hint = "Class, race and set macros go to the character tab, everything else to the general tab.",
}

local ORDER = { "class", "race", "general", "equip", "items", "quests", "professions", "sets" }
local ROW, HEADER = 24, 26

local frame, content, installButton, slotText
local rows, headers, defs, byGroup = {}, {}, {}, {}

local function GroupOf(def)
	if def.scope == "class" or def.scope == "race" or def.scope == "set" then return def.scope == "set" and "sets" or def.scope end
	return def.group
end

local function Selected() return ForeverMacrosCharDB.selected end

local function SelectedDefs()
	local list = {}
	for _, def in ipairs(defs) do if Selected()[def.id] then list[#list + 1] = def end end
	return list
end

local function UpdateFooter()
	local numAccount, maxAccount, numChar, maxChar = ns.Limits()
	slotText:SetText(T.slots:format(numChar, maxChar, numAccount, maxAccount))
	local count = #SelectedDefs()
	if InCombatLockdown() then installButton:SetText(T.combat); installButton:Disable()
	else installButton:SetText(T.install:format(count)); installButton:SetEnabled(count > 0) end
end

local function Status(def)
	local name, perChar = ns.MacroName(def), ns.PerCharacter(def)
	local index, current = ns.Find(name, perChar)
	local store = perChar and ForeverMacrosCharDB.made or ForeverMacrosDB.made
	local status
	if index then
		local record = store[name]
		status = (record and record.body == current) and ("|cff40c040" .. T.installed .. "|r") or ("|cffff9020" .. T.taken .. "|r")
	end
	if def.scope ~= "set" then
		local _, _, missing = ns.Render(def)
		if missing and #missing > 0 and not status then status = "|cff909090" .. T.unlearned .. "|r" end
	end
	return name, status
end

local function ShowTooltip(row)
	local def = row.def
	GameTooltip:SetOwner(row, "ANCHOR_RIGHT")
	GameTooltip:AddLine(ns.MacroName(def))
	if def.note then GameTooltip:AddLine(def.note, 1, 1, 1, true) end
	GameTooltip:AddLine(ns.PerCharacter(def) and T.charTab or T.accountTab, 0.6, 0.6, 0.6)
	local body = def.scope == "set" and def.body or ns.Render(def)
	if body then
		GameTooltip:AddLine(" ")
		for line in body:gmatch("[^\n]+") do GameTooltip:AddLine(line, 0.55, 0.85, 1, true) end
	end
	GameTooltip:Show()
end

local function Row(i)
	local row = rows[i]
	if row then return row end
	row = CreateFrame("CheckButton", nil, content, "UICheckButtonTemplate")
	row:SetSize(24, 24)
	row.Text:SetFontObject("GameFontHighlight")
	row.status = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
	row.status:SetPoint("LEFT", row.Text, "RIGHT", 8, 0)
	row:SetScript("OnClick", function(self)
		Selected()[self.def.id] = self:GetChecked() and true or nil
		UpdateFooter()
	end)
	row:SetScript("OnEnter", ShowTooltip)
	row:SetScript("OnLeave", function() GameTooltip:Hide() end)
	rows[i] = row
	return row
end

local function Header(i)
	local header = headers[i]
	if header then return header end
	header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
	headers[i] = header
	return header
end

local Refresh
local refreshQueued = false
-- UPDATE_MACROS fires once per created macro: coalesce them into one refresh.
local function QueueRefresh()
	if refreshQueued then return end
	refreshQueued = true
	C_Timer.After(0.2, function() refreshQueued = false; Refresh() end)
end

function Refresh()
	if not frame or not frame:IsShown() then return end
	defs = ns.Definitions()
	wipe(byGroup)
	for _, def in ipairs(defs) do
		local group = GroupOf(def)
		byGroup[group] = byGroup[group] or {}
		table.insert(byGroup[group], def)
	end
	for _, row in ipairs(rows) do row:Hide() end
	for _, header in ipairs(headers) do header:Hide() end
	local y, r, h = -4, 0, 0
	local className = UnitClass("player")
	for _, group in ipairs(ORDER) do
		local list = byGroup[group]
		if list and #list > 0 then
			h = h + 1
			local header = Header(h)
			header:SetText(group == "class" and T.class:format(className or "") or T[group])
			header:ClearAllPoints(); header:SetPoint("TOPLEFT", 4, y); header:Show()
			y = y - HEADER
			for _, def in ipairs(list) do
				r = r + 1
				local row = Row(r)
				row.def = def
				local name, status = Status(def)
				row.Text:SetText(name)
				row.status:SetText(status or "")
				row:SetChecked(Selected()[def.id] and true or false)
				row:ClearAllPoints(); row:SetPoint("TOPLEFT", 8, y); row:Show()
				y = y - ROW
			end
			y = y - 6
		end
	end
	content:SetHeight(-y + 8)
	UpdateFooter()
end
ns.Refresh = Refresh

local function SetAll(value)
	for _, def in ipairs(defs) do Selected()[def.id] = value or nil end
	Refresh()
end

local function Build()
	frame = CreateFrame("Frame", "ForeverMacrosFrame", UIParent, "BasicFrameTemplateWithInset")
	frame:SetSize(480, 580)
	frame:SetPoint("CENTER")
	frame:SetFrameStrata("DIALOG")
	frame:SetClampedToScreen(true)
	frame:SetMovable(true)
	frame:EnableMouse(true)
	frame:RegisterForDrag("LeftButton")
	frame:SetScript("OnDragStart", frame.StartMoving)
	frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
	if frame.TitleText then frame.TitleText:SetText(T.title) end
	tinsert(UISpecialFrames, "ForeverMacrosFrame")

	local scroll = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
	scroll:SetPoint("TOPLEFT", 12, -30)
	scroll:SetPoint("BOTTOMRIGHT", -34, 84)
	content = CreateFrame("Frame", nil, scroll)
	content:SetSize(420, 10)
	scroll:SetScrollChild(content)

	local hint = frame:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
	hint:SetPoint("BOTTOMLEFT", 14, 62)
	hint:SetPoint("BOTTOMRIGHT", -14, 62)
	hint:SetJustifyH("LEFT")
	hint:SetText(T.hint)

	slotText = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
	slotText:SetPoint("BOTTOMLEFT", 14, 42)

	local all = CreateFrame("Button", nil, frame, "UIPanelButtonTemplate")
	all:SetSize(80, 24); all:SetPoint("BOTTOMLEFT", 12, 12); all:SetText(T.all)
	all:SetScript("OnClick", function() SetAll(true) end)
	local none = CreateFrame("Button", nil, frame, "UIPanelButtonTemplate")
	none:SetSize(80, 24); none:SetPoint("LEFT", all, "RIGHT", 6, 0); none:SetText(T.none)
	none:SetScript("OnClick", function() SetAll(false) end)

	installButton = CreateFrame("Button", nil, frame, "UIPanelButtonTemplate")
	installButton:SetSize(160, 24); installButton:SetPoint("BOTTOMRIGHT", -12, 12)
	installButton:SetScript("OnClick", function()
		local list = SelectedDefs()
		if #list == 0 then ns.Print(T.empty); return end
		installButton:Disable()
		ns.Install(list, function() Refresh() end)
	end)

	frame:SetScript("OnShow", function()
		-- ask the server for item data now, so tooltips and the install show localized item names
		if C_Item.RequestLoadItemDataByID then for id in pairs(ns.ITEMS) do C_Item.RequestLoadItemDataByID(id) end end
		Refresh()
	end)
	frame:SetScript("OnEvent", function(_, event)
		if event == "UPDATE_MACROS" then QueueRefresh() else UpdateFooter() end
	end)
	frame:RegisterEvent("UPDATE_MACROS")
	frame:RegisterEvent("PLAYER_REGEN_DISABLED")
	frame:RegisterEvent("PLAYER_REGEN_ENABLED")
	frame:Hide()
end

function ns.Toggle()
	if not frame then Build() end
	frame:SetShown(not frame:IsShown())
end

SLASH_FOREVERMACROS1 = "/macros"
SLASH_FOREVERMACROS2 = "/forevermacros"
SlashCmdList.FOREVERMACROS = function() ns.Toggle() end

function ForeverMacros_OnAddonCompartmentClick() ns.Toggle() end
