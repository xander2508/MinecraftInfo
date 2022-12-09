import json
import sys
import requests

from MinecraftInfo.Util.Logging import LogError


def LoadJsonFile(path: str) -> json:
    try:
        with open(path) as JsonFile:
            DataSource = json.load(JsonFile)
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource


def LoadWebJsonFile(urlPath: str) -> json:
    try:
        response = requests.get(urlPath)
        DataSource = json.loads(response.text)
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource


def GetUserModel(user: str) -> str:
    API_URL = "https://api.mojang.com/profiles/minecraft"
    Render_URL = "https://crafatar.com/renders/body/"
    Headers = {"Content-Type": "application/json"}

    Session = requests.Session()
    Response = Session.post(API_URL, headers=Headers, data='"' + user + '"')
    try:
        ID = json.loads(Response.text)[0]["id"]
    except:
        return ""
    return '<img src="' + Render_URL + ID + '?overlay=true"><br>'
