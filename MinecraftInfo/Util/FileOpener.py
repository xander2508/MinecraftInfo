import json

from black import err


def LoadJsonFile(path: str) -> json:
    try:
        with open(path) as JsonFile:
            DataSource = json.load(JsonFile)
    except Exception as error:
        print(error)  # Log
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource
