import requests
import json


class DiscordMessages:
    def __init__(self, channelID: int) -> None:
        self.__ChannelID = channelID

    def RetrieveMessageList(self) -> list:
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
