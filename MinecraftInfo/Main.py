import sys

# sys.path.append("C:\\Program Files\\Brainwy\\PyVmMonitor 2.0.2\\public_api")
# import pyvmmonitor
import os
import time

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
    # pyvmmonitor.connect()
    MainProgram = Main()
    MainProgram.UpdateDiscordData()
    MainProgram.UpdatePlayerStatistics()
