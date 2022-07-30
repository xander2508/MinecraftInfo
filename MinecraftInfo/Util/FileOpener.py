import json


def LoadJsonFile(path: str) -> json:
    try:
        with open(path) as JsonFile:
            DataSource = json.load(JsonFile)
    except Exception as error:
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource
