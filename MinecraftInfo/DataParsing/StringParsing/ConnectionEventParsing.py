import json
import re
from MinecraftInfo.DataParsing.StringParsing.NameParsing import NameParsing
from MinecraftInfo.Util.JsonQueries import GetUsernameUrl
from MinecraftInfo.Util.SqlQueries import (
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


def UpdatePlayerConnections(
    connectionMessages: json, messagesValidated, nameParser, sqlQueryHandler
) -> None:
    """Provided list of player connection events, extract relevant info from the message and log it.
    Args:
        connectionMessages (json): Player connection events {ID:[Message,Time]}.
        messagesValidated (_type_): Object to track the messages already reviewed.
    """
    connectionMessagesList = list(connectionMessages.keys())
    connectionMessagesList_int = map(int, connectionMessagesList)
    connectionMessagesList_str_sorted = map(str, sorted(connectionMessagesList_int))

    for ConnectionMessageIndex in connectionMessagesList_str_sorted:
        ConnectionMessage = connectionMessages[ConnectionMessageIndex][0]
        FinalConnectionMessage, ConnectionEventMatch = GetConnectionEvent(
            ConnectionMessage
        )
        if FinalConnectionMessage == None:
            sqlQueryHandler.QueueQuery(LogUnknownEvent, ConnectionMessage)
        else:
            LogConnectionMessageEvent(
                int(ConnectionMessageIndex),
                FinalConnectionMessage,
                ConnectionEventMatch,
                connectionMessages[ConnectionMessageIndex][1],
                nameParser,
                sqlQueryHandler,
            )
        messagesValidated.MessageReviewed(ConnectionMessageIndex)
    UpdatePlayersOnlineFromMap(sqlQueryHandler)


def GetConnectionEvent(connectionMessage: str) -> tuple:
    FinalConnectionMessage = None
    ConnectionEventMatch = None
    ConnectionEventMatchCount = 0
    ConnectionEventDict = GetConnectionMessages()
    for ConnectionEventIndex in ConnectionEventDict:
        ConnectionEventString = ConnectionEventDict[ConnectionEventIndex]
        ConnectionEventRegex = ConnectionEventString
        ConnectionEventRegex = ConnectionEventRegex.replace("<player>", "(.*)")
        if match := re.search(ConnectionEventRegex, connectionMessage):
            numberOfMatches = len(match.groups())
            if numberOfMatches > ConnectionEventMatchCount:
                ConnectionEventMatchCount = numberOfMatches
                FinalConnectionMessage = connectionMessage
                ConnectionEventMatch = match

    return FinalConnectionMessage, ConnectionEventMatch


def LogConnectionMessageEvent(
    connectionMessageIndex: int,
    finalConnectionMessage: str,
    connectionEventMatch: re.match,
    timestamp: str,
    nameParser: callable,
    sqlQueryHandler,
) -> None:
    # datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    Username = connectionEventMatch.group(1)
    User = nameParser(Username)
    if "joined" in finalConnectionMessage.strip(Username):
        if not GetOnlineStatus(User):
            sqlQueryHandler.QueueQuery(UpdateLoginTime, User, timestamp)
            sqlQueryHandler.QueueQuery(UpdateUserLastSeen, User, timestamp)
    elif "left" in finalConnectionMessage.strip(Username):
        if GetOnlineStatus(User):
            sqlQueryHandler.QueueQuery(UpdateUserLastSeen, User, timestamp)
            sqlQueryHandler.QueueQuery(UpdateUserTotalPlayTime, User)


def UpdatePlayersOnlineFromMap(sqlQueryHandler) -> None:
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    for player in UsernameJson["players"]:
        sqlQueryHandler.QueueQuery(AddUser, player["account"])
        sqlQueryHandler.QueueQuery(AddNickname, player["account"], player["name"])
        sqlQueryHandler.QueueQuery(
            UpdateLoginTime, player["account"], datetime.now(timezone.utc)
        )
        sqlQueryHandler.QueueQuery(
            UpdateUserLastSeen, player["account"], datetime.now(timezone.utc)
        )

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
        sqlQueryHandler.QueueQuery(UpdateUserTotalPlayTime, i)
