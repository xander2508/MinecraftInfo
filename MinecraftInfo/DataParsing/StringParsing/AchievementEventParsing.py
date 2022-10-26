import json
import re

from MinecraftInfo.DataStorage.SqlQueries import (
    AddAchievement,
    AddAchievementLink,
    GetAchievementMessages,
    LogUnknownEvent,
)
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing


def UpdatePlayerAchievement(achievementMessages: json, messagesValidated):
    """Provided list of player achievements, extract relevant info from the message and log it.
    Args:
        achievementMessages (json): Player achievement messages {ID:[Achievement message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    for AchievementMessageIndex in achievementMessages:
        AchievementMessage = achievementMessages[AchievementMessageIndex][0]
        FinalAchievementMessage, AchievementEventMatch = GetAchievementEvent(
            AchievementMessage
        )
        if FinalAchievementMessage == None:
            LogUnknownEvent(AchievementMessage)
        else:
            LogAchievementMessageEvent(
                int(AchievementMessageIndex),
                FinalAchievementMessage,
                AchievementEventMatch,
            )
        messagesValidated.MessageReviewed(AchievementMessageIndex)


def GetAchievementEvent(AchievementMessage: json):
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
        if match := re.search(AchievementTypeStringRegex, AchievementMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > AchievementTypeMatchCount:
                AchievementTypeMatchCount = numberOfMatches
                FinalAchievementString = AchievementTypeString
                AchievementTypeMatch = match
    return FinalAchievementString, AchievementTypeMatch


def LogAchievementMessageEvent(
    AchievementMessageIndex: int,
    FinalAchievementString: str,
    AchievementTypeMatch: re,
):
    NameParser = NameParsing()
    Username = NameParser(AchievementTypeMatch.group(1))
    AchievementString = AchievementTypeMatch.group(2)
    AddAchievement(AchievementString)
    AddAchievementLink(Username, AchievementString)
