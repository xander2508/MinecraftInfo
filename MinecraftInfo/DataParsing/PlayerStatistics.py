from typing import Iterable


def PlayerStatistics(minecraftChatLog: list) -> None:
    """Given discord chat data update the player statistics.

    Args:
        minecraftChatLog (list): Minecraft chat log.
    """

    UpdatePlayerDeaths(
        (
            x
            for x in minecraftChatLog
            if x[2] != [] and "title" in x[2][0] and x[2][0]["title"] == "Death Message"
        )
    )


def UpdatePlayerDeaths(playerDeaths: Iterable):
    for i in playerDeaths:
        print(i)
    # Check if death message is in list
    # Assign it to user / make user etc
    # Generate a new death message regex
    # http://104.238.222.67:2096/up/world/newrathnir/
