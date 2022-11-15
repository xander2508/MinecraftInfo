from collections import deque

from MinecraftInfo.Util.SqlQueries import (
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

    def ReviewMessage(self, messageID: int) -> bool:
        if messageID not in self.IDsReviewed:
            return True
        else:
            return False

    def __GetFromDatabase(self) -> None:
        self.IDsReviewed.append(GetMessageReviewedIDs())

    def __PushToDatabase(self, messageID: int) -> None:
        InsertMessageReviewedID(messageID)

    def MessageReviewed(self, messageID) -> None:
        if messageID not in self.IDsReviewed:
            if len(self.IDsReviewed) >= ID_LIMIT:
                DeleteMessageReviewedID(self.IDsReviewed.popleft())
            self.IDsReviewed.append(messageID)
            self.__PushToDatabase(messageID)
