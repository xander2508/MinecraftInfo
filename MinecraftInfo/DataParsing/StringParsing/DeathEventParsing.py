from datetime import datetime, timezone
import json
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
import re
from MinecraftInfo.Util.SqlQueries import (
    LogUnknownEvent,
    AddItem,
    AddDeath,
    GetDeathMessages,
)


def UpdatePlayerDeaths(
    playerDeathMessages: json, messagesValidated, nameParser: callable, sqlQueryHandler
):
    """Provided list of player deaths, extract relevant info from the message and log it.
    Args:
        playerDeathMessages (json): Player deaths {ID:[Message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    playerDeathMessagesList = list(playerDeathMessages.keys())
    playerDeathMessagesList_int = map(int, playerDeathMessagesList)
    playerDeathMessagesList_str_sorted = map(str, sorted(playerDeathMessagesList_int))

    for DeathMessageIndex in playerDeathMessagesList_str_sorted:
        DeathMessage = playerDeathMessages[DeathMessageIndex][0]

        FinalDeathString, DeathTypeMatch = GetDeathMessage(DeathMessage)
        if FinalDeathString == None:
            sqlQueryHandler.QueueQuery(LogUnknownEvent, DeathMessage)
        else:
            LogDeathMessageEvent(
                DeathTypeMatch,
                FinalDeathString,
                int(DeathMessageIndex),
                playerDeathMessages[DeathMessageIndex][1],
                nameParser,
                sqlQueryHandler,
            )
        messagesValidated.MessageReviewed(DeathMessageIndex)


def LogDeathMessageEvent(
    deathTypeMatch: re,
    finalDeathString: str,
    deathMessageIndex: int,
    timestamp: int,
    nameParser: callable,
    sqlQueryHandler,
) -> None:
    """Extract info from the death message string and log the event.

    Args:
        deathTypeMatch (re): The regex object of the important info. eg: players or items used.
        finalDeathString (str): The string being interpreted.
        deathMessageIndex (int): The message index.
        timestamp (int): Time stamp the message was collected.
    """
    Timestamp = timestamp  # datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    NumberOfMatches = len(deathTypeMatch.groups())
    if NumberOfMatches >= 1:
        UsernameDead = nameParser(deathTypeMatch.group(1))
        if NumberOfMatches >= 2:
            UsernameKiller = nameParser(deathTypeMatch.group(2))
        else:
            UsernameKiller = nameParser("None")
        if NumberOfMatches >= 3:
            ItemUsed = deathTypeMatch.group(3)
            sqlQueryHandler.QueueQuery(AddItem, ItemUsed)
        else:
            sqlQueryHandler.QueueQuery(AddItem, "None")
            ItemUsed = "None"
        sqlQueryHandler.QueueQuery(
            AddDeath,
            deathMessageIndex,
            finalDeathString,
            UsernameDead,
            Timestamp,
            UsernameKiller,
            ItemUsed,
        )


def GetDeathMessage(deathMessage: str) -> tuple:
    """From the death message string extract the information groups.

    Args:
        deathMessage (str): The death message string.

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
        if match := re.search(DeathTypeStringRegex, deathMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > DeathTypeMatchCount:
                DeathTypeMatchCount = numberOfMatches
                FinalDeathString = DeathTypeString
                DeathTypeMatch = match
    return FinalDeathString, DeathTypeMatch
