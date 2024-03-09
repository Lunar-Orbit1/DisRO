local m = {}
local rs, studio, ms =game:GetService("RunService"), game:GetService("StudioService"), game:GetService("MarketplaceService")

local s,e = pcall(function()
	return ms:GetProductInfo(game.PlaceId)
end)
if s then
	m.Place = e.Name
else
	m.Place = game.Name
end

function m:LinesOfCode(scriptToRead:Script)
	if scriptToRead then
		if scriptToRead:IsA("Script") or scriptToRead:IsA("ModuleScript") or scriptToRead:IsA("LocalScript") then
			return #string.split(scriptToRead.Source,"\n") --//Kinda jenky. Gets lines by seeing how many line breaks there are
		else
			return 0
		end
	else
		return 0
	end
end

function m:GetCurrentStatus()
	return {
		place=m.Place,
		editing = studio.ActiveScript,
		LOC = m:LinesOfCode(studio.ActiveScript),
		testing = rs:IsRunning()
	}
end

function m:WhatAmICurrentlyDoing()
	local status = m:GetCurrentStatus()
	if status.editing and status.testing == false then
		--//We're in a script
		if status.editing:IsA("LocalScript") then
			return "editinglocal"
		elseif status.editing:IsA("ModuleScript") then
			return "editingmod"
		else
			return "editing"
		end
	elseif status.testing == true then
		--//We're playtesting
		return "testing"
	elseif status.testing == false and not status.editing then
		--//We're not testing we're in studio developing
		return "developing"
	end
end

return m

