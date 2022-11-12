from collections import deque
import sys
import time
from typing import Callable
import threading


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

    def DeQueueQuery(self):
        Query = self.SqlQueryQueue.popleft()
        Query[0](*(Query[1]))

    def QueueHandler(self):
        while True:
            if self.Quit and len(self.SqlQueryQueue) == 0:
                return
            elif len(self.SqlQueryQueue) != 0:
                self.Timeout = 0
                self.DeQueueQuery()
            elif self.Timeout == 0:
                self.Timeout = time.time()
            elif time.time() - self.Timeout >= 60: # One Min
                return
