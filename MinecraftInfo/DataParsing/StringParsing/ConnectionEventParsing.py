import json
import re
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
from MinecraftInfo.DataStorage.JsonQueries import GetUsernameUrl
from MinecraftInfo.DataStorage.SqlQueries import (
    AddNickname,
    AddUser,
    GetConnectionMessages,
    GetOnlinePlayers,
    GetOnlineStatus,
    LogUnknownEvent,
    UpdateLoginTime,
    UpdateUserLastSeen,
    UpdateUserTotalPlayTime,
)
from MinecraftInfo.Util.FileOpener import LoadWebJsonFile
from datetime import datetime, timezone


def UpdatePlayerConnections(connectionMessages: json, messagesValidated,NameParser, SqlQueryHandler):
    """Provided list of player connection events, extract relevant info from the message and log it.
    Args:
        connectionMessages (json): Player connection events {ID:[Message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    connectionMessagesList = list(connectionMessages.keys())
    connectionMessagesList_int = map(int, connectionMessagesList)
    connectionMessagesList_str_sorted =  map(str,sorted(connectionMessagesList_int))

    for ConnectionMessageIndex in connectionMessagesList_str_sorted:
        ConnectionMessage = connectionMessages[ConnectionMessageIndex][0]
        FinalConnectionMessage, ConnectionEventMatch = GetConnectionEvent(
            ConnectionMessage
        )
        if FinalConnectionMessage == None:
            SqlQueryHandler.QueueQuery(LogUnknownEvent,ConnectionMessage)
        else:
            LogConnectionMessageEvent(
                int(ConnectionMessageIndex),
                FinalConnectionMessage,
                ConnectionEventMatch,
                connectionMessages[ConnectionMessageIndex][1],
                NameParser,
                SqlQueryHandler,
            )
        messagesValidated.MessageReviewed(ConnectionMessageIndex)
    UpdatePlayersOnlineFromMap(SqlQueryHandler)


def GetConnectionEvent(ConnectionMessage: str):
    FinalConnectionMessage = None
    ConnectionEventMatch = None
    ConnectionEventMatchCount = 0
    ConnectionEventDict = GetConnectionMessages()
    for ConnectionEventIndex in ConnectionEventDict:
        ConnectionEventString = ConnectionEventDict[ConnectionEventIndex]
        ConnectionEventRegex = ConnectionEventString
        ConnectionEventRegex = ConnectionEventRegex.replace("<player>", "(.*)")
        if match := re.search(ConnectionEventRegex, ConnectionMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > ConnectionEventMatchCount:
                ConnectionEventMatchCount = numberOfMatches
                FinalConnectionMessage = ConnectionMessage
                ConnectionEventMatch = match

    return FinalConnectionMessage, ConnectionEventMatch


def LogConnectionMessageEvent(
    connectionMessageIndex: int,
    finalConnectionMessage: str,
    connectionEventMatch: re.match,
    Timestamp: str,
    NameParser: callable,
    SqlQueryHandler,
):
    # datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    Username = connectionEventMatch.group(1)
    User = NameParser(Username)
    if "joined" in finalConnectionMessage.strip(Username):
        if not GetOnlineStatus(User):
            SqlQueryHandler.QueueQuery(UpdateLoginTime,User, Timestamp)
            SqlQueryHandler.QueueQuery(UpdateUserLastSeen,User, Timestamp)
    elif "left" in finalConnectionMessage.strip(Username):
        if GetOnlineStatus(User):
            SqlQueryHandler.QueueQuery(UpdateUserLastSeen,User, Timestamp)
            SqlQueryHandler.QueueQuery(UpdateUserTotalPlayTime,User)



def UpdatePlayersOnlineFromMap(SqlQueryHandler):
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    for player in UsernameJson["players"]:
        SqlQueryHandler.QueueQuery(AddUser,player["account"])
        SqlQueryHandler.QueueQuery(AddNickname,player["account"], player["name"])
        SqlQueryHandler.QueueQuery(UpdateLoginTime,player["account"], datetime.now(timezone.utc))
        SqlQueryHandler.QueueQuery(UpdateUserLastSeen,player["account"], datetime.now(timezone.utc))

    OnlinePlayers = GetOnlinePlayers()
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    OfflinePlayers = []
    for player in UsernameJson["players"]:
        if player["account"] not in OnlinePlayers:
            try:
                OfflinePlayers.append(player["account"])
            except:
                pass

    for i in OfflinePlayers:
        SqlQueryHandler.QueueQuery(UpdateUserTotalPlayTime,i)
