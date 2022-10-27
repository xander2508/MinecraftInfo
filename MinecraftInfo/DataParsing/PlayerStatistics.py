import threading

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
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing, ValidateUsers


def PlayerStatistics(minecraftChatLog: list, messagesValidated,SqlQueryHandler) -> None:
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
    NameParser = NameParsing(SqlQueryHandler)

    for Source in minecraftChatLog:
        UpdatePlayerDeathsThread = threading.Thread(
            target=UpdatePlayerDeaths,
            args=(
                Source["Embeds"]["Death"],
                messagesValidated,
                NameParser,
                SqlQueryHandler,
            ),
        )
        # UpdatePlayerDeaths(Source["Embeds"]["Death"], messagesValidated)
        UpdatePlayerConnectionsThread = threading.Thread(
            target=UpdatePlayerConnections,
            args=(
                Source["Embeds"]["Connection"],
                messagesValidated,
                NameParser,
                SqlQueryHandler,
            ),
        )
        # UpdatePlayerConnections(Source["Embeds"]["Connection"], messagesValidated)
        UpdatePlayerAchievementThread = threading.Thread(
            target=UpdatePlayerAchievement,
            args=(
                Source["Embeds"]["Achievement"],
                messagesValidated,
                NameParser,
                SqlQueryHandler,
            ),
        )
        # UpdatePlayerAchievement(Source["Embeds"]["Achievement"], messagesValidated)
        UpdatePlayerMessagesThread = threading.Thread(
            target=UpdatePlayerMessages,
            args=(
                Source["Message"],
                messagesValidated,
                NameParser,
                SqlQueryHandler,
            ),
        )
        # UpdatePlayerMessages(Source["Message"], messagesValidated)
        UpdatePlayerDeathsThread.start()
        UpdatePlayerConnectionsThread.start()
        UpdatePlayerAchievementThread.start()
        UpdatePlayerMessagesThread.start()
        UpdatePlayerDeathsThread.join()
        UpdatePlayerConnectionsThread.join()
        UpdatePlayerAchievementThread.join()
        UpdatePlayerMessagesThread.join()
    ValidateUsers(SqlQueryHandler)
