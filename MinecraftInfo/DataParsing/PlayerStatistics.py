import json
from types import GeneratorType
from MinecraftInfo.Util.FileOpener import LoadJsonFile
import re


def PlayerStatistics(minecraftChatLog: list, dataSourceHandler: str) -> None:
    """Given discord chat data update the player statistics.

    Args:
        minecraftChatLog (list): Minecraft chat log.
    """
    UpdatePlayerDeaths(
        (
            x
            for x in minecraftChatLog
            if x["embeds"] != []
            and "title" in x["embeds"][0]
            and x["embeds"][0]["title"] == "Death Message"
        ),
        dataSourceHandler,
    )


def UpdatePlayerDeaths(playerDeathMessages: GeneratorType, dataSourceHandler: str):
    # playerDeathMessages = [
    #     {
    #         "type": "rich",
    #         "title": "Death Message",
    #         "description": "❀True Blod'nd❀ melvaren was slain by Mod Korulein using [❀ The Chocolatiers Sabre ❀]",
    #         "color": 255,
    #         "timestamp": "2022-08-01T18:35:30.615000+00:00",
    #         "author": {
    #             "name": "❀True Blod'nd❀ melvaren was slain by Mod Korulein using [❀ The Chocolatiers Sabre ❀]",
    #             "icon_url": "https://crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #             "proxy_icon_url": "https://images-ext-1.discordapp.net/external/DRBsAsfn8GQlkM8g8Xi50SFMKRcyrALSZT7m8Eqn6hc/https/crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #         },
    #         "thumbnail": {
    #             "url": "https://crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #             "proxy_url": "https://images-ext-1.discordapp.net/external/DRBsAsfn8GQlkM8g8Xi50SFMKRcyrALSZT7m8Eqn6hc/https/crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #             "width": 160,
    #             "height": 160,
    #         },
    #         "footer": {
    #             "text": "F in the chat",
    #             "icon_url": "https://crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #             "proxy_icon_url": "https://images-ext-1.discordapp.net/external/DRBsAsfn8GQlkM8g8Xi50SFMKRcyrALSZT7m8Eqn6hc/https/crafatar.com/avatars/3c50898e-f596-4c99-8214-efcb1f26c56f",
    #         },
    #     }
    # ]
    ConfiguartionFile = LoadJsonFile(dataSourceHandler)
    for DeathMessage in playerDeathMessages:
        DeathTypeIndex, DeathTypeMatch = GetDeathMessage(
            ConfiguartionFile, DeathMessage
        )
        if DeathTypeIndex == None:
            pass
            # create new death message
        else:
            NumberOfMatches = len(DeathTypeMatch.groups())
            if NumberOfMatches == 1:
                GetUsername(DeathTypeMatch[0],ConfiguartionFile["UsernameURL"])
                if NumberOfMatches == 2:
                    GetUsername(DeathTypeMatch[1],ConfiguartionFile["UsernameURL"])
                    if NumberOfMatches == 3:
                        pass
        
            # print(DeathTypeIndex)
            # print(DeathTypeMatch.groups())
            # print(ConfiguartionFile["Death Messages"][DeathTypeIndex])

    # Assign it to user / make user etc
    # Generate a new death message regex
    # http://104.238.222.67:2096/up/world/newrathnir/


def GetDeathMessage(ConfiguartionFile: json, DeathMessage: json):
    DeathTypeIndex = None
    DeathTypeMatchCount = 0
    for DeathType in ConfiguartionFile["Death Messages"]:
        DeathTypeString = ConfiguartionFile["Death Messages"][DeathType]
        DeathTypeString = DeathTypeString.replace("<player>", "(.*)")
        DeathTypeString = DeathTypeString.replace("<player/mob>", "(.*)")
        DeathTypeString = DeathTypeString.replace("<item>", "(.*)")
        if match := re.search(
            DeathTypeString, DeathMessage["embeds"][0]["description"]
        ):
            numberOfMatches = len(match.groups())
            if numberOfMatches > DeathTypeMatchCount:
                DeathTypeMatchCount = numberOfMatches
                DeathTypeIndex = DeathType
                DeathTypeMatch = match
    return DeathTypeIndex, DeathTypeMatch


def GetUsername(username: str, usernameListUrl: str):
    #ConfiguartionFile = LoadJsonFile(usernameListUrl)

