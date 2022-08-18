import sqlite3
from contextlib import closing


def AddUsername(username: str):
    try:
        sqliteConnection = sqlite3.connect("MinecraftInfo\Configuration\DataStorage.db")
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("INSERT or IGNORE INTO Users VALUES (?)", (username,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddItem(item: str):
    try:
        sqliteConnection = sqlite3.connect("MinecraftInfo\Configuration\DataStorage.db")
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("INSERT or IGNORE INTO Items VALUES (?)", (item,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddNickname(nickname: str):
    try:
        sqliteConnection = sqlite3.connect("MinecraftInfo\Configuration\DataStorage.db")
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute("INSERT or IGNORE INTO Nicknames VALUES (?)", (nickname,))
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddNicknameLink(username: str, nickname: str):
    try:
        sqliteConnection = sqlite3.connect("MinecraftInfo\Configuration\DataStorage.db")
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute(
                "INSERT or IGNORE INTO NicknameLinks('Nickname','User') VALUES (?,?)",
                (
                    nickname,
                    username,
                ),
            )
            sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Log", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def AddDeath(UsernameDead: str, UsernameKiller: str = None, ItemUsed: str = None):
    pass


if __name__ == "__main__":
    AddUsername("Username")
    AddNickname("TestName")  # Not unique
    AddNicknameLink("sssss", "TestNamsssse")
