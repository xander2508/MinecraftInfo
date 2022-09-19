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
    UpdateUserLastOnline,
    UpdateUserOnline,
    UpdateUserPlayTime,
)
from MinecraftInfo.Util.FileOpener import LoadWebJsonFile
from datetime import datetime, timezone


def UpdatePlayerConnections(ConnectionMessages: json, messagesValidated):
    for ConnectionMessageIndex in ConnectionMessages:
        ConnectionMessage = ConnectionMessages[ConnectionMessageIndex][0]
        FinalConnectionMessage, ConnectionEventMatch = GetConnectionEvent(
            ConnectionMessage
        )
        if FinalConnectionMessage == None:
            LogUnknownEvent(ConnectionMessage)
        else:
            LogConnectionMessageEvent(
                int(ConnectionMessageIndex),
                FinalConnectionMessage,
                ConnectionEventMatch,
                ConnectionMessages[ConnectionMessageIndex][1],
            )
        messagesValidated.MessageReviewed(ConnectionMessageIndex)
    UpdatePlayersOnlineFromMap()


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
    timestamp: str,
):
    Timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    NameParser = NameParsing()
    Username = connectionEventMatch.group(1)
    User = NameParser(Username)
    if "joined" in finalConnectionMessage.strip(Username):
        if not GetOnlineStatus(User):
            UpdateUserOnline(User, True)
            UpdateUserLastOnline(User, Timestamp)
    elif "left" in finalConnectionMessage.strip(Username):
        if GetOnlineStatus(User):
            UpdateUserOnline(User, False)
            UpdateUserPlayTime(User, Timestamp)
            UpdateUserLastOnline(User, Timestamp)

    OnlinePlayers = GetOnlinePlayers()
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    OfflinePlayers = []
    OnlinePlayersMisssed = []
    for i in OnlinePlayers:
        OnlinePlayersMisssed.append(i)
    for player in UsernameJson["players"]:
        if player["account"] not in OnlinePlayers:
            try:
                OfflinePlayers.append(player["account"])
            except:
                pass
            try:
                OnlinePlayersMisssed.pop(player["account"])
            except:
                pass

    for i in OfflinePlayers:
        UpdateUserOnline(i, False)
        UpdateUserLastOnline(i, Timestamp)
    for i in OnlinePlayersMisssed:
        UpdateUserOnline(i, True)
        UpdateUserLastOnline(i, Timestamp)


def UpdatePlayersOnlineFromMap():
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    for player in UsernameJson["players"]:
        AddUser(player["account"])
        AddNickname(player["account"], player["name"])
        UpdateUserOnline(player["account"], True)
        UpdateUserLastOnline(
            player["account"], int(datetime.now(timezone.utc).timestamp() * 1000)
        )
