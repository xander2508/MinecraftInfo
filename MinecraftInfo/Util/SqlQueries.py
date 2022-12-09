import sqlite3
import sys
from MinecraftInfo.Util.JsonQueries import GetDatabaseLocation
from contextlib import closing
from datetime import datetime

from MinecraftInfo.Util.Logging import LogError, LogInfo


DATABASE_LOCATION = GetDatabaseLocation()


def Top50LargestNationByUsers() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City GROUP BY Nation ORDER BY COUNT(UserCityLink.Name) DESC LIMIT 50"
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
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
                "SELECT COUNT(UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City WHERE Nation = (?) GROUP BY Nation",
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
                NationChunks = str(i[0])

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


def Top50LargestClaimByUsers() -> list:
    Claims = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetClaimInfo(claim: str) -> tuple:
    ClaimLevel, ClaimCoords, ClaimChunks, ClaimNation, UserList = "", "", "", "None", []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
                ClaimNation = i[0]

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


def GetLargestNationByClaims() -> list:
    Nation = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(City) FROM NationCityLink GROUP BY Nation ORDER BY COUNT(City) DESC LIMIT 1"
            )
            rows = cursor.fetchall()
            for i in rows:
                Nation = [
                    "<a href=/claim?search=" + str(i[0]) + ">" + i[0] + "</a>",
                    str(i[1]),
                ]

    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Nation


def GetLargestNationByUsers() -> list:
    Nation = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Nation, COUNT(UserCityLink.Name) FROM NationCityLink JOIN UserCityLink ON NationCityLink.City=UserCityLink.City GROUP BY Nation ORDER BY COUNT(UserCityLink.Name) DESC LIMIT 1"
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
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetAllNations() -> list:
    Nations = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetAllClaims() -> list:
    Claims = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetClaimNation(claim: str) -> list:
    Nation = "None"
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetUserClaimList(user: str) -> list:
    Claims = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetUserNicknameList(user: str) -> list:
    Nicknames = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetUserRoleList(user: str) -> list:
    Roles = [""]
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            Roles = []
            cursor.execute("SELECT Role FROM RoleLinks WHERE User=(?)", (user,))
            rows = cursor.fetchall()
            for i in rows:
                Roles.append(
                    ["<a href=/role?search=" + str(i[0]) + ">" + i[0] + "</a>"]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Roles


def GetTop50Roles():
    Roles = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "SELECT Role,COUNT(Role) FROM RoleLinks WHERE NOT Role = 'None' GROUP BY Role ORDER BY COUNT(Role) DESC LIMIT 50"
            )
            rows = cursor.fetchall()
            for index, i in enumerate(rows):
                Roles.append(
                    [
                        str(index + 1),
                        "<a href=/role?search=" + str(i[0]) + ">" + i[0] + "</a>",
                        str(i[1]),
                    ]
                )
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return Roles


def GetTop50Achievement():
    Achievements = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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


def GetTop50Items():
    Items = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
                        "<a href=/item?search="
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


def GetTop50UserTotalPlayTime():
    PlaytimeList = []
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
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
            cursor.execute(
                "SELECT CurrentRole FROM Users WHERE User=(?) LIMIT 1", (user,)
            )
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


def LinkCityUsers(player: str, cityName: str) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO UserCityLink('Name','City') VALUES (?,?)",
                (
                    player,
                    cityName,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def ClearClaimDatabase() -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute("DELETE FROM UserCityLink")
            cursor.execute("DELETE FROM NationCityLink")
            cursor.execute("DELETE FROM Cities")
            cursor.execute("DELETE FROM Nations")
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def LinkNationCity(nationName: str, cityName: str):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO NationCityLink('Nation','City') VALUES (?,?)",
                (
                    nationName,
                    cityName,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogInfo(
            str(error) + " - Claim most likely cannot be found. Error with dynmap.",
            __name__,
            sys._getframe().f_code.co_name,
        )
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddNationClaim(nationName: str, nationLevel: str, nationCapital: str) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "INSERT or IGNORE INTO Nations('Name','Level','Capital') VALUES (?,?,?)",
                (
                    nationName,
                    nationLevel,
                    nationCapital,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddCityClaim(
    cityName: str, cityLevel: str, cityChunks: int, XCoord: int, ZCoord: int
) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
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
            sqliteConnection.commit()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


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


def AddCurrentNickname(username: str, nickname: str) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET CurrentNickname = (?) WHERE Name = (?)",
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


def AddCurrentRole(username: str, role: str) -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("pragma foreign_keys=ON")
            cursor.execute(
                "UPDATE Users SET CurrentRole = (?) WHERE Name = (?)",
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
        messageID = int(messageID)
    except:
        messageID = 0
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
