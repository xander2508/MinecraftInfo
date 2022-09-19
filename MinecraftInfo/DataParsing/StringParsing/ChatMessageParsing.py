import json
import re

from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing


def UpdatePlayerMessages(playerMessages: json, messagesValidated):
    for MessageIndex in playerMessages:
        Message = playerMessages[MessageIndex]
        NameParser = NameParsing()


def GetMessage(DeathMessage: json):
    FinalDeathString = None
    DeathTypeMatch = None
    DeathTypeMatchCount = 0
    DeathMessageDict = GetDeathMessages()
    for DeathTypeIndex in DeathMessageDict:
        DeathTypeString = DeathMessageDict[DeathTypeIndex]
        DeathTypeStringRegex = DeathTypeString
        DeathTypeStringRegex = DeathTypeStringRegex.replace("<player>", "(.*)")
        DeathTypeStringRegex = DeathTypeStringRegex.replace("<player/mob>", "(.*)")
        DeathTypeStringRegex = DeathTypeStringRegex.replace("<item>", "(.*)")
        if match := re.search(DeathTypeStringRegex, DeathMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > DeathTypeMatchCount:
                DeathTypeMatchCount = numberOfMatches
                FinalDeathString = DeathTypeString
                DeathTypeMatch = match
    return FinalDeathString, DeathTypeMatch
