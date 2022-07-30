from MinecraftInfo.DataSources.DiscordMessages import DiscordMessages


class DiscordGuildHandler:
    """Given a guild id manage the guild, getting channels to monitor and their chat logs."""

    def __init__(self, guildId: int) -> None:
        self.GuildId = guildId

    def GetGuildChannels(self) -> list:
        return []

    def GetGuildChatLogs(self) -> list:
        return []
