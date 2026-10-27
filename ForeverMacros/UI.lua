-- ForeverMacros window: pick macros, see what each one will be, install the selection with one click.
local ADDON, ns = ...

local T = ns.DE and {
	title = "ForeverMacros", all = "Alle", none = "Keine", install = "Einbauen (%d)",
	class = "Klasse: %s", race = "Rasse", general = "Allgemein", equip = "Ausrüstung",
	quests = "Quests", engineering = "Ingenieurskunst", professions = "Berufe", sets = "Ausrüstungssets",
	installed = "eingebaut", taken = "Name belegt", unlearned = "noch nicht gelernt", changed = "geändert: neu einbauen",
	opt = { mo = "MO", focus = "Fokus", tgt = "Ziel", self = "Ich", cursor = "Maus" },
	optTip = {
		mo = "Mouseover: wirkt auf die Einheit unter dem Mauszeiger (Welt oder Rahmen).",
		focus = "Fokus: wirkt auf dein Fokusziel (/focus).",
		tgt = "Ziel: wirkt auf dein aktuelles Ziel.",
		self = "Ich: wirkt auf dich selbst, wenn nichts davor passt.",
		cursor = "Maus: landet sofort an der Mausposition, ohne Zielkreis.",
		groundSelf = "Ich: landet sofort unter dir, ohne Zielkreis.",
	},
	optOrder = "Reihenfolge: MO > Fokus > Ziel > Ich. Nichts angehakt: normales Verhalten.",
	optGround = "Nur eins geht. Nichts angehakt: normaler Zielkreis.",
	optUnit = "Ohne Haken wirkt es wie gewohnt; mit Haken zuerst auf die gewählte Einheit.",
	slots = "Charakter %d/%d   Allgemein %d/%d", charTab = "Tab: Charakter", accountTab = "Tab: Allgemein (alle Charaktere)",
	combat = "Im Kampf gesperrt", empty = "Nichts ausgewählt.",
	hint = "Klasse, Rasse und Sets landen im Charakter-Tab, alles andere im allgemeinen Tab.",
} or {
	title = "ForeverMacros", all = "All", none = "None", install = "Install (%d)",
	class = "Class: %s", race = "Race", general = "General", equip = "Equipment",
	quests = "Quests", engineering = "Engineering", professions = "Professions", sets = "Equipment sets",
	installed = "installed", taken = "name taken", unlearned = "not learned yet", changed = "changed: install again",
	opt = { mo = "MO", focus = "Focus", tgt = "Target", self = "Self", cursor = "Cursor" },
	optTip = {
		mo = "Mouseover: hits the unit under the mouse pointer (world or frames).",
		focus = "Focus: hits your focus (/focus).",
		tgt = "Target: hits your current target.",
		self = "Self: hits you when nothing before it applies.",
		cursor = "Cursor: lands at the mouse position at once, no reticle.",
		groundSelf = "Self: lands at your feet at once, no reticle.",
	},
	optOrder = "Order: MO > Focus > Target > Self. Nothing ticked: normal behaviour.",
	optGround = "Only one at a time. Nothing ticked: normal reticle.",
	optUnit = "Unticked it works as usual; ticked it goes to the chosen unit first.",
	slots = "Character %d/%d   General %d/%d", charTab = "Tab: Character", accountTab = "Tab: General (all characters)",
	combat = "Locked in combat", empty = "Nothing selected.",
	hint = "Class, race and set macros go to the character tab, everything else to the general tab.",
}

