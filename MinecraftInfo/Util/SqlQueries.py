import sqlite3
import sys
from contextlib import closing
from datetime import datetime

from MinecraftInfo.Util.JsonQueries import GetDatabaseLocation
from MinecraftInfo.Util.Logging import LogError, LogInfo

DATABASE_LOCATION = GetDatabaseLocation()


def LinkCityUsers(player: str, cityName: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO UserCityLink('Name','City') VALUES (?,?)",
            (
                player,
                cityName,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def ClearClaimDatabase(cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute("DELETE FROM UserCityLink")
        cursor.execute("DELETE FROM NationCityLink")
        cursor.execute("DELETE FROM Cities")
        cursor.execute("DELETE FROM Nations")
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def LinkNationCity(nationName: str, cityName: str, cursor: object):
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO NationCityLink('Nation','City') VALUES (?,?)",
            (
                nationName,
                cityName,
            ),
        )
    except sqlite3.Error as error:
        LogInfo(
            str(error) + " - Claim most likely cannot be found. Error with dynmap.",
            __name__,
            sys._getframe().f_code.co_name,
        )


def AddNationClaim(
    nationName: str, nationLevel: str, nationCapital: str, cursor: object
) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO Nations('Name','Level','Capital') VALUES (?,?,?)",
            (
                nationName,
                nationLevel,
                nationCapital,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddCityClaim(
    cityName: str,
    cityLevel: str,
    cityChunks: int,
    XCoord: int,
    ZCoord: int,
    cursor: object,
) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO Cities('Name','Level','Chunks', 'Coord') VALUES (?,?,?,?)",
            (
                cityName,
                cityLevel,
                int(cityChunks),
                str(XCoord) + ", " + str(ZCoord),
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddUser(username: str, cursor: object) -> None:
    username = str(username)
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute("INSERT or IGNORE INTO Users('Name') VALUES (?)", (username,))
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddItem(item: str, cursor: object) -> None:
    item = str(item)
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute("INSERT or IGNORE INTO Items VALUES (?)", (item,))
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddRole(role: str, cursor: object) -> None:
    role = str(role)
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute("INSERT or IGNORE INTO Roles VALUES (?)", (role,))
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddRoleLink(username: str, role: str, cursor: object) -> None:
    username = str(username)
    role = str(role)
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO RoleLinks('User','Role') VALUES (?,?)",
            (
                username,
                role,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddDeath(
    messageID: int,
    deathMessage: str,
    usernameDead: str,
    timestamp: int,
    usernameKiller: str = None,
    itemUsed: str = None,
    cursor: object = None,
) -> None:
    messageID = int(messageID)
    deathMessage = str(deathMessage)
    usernameDead = str(usernameDead)
    usernameKiller = str(usernameKiller)
    itemUsed = str(itemUsed)
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO Deaths('Key','UserDead','UserKiller','ItemUsed','DeathMessage','Time') VALUES (?,?,?,?,?,?)",
            (
                messageID,
                usernameDead,
                usernameKiller,
                itemUsed,
                deathMessage,
                int(timestamp.timestamp() * 1000),
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddDeathMessage(deathMessage: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT INTO DeathMessages('DeathMessage') VALUES (?)",
            (deathMessage,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def GetDeathMessages(cursor: object) -> dict:
    DeathMessages = {}
    try:

        cursor.execute("pragma foreign_keys=ON")
        DeathsMessages = cursor.execute("SELECT * FROM DeathMessages")
        DeathMessages = {}
        for index, DeathMessage in enumerate(DeathsMessages):
            DeathMessages[index] = DeathMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        DeathMessages = {}
    finally:
        return DeathMessages


def GetAchievementMessages(cursor: object) -> dict:
    AchievementMessages = {}
    try:

        cursor.execute("pragma foreign_keys=ON")
        AchievementMessagesSQL = cursor.execute("SELECT * FROM AchievementEvents")
        for index, AchievementMessage in enumerate(AchievementMessagesSQL):
            AchievementMessages[index] = AchievementMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        return AchievementMessages


def GetConnectionMessages(cursor: object) -> dict:
    ConnectionMessages = {}
    try:

        cursor.execute("pragma foreign_keys=ON")
        ConnectionEventMessages = cursor.execute("SELECT * FROM ConnectionEvents")
        ConnectionMessages = {}
        for index, ConnectionMessage in enumerate(ConnectionEventMessages):
            ConnectionMessages[index] = ConnectionMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        ConnectionMessages = {}
    finally:
        return ConnectionMessages


def GetNicknameLinks(cursor: object) -> dict:
    try:

        cursor.execute("pragma foreign_keys=ON")
        NicknameLinks = cursor.execute("SELECT * FROM NicknameLinks")
        NicknameLinksDict = {}
        for index, NicknameLink in enumerate(NicknameLinks):
            NicknameLinksDict[index] = [NicknameLink[0], NicknameLink[1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        NicknameLinksDict = {}
    finally:
        return NicknameLinksDict


def UpdateUserLastSeen(user: str, timestamp: datetime, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "UPDATE Users SET LastSeenOnline = (?) WHERE Name = (?)",
            (
                int(timestamp.timestamp() * 1000),
                user,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def SetUserOffline(user: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "UPDATE Users SET LoginTime = 0 WHERE Name = (?)",
            (user,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def UpdateUserTotalPlayTime(user: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        LoginTimeSQL = cursor.execute(
            "SELECT LoginTime, LastSeenOnline FROM Users WHERE Name = (?) LIMIT 1",
            (user,),
        )
        LoginTime = 0
        LastSeenOnline = 0
        for i in LoginTimeSQL:
            LoginTime, LastSeenOnline = i[0], i[1]

        if LoginTime != 0:
            PlayTime = LastSeenOnline - LoginTime
            if PlayTime >= 3600000:  # One HR
                PlayTime = 0
        else:
            PlayTime = 0

        TotalPlayTimeSQL = cursor.execute(
            "SELECT TotalPlayTime FROM Users WHERE Name = (?) LIMIT 1",
            (user,),
        )
        TotalPlayTime = 0
        for i in TotalPlayTimeSQL:
            TotalPlayTime = i[0]
        TotalPlayTime += PlayTime
        cursor.execute(
            "UPDATE Users SET TotalPlayTime = (?) WHERE Name = (?)",
            (
                int(TotalPlayTime),
                user,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    SetUserOffline(user)


def GetOnlinePlayers(cursor: object) -> list:
    OnlinePlayers = []
    try:

        cursor.execute("pragma foreign_keys=ON")
        OnlinePlayersSQL = cursor.execute(
            "SELECT Name FROM Users WHERE NOT LoginTime = 0",
        )
        for Account in OnlinePlayersSQL:
            OnlinePlayers.append(Account[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)

        return OnlinePlayers


def GetOnlineStatus(user: str, cursor: object) -> None:
    OnlineStatus = False
    try:

        cursor.execute("pragma foreign_keys=ON")
        OnlineStatusSQL = cursor.execute(
            "SELECT LoginTime FROM Users WHERE Name = (?) LIMIT 1",
            (user,),
        )
        for i in OnlineStatusSQL:
            Online = i[0]
        if int(Online):
            OnlineStatus = True
        else:
            OnlineStatus = False
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)

        return OnlineStatus


def UpdateLoginTime(user: str, timestamp: datetime, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        if not GetOnlineStatus(user):
            cursor.execute(
                "UPDATE Users SET LoginTime = (?) WHERE Name = (?)",
                (
                    int(timestamp.timestamp() * 1000),
                    user,
                ),
            )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def UpdateUsername(oldUsername: str, newUsername: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "UPDATE Users SET Name = (?) WHERE Name = (?)",
            (newUsername, oldUsername),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddNickname(username: str, nickname: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO NicknameLinks('Name','Nickname') VALUES (?,?)",
            (
                username,
                nickname,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddCurrentNickname(username: str, nickname: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "UPDATE Users SET CurrentNickname = (?) WHERE Name = (?)",
            (
                username,
                nickname,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddCurrentRole(username: str, role: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "UPDATE Users SET CurrentRole = (?) WHERE Name = (?)",
            (
                username,
                role,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def LogUnknownEvent(unknownEvent: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO UnknownEvents('EventMessage') VALUES (?)",
            (unknownEvent,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def GetExistingNicknameLink(nickname: str, cursor: object) -> str:
    Link = None
    try:

        cursor.execute("pragma foreign_keys=ON")

        NicknameLink = cursor.execute(
            "SELECT * FROM NicknameLinks WHERE Nickname = (?) LIMIT 1",
            (nickname,),
        )
        Link = None
        for Account in NicknameLink:
            Link = Account[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        Link = None
    finally:
        return Link


def GetMessageReviewedIDs(cursor: object) -> list:
    MessageIDs = []
    try:

        MessageIDsSQL = cursor.execute(
            "SELECT * FROM MessagesReviewed",
        )
        for IDs in MessageIDsSQL:
            MessageIDs.append(IDs[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)

        return MessageIDs


def InsertMessageReviewedIDs(messageIDs: list, cursor: object) -> None:
    try:

        Messages = [(s,) for s in messageIDs]
        cursor.executemany(
            "INSERT INTO MessagesReviewed('MessageID') VALUES (?)", Messages
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def InsertMessageReviewedID(messageID: int, cursor: object) -> None:
    try:

        cursor.execute(
            "INSERT or IGNORE INTO MessagesReviewed('MessageID') VALUES (?)",
            (messageID,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def DeleteMessageReviewedID(messageID: int, cursor: object) -> None:
    try:
        messageID = int(messageID)
    except:
        messageID = 0
    try:

        cursor.execute(
            "DELETE FROM MessagesReviewed WHERE MessageID = (?)",
            (messageID,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddAchievement(achievement: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO Achievements('Achievement') VALUES (?)",
            (achievement,),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def AddAchievementLink(username: str, achievement: str, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        cursor.execute(
            "INSERT or IGNORE INTO AchievementLinks('User','Achievement') VALUES (?,?)",
            (
                username,
                achievement,
            ),
        )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)


def UpdateUserMessageCount(user: str, messageCount: int, cursor: object) -> None:
    try:

        cursor.execute("pragma foreign_keys=ON")
        MessagesSentSQL = cursor.execute(
            "SELECT MessagesSent FROM Users WHERE Name = (?) LIMIT 1",
            (user,),
        )
        MessagesSent = 0
        for i in MessagesSentSQL:
            MessagesSent = int(i[0])
        MessagesSent += messageCount
        cursor.execute(
            "UPDATE Users SET MessagesSent = (?) WHERE Name = (?)",
            (
                MessagesSent,
                user,
            ),
        )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
