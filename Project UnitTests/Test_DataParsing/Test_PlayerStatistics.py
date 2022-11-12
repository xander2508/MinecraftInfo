import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.DataParsing.PlayerStatistics import PlayerStatistics


def test__PlayerStatistics_CallsValidateUserOnce_WithOneEntry(mocker):
    mocker.patch(
        "MinecraftInfo.DataParsing.PlayerStatistics.UpdatePlayerDeaths",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.PlayerStatistics.UpdatePlayerConnections",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.PlayerStatistics.UpdatePlayerAchievement",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.PlayerStatistics.UpdatePlayerMessages",
    )
    Object = mocker.patch("MinecraftInfo.DataParsing.PlayerStatistics.ValidateUsers")
    PlayerStatistics(
        [
            {
                "Message": {},
                "Embeds": {
                    "Death": {},
                    "Connection": {},
                    "Achievement": {},
                    "Other": {},
                },
            }
        ],
        "",
    )
    Object.assert_called_once()
