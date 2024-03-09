local configuration = { --//Don't mess with. Configures stuff like the endpoints
	API_URL = "http://127.0.0.1:2000/api",
	CLIENT_VERSION = "0.2",
	MINIMUM_SERVER_VERSION = "0.1",
	START_TIME = math.floor(os.time()),
	SETTINGS = nil, --//Placeholder for the settings loaded in from the server
}
local serverdata --//Placeholder for fetched information for when the plugin is started
local currentpage = 2 --//1 - github. 2 - about. 3 - config
local pages = {"github", "about", "config"}
local http, toolbar = game:GetService("HttpService"), plugin:CreateToolbar("DisRO")
local gui, utils = script.Parent.Frame, require(script.StudioSystems)
local pluginButton, info = toolbar:CreateButton(
	"Open Menu", --//Text below button
	"Information about DisRO", --//Text above button
	"rbxassetid://8740888472" --//Icon
),DockWidgetPluginGuiInfo.new(
	Enum.InitialDockState.Float,
	false, 
	false,
	500, --default weight
	500, --default height
	500, --minimum weight (optional)
	500 --minimum height (optional)
)
local widget = plugin:CreateDockWidgetPluginGui(
	"DISROSTUFF", --A unique and consistent identifier used to storing the widget’s dock state and other internal details
	info --dock widget info
)
widget.Title = "DisRO Menu" --Giving title to our widget gui
gui.Parent = widget


--//Functions and misc event handlers
gui.Message.save.MouseButton1Click:Connect(function()
	gui.Message.Visible = false
end)
gui.Error.save.MouseButton1Click:Connect(function()
	gui.Error.Visible = false
end)
pluginButton.Click:Connect(function()
	widget.Enabled = not widget.Enabled
end)

--//Shows the user a message
function notify(description, title)
	assert(description, "Description required")
	if title then
		gui.Message.title.Text = title
	else
		gui.Message.title.Text = "Notification"
	end
	gui.Message.desc.Text = description
	gui.Message.Visible = true
end

--//Shows the user an error
function notifyError(description, title)
	assert(description, "Description required")
	if title then
		gui.Error.title.Text = title
	else
		gui.Error.title.Text = "Error"
	end
	gui.Error.desc.Text = description
	gui.Error.Visible = true
	warn("// DISRO:",description)
end

--//Makes a get request to the endpoint on the server
--//Returns nil if error
function getrequest(endpoint)
	local s,e = pcall(function()
		return http:GetAsync(string.format("%s/%s", configuration.API_URL, endpoint))
	end)
	if s then 
		return http:JSONDecode(e)
	else
		return nil
	end
end

--//Changes the page on the gui
function changePage(pagenumber:number)
	for _,v in pairs(gui.Mainframe:GetChildren()) do 
		if v:IsA("Frame") and v.Name ~= pages[pagenumber] then
			v.Visible = false
		elseif v.Name == pages[pagenumber] and v:IsA("Frame") then
			v.Visible = true
		end
	end
end

function waitForServerConnection()
	--//This will wait for the webserver to be online and return the information
	local fetched
	repeat
		fetched = getrequest("fetchinfo")
		task.wait(5)
	until fetched ~= nil
	return fetched
end

function mainEventLoop()
	local oldstatus = nil
	while true do 
		local status = utils:GetCurrentStatus()
		if status ~= oldstatus then
			oldstatus = status
			local dataToSend = {}
		end
	end
end

serverdata = waitForServerConnection()['data']
configuration.SETTINGS = serverdata['settings']

if tonumber(serverdata.serverversion) < tonumber(configuration.MINIMUM_SERVER_VERSION) then
	print("NO")
else
	print("YAY")
end