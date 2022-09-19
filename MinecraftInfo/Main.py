import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from MinecraftInfo.DataParsing.MessageValidation import MessagesReviewed

from MinecraftInfo.DataSources.DataHandler import DataHandler
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics


class Main:
    def __init__(self) -> None:
        self.MessagesValidated = MessagesReviewed()
        self.DataSourceHandler = DataHandler(self.MessagesValidated)
        self.DiscordData = {}

    def UpdateDiscordData(self) -> None:
        self.DiscordData = self.DataSourceHandler.GetData()

    def UpdatePlayerStatistics(self) -> None:
        PlayerStatistics(self.DiscordData, self.MessagesValidated)


if __name__ == "__main__":

    MainProgram = Main()
    MainProgram.UpdateDiscordData()
    MainProgram.UpdatePlayerStatistics()
