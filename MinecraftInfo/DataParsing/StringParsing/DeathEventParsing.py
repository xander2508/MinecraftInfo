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


def UpdatePlayerDeaths(playerDeathMessages: json, messagesValidated, NameParser:callable, SqlQueryHandler):
    """Provided list of player deaths, extract relevant info from the message and log it.
    Args:
        playerDeathMessages (json): Player deaths {ID:[Message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    for DeathMessageIndex in playerDeathMessages:
        DeathMessage = playerDeathMessages[DeathMessageIndex][0]

        FinalDeathString, DeathTypeMatch = GetDeathMessage(DeathMessage)
        if FinalDeathString == None:
            SqlQueryHandler.QueueQuery(LogUnknownEvent,DeathMessage)
        else:
            LogDeathMessageEvent(
                DeathTypeMatch,
                FinalDeathString,
                int(DeathMessageIndex),
                playerDeathMessages[DeathMessageIndex][1],
                NameParser,
                SqlQueryHandler,
            )
        messagesValidated.MessageReviewed(DeathMessageIndex)


def LogDeathMessageEvent(
    deathTypeMatch: re, finalDeathString: str, deathMessageIndex: int, timestamp: int, NameParser: callable,SqlQueryHandler
):
    """Extract info from the death message string and log the event.

    Args:
        deathTypeMatch (re): The regex object of the important info. eg: players or items used.
        finalDeathString (str): The string being interpreted.
        deathMessageIndex (int): The message index.
        timestamp (int): Time stamp the message was collected.
    """
    Timestamp = timestamp#datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    NumberOfMatches = len(deathTypeMatch.groups())
    if NumberOfMatches >= 1:
        UsernameDead = NameParser(deathTypeMatch.group(1))
        if NumberOfMatches >= 2:
            UsernameKiller = NameParser(deathTypeMatch.group(2))
        else:
            UsernameKiller = None
        if NumberOfMatches >= 3:
            ItemUsed = deathTypeMatch.group(3)
            SqlQueryHandler.QueueQuery(AddItem,ItemUsed)
        else:
            ItemUsed = None
        SqlQueryHandler.QueueQuery(AddDeath,
            deathMessageIndex,
            finalDeathString,
            UsernameDead,
            Timestamp,
            UsernameKiller,
            ItemUsed,
        )


def GetDeathMessage(DeathMessage: str):
    """From the death message string extract the information groups.

    Args:
        DeathMessage (str): The death message string.

    Returns:
        _type_: The matched death message string and the regex object of those matches.
    """
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
