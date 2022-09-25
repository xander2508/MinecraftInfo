from typing import Callable
import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MinecraftInfo.DataParsing.StringParsing.NameParsing import (
    GetUsername,
    NameParsing,
    ValidateUsers,
)


def test_NameParsing_ReturnsFunctionAndCallsJson(mocker):
    Object = mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value="",
    )
    assert type(NameParsing()) == type(test_NameParsing_ReturnsFunctionAndCallsJson)
    Object.assert_called_once()


def test_ExtractNamesFunction_ReturnsUsername(mocker):
    Username = "A"
    Nickname = "B"
    UsernameString = Nickname + Username
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value="",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetExistingNicknameLink",
        return_value=Username,
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetUsername",
        return_value=[Username, Nickname],
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddUser")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddNickname")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRole")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRoleLink")

    ExtractNamesFunction = NameParsing()
    assert ExtractNamesFunction(UsernameString) == Username


def test_ExtractNamesFunction_FindsCorrectNickname_WithValidUsername(mocker):
    Username = "A"
    Nickname = "B"
    UsernameString = Nickname + " " + Username
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value="",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetExistingNicknameLink",
        return_value=Username,
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetUsername",
        return_value=[Username, Nickname],
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddUser")
    AddNicknameObject = mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.AddNickname"
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRole")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRoleLink")

    ExtractNamesFunction = NameParsing()
    assert ExtractNamesFunction(UsernameString) == Username
    assert AddNicknameObject.call_args_list[0][0][1] == "B"


def test_ExtractNamesFunction_FindsCorrectNickname_WithInValidUsername(mocker):
    Username = "A"
    Nickname = "B"
    UsernameString = Nickname + " " + Username
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value="",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetExistingNicknameLink",
        return_value=None,
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetUsername",
        return_value=[None, Nickname],
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddUser")
    AddNicknameObject = mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.AddNickname"
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRole")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRoleLink")

    ExtractNamesFunction = NameParsing()
    assert ExtractNamesFunction(UsernameString) == "A"
    assert AddNicknameObject.call_args_list[0][0][1] == "A"


def test_ExtractNamesFunction_FindsCorrectAccount_WithValidNickname(mocker):
    Username = "A"
    Nickname = "B"
    UsernameString = Nickname + " " + Username
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value="",
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetExistingNicknameLink",
        return_value=Username,
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetUsername",
        return_value=[None, Nickname],
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddUser")
    AddNicknameObject = mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.AddNickname"
    )
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRole")
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.AddRoleLink")

    ExtractNamesFunction = NameParsing()
    assert ExtractNamesFunction(UsernameString) == Username


def test_GetUsername_FindsCorrectAccount(mocker):
    Account = "A"
    Nickname = "B"
    usernameJson = {"players": [{"name": Nickname, "account": Account}]}
    assert GetUsername(Account, usernameJson) == (Account, Nickname)


def test_GetUsername_Error_WithIncorrectJSON(mocker):
    Account = "A"
    Nickname = "B"
    usernameJson = {}
    assert GetUsername(Account, usernameJson) == (None, Account)


def test_GetUsername_FindsCorrectAccount_WithMultipleEntires(mocker):
    Account = "A"
    Nickname = "B"
    usernameJson = {
        "players": [
            {"name": "C", "account": "C"},
            {"name": Nickname, "account": Account},
        ]
    }
    assert GetUsername(Account, usernameJson) == (Account, Nickname)


def test_ValidateUsers_UpdateUsername(mocker):
    mocker.patch("MinecraftInfo.DataParsing.StringParsing.NameParsing.GetUsernameUrl")
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.LoadWebJsonFile",
        return_value={
            "players": [
                {"name": "C", "account": "C"},
                {"name": "B", "account": "A"},
            ]
        },
    )
    mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.GetNicknameLinks",
        return_value={"1": ["B", "B"]},
    )

    UpdateUsernameObject = mocker.patch(
        "MinecraftInfo.DataParsing.StringParsing.NameParsing.UpdateUsername"
    )
    ValidateUsers()
    assert UpdateUsernameObject.call_args_list[0][0][1] == "A"
