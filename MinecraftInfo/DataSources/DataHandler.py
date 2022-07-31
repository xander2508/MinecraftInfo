from MinecraftInfo.DataSources.DiscordMessages import DiscordMessages
from MinecraftInfo.DataSources.DiscordGuildHandler import DiscordGuildHandler
from MinecraftInfo.Util.FileOpener import LoadJsonFile


class DataHandler:
    """Manage the data sources."""

    def __init__(self, dataSourceLocationsFile: str) -> None:
        """Class constructor. Set the minecraft chat location and guilds to monitor.

        Args:
            dataSourceLocationsFile (str): The configuration file of the discord guilds and minecraft chat log to monitor.
        """
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
        """Return the last messages from the minecraft chat log and monitored guilds.

        Returns:
            list[list, list]: The last messages from the monitored sources.
        """
        Data = [[], []]
        Data[0].append(self.OfficialChatChannelHandler.RetrieveMessageList())
        for Guild in self.MonitoredGuilds:
            Data[1].append(Guild.GetGuildChatLogs())
        return Data
