# main.py
# This file runs the entire webserver and CLI interface that runs the backend of the RPC

# Import required modules first
import requests, os, json, logging, time, threading
from flask import Flask, render_template, request

# Setup variables/basic functions
currentVersion = "0.1" #The current version. This is for autoupdate
githubName = "DisRO-development" # The name of he repo, used in fetch/auto update shitttt
app = Flask(__name__)

# This jenk to disable flask logging
# Fuck you flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

def readSettings(keyname:str, filepath:str="./Server/config.json"):
    "Returns the setting associated with `keyname` from the `config.json` file \n\nFilepath is optional"
    try:
        file = open(filepath)
        data = json.load(file)[keyname]
        file.close()
        return data
    except Exception as e:
        print(f"ERROR READING SETTINGS: {e}")
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
        print(f"ERROR READING SETTINGS: {e}")
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
    app.run(debug=False, port=2020)

# Main startup code
def startup():
    try:
        autoUpdate = readSettings('autoUpdate')
        if autoUpdate != None and autoUpdate == True:
            # Check if there is an update to do
            githubData = getCurrentGithubVersion()
            latest = githubData[0]
            if latest != currentVersion:
                print(f"An update is ready to be installed! \nYou will update from {currentVersion} -> {latest}")
                print(f"View the  changelogs here: {githubData[1]['html_url']}")
                userchoice = askYORN("Do you want to update?") #Ask recursivly in-case they type the wrong thing
                if userchoice == True:
                    # Update here
                    print("Getting update ready for you!")
                else:
                    print("Skipping update. REMEMBER: You can always update with the update command!")

        
        # Auto update is either off, or no updates are needed
        # Startup webserver
        @app.route('/api/setstatus', methods=['POST'])
        def setstatus():
            print(request.data)
            return {"maybe": "Did it work?"}

        if __name__ == '__main__':
            app.logger.setLevel(logging.ERROR) # Hides default flask outputs

            # This needs to be in it's own thread
            # TODO: FIX
            thread = threading.Thread(target=startApp)
            thread.start()

        os.system("clear")
    except Exception as e:
        print("An error occured during startup:", e)

startup()