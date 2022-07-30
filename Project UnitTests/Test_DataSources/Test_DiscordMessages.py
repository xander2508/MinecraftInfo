import pytest
import json
import MinecraftInfo.DataSources.DiscordMessages


def test_DiscordMessage_ReturnsList(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "author": {"username": "test", "discriminator": "test"},
                    "content": "test",
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    a = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(916798277746298883)
    assert type(a.RetrieveMessageList()) == list


def test_DiscordMessage_ReturnsCorrectUsername(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "author": {
                        "username": "UsernameTest",
                        "discriminator": "test",
                    },
                    "content": "test",
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    a = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(916798277746298883)
    assert "UsernameTest" in a.RetrieveMessageList()[0][0]


def test_DiscordMessage_ReturnsCorrectMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "author": {
                        "username": "test",
                        "discriminator": "test",
                    },
                    "content": "ContentTest",
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    a = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(916798277746298883)
    assert "ContentTest" in a.RetrieveMessageList()[0][1]


def test_DiscordMessage_ReturnsTwoMessages(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "author": {
                        "username": "test",
                        "discriminator": "test",
                    },
                    "content": "ContentTest",
                },
                {
                    "author": {
                        "username": "test",
                        "discriminator": "test",
                    },
                    "content": "ContentTest",
                },
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    a = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(916798277746298883)
    assert len(a.RetrieveMessageList()) == 2


def test_DiscordMessage_ReturnsNoMessages(mocker):
    MockJson = json.loads(json.dumps([]))
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    a = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(916798277746298883)
    assert len(a.RetrieveMessageList()) == 0
