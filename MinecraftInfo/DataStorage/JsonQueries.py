from MinecraftInfo.Util.FileOpener import LoadJsonFile


JSON_LOCATION = "MinecraftInfo\DataStorage\Configuration\DataSourceLocations.json"


def GetUsernameUrl():
    return LoadJsonFile(JSON_LOCATION)["UsernameURL"]


def GetOfficialChatChannelHandler():
    return LoadJsonFile(JSON_LOCATION)["Discord"]["Guilds"]["OfficialChat"]


def GetFullJson():
    return LoadJsonFile(JSON_LOCATION)


def LogUnknownDeathMessage(deathMessage: str):
    pass
