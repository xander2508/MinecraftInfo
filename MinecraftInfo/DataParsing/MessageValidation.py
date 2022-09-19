from collections import deque

from MinecraftInfo.DataStorage.SqlQueries import (
    GetMessageReviewedIDs,
    InsertMessageReviewedIDs,
    InsertMessageReviewedID,
    DeleteMessageReviewedID,
)

ID_LIMIT = 1000


class MessagesReviewed:
    def __init__(self) -> None:

        self.IDsReviewed = deque()
        self.__GetFromDatabase()

    def ReviewMessage(self, messageID: int):
        if messageID not in self.IDsReviewed:
            return True
        else:
            return False

    def __GetFromDatabase(self):
        self.IDsReviewed.append(GetMessageReviewedIDs())

    def __PushToDatabase(self, messageID: int):
        InsertMessageReviewedID(messageID)

    def MessageReviewed(self, messageID):
        if messageID not in self.IDsReviewed:
            if len(self.IDsReviewed) >= ID_LIMIT:
                DeleteMessageReviewedID(self.IDsReviewed.popleft())
            self.IDsReviewed.append(messageID)
            self.__PushToDatabase(messageID)
