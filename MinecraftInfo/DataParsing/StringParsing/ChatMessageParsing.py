import json
import re
import sys
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
from MinecraftInfo.Util.Logging import LogError
from MinecraftInfo.Util.SqlQueries import UpdateUserMessageCount


def UpdatePlayerMessages(
    playerMessages: json, messagesValidated, nameParser, sqlQueryHandler
) -> None:
    """Provided list of all player chat messages, extract relevant info and log it.

    Args:
        playerMessages (json): {ID:Message}
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    MessageCount = {}
    playerMessagesList = list(playerMessages.keys())
    playerMessagesList_int = map(int, playerMessagesList)
    playerMessagesList_str_sorted = map(str, sorted(playerMessagesList_int))

    for MessageIndex in playerMessagesList_str_sorted:
        Message = playerMessages[MessageIndex]
        Username, MessageText = GetMessage(Message)
        Username = Username.replace("\_", "_")
        User = nameParser(Username)
        if User not in MessageCount:
            MessageCount[User] = 0
        MessageCount[User] += 1
        messagesValidated.MessageReviewed(MessageIndex)

    for User in MessageCount:
        sqlQueryHandler.QueueQuery(UpdateUserMessageCount, User, MessageCount[User])


def GetMessage(message: json) -> tuple:
    TypeStringRegex = "(.*) » (.*)"
    match = re.search(TypeStringRegex, message)
    try:
        Username = match.group(1)
        MessageText = match.group(2)
    except:
        LogError(message, __name__, sys._getframe().f_code.co_name)
    return Username, MessageText
