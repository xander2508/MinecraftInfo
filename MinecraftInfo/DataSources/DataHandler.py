from MinecraftInfo.DataSources.DiscordMessages import DiscordMessages
from MinecraftInfo.DataSources.DiscordGuildHandler import DiscordGuildHandler
from MinecraftInfo.Util.JsonQueries import (
    GetMarketplacesHandler,
    GetOfficialChatChannelHandler,
)


class DataHandler:
    """Manage the data sources."""

    def __init__(self, messagesValidated) -> None:
        """Class constructor. Set the minecraft chat location and guilds to monitor.

        Args:
            dataSourceLocationsFile (str): The configuration file of the discord guilds and minecraft chat log to monitor.
        """
        self.MessagesValidated = messagesValidated
        self.OfficialChatChannelHandler = DiscordMessages(
            GetOfficialChatChannelHandler()
        )

        self.DataSourceLocations = GetMarketplacesHandler()
        self.MonitoredGuilds = []
        for Guild in self.DataSourceLocations:
            self.MonitoredGuilds.append(
                DiscordGuildHandler(self.DataSourceLocations[Guild])
            )

    def GetData(self) -> list:
        """Return the last messages from the minecraft chat log and monitored guilds.

        Returns:
            list[list, list]: The last messages from the monitored sources.
        """
        Data = []
        Data.append(
            self.OfficialChatChannelHandler.RetrieveMessageList(self.MessagesValidated)
        )
        for Guild in self.MonitoredGuilds:
            Data.append(Guild.GetGuildChatLogs())
        return Data
