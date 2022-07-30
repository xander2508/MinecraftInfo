import json
from unittest.mock import Mock
from MinecraftInfo.DataSources.DataHandler import DataHandler
import MinecraftInfo.DataSources.DiscordMessages
import MinecraftInfo.Util.FileOpener


def test__GetData_ReturnsList(monkeypatch):
    MockJson = json.loads(
        json.dumps({"Discord": {"Guilds": {"OfficialChat": 0, "Marketplaces": {}}}})
    )
    FileIOMock = Mock(return_value=MockJson)
    DiscordMessagesMock = Mock(
        return_value=type("", (object,), {"RetrieveMessageList": lambda x: []})()
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.LoadJsonFile", FileIOMock
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.DiscordMessages", DiscordMessagesMock
    )
    DataHandlerObject = DataHandler("")
    assert DataHandlerObject.GetData() == [[[]], []]


def test__GetData_ReturnsFilledList(monkeypatch):
    MockJson = json.loads(
        json.dumps({"Discord": {"Guilds": {"OfficialChat": 0, "Marketplaces": {}}}})
    )
    FileIOMock = Mock(return_value=MockJson)
    DiscordMessagesMock = Mock(
        return_value=type("", (object,), {"RetrieveMessageList": lambda x: ["Test"]})()
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.LoadJsonFile", FileIOMock
    )
    monkeypatch.setattr(
        "MinecraftInfo.DataSources.DataHandler.DiscordMessages", DiscordMessagesMock
    )
    DataHandlerObject = DataHandler("")
    assert DataHandlerObject.GetData() == [[["Test"]], []]
