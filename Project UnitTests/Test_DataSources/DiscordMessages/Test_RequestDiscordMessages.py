import pytest
import json
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.DataSources.DiscordMessages import RequestDiscordMessages


@pytest.mark.skip(reason="Calls Discord API")
def test_RequestDiscordMessages_ReturnsNoMessages(mocker):
    assert RequestDiscordMessages(0) == []
