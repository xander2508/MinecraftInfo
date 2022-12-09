import sqlite3
import sys
from MinecraftInfo.Util.JsonQueries import (
    GetDatabaseBackupLocation,
    GetDatabaseLocation,
)
from contextlib import closing
from datetime import datetime

from MinecraftInfo.Util.Logging import LogError, LogInfo


DATABASE_LOCATION = GetDatabaseLocation()
DATABASE_BACKUP_LOCATION = GetDatabaseBackupLocation()


def BackupDatabase() -> None:
    try:
        sqliteConnection = sqlite3.connect(DATABASE_LOCATION, timeout=20)
        with closing(sqliteConnection.cursor()) as cursor:
            cursor.execute()
            BackupDatabaseConnection = sqlite3.connect(
                DATABASE_BACKUP_LOCATION, timeout=5
            )
            cursor.backup(BackupDatabaseConnection)
            BackupDatabaseConnection.close()
    except sqlite3.Error as error:
        LogError(error, __name__, sys._getframe().f_code.co_name)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            BackupDatabaseConnection.close()
