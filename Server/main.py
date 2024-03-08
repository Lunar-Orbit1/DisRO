# main.py
# This file runs the entire webserver and CLI interface that runs the backend of the RPC

# Import required modules first
import requests, os, json
from flask import Flask, render_template, request

# Setup variables/basic functions
currentVersion = "0.1" #The current version. This is for autoupdate
githubName = "DisRO-development"

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
        return request.json()['tag_name'][1:]
    else:
        print("Error fetching github version")
        print(f"Status code: {str(request.status_code)}")
        print(request.json())
        return currentVersion

# Main startup code
def startup():
    try:
        autoUpdate = readSettings('autoUpdate')
        if autoUpdate != None and autoUpdate == True:
            # Check if there is an update to do
            latest = getCurrentGithubVersion()
            print(latest)
        
        # Auto update is either off, or no updates are needed
        pass
    except Exception as e:
        print("An error occured during startup:", e)

startup()