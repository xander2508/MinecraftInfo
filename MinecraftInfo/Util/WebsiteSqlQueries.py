import sqlite3
import sys
from contextlib import closing

from MinecraftInfo.Util.JsonQueries import (
    GetDatabaseBackupLocation,
    GetDatabaseLocation,
)
from MinecraftInfo.Util.Logging import LogError, LogInfo

import os

DATABASE_LOCATION = os.path.dirname(os.path.abspath(__file__)) + GetDatabaseLocation()
DATABASE_BACKUP_LOCATION = (
    os.path.dirname(os.path.abspath(__file__)) + GetDatabaseBackupLocation()
)


def BackupDatabase() -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION, timeout=20)
        BackupDatabaseConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        sqliteConnection.backup(BackupDatabaseConnection)
        sqliteConnection.close()
        BackupDatabaseConnection.close()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if BackupDatabaseConnection:
            BackupDatabaseConnection.close()


def Top50LargestNationByClaims() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(City) FROM NationCityLink GROUP BY Nation ORDER BY COUNT(City) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Nations.append(
                    [
                        str(index + 1),
                        "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nations


def Top50LargestNationByChunks() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, SUM(Cities.Chunks) FROM NationCityLink JOIN Cities ON NationCityLink.City=Cities.Name GROUP BY Nation ORDER BY SUM(Cities.Chunks) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Nations.append(
                    [
                        str(index + 1),
                        "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nations


def Top50LargestNationByUsers() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(DISTINCT UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City GROUP BY Nation ORDER BY COUNT(DISTINCT UserCityLink.Name) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Nations.append(
                    [
                        str(index + 1),
                        "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nations


def Top50LargestClaimByChunks() -> list:
    Claims = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Name, Chunks FROM Cities ORDER BY Chunks DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Claims.append(
                    [
                        str(index + 1),
                        "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claims


def Top50LargestClaimByUsers() -> list:
    Claims = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT City, COUNT(Name) FROM UserCityLink GROUP BY City ORDER BY COUNT(Name) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Claims.append(
                    [
                        str(index + 1),
                        "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claims


def GetUserClaimList(user: str) -> list:
    Claims = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Claims = []
            cursor.execute("SELECT City FROM UserCityLink WHERE Name=(?)", (user,))
            rows = cursor.fetchall()
            for i in rows:
                Claims.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claims


def GetUserTotalPlayTime(user: str):
    Playtime = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserRole(user: str) -> str:
    Role = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT CurrentRole FROM Users WHERE Name=(?) LIMIT 1", (user,)
            )
            rows = cursor.fetchall()
            Role = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Role


def GetUserNicknameList(user: str) -> list:
    Nicknames = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Nicknames = []
            cursor.execute("SELECT Nickname FROM NicknameLinks WHERE Name=(?)", (user,))
            rows = cursor.fetchall()
            for i in rows:
                Nicknames.append([i[0]])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nicknames


def GetUsername(username: str) -> str:
    User = ""
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserRoleList(user: str) -> list:
    Roles = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Roles = []
            cursor.execute("SELECT Role FROM RoleLinks WHERE User=(?)", (user,))
            rows = cursor.fetchall()
            for i in rows:
                Roles.append(
                    [
                        "<a href=/role?search="
                        + str(i[0]).replace(" ", "+")
                        + ">"
                        + str(i[0])
                        + "</a>"
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Roles


def GetUserMurderList(user: str) -> dict:
    KillList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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
                        "<a href=/weapon?search="
                        + str(i[1]).strip("[").strip("]").replace(" ", "+")
                        + ">"
                        + str(i[1]).strip("[").strip("]")
                        + "</a>",
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return KillList


def GetUserMurderCount(user: str) -> int:
    Kills = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserMessageCount(user: str) -> int:
    MessagesSent = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserDeathList(user: str) -> dict:
    DeathList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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
                        "<a href=/weapon?search="
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


def GetUserDeathCount(user: str) -> str:
    Deaths = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserCurrentPlayTime(user: str) -> tuple:
    LoginTime = 0
    LastSeenOnline = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserAchievementList(user: str) -> dict:
    AchievementList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetUserAchievementCount(user: str) -> dict:
    Achievement = 0
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetTopUserTotalPlayTime() -> list:
    Playtime = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetTopUserRole() -> list:
    Role = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT CurrentRole,COUNT(CurrentRole) FROM Users WHERE NOT CurrentRole='None' GROUP BY CurrentRole ORDER BY COUNT(CurrentRole) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Role = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Role


def GetTopUserMessagesCount() -> list:
    MessagesSent = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetTopUserKiller() -> list:
    Kills = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetTopItem() -> list:
    Item = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT ItemUsed,COUNT(ItemUsed) FROM Deaths WHERE NOT ItemUsed = 'None' GROUP BY ItemUsed ORDER BY COUNT(ItemUsed) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            Item = [rows[0][0], rows[0][1]]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Item


def GetTopAchievementCount() -> list:
    TopAchievement = ["", ""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetTop50UserTotalPlayTime():
    PlaytimeList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Users = []
            cursor.execute(
                "SELECT Name,TotalPlayTime FROM Users GROUP BY TotalPlayTime ORDER BY TotalPlayTime DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                PlaytimeList.append(
                    [
                        str(index + 1),
                        "<a href=/player?search=" + i[0] + ">" + i[0] + "</a>",
                        str(float("{:.2f}".format(i[1] / 3600000))) + " Hours",
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return PlaytimeList


def GetTop50Roles():
    Roles = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT CurrentRole,COUNT(CurrentRole) FROM Users WHERE NOT CurrentRole = 'None' GROUP BY CurrentRole ORDER BY COUNT(CurrentRole) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Roles.append(
                    [
                        str(index + 1),
                        "<a href=/role?search="
                        + str(i[0]).replace(" ", "+")
                        + ">"
                        + i[0]
                        + "</a>",
                        str(i[1]),
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Roles


def GetTop50Items():
    Items = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Users = []
            cursor.execute(
                "SELECT ItemUsed,COUNT(ItemUsed) FROM Deaths WHERE NOT ItemUsed = 'None' GROUP BY ItemUsed ORDER BY COUNT(ItemUsed) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Items.append(
                    [
                        str(index + 1),
                        "<a href=/weapon?search="
                        + str(i[0]).replace(" ", "+").strip("[").strip("]")
                        + ">"
                        + i[0].strip("[").strip("]")
                        + "</a>",
                        str(i[1]),
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Items


def GetTop50Achievement():
    Achievements = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            Users = []
            cursor.execute(
                "SELECT Achievement,COUNT(Achievement) FROM AchievementLinks GROUP BY Achievement ORDER BY COUNT(Achievement) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Achievements.append(
                    [
                        str(index + 1),
                        "<a href=/achievement?search="
                        + str(i[0].replace(" ", "+"))
                        + ">"
                        + i[0]
                        + "</a>",
                        str(i[1]),
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Achievements


def GetRoleList(role: str) -> list:
    RoleList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name FROM Users WHERE CurrentRole=(?)", (role,))
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


def GetNationCapital(nation: str) -> str:
    CapitalName = ""
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Capital FROM Nations WHERE Name = (?)", (nation,))
            rows = cursor.fetchall()
            for i in rows:
                CapitalName = i[0]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return CapitalName


def GetNationClaimList(nation: str) -> dict:
    ClaimList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT City FROM NationCityLink WHERE Nation = (?)",
                (nation,),
            )
            rows = cursor.fetchall()
            for i in rows:
                ClaimList.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return ClaimList


def GetNationInfo(nation: str) -> tuple:
    NationLevel, CaptialCoords, Captial, NationChunks, NationPlayers, NationClaims = (
        "",
        "",
        "",
        0,
        0,
        [],
    )
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Level FROM Nations WHERE Name = (?)", (nation,))
            rows = cursor.fetchall()
            for i in rows:
                NationLevel = i[0]

            cursor.execute("SELECT Capital FROM Nations WHERE Name = (?)", (nation,))
            rows = cursor.fetchall()
            for i in rows:
                CapitalName = i[0]
                Captial = "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>"

            cursor.execute("SELECT Coord FROM Cities WHERE Name = (?)", (CapitalName,))
            rows = cursor.fetchall()
            for i in rows:
                CaptialCoords = i[0]

            cursor.execute(
                "SELECT COUNT(DISTINCT UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City WHERE Nation = (?) GROUP BY Nation",
                (nation,),
            )
            rows = cursor.fetchall()
            for i in rows:
                NationPlayers = str(i[0])

            cursor.execute(
                "SELECT Nation, SUM(Cities.Chunks) FROM NationCityLink JOIN Cities ON NationCityLink.City=Cities.Name WHERE Nation = (?) GROUP BY Nation ORDER BY SUM(Cities.Chunks)",
                (nation,),
            )
            rows = cursor.fetchall()
            for i in rows:
                NationChunks = str(i[1])

            cursor.execute(
                "SELECT NationCityLink.City, (SELECT COUNT(UserCityLink.Name) FROM UserCityLink WHERE UserCityLink.City=NationCityLink.City) FROM NationCityLink WHERE Nation = (?) ORDER BY (SELECT COUNT(UserCityLink.Name) FROM UserCityLink WHERE UserCityLink.City=NationCityLink.City) DESC",
                (nation,),
            )
            rows = cursor.fetchall()
            for i in rows:
                NationClaims.append(
                    [
                        "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return (
            NationLevel,
            CaptialCoords,
            Captial,
            NationChunks,
            NationPlayers,
            NationClaims,
        )


def GetLargestNationByUsers() -> list:
    Nation = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(DISTINCT UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City GROUP BY Nation ORDER BY COUNT(DISTINCT UserCityLink.Name) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Nation = [
                    "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nation


def GetLargestNationByClaims() -> list:
    Nation = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(City) FROM NationCityLink GROUP BY Nation ORDER BY COUNT(City) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Nation = [
                    "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nation


def GetLargestNationByChunks() -> list:
    Nation = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, SUM(Cities.Chunks) FROM NationCityLink JOIN Cities ON NationCityLink.City=Cities.Name GROUP BY Nation ORDER BY SUM(Cities.Chunks) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Nation = [
                    "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nation


def GetLargestClaimByUsers() -> list:
    Claim = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT City,COUNT(Name) FROM UserCityLink GROUP BY City ORDER BY COUNT(Name) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Claim = [
                    "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claim


def GetLargestClaimByChunks() -> list:
    Claim = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Name, Chunks FROM Cities ORDER BY Chunks DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Claim = [
                    "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claim


def GetItemMurderList(item: str) -> list:
    KillList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetItem(itemInput: str) -> str:
    Item = ""
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetClaimNation(claim: str) -> list:
    Nation = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation FROM NationCityLink WHERE City=(?) LIMIT 1", (claim,)
            )
            rows = cursor.fetchall()
            for i in rows:
                Nation = "<a href=/nation?search=" + str(i[0]) + ">" + i[0] + "</a>"
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nation


def GetClaimInfo(claim: str) -> tuple:
    ClaimLevel, ClaimCoords, ClaimChunks, ClaimNation, UserList = "", "", "", "None", []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Level, Coord, Chunks FROM Cities WHERE Name = (?)", (claim,)
            )
            rows = cursor.fetchall()
            for i in rows:
                ClaimLevel, ClaimCoords, ClaimChunks = i[0], i[1], i[2]

            cursor.execute(
                "SELECT Nation FROM NationCityLink WHERE City = (?)", (claim,)
            )
            rows = cursor.fetchall()
            for i in rows:
                ClaimNation = "<a href=/nation?search=" + i[0] + ">" + i[0] + "</a>"

            cursor.execute("SELECT Name FROM UserCityLink WHERE City = (?)", (claim,))
            rows = cursor.fetchall()
            for i in rows:
                UserList.append(
                    ["<a href=/player?search=" + i[0] + ">" + i[0] + "</a>"]
                )

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return ClaimLevel, ClaimCoords, ClaimChunks, ClaimNation, UserList


def GetAllUsers() -> list:
    Users = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetAllRoles() -> list:
    Roles = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetAllNations() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name FROM Nations")
            rows = cursor.fetchall()
            for i in rows:
                Nations.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nations


def GetAllItems() -> list:
    Items = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetAllClaims() -> list:
    Claims = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("SELECT Name FROM Cities")
            rows = cursor.fetchall()
            for i in rows:
                Claims.append(i[0])
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Claims


def GetAllAchievements() -> list:
    Achievements = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
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


def GetAchievementList(achievement: str) -> list:
    AchievementList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT User FROM AchievementLinks WHERE Achievement=(?)",
                (achievement,),
            )
            rows = cursor.fetchall()
            for i in rows:
                AchievementList.append(
                    [
                        "<a href=/player?search="
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
        if AchievementList == []:
            return False
        else:
            return AchievementList


def GetUserNickname(user: str) -> str:
    Nickname = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_BACKUP_LOCATION, timeout=5)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT CurrentNickname FROM Users WHERE Name=(?) LIMIT 1", (user,)
            )
            rows = cursor.fetchall()
            Nickname = rows[0][0]
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nickname
