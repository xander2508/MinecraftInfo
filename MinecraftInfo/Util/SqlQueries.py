import sqlite3
import sys
from MinecraftInfo.Util.JsonQueries import GetDatabaseLocation
from contextlib import closing
from datetime import datetime

from MinecraftInfo.Util.Logging import LogError


DATABASE_LOCATION = GetDatabaseLocation()


def GetAllUsers() -> list:
    Users = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Users = []
            cursor.execute("SELECT Name FROM Users")
            rows = cursor.fetchall()
            for i in rows:
                Users.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Users


def GetAllItems() -> list:
    Items = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Items = []
            cursor.execute("SELECT Name FROM Items")
            rows = cursor.fetchall()
            for i in rows:
                Items.append(i[0].strip("[").strip("]"))
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Items


def GetAllAchievements() -> list:
    Achievements = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Achievements = []
            cursor.execute("SELECT Achievement FROM Achievements")
            rows = cursor.fetchall()
            for i in rows:
                Achievements.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Achievements


def GetAllRoles() -> list:
    Roles = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Roles = []
            cursor.execute("SELECT Role FROM Roles")
            rows = cursor.fetchall()
            for i in rows:
                Roles.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Roles


def GetTopUserMessagesCount() -> list:
    MessagesSent = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name,MAX(MessagesSent) FROM Users")
            rows = cursor.fetchall()
            MessagesSent = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return MessagesSent


def GetTopUserTotalPlayTime() -> list:
    Playtime = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name,MAX(TotalPlayTime) FROM Users")
            rows = cursor.fetchall()
            Playtime = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Playtime


def GetTopUserKiller() -> list:
    Kills = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT UserKiller,COUNT(UserKiller) FROM Deaths GROUP BY UserKiller ORDER BY COUNT(UserKiller) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Kills = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Kills


def GetTopUserDeaths() -> list:
    Deaths = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT UserDead,COUNT(UserDead) FROM Deaths GROUP BY UserDead ORDER BY COUNT(UserDead) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Deaths = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Deaths


def GetTopUserAchievementCount() -> list:
    TopUserAchievement = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT User,COUNT(User) FROM AchievementLinks GROUP BY User ORDER BY COUNT(User) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            TopUserAchievement = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return TopUserAchievement


def GetTopAchievementCount() -> list:
    TopAchievement = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Achievement ,COUNT(Achievement) FROM AchievementLinks GROUP BY Achievement ORDER BY COUNT(Achievement) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            TopAchievement = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return TopAchievement


def GetTopUserRole() -> list:
    Role = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Role,COUNT(Role) FROM RoleLinks WHERE NOT Role='None' GROUP BY Role ORDER BY COUNT(Role) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Role = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Role


def GetTopItem() -> list:
    Item = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT ItemUsed,COUNT(ItemUsed) FROM Deaths GROUP BY ItemUsed ORDER BY COUNT(ItemUsed) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Item = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Item


def GetUsername(username: str) -> str:
    User = ""
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name FROM Users WHERE Name=(?) LIMIT 1", (username,))
            rows = cursor.fetchall()
            User = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if User == "":
            return False
        else:
            return User


def GetUserMessageCount(user: str) -> int:
    MessagesSent = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT MessagesSent FROM Users WHERE Name = (?) LIMIT 1", (user,)
            )
            rows = cursor.fetchall()
            MessagesSent = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return MessagesSent


def GetUserTotalPlayTime(user: str):
    Playtime = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT TotalPlayTime FROM Users WHERE Name = (?) LIMIT 1", (user,)
            )
            rows = cursor.fetchall()
            Playtime = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Playtime


def GetUserCurrentPlayTime(user: str) -> tuple:
    LoginTime = 0
    LastSeenOnline = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT LoginTime,LastSeenOnline FROM Users WHERE Name = (?) LIMIT 1",
                (user,),
            )
            rows = cursor.fetchall()
            LoginTime, LastSeenOnline = int(rows[0][0]), int(rows[0][1])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return LoginTime, LastSeenOnline


def GetUserMurderCount(user: str) -> int:
    Kills = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT COUNT(UserKiller) FROM Deaths WHERE UserKiller = (?) LIMIT 1",
                (user,),
            )
            rows = cursor.fetchall()
            Kills = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Kills


def GetUserDeathCount(user: str) -> str:
    Deaths = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT COUNT(UserDead) FROM Deaths WHERE UserDead= (?) LIMIT 1",
                (user,),
            )
            rows = cursor.fetchall()
            Deaths = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Deaths


def GetUserRole(user: str) -> str:
    Role = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Role FROM RoleLinks WHERE User=(?) LIMIT 1", (user,))
            rows = cursor.fetchall()
            Role = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Role


def GetUserNickname(user: str) -> str:
    Nickname = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nickname FROM NicknameLinks WHERE Name=(?) LIMIT 1", (user,)
            )
            rows = cursor.fetchall()
            Nickname = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nickname


def GetUserAchievementCount(user: str) -> dict:
    Achievement = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT COUNT(User) FROM AchievementLinks WHERE User=(?)", (user,)
            )
            rows = cursor.fetchall()
            Achievement = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Achievement


