import json
import requests


def LoadJsonFile(path: str) -> json:
    try:
        with open(path) as JsonFile:
            DataSource = json.load(JsonFile)
    except Exception as error:
        print(error)  # Log
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource


def LoadWebJsonFile(urlPath: str) -> json:
    try:
        response = requests.get(urlPath)
        DataSource = json.loads(response.text)
    except Exception as error:
        print(error)  # Log
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource
