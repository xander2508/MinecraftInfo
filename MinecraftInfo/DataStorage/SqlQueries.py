import sqlite3
from contextlib import closing
from datetime import datetime, timezone


DATABASE_LOCATION = "MinecraftInfo\DataStorage\DataStorage.db"


def AddUser(username: str):
    username = str(username)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO Users('Name') VALUES (?)", (username,)
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddItem(item: str):
    item = str(item)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute("INSERT or IGNORE INTO Items VALUES (?)", (item,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddRole(role: str):
    role = str(role)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute("INSERT or IGNORE INTO Roles VALUES (?)", (role,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddRoleLink(username: str, role: str):
    username = str(username)
    role = str(role)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO RoleLinks('User','Role') VALUES (?,?)",
                (
                    username,
                    role,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddDeath(
    messageID: int,
    deathMessage: str,
    usernameDead: str,
    timestamp: int,
    usernameKiller: str = None,
    itemUsed: str = None,
):
    messageID = int(messageID)
    deathMessage = str(deathMessage)
    usernameDead = str(usernameDead)
    usernameKiller = str(usernameKiller)
    itemUsed = str(itemUsed)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO Deaths('Key','UserDead','UserKiller','ItemUsed','DeathMessage','Time') VALUES (?,?,?,?,?,?)",
                (
                    messageID,
                    usernameDead,
                    usernameKiller,
                    itemUsed,
                    deathMessage,
                    int(
                        timestamp.timestamp() * 1000
                    ),
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddDeathMessage(deathMessage: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT INTO DeathMessages('DeathMessage') VALUES (?)",
                (deathMessage,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def GetDeathMessages():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            DeathsMessages = cursor.execute("SELECT * FROM DeathMessages")
            DeathMessages = {}
            for index, DeathMessage in enumerate(DeathsMessages):
                DeathMessages[index] = DeathMessage[0]
    except sqlite3.Error as error:
        print("Log", error)
        DeathMessages = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return DeathMessages


def GetAchievementMessages():
    AchievementMessages = {}
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            AchievementMessagesSQL = cursor.execute("SELECT * FROM AchievementEvents")
            for index, AchievementMessage in enumerate(AchievementMessagesSQL):
                AchievementMessages[index] = AchievementMessage[0]
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return AchievementMessages


def GetConnectionMessages():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            ConnectionEventMessages = cursor.execute("SELECT * FROM ConnectionEvents")
            ConnectionMessages = {}
            for index, ConnectionMessage in enumerate(ConnectionEventMessages):
                ConnectionMessages[index] = ConnectionMessage[0]
    except sqlite3.Error as error:
        print("Log", error)
        ConnectionMessages = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return ConnectionMessages


def GetNicknameLinks():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            NicknameLinks = cursor.execute("SELECT * FROM NicknameLinks")
            NicknameLinksDict = {}
            for index, NicknameLink in enumerate(NicknameLinks):
                NicknameLinksDict[index] = [NicknameLink[0], NicknameLink[1]]
    except sqlite3.Error as error:
        print("Log", error)
        NicknameLinksDict = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return NicknameLinksDict


def UpdateUserLastSeen(user: str, timestamp: datetime):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET LastSeenOnline = (?) WHERE Name = (?)",
                (
                    int(timestamp.timestamp() * 1000),
                    user,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def SetUserOffline(user: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET LoginTime = 0 WHERE Name = (?)",
                (
                    user,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUserTotalPlayTime(user: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
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
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    SetUserOffline(user)


def GetOnlinePlayers():
    OnlinePlayers = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            OnlinePlayersSQL = cursor.execute(
                "SELECT Name FROM Users WHERE NOT LoginTime = 0",
            )
            for Account in OnlinePlayersSQL:
                OnlinePlayers.append(Account[0])
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return OnlinePlayers


def GetOnlineStatus(user: str):
    OnlineStatus = False
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
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
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return OnlineStatus


def UpdateLoginTime(user: str, timestamp: datetime):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            if not GetOnlineStatus(user):
                cursor.execute(
                    "UPDATE Users SET LoginTime = (?) WHERE Name = (?)",
                    (
                        int(timestamp.timestamp() * 1000),
                        user,
                    ),
                )
                sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUsername(oldUsername: str, newUsername: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET Name = (?) WHERE Name = (?)",
                (newUsername, oldUsername),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddNickname(username: str, nickname: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO NicknameLinks('Name','Nickname') VALUES (?,?)",
                (
                    username,
                    nickname,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def LogUnknownEvent(unknownEvent: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO UnknownEvents('EventMessage') VALUES (?)",
                (unknownEvent,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def GetExistingNicknameLink(nickname: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")

            NicknameLink = cursor.execute(
                "SELECT * FROM NicknameLinks WHERE Nickname = (?) LIMIT 1",
                (nickname,),
            )
            Link = None
            for Account in NicknameLink:
                Link = Account[0]
    except sqlite3.Error as error:
        print("Log", error)
        Link = None
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Link


def GetMessageReviewedIDs():
    MessageIDs = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            MessageIDsSQL = cursor.execute(
                "SELECT * FROM MessagesReviewed",
            )
            for IDs in MessageIDsSQL:
                MessageIDs.append(IDs[0])
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return MessageIDs


def InsertMessageReviewedIDs(messageIDs: list):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Messages = [(s,) for s in messageIDs]
            cursor.executemany(
                "INSERT INTO MessagesReviewed('MessageID') VALUES (?)", Messages
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def InsertMessageReviewedID(messageID: int):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "INSERT or IGNORE INTO MessagesReviewed('MessageID') VALUES (?)",
                (messageID,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def DeleteMessageReviewedID(messageID: int):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM MessagesReviewed WHERE MessageID = (?)",
                (messageID,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddAchievement(achievement: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO Achievements('Achievement') VALUES (?)",
                (achievement,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddAchievementLink(username: str, achievement: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO AchievementLinks('User','Achievement') VALUES (?,?)",
                (
                    username,
                    achievement,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUserMessageCount(user: str, messageCount: int):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
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
            sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


if __name__ == "__main__":
    print(GetExistingNicknameLink("- uke_Tamato"))
    # AddItem("Fist")
    # AddUser("Dead")
    # AddUser("Killer")
    # AddDeath(1, 1, "Dead", "Killer", "Fist")
