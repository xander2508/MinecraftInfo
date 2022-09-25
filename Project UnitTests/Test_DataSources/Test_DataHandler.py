import json
import os
import sys
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import MinecraftInfo.DataSources.DiscordMessages
import MinecraftInfo.Util.FileOpener
from MinecraftInfo.DataSources.DataHandler import DataHandler


def test__GetData_ReturnsEmptyList(monkeypatch):
    MockJson = json.loads(json.dumps({"Marketplaces": {}}))
    FileIOMock = Mock(return_value=MockJson)
    DiscordMessagesMock = Mock(
        return_value=type("", (object,), {"RetrieveMessageList": lambda x, y: []})()
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.GetMarketplacesHandler", FileIOMock
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.DiscordMessages", DiscordMessagesMock
    )
    DataHandlerObject = DataHandler("A")
    assert DataHandlerObject.GetData() == [[], []]


def test__GetData_ReturnsFilledList(monkeypatch):
    MockJson = json.loads(json.dumps({"Marketplaces": {}}))
    FileIOMock = Mock(return_value=MockJson)
    DiscordMessagesMock = Mock(
        return_value=type(
            "", (object,), {"RetrieveMessageList": lambda x, y: ["Test"]}
        )()
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.GetMarketplacesHandler", FileIOMock
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.DiscordMessages", DiscordMessagesMock
    )
    DataHandlerObject = DataHandler("A")
    assert DataHandlerObject.GetData() == [["Test"], []]