local ORDER = { "class", "race", "general", "equip", "quests", "engineering", "professions", "sets" }
local ROW, HEADER = 24, 26
local OPT_X, OPT_W, STATUS_X = 190, 62, 440   -- target option boxes and status column, from the row's left edge

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
		if not record or record.body ~= current then status = "|cffff9020" .. T.taken .. "|r"
		elseif def.scope ~= "set" and ns.Render(def) ~= current then status = "|cffffd200" .. T.changed .. "|r"
		else status = "|cff40c040" .. T.installed .. "|r" end
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
	row.Text:SetWidth(OPT_X - 30)
	row.Text:SetWordWrap(false)
	row.Text:SetJustifyH("LEFT")
	row.status = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
	row.status:SetPoint("LEFT", row, "LEFT", STATUS_X, 0)
	row.options = {}
	row:SetScript("OnClick", function(self)
		Selected()[self.def.id] = self:GetChecked() and true or nil
		UpdateFooter()
	end)
	row:SetScript("OnEnter", ShowTooltip)
	row:SetScript("OnLeave", function() GameTooltip:Hide() end)
	rows[i] = row
	return row
end

local Refresh

local function ShowOptionTooltip(box)
	local kind = ns.TARGETS[box.row.def.target]
	GameTooltip:SetOwner(box, "ANCHOR_RIGHT")
	GameTooltip:AddLine(T.opt[box.option])
	local tip = (kind.exclusive and box.option == "self") and T.optTip.groundSelf or T.optTip[box.option]
	GameTooltip:AddLine(tip, 1, 1, 1, true)
	GameTooltip:AddLine(kind.exclusive and T.optGround or kind.fallback and T.optUnit or T.optOrder, 0.6, 0.6, 0.6, true)
	GameTooltip:Show()
end

-- Small tick boxes behind a row: which units the macro aims at (only the options its spell or item allows).
local function OptionBox(row, i)
	local box = row.options[i]
	if box then return box end
	box = CreateFrame("CheckButton", nil, row, "UICheckButtonTemplate")
	box:SetSize(18, 18)
	box.Text:SetFontObject("GameFontHighlightSmall")
	box.row = row
	box:SetPoint("LEFT", row, "LEFT", OPT_X + (i - 1) * OPT_W, 0)
	box:SetScript("OnClick", function(self)
		local def = self.row.def
		ns.SetTargetOption(def, self.option, self:GetChecked())
		Selected()[def.id] = true   -- a changed macro must be installed again to take effect
		Refresh()
	end)
	box:SetScript("OnEnter", ShowOptionTooltip)
	box:SetScript("OnLeave", function() GameTooltip:Hide() end)
	row.options[i] = box
	return box
end

local function GroupDefs(group) return byGroup[group] or {} end

local function Header(i)
	local header = headers[i]
	if header then return header end
	header = CreateFrame("CheckButton", nil, content, "UICheckButtonTemplate")
	header:SetSize(24, 24)
	header.Text:SetFontObject("GameFontNormalLarge")
	header:SetScript("OnClick", function(self)
		local value = self:GetChecked() and true or nil
		for _, def in ipairs(GroupDefs(self.group)) do Selected()[def.id] = value end
		Refresh()
	end)
	headers[i] = header
	return header
end

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
			header.group = group
			header.Text:SetText(group == "class" and T.class:format(className or "") or T[group])
			local all = true
			for _, def in ipairs(list) do if not Selected()[def.id] then all = false end end
			header:SetChecked(all)
			header:ClearAllPoints(); header:SetPoint("TOPLEFT", 0, y); header:Show()
			y = y - HEADER
			for _, def in ipairs(list) do
				r = r + 1
				local row = Row(r)
				row.def = def
				local name, status = Status(def)
				row.Text:SetText(name)
				row.status:SetText(status or "")
				row:SetChecked(Selected()[def.id] and true or false)
				for _, box in ipairs(row.options) do box:Hide() end
				local kind = ns.TARGETS[def.target]
				if kind then
					local choice = ns.TargetChoice(def)
					for k, option in ipairs(kind.order) do
						local box = OptionBox(row, k)
						box.option = option
						box.Text:SetText(T.opt[option])
						box:SetChecked(choice[option] and true or false)
						box:Show()
					end
				end
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
	frame:SetSize(600, 600)
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
	content:SetSize(540, 10)
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
