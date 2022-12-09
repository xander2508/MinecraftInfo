from collections import deque
from contextlib import closing
import sqlite3
import sys
import time
from typing import Callable
import threading
from MinecraftInfo.Util.JsonQueries import GetDatabaseLocation

DATABASE_LOCATION = GetDatabaseLocation()


class SqlQueryHandler:
    def __init__(self) -> None:
        self.SqlQueryQueue = deque()
        self.Quit = False
        self.Timeout = 0
        self.QueueHandlerThread = threading.Thread(
            target=self.QueueHandler,
        )
        self.QueueHandlerThread.start()

    def QueueQuery(self, queryFunction: Callable, *args: list) -> None:
        self.SqlQueryQueue.append([queryFunction, args])

    def DeQueueQuery(self, cursor: object) -> None:
        Query = self.SqlQueryQueue.popleft()
        Query[0](*(Query[1]), cursor)

    def QueueHandler(self) -> None:
        while True:
            if self.Quit and len(self.SqlQueryQueue) == 0:
                return
            elif len(self.SqlQueryQueue) != 0:
                sqliteConnection = sqlite3.connect(DATABASE_LOCATION)
                with closing(sqliteConnection.cursor()) as cursor:
                    for queries in range(len(self.SqlQueryQueue)):
                        self.DeQueueQuery(cursor)
                        sqliteConnection.commit()

                self.Timeout = 0
            elif self.Timeout == 0:
                self.Timeout = time.time()
            elif time.time() - self.Timeout >= 60:  # One Min
                return
