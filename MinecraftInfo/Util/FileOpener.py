import json
import sys

from MinecraftInfo.Util.Logging import LogError
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(urlPath, verify=False, timeout=10)
        DataSource = json.loads(response.text)
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        DataSource = json.loads(json.dumps([{}]))
    finally:
        return DataSource
