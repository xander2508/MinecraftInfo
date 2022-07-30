import requests
import json


class DiscordMessages:
    """Retrieve the chat logs from a given discord channel."""

    def __init__(self, channelID: int) -> None:
        """Class constructor.

        Args:
            channelID (int): Discord channel ID to retrieve the chat logs from.
        """
        self.__ChannelID = channelID

    def RetrieveMessageList(self) -> list:
        """Format the retrieved messages from the discord channel into a list.

        Returns:
            _type_: _description_
        """
        DiscordJsonMessages = RequestDiscordMessages(self.__ChannelID, "")
        DiscordMessagesList = []
        for Message in DiscordJsonMessages:
            DiscordMessagesList.append(
                (
                    Message["author"]["username"]
                    + "#"
                    + Message["author"]["discriminator"],
                    Message["content"],
                )
            )
        return DiscordMessagesList


def RequestDiscordMessages(channelID: int, Authorization: str) -> json:
    """Retrieve the chat logs from a provided channel.

    Args:
        channelID (int): _description_

    Returns:
        json: The chat logs from discord channel.
    """
    Header = {
        "Authorization": "MTAwMjI1NzY2ODkyMjE1OTE1Nw.GtE3uY.YTuJQv-CPIO7cjOCXh_hxpZRp-dpRwPv721XAY"
    }
    Response = requests.get(
        url="https://discord.com/api/v9/channels/"
        + str(channelID)
        + "/messages?limit=50",
        headers=Header,
    )
    return json.loads(Response.text)


if __name__ == "__main__":
    a = DiscordMessages(916798277746298883)
    print(a.RetrieveMessageList())
