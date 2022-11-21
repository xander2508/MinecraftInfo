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
