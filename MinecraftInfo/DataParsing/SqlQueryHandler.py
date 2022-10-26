from collections import deque
import sys
import time
from typing import Callable
import threading


class SqlQueryHandler:
    def __init__(self) -> None:
        self.SqlQueryQueue = deque()
        self.HeartBeat = 1
        QueueHandlerThread = threading.Thread(
            target=self.QueueHandler,
        )
        QueueHandlerThread.start()
        HeartBeatHandlerThread = threading.Thread(
            target=self.HeartBeatHandler,
        )
        QueueHandlerThread.start()
        HeartBeatHandlerThread.daemon = True
        HeartBeatHandlerThread.start()
        while True:
            pass

    def QueueQuery(self, queryFunction: Callable, *args: list) -> None:
        self.SqlQueryQueue.append([queryFunction, args])

    def DeQueueQuery(self):
        Query = self.SqlQueryQueue.popleft()
        Query[0](*(Query[1]))

    def HeartBeatHandler(self):
        while True:
            time.sleep(5)
            self.HeartBeat = 1

    def QueueHandler(self):
        while True:
            if len(self.SqlQueryQueue) == 0:
                if self.HeartBeat == 0:
                    return
                self.HeartBeat = 0
                time.sleep(10)
            else:
                self.DeQueueQuery()
