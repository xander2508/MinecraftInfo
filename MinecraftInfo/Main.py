import os
import sys
import threading
import time
from logging import exception

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.Website.Website import RunWebsite
from MinecraftInfo.DataParsing.MessageValidation import MessagesReviewed
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics
from MinecraftInfo.DataParsing.SqlQueryHandler import SqlQueryHandler
from MinecraftInfo.DataSources.DataHandler import DataHandler
from MinecraftInfo.Util.Logging import LogError, LogInfo


class Main:
    """Main handles the main aspects of the program. Collects data and then parses it."""

    def __init__(self) -> None:
        self.MessagesValidated = MessagesReviewed()
        self.DataSourceHandler = DataHandler(self.MessagesValidated)
        self.DiscordData = {}

    def UpdateDiscordData(self) -> None:
        self.DiscordData = self.DataSourceHandler.GetData()

    def UpdatePlayerStatistics(self, SqlQueryHandler: object) -> None:
        PlayerStatistics(self.DiscordData, self.MessagesValidated, SqlQueryHandler)


def DataCollection():
    MainProgram = Main()
    StartTime = time.time()
    while True:
        try:
            MainProgram.UpdateDiscordData()
            MainProgram.UpdatePlayerStatistics(SqlQueryHandler)
            CurrentTime = time.time()
            LogInfo(
                "Program Runtime - " + str(CurrentTime - StartTime),
                __name__,
                sys._getframe().f_code.co_name,
            )
        except Exception as e:
            LogError(e, __name__, sys._getframe().f_code.co_name)
        except KeyboardInterrupt as e:
            LogError("KeyboardInterrupt", __name__, sys._getframe().f_code.co_name)
            break
        time.sleep(20)


if __name__ == "__main__":
    # WebsiteThread = threading.Thread(
    #    target=RunWebsite,
    #    args=(),
    # )
    # WebsiteThread.start()
    SqlQueryHandler = SqlQueryHandler()
    DataCollection()
    SqlQueryHandler.Quit = True
