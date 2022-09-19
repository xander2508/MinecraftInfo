from logging import exception
import requests
import json
import MinecraftInfo.DataSources.AuthToken as AuthToken
from MinecraftInfo.DataStorage.SqlQueries import LogUnknownEvent


class DiscordMessages:
    """Retrieve the chat logs from a given discord channel."""

    def __init__(self, channelID: int) -> None:
        """Class constructor.

        Args:
            channelID (int): Discord channel ID to retrieve the chat logs from.
        """
        self.__ChannelID = channelID

    def RetrieveMessageList(self, messagesValidated) -> list:
        """Format the retrieved messages from the discord channel into a list.

        Returns:
            _type_: _description_
        """
        DiscordJsonMessages = RequestDiscordMessages(self.__ChannelID, "")
        DiscordMessagesList = {
            "Message": {},
            "Embeds": {"Death": {}, "Connection": {}, "Achievement": {}, "Other": {}},
        }
        if len(DiscordJsonMessages) <= 1:
            LogUnknownEvent("Could not retrieve messages: " + str(DiscordJsonMessages))

        for Message in DiscordJsonMessages:
            if messagesValidated.ReviewMessage(Message["id"]):
                if Message["embeds"] == []:
                    DiscordMessagesList["Message"][Message["id"]] = Message["content"]
                else:
                    if (
                        "title" in Message["embeds"][0]
                        and Message["embeds"][0]["title"] == "Death Message"
                    ):
                        DiscordMessagesList["Embeds"]["Death"][Message["id"]] = [
                            Message["embeds"][0]["author"]["name"],
                            Message["timestamp"],
                        ]
                    elif "name" in Message["embeds"][0]["author"] and (
                        "has made the advancement"
                        in Message["embeds"][0]["author"]["name"]
                    ):
                        DiscordMessagesList["Embeds"]["Achievement"][
                            Message["id"]
                        ] = Message["embeds"][0]["author"]["name"]
                        print(Message)
                    elif "name" in Message["embeds"][0]["author"] and (
                        "joined" in Message["embeds"][0]["author"]["name"]
                        or "left" in Message["embeds"][0]["author"]["name"]
                    ):
                        DiscordMessagesList["Embeds"]["Connection"][Message["id"]] = (
                            Message["embeds"][0]["author"]["name"],
                            Message["timestamp"],
                        )
                    else:
                        DiscordMessagesList["Embeds"]["Other"][Message["id"]] = Message[
                            "embeds"
                        ][0]["author"]["name"]
        return DiscordMessagesList


def RequestDiscordMessages(channelID: int, Authorization: str) -> json:
    """Retrieve the chat logs from a provided channel.

    Args:
        channelID (int): _description_

    Returns:
        json: The chat logs from discord channel.
    """
    Header = {"Authorization": AuthToken.AUTH_TOKEN}
    try:
        Response = requests.get(
            url="https://discord.com/api/v9/channels/"
            + str(channelID)
            + "/messages?limit=100",
            headers=Header,
        )
    except exception as e:
        print("Error", e)  # LOG
        return json.loads(json.dumps({"players": {}}))
    return json.loads(Response.text)
