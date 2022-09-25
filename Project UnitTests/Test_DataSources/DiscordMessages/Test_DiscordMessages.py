import pytest
import json
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import MinecraftInfo.DataSources.DiscordMessages


def test_DiscordMessage_ReturnsDict(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [
                        {
                            "type": "rich",
                            "color": 16766720,
                            "author": {
                                "name": "X has made the advancement Getting an Upgrade!",
                                "icon_url": "https://crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png?size=128&overlay#ade160d117f3c93164bc59c69a3a45a5b3581440de80027ae1594983a3757c33",
                                "proxy_icon_url": "https://images-ext-1.discordapp.net/external/QITwRzDd4dKwiOuMaaWBs3XCXyjHXbjQC545GaM-_-8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png",
                            },
                        }
                    ],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "2022-09-19T12:14:07.662000+00:00",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert (
        type(DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated)) == dict
    )


def test_DiscordMessage_ReturnsEmptyDict_WithEmptyJson(mocker):
    MockJson = json.loads(json.dumps([{}]))
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {"Death": {}, "Connection": {}, "Achievement": {}, "Other": {}},
    }


def test_DiscordMessage_ReturnsEmptyDict_WithReviewedMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [
                        {
                            "type": "rich",
                            "color": 16766720,
                            "author": {
                                "name": "X has made the advancement Getting an Upgrade!",
                                "icon_url": "https://crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png?size=128&overlay#ade160d117f3c93164bc59c69a3a45a5b3581440de80027ae1594983a3757c33",
                                "proxy_icon_url": "https://images-ext-1.discordapp.net/external/QITwRzDd4dKwiOuMaaWBs3XCXyjHXbjQC545GaM-_-8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png",
                            },
                        }
                    ],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "2022-09-19T12:14:07.662000+00:00",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = False
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {"Death": {}, "Connection": {}, "Achievement": {}, "Other": {}},
    }


def test_DiscordMessage_ReturnsOneMessage_WithOneReceivedMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "A",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "2022-09-19T12:14:07.662000+00:00",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {"1021393754545979472": "A"},
        "Embeds": {"Death": {}, "Connection": {}, "Achievement": {}, "Other": {}},
    }


def test_DiscordMessage_ReturnsOneDeathMessage_WithOneDeathMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [
                        {
                            "type": "rich",
                            "title": "Death Message",
                            "color": 16766720,
                            "author": {
                                "name": "A",
                                "icon_url": "https://crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png?size=128&overlay#ade160d117f3c93164bc59c69a3a45a5b3581440de80027ae1594983a3757c33",
                                "proxy_icon_url": "https://images-ext-1.discordapp.net/external/QITwRzDd4dKwiOuMaaWBs3XCXyjHXbjQC545GaM-_-8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png",
                            },
                        }
                    ],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "B",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {
            "Death": {"1021393754545979472": ["A", "B"]},
            "Connection": {},
            "Achievement": {},
            "Other": {},
        },
    }


def test_DiscordMessage_ReturnsOneAchievementMessage_WithOneAchievementMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [
                        {
                            "type": "rich",
                            "title": "N/A",
                            "color": 16766720,
                            "author": {
                                "name": "has made the advancement",
                                "icon_url": "https://crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png?size=128&overlay#ade160d117f3c93164bc59c69a3a45a5b3581440de80027ae1594983a3757c33",
                                "proxy_icon_url": "https://images-ext-1.discordapp.net/external/QITwRzDd4dKwiOuMaaWBs3XCXyjHXbjQC545GaM-_-8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png",
                            },
                        }
                    ],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "B",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {
            "Death": {},
            "Connection": {},
            "Achievement": {"1021393754545979472": "has made the advancement"},
            "Other": {},
        },
    }


def test_DiscordMessage_ReturnsOneConnectionMessage_WithOneConnectionMessage(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                    "type": 0,
                    "content": "",
                    "channel_id": "983831795852271666",
                    "author": {
                        "id": "761981472000180254",
                        "username": "MinecraftServerBot",
                        "avatar": "c5f696b0fa46f706141e9cc300662c17",
                        "avatar_decoration": None,
                        "discriminator": "0934",
                        "public_flags": 0,
                        "bot": True,
                    },
                    "attachments": [],
                    "embeds": [
                        {
                            "type": "rich",
                            "title": "N/A",
                            "color": 16766720,
                            "author": {
                                "name": "left",
                                "icon_url": "https://crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png?size=128&overlay#ade160d117f3c93164bc59c69a3a45a5b3581440de80027ae1594983a3757c33",
                                "proxy_icon_url": "https://images-ext-1.discordapp.net/external/QITwRzDd4dKwiOuMaaWBs3XCXyjHXbjQC545GaM-_-8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/7af84d0fe1e64584ad84d6996d4eea21.png",
                            },
                        }
                    ],
                    "mentions": [],
                    "mention_roles": [],
                    "pinned": False,
                    "mention_everyone": False,
                    "tts": False,
                    "timestamp": "B",
                    "edited_timestamp": None,
                    "flags": 0,
                    "components": [],
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {
            "Death": {},
            "Connection": {"1021393754545979472": ["left", "B"]},
            "Achievement": {},
            "Other": {},
        },
    }


def test_DiscordMessage_ReturnsEmptyDict_WithMalformedJSON(mocker):
    MockJson = json.loads(
        json.dumps(
            [
                {
                    "id": "1021393754545979472",
                }
            ]
        )
    )
    mocker.patch(
        "MinecraftInfo.DataSources.DiscordMessages.RequestDiscordMessages",
        return_value=MockJson,
    )
    DiscordMessagesObject = MinecraftInfo.DataSources.DiscordMessages.DiscordMessages(0)
    MockMessagesValidated = mocker.MagicMock()
    MockMessagesValidated.ReviewMessage.return_value = True
    assert DiscordMessagesObject.RetrieveMessageList(MockMessagesValidated) == {
        "Message": {},
        "Embeds": {
            "Death": {},
            "Connection": {},
            "Achievement": {},
            "Other": {},
        },
    }
