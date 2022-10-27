import json
import re

from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
from MinecraftInfo.DataStorage.SqlQueries import UpdateUserMessageCount


def UpdatePlayerMessages(playerMessages: json, messagesValidated,NameParser, SqlQueryHandler):
    """Provided list of all player chat messages, extract relevant info and log it.

    Args:
        playerMessages (json): {ID:Message}
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    MessageCount = {}
    for MessageIndex in playerMessages:
        Message = playerMessages[MessageIndex]
        Username, MessageText = GetMessage(Message)
        User = NameParser(Username)
        if User not in MessageCount:
            MessageCount[User] = 0
        MessageCount[User] += 1
        messagesValidated.MessageReviewed(MessageIndex)

    for User in MessageCount:
        SqlQueryHandler.QueueQuery(UpdateUserMessageCount,User, MessageCount[User])


def GetMessage(message: json):
    TypeStringRegex = "(.*) » (.*)"
    match = re.search(TypeStringRegex, message)
    Username = match.group(1)
    MessageText = match.group(2)
    return Username, MessageText
