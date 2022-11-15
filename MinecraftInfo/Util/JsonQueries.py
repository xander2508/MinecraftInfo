import json
from MinecraftInfo.Util.FileOpener import LoadJsonFile


JSON_LOCATION = "MinecraftInfo\DataStorage\Configuration\DataSourceLocations.json"


def GetUsernameUrl() -> str:
    return LoadJsonFile(JSON_LOCATION)["UsernameURL"]


def GetOfficialChatChannelHandler() -> str:
    return LoadJsonFile(JSON_LOCATION)["Discord"]["Guilds"]["OfficialChat"]


def GetMarketplacesHandler() -> dict(str):
    return LoadJsonFile(JSON_LOCATION)["Discord"]["Guilds"]["Marketplaces"]


def GetDatabaseLocation() -> str:
    return LoadJsonFile(JSON_LOCATION)["DatabaseLocation"]


def GetFullJson() -> json:
    return LoadJsonFile(JSON_LOCATION)
