import json
import sys
from MinecraftInfo.Util.FileOpener import LoadJsonFile
from MinecraftInfo.Util.Logging import LogError


JSON_LOCATION = "MinecraftInfo\DataStorage\Configuration\DataSourceLocations.json"


def GetUsernameUrl() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["UsernameURL"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetOfficialChatChannelHandler() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["Discord"]["Guilds"]["OfficialChat"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetMarketplacesHandler() -> dict:
    try:
        return LoadJsonFile(JSON_LOCATION)["Discord"]["Guilds"]["Marketplaces"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetDatabaseLocation() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["DatabaseLocation"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetDatabaseBackupLocation() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["DatabaseBackupLocation"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetClaimURL() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["ClaimURL"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetAPI_URL() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["API_URL"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetRenderURL() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["RenderURL"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetMapPath() -> str:
    try:
        return LoadJsonFile(JSON_LOCATION)["MapPath"]
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""


def GetFullJson() -> json:
    try:
        return LoadJsonFile(JSON_LOCATION)
    except Exception as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        return ""
