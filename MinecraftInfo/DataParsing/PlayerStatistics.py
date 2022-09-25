from MinecraftInfo.DataParsing.StringParsing.AchievementEventParsing import (
    UpdatePlayerAchievement,
)
from MinecraftInfo.DataParsing.StringParsing.ChatMessageParsing import (
    UpdatePlayerMessages,
)
from MinecraftInfo.DataParsing.StringParsing.ConnectionEventParsing import (
    UpdatePlayerConnections,
)
from MinecraftInfo.DataParsing.StringParsing.DeathEventParsing import UpdatePlayerDeaths
from MinecraftInfo.DataParsing.StringParsing.NameParsing import ValidateUsers


def PlayerStatistics(minecraftChatLog: list, messagesValidated) -> None:
    """Given discord chat data update the player statistics.

    Args:
        minecraftChatLog (list): Formatted Minecraft chat log. [
            {
                "Message": {},
                "Embeds": {
                    "Death": {},
                    "Connection": {},
                    "Achievement": {},
                    "Other": {},
                },
            }
        ]
    """
    for Source in minecraftChatLog:
        UpdatePlayerDeaths(Source["Embeds"]["Death"], messagesValidated)
        UpdatePlayerConnections(Source["Embeds"]["Connection"], messagesValidated)
        UpdatePlayerAchievement(Source["Embeds"]["Achievement"], messagesValidated)
        UpdatePlayerMessages(Source["Message"], messagesValidated)
        ValidateUsers()
