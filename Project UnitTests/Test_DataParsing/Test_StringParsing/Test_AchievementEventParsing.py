import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.DataParsing.StringParsing.AchievementEventParsing import UpdatePlayerAchievement

def test_UpdatePlayerAchievement_Functions(mocker):
    achievementMessages = {'1040347002287968328': 'PVPBrain has made the advancement Getting an Upgrade!', '1040346536376291378': 'MrBlockLP has made the advancement Getting an Upgrade!', '1040346227591622696': 'ParrotAce has made the advancement Getting an Upgrade!'}
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.AchievementEventParsing.LogAchievementMessageEvent",
    )
    messagesValidated = type("", (object,), {"MessageReviewed": lambda x,y: []})()
    NameParser = type("", (object,), {"a": lambda x: []})()
    SqlQueryHandler = type("", (object,), {"QueueQuery": lambda x,y,z: []})() 
    assert UpdatePlayerAchievement(achievementMessages,messagesValidated,NameParser,SqlQueryHandler) == True