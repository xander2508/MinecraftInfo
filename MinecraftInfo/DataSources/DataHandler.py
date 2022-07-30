from MinecraftInfo.DataSources import DiscordMessages
from MinecraftInfo.DataSources import DiscordGuildHandler
from MinecraftInfo.Util.FileOpener import LoadJsonFile


class DataHandler:
    def __init__(self, dataSourceLocationsFile: str) -> None:
        self.DataSourceLocations = LoadJsonFile(dataSourceLocationsFile)
        self.OfficialChatChannelHandler = DiscordMessages(
            self.DataSourceLocations["Discord"]["Guilds"]["OfficialChat"]
        )
        self.MonitoredGuilds = []
        for Guild in self.DataSourceLocations["Discord"]["Guilds"]["Marketplaces"]:
            self.MonitoredGuilds.append(
                DiscordGuildHandler(
                    self.DataSourceLocations["Discord"]["Guilds"]["Marketplaces"][Guild]
                )
            )

    def GetData(self) -> list[list, list]:
        Data = [[], []]
        print(self.OfficialChatChannelHandler)
        print(self.OfficialChatChannelHandler.RetrieveMessageList())
        Data[0].append(self.OfficialChatChannelHandler.RetrieveMessageList())
        for Guild in self.MonitoredGuilds:
            Data[1].append(Guild.GetGuildChatLogs())
        return Data
