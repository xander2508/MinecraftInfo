import json
from types import GeneratorType
from MinecraftInfo.Util.FileOpener import LoadJsonFile
from MinecraftInfo.Util.FileOpener import LoadWebJsonFile
import re
from MinecraftInfo.DataParsing.Sql import (
    AddUsername,
    AddItem,
    AddDeath,
    AddNickname,
    AddNicknameLink,
)


def PlayerStatistics(minecraftChatLog: list, dataSourceHandler: str) -> None:
    """Given discord chat data update the player statistics.

    Args:
        minecraftChatLog (list): Minecraft chat log.
    """
    for Source in minecraftChatLog:
        UpdatePlayerDeaths(
            Source["Embeds"]["Death"],
            dataSourceHandler,
        )


def UpdatePlayerDeaths(playerDeathMessages: json, dataSourceHandler: str):
    playerDeathMessages = {
        "1005194029589336216": "Khagan TheRealYuca was slain by Evil Helsian GayForDaddy using Test"
    }
    ConfiguartionFile = LoadJsonFile(dataSourceHandler)
    for DeathMessageIndex in playerDeathMessages:
        DeathMessage = playerDeathMessages[DeathMessageIndex]
        DeathTypeIndex, DeathTypeMatch = GetDeathMessage(
            ConfiguartionFile, DeathMessage
        )
        UsernameDead = None
        UsernameKiller = None
        ItemUsed = None
        Nickname = None
        if DeathTypeIndex == None:
            pass
            # create new death message
        else:
            UsernameJson = LoadWebJsonFile(ConfiguartionFile["UsernameURL"])
            NumberOfMatches = len(DeathTypeMatch.groups())
            if NumberOfMatches >= 1:
                UsernameDead = GetUsername(DeathTypeMatch[0], UsernameJson)
                if UsernameDead == None:
                    UsernameDead = (DeathTypeMatch[0].split(" "))[-1]
                AddUsername(UsernameDead)
                if DeathTypeMatch[0].split(" ") > 1:
                    Nickname = " ".join((DeathTypeMatch[0].split(" ")))[:-1]
                    AddNickname(Nickname)
                    AddNicknameLink(Nickname, UsernameDead)
            if NumberOfMatches >= 2:
                UsernameKiller = GetUsername(DeathTypeMatch[1], UsernameJson)
                if UsernameKiller == None:
                    UsernameKiller = (DeathTypeMatch[1].split(" "))[-1]
                AddUsername(UsernameKiller)
                if DeathTypeMatch[1].split(" ") > 1:
                    AddNickname(" ".join((DeathTypeMatch[1].split(" ")))[:-1])
                    AddNicknameLink(Nickname, UsernameKiller)
            if NumberOfMatches >= 3:
                ItemUsed = DeathTypeMatch.group(3)
                AddItem(ItemUsed)
            AddDeath(UsernameDead, UsernameKiller, ItemUsed)

            # strip
            # testing and move into propper files
            # print(UsernameDead)
            # print(UsernameKiller)
            # print(ItemUsed)
            # print(NumberOfMatches)
            # print(DeathTypeIndex)
            # print(DeathTypeMatch.groups())
            # print(ConfiguartionFile["Death Messages"][DeathTypeIndex])

    # Known nickname
    # Flag next to unkonwn user to be check against known usernames + names
    # Assign it to user / make user etc
    # Generate a new death message regex
    # http://104.238.222.67:2096/up/world/newrathnir/


def GetDeathMessage(ConfiguartionFile: json, DeathMessage: json):
    DeathTypeIndex = None
    DeathTypeMatch = None
    DeathTypeMatchCount = 0
    for DeathType in ConfiguartionFile["Death Messages"]:
        DeathTypeString = ConfiguartionFile["Death Messages"][DeathType]
        DeathTypeString = DeathTypeString.replace("<player>", "(.*)")
        DeathTypeString = DeathTypeString.replace("<player/mob>", "(.*)")
        DeathTypeString = DeathTypeString.replace("<item>", "(.*)")
        if match := re.search(DeathTypeString, DeathMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > DeathTypeMatchCount:
                DeathTypeMatchCount = numberOfMatches
                DeathTypeIndex = DeathType
                DeathTypeMatch = match
    return DeathTypeIndex, DeathTypeMatch


def GetUsername(username: str, UsernameJson: json):
    for player in UsernameJson["players"]:
        if player["name"] in username or player["account"] in username:
            return player["account"]
    return None
