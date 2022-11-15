import json
import re

from MinecraftInfo.Util.SqlQueries import (
    AddAchievement,
    AddAchievementLink,
    GetAchievementMessages,
    LogUnknownEvent,
)
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing


def UpdatePlayerAchievement(
    achievementMessages: json, messagesValidated, nameParser, sqlQueryHandler
) -> None:
    """Provided list of player achievements, extract relevant info from the message and log it.
    Args:
        achievementMessages (json): Player achievement messages {ID:[Achievement message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    achievementMessagesList = list(achievementMessages.keys())
    achievementMessagesList_int = map(int, achievementMessagesList)
    achievementMessagesList_str_sorted = map(str, sorted(achievementMessagesList_int))

    for AchievementMessageIndex in achievementMessagesList_str_sorted:
        AchievementMessage = achievementMessages[AchievementMessageIndex]
        FinalAchievementMessage, AchievementEventMatch = GetAchievementEvent(
            AchievementMessage
        )
        if FinalAchievementMessage == None:
            sqlQueryHandler.QueueQuery(LogUnknownEvent, AchievementMessage)
        else:
            LogAchievementMessageEvent(
                int(AchievementMessageIndex),
                FinalAchievementMessage,
                AchievementEventMatch,
                nameParser,
                sqlQueryHandler,
            )
        messagesValidated.MessageReviewed(AchievementMessageIndex)


def GetAchievementEvent(achievementMessage: json) -> tuple(str, object):
    """Retrieve the achievement type from the raw message

    Args:
        achievementMessage (json): Raw achievement message

    Returns:
        Achievement: Returns both the raw achievement and the match object
    """
    FinalAchievementString = None
    AchievementTypeMatch = None
    AchievementTypeMatchCount = 0
    AchievementMessageDict = GetAchievementMessages()
    for AchievementTypeIndex in AchievementMessageDict:
        AchievementTypeString = AchievementMessageDict[AchievementTypeIndex]
        AchievementTypeStringRegex = AchievementTypeString
        AchievementTypeStringRegex = AchievementTypeStringRegex.replace(
            "<player>", "(.*)"
        )
        AchievementTypeStringRegex = AchievementTypeStringRegex.replace(
            "<achievement>", "(.*)"
        )
        if match := re.search(AchievementTypeStringRegex, achievementMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > AchievementTypeMatchCount:
                AchievementTypeMatchCount = numberOfMatches
                FinalAchievementString = AchievementTypeString
                AchievementTypeMatch = match
    return FinalAchievementString, AchievementTypeMatch


def LogAchievementMessageEvent(
    achievementMessageIndex: int,
    finalAchievementString: str,
    achievementTypeMatch: re,
    nameParser,
    sqlQueryHandler,
) -> None:
    """_summary_ Log the achievement event.

    Args:
        AchievementMessageIndex (int): _description_
        FinalAchievementString (str): _description_
        AchievementTypeMatch (re): _description_
        NameParser (_type_): _description_
        SqlQueryHandler (_type_): _description_
    """
    Username = nameParser(achievementTypeMatch.group(1))
    AchievementString = achievementTypeMatch.group(2)
    sqlQueryHandler.QueueQuery(AddAchievement, AchievementString)
    sqlQueryHandler.QueueQuery(AddAchievementLink, Username, AchievementString)