def GetUserMurderList(user: str) -> dict:
    KillList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT UserDead, ItemUsed FROM Deaths WHERE UserKiller = (?)", (user,)
            )
            rows = cursor.fetchall()
            KillList = []
            for i in rows:
                KillList.append(
                    [
                        "<a href=/player?search=" + i[0] + ">" + i[0] + "</a>",
                        "<a href=/item?search="
                        + i[1].strip("[").strip("]").replace(" ", "+")
                        + ">"
                        + i[1].strip("[").strip("]")
                        + "</a>",
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return KillList


def GetUserDeathList(user: str) -> dict:
    DeathList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT UserKiller, ItemUsed FROM Deaths WHERE UserDead = (?)", (user,)
            )
            rows = cursor.fetchall()
            DeathList = []
            for i in rows:
                DeathList.append(
                    [
                        "<a href=/player?search=" + i[0] + ">" + i[0] + "</a>",
                        "<a href=/item?search="
                        + i[1].strip("[").strip("]").replace(" ", "+")
                        + ">"
                        + i[1].strip("[").strip("]")
                        + "</a>",
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return DeathList


def GetUserAchievementList(user: str) -> dict:
    AchievementList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Achievement FROM AchievementLinks WHERE User=(?)", (user,)
            )
            rows = cursor.fetchall()
            AchievementList = []
            for i in rows:
                AchievementList.append(
                    [
                        "<a href=/achievement?search="
                        + i[0].replace(" ", "+")
                        + ">"
                        + i[0]
                        + "</a>"
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return AchievementList


def GetItem(itemInput: str) -> str:
    Item = ""
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Name FROM Items WHERE Name=(?) LIMIT 1", (itemInput,)
            )
            rows = cursor.fetchall()
            Item = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if Item == "":
            return False
        else:
            return Item


def GetItemMurderList(item: str) -> list:
    KillList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT UserKiller,UserDead FROM Deaths WHERE ItemUsed = (?)", (item,)
            )
            rows = cursor.fetchall()
            for i in rows:
                KillList.append(
                    [
                        "<a href=/player?search=" + i[0] + ">" + i[0] + "</a>",
                        "<a href=/player?search=" + i[1] + ">" + i[1] + "</a>",
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return KillList


def GetAchievementList(achievement: str) -> list:
    AchievementList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT User FROM AchievementLinks WHERE Achievement=(?)",
                (achievement,),
            )
            rows = cursor.fetchall()
            for i in rows:
                AchievementList.append(
                    ["<a href=/player?search=" + i[0] + ">" + i[0] + "</a>"]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if AchievementList == []:
            return False
        else:
            return AchievementList


def GetRoleList(role: str) -> list:
    RoleList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT User FROM RoleLinks WHERE Role=(?)", (role,))
            rows = cursor.fetchall()
            for i in rows:
                RoleList.append(
                    ["<a href=/player?search=" + i[0] + ">" + i[0] + "</a>"]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if RoleList == []:
            return False
        else:
            return RoleList


def AddUser(username: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddItem(item: str) -> None:
    item = str(item)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute("INSERT or IGNORE INTO Items VALUES (?)", (item,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddRole(role: str) -> None:
    role = str(role)
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute("INSERT or IGNORE INTO Roles VALUES (?)", (role,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddRoleLink(username: str, role: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
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
) -> None:
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
                    int(timestamp.timestamp() * 1000),
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddDeathMessage(deathMessage: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def GetDeathMessages() -> dict:
    DeathMessages = {}
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            DeathsMessages = cursor.execute("SELECT * FROM DeathMessages")
            DeathMessages = {}
            for index, DeathMessage in enumerate(DeathsMessages):
                DeathMessages[index] = DeathMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        DeathMessages = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return DeathMessages


def GetAchievementMessages() -> dict:
    AchievementMessages = {}
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            AchievementMessagesSQL = cursor.execute("SELECT * FROM AchievementEvents")
            for index, AchievementMessage in enumerate(AchievementMessagesSQL):
                AchievementMessages[index] = AchievementMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return AchievementMessages


def GetConnectionMessages() -> dict:
    ConnectionMessages = {}
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            ConnectionEventMessages = cursor.execute("SELECT * FROM ConnectionEvents")
            ConnectionMessages = {}
            for index, ConnectionMessage in enumerate(ConnectionEventMessages):
                ConnectionMessages[index] = ConnectionMessage[0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        ConnectionMessages = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return ConnectionMessages


def GetNicknameLinks() -> dict:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            NicknameLinks = cursor.execute("SELECT * FROM NicknameLinks")
            NicknameLinksDict = {}
            for index, NicknameLink in enumerate(NicknameLinks):
                NicknameLinksDict[index] = [NicknameLink[0], NicknameLink[1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
        NicknameLinksDict = {}
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return NicknameLinksDict


def UpdateUserLastSeen(user: str, timestamp: datetime) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def SetUserOffline(user: str) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET LoginTime = 0 WHERE Name = (?)",
                (user,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUserTotalPlayTime(user: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    SetUserOffline(user)


def GetOnlinePlayers() -> list:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return OnlinePlayers


def GetOnlineStatus(user: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return OnlineStatus


def UpdateLoginTime(user: str, timestamp: datetime) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUsername(oldUsername: str, newUsername: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddNickname(username: str, nickname: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def LogUnknownEvent(unknownEvent: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def GetExistingNicknameLink(nickname: str) -> str:
    Link = None
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
        Link = None
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Link


def GetMessageReviewedIDs() -> list:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

        return MessageIDs


def InsertMessageReviewedIDs(messageIDs: list) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Messages = [(s,) for s in messageIDs]
            cursor.executemany(
                "INSERT INTO MessagesReviewed('MessageID') VALUES (?)", Messages
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def InsertMessageReviewedID(messageID: int) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "INSERT or IGNORE INTO MessagesReviewed('MessageID') VALUES (?)",
                (messageID,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def DeleteMessageReviewedID(messageID: int) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM MessagesReviewed WHERE MessageID = (?)",
                (messageID,),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddAchievement(achievement: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddAchievementLink(username: str, achievement: str) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def UpdateUserMessageCount(user: str, messageCount: int) -> None:
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
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
