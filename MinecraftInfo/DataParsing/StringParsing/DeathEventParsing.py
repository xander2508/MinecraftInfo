from datetime import datetime, timezone
import json
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
import re
from MinecraftInfo.DataStorage.SqlQueries import (
    LogUnknownEvent,
    AddItem,
    AddDeath,
    GetDeathMessages,
)


def UpdatePlayerDeaths(playerDeathMessages: json, messagesValidated):

    for DeathMessageIndex in playerDeathMessages:
        DeathMessage = playerDeathMessages[DeathMessageIndex][0]

        FinalDeathString, DeathTypeMatch = GetDeathMessage(DeathMessage)
        if FinalDeathString == None:
            LogUnknownEvent(DeathMessage)
        else:
            LogDeathMessageEvent(
                DeathTypeMatch,
                FinalDeathString,
                int(DeathMessageIndex),
                int(playerDeathMessages[DeathMessageIndex][1]),
            )
        messagesValidated.MessageReviewed(DeathMessageIndex)


def LogDeathMessageEvent(
    DeathTypeMatch: re, FinalDeathString: str, DeathMessageIndex: int, timestamp: int
):
    Timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    NameParser = NameParsing()
    NumberOfMatches = len(DeathTypeMatch.groups())
    if NumberOfMatches >= 1:
        UsernameDead = NameParser(DeathTypeMatch.group(1))
        if NumberOfMatches >= 2:
            UsernameKiller = NameParser(DeathTypeMatch.group(2))
        else:
            UsernameKiller = None
        if NumberOfMatches >= 3:
            ItemUsed = DeathTypeMatch.group(3)
            AddItem(ItemUsed)
        else:
            ItemUsed = None
        AddDeath(
            DeathMessageIndex,
            FinalDeathString,
            UsernameDead,
            Timestamp,
            UsernameKiller,
            ItemUsed,
        )


def GetDeathMessage(DeathMessage: json):
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
