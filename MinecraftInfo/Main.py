import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.DataSources.DataHandler import DataHandler
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics
from MinecraftInfo.DataParsing.ItemStatistics import ItemStatistics


class Main:
    def __init__(self, dataSourceLocationsFile: str) -> None:
        self.DataSourceHandler = DataHandler(dataSourceLocationsFile)
        self.DiscordData = []

    def UpdateDiscordData(self) -> None:
        self.DiscordData = self.DataSourceHandler.GetData()

    def UpdatePlayerStatistics(self) -> None:
        PlayerStatistics(self.DiscordData[0])

    def UpdateItemStatistics(self) -> None:
        ItemStatistics(self.DiscordData)


if __name__ == "__main__":
    MainProgram = Main(
        r"C:\Users\alexa\Desktop\Minecraft\MinecraftInfo\MinecraftInfo\Configuration\DataSourceLocations.json"
    )
