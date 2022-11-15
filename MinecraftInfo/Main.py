import os
import sys
import time
from logging import exception

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from MinecraftInfo.DataParsing.MessageValidation import MessagesReviewed
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics
from MinecraftInfo.DataParsing.SqlQueryHandler import SqlQueryHandler
from MinecraftInfo.DataSources.DataHandler import DataHandler


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


if __name__ == "__main__":
    count = 0
    try:
        SqlQueryHandler = SqlQueryHandler()
        MainProgram = Main()
        while True:
            MainProgram.UpdateDiscordData()
            MainProgram.UpdatePlayerStatistics(SqlQueryHandler)
            time.sleep(20)
            print(count)
            count += 1
    except Exception as e:
        SqlQueryHandler.Quit = True
        print(e)
    except KeyboardInterrupt:
        SqlQueryHandler.Quit = True
