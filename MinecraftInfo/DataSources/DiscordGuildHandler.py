from MinecraftInfo.DataSources.DiscordMessages import DiscordMessages


class DiscordGuildHandler:
    def __init__(self, guildId: int) -> None:
        self.GuildId = guildId

    def GetGuildChannels(self) -> list:
        return []

    def GetGuildChatLogs(self) -> list:
        return []
