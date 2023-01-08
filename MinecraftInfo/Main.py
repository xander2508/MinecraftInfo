import os
import sys
import threading
import time
from logging import exception

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.Util.WebsiteSqlQueries import BackupDatabase
from MinecraftInfo.DataParsing.MapInfo import UpdateClaimInfo
from MinecraftInfo.Website.Website import RunWebsite
from MinecraftInfo.DataParsing.MessageValidation import MessagesReviewed
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics
from MinecraftInfo.DataParsing.SqlQueryHandler import SqlQueryHandler
from MinecraftInfo.DataSources.DataHandler import DataHandler
from MinecraftInfo.Util.Logging import LogError, LogInfo


class Main:
    """Main handles the main aspects of the program. Collects data and then parses it."""

    def __init__(self, sqlQueryHandler: object) -> None:
        self.MessagesValidated = MessagesReviewed(sqlQueryHandler)
        self.DataSourceHandler = DataHandler(self.MessagesValidated)
        self.DiscordData = {}

    def UpdateDiscordData(self) -> None:
        self.DiscordData = self.DataSourceHandler.GetData()

    def UpdatePlayerStatistics(self, sqlQueryHandler: object) -> None:
        PlayerStatistics(self.DiscordData, self.MessagesValidated, sqlQueryHandler)


def DataCollection() -> None:
    MainProgram = Main(SqlQueryHandler)
    StartTime = time.time()
    counter = 0
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
            counter = DelayUpdateClaimInfo(counter)
        except Exception as e:
            LogError(e, __name__, sys._getframe().f_code.co_name)
        except KeyboardInterrupt as e:
            LogError("KeyboardInterrupt", __name__, sys._getframe().f_code.co_name)
            break
        try:
            time.sleep(20)
            BackupDatabase()
            time.sleep(10)
        except Exception as e:
            LogError(e, __name__, sys._getframe().f_code.co_name)
        except KeyboardInterrupt as e:
            LogError("KeyboardInterrupt", __name__, sys._getframe().f_code.co_name)
            break


def DelayUpdateClaimInfo(counter: int) -> int:
    if counter == 0:
        UpdateClaimInfo(SqlQueryHandler)
        counter += 1
    elif counter >= 1000:
        counter = 0
    else:
        counter += 1
    return counter


if __name__ == "__main__":
    # WebsiteThread = threading.Thread(
    #    target=RunWebsite,
    #    args=(),
    # )
    # WebsiteThread.start()
    SqlQueryHandler = SqlQueryHandler()
    DataCollection()
    SqlQueryHandler.Quit = True
