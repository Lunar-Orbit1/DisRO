# main.py
# This file runs the entire webserver and CLI interface that runs the backend of the RPC

# Import required modules first
import requests, os, json, logging, time, threading
from pypresence import Presence
from flask import Flask, request

# Setup variables/basic functions
currentVersion = "0.2" #The current version. This is for autoupdate
githubName = "DisRO" # The name of he repo, used in fetch/auto update shitttt
assets = {
    "developing": {
        "name": "developing",
        "robloxID": 0,
    },
    "mainicon": {
        "name": "mainicon",
        "robloxID": 0,
    },
    "studio": {
        "name": "studio",
        "robloxID": 0,
    },
    "arrow": {
        "name": "arrow",
        "robloxID": 0,
    },
    "editing": {
        "name": "editing",
        "robloxID": 0,
    },
    "editinglocal": {
        "name": "editinglocal",
        "robloxID": 0,
    },
    "editingmod": {
        "name": "editingmod",
        "robloxID": 0,
    },
}
app = Flask(__name__)

# This jenk to disable flask logging
# Fuck you flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True
class tc: #console colors
    Header = '\033[95m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    Green = '\033[92m'
    Warn = '\033[93m'
    Fail = '\033[91m'
    End = '\033[0m'
    Bold = '\033[1m'
    Underline = '\033[4m'

def readSettings(keyname:str="all", filepath:str="./Server/config.json"):
    "Returns the setting associated with `keyname` from the `config.json` file \n\nFilepath is optional"
    try:
        file = open(filepath)
        data = json.load(file)
        if keyname != "all":
            data = data[keyname]
        file.close()
        return data
    except Exception as e:
        print(f"{tc.Fail}[ERROR]{tc.End} An error occured while reading settings:", e)
        return None

def setSettings(keyname:str, value:any, filepath:str="./Server/config.json"):
    "Writes to the settings file under the key associated with `keyname`"
    try:
        # This is messy code
        # TODO: Rewrite to make it better and prettier
        file = open(filepath, "r+")
        data = json.load(file)
        file.seek(0)
        data[keyname] = value
        jsonData = json.dumps(data, indent=4)
        file.write(jsonData)
        file.close()
        del file, data, jsonData
        return True
    except Exception as e:
        print(f"{tc.Fail}[ERROR]{tc.End} An error occured while writing settings:", e)
        return None
    
def getCurrentGithubVersion():
    url = f"https://api.github.com/repos/lunar-orbit1/{githubName}/releases/latest"
    request = requests.get(url)
    if request.status_code == 200:
        return [request.json()['tag_name'], request.json()]
    else:
        print("Error fetching github version")
        print(f"Status code: {str(request.status_code)}")
        print(request.json())
        return [currentVersion, request.json()]
# Recursive bullshit that'll prompt users yes/no questions.
def askYORN(question:str):
    "Asks the user the specified yes or no question"
    userchoice = input(question+" (y/n) \n> ").lower()
    if userchoice != "y" and userchoice != "n":
        return askYORN(question)
    elif userchoice == "y":
        return True
    elif userchoice == "n":
        return False

def startApp():
    app.run(debug=False, port=2000)

@app.route('/api/fetchinfo', methods=['GET'])
def setstatus():
    return {"data": {
        "serverversion": currentVersion,
        "artassets": assets,
        "settings": readSettings(),
    }}, 200

# Main startup code
def startup():
    try:
        autoUpdate = readSettings('autoUpdate')
        if autoUpdate != None and autoUpdate == True:
            # Check if there is an update to do
            githubData = getCurrentGithubVersion()
            latest = githubData[0]
            if latest != currentVersion:
                print(f"{tc.Header}An update is ready to be installed!{tc.End} \nYou will update from {currentVersion} -> {latest}")
                print(f"View the changelogs here: {githubData[1]['html_url']}")
                userchoice = askYORN(f"{tc.Green}Do you want to update?{tc.End}") #Ask recursivly in-case they type the wrong thing
                if userchoice == True:
                    # Update here
                    print(f"{tc.Green}Getting update ready for you!{tc.End}")
                else:
                    print(f"{tc.Fail}Skipping update. REMEMBER: You can always update with the update command!{tc.End}")
        # Auto update is either off, the user skipped updates, or no updates are needed
        # Startup webserver
        if __name__ == '__main__':
            app.logger.setLevel(logging.ERROR) # Hides default flask outputs
            global thread
            thread = threading.Thread(target=startApp)
            thread.start()

        time.sleep(0.1)
        os.system("cls")
        # Put the cli input here now
        print(f"{tc.Green}DisRO webserver online\nYou can minimize this window now")
        print(f"{tc.Fail}Close this terminal tab to stop the server{tc.End}")
    except Exception as e:
        print(f"{tc.Fail}[ERROR]{tc.End} An error occured during startup:", e)

startup()
#python -m auto_py_to_exe