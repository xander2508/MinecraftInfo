import json
from logging import exception
from typing import Callable
from MinecraftInfo.DataStorage.SqlQueries import (
    AddNickname,
    AddRole,
    AddRoleLink,
    AddUser,
    GetExistingNicknameLink,
    GetNicknameLinks,
    UpdateUsername,
)
from MinecraftInfo.Util.FileOpener import LoadWebJsonFile
from MinecraftInfo.DataStorage.JsonQueries import GetUsernameUrl


def NameParsing(SqlQueryHandler) -> Callable:
    """Wrapper for ExtractNames. Stores the JSON from the website containing online users so that the large JSON does not have to be repeatably called.

    Returns:
        ExtractNames: ExtractNames function
    """
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    SqlQueryHandler  = SqlQueryHandler
    
    def ExtractNames(nameString: str):
        """Given a username string containing a nickname and account name, split them up and store the relevant parts in the database.

        Args:
            nameString (str): Nickname + Account string

        Returns:
            PlayerAccount : User account string, or best guess.
        """
        PlayerAccount, PlayerName = GetUsername(nameString.split(" ")[-1], UsernameJson)
        if PlayerAccount == None:
            Nickname = ((nameString.split(" "))[-1]).strip()
            Account = GetExistingNicknameLink(Nickname)
            if Account != None:
                PlayerAccount = Account
            else:
                SqlQueryHandler.QueueQuery(AddUser,Nickname)
                SqlQueryHandler.QueueQuery(AddNickname,Nickname, Nickname)
                PlayerAccount = Nickname
        else:
            SqlQueryHandler.QueueQuery(AddUser,PlayerAccount)
            SqlQueryHandler.QueueQuery(AddNickname,PlayerAccount, PlayerName)
        if len(nameString.split(" ")) > 1:
            Nickname = (" ".join((nameString.split(" ")[:-1]))).strip()
        else:
            Nickname = None

        if Nickname == None:
            SqlQueryHandler.QueueQuery(AddRole,"None")
            SqlQueryHandler.QueueQuery(AddRoleLink,PlayerAccount, "None")
        else:
            SqlQueryHandler.QueueQuery(AddRole,Nickname)
            SqlQueryHandler.QueueQuery(AddRoleLink,PlayerAccount, Nickname)

        return PlayerAccount

    return ExtractNames


def GetUsername(username: str, usernameJson: json):
    """Given a username, validate the string with the up-to-date website log and return the account and nickname.

    Args:
        username (str): Username string to validate.

    Returns:
        Account, Nickname: The validated account name and nickname if avaliable.
    """
    try:
        for player in usernameJson["players"]:
            if player["name"] in username or player["account"] in username:
                return player["account"], player["name"]
    except Exception as e:
        print("Log" + str(e))

    return None, username


def ValidateUsers(SqlQueryHandler):
    """Get all the nickname links where both entries are the same and check for a logged in user with the same nickname.
    If a user with that nickname is found, update the entry to the correct account name.
    """
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    Nicknames = GetNicknameLinks()
    for NicknameIndex in Nicknames:
        if Nicknames[NicknameIndex][0] == Nicknames[NicknameIndex][1]:
            Username = Nicknames[NicknameIndex][0]
            for player in UsernameJson["players"]:
                if player["account"] in Username or player["name"] in Username:
                    UsernameVerified = player["account"]
                    SqlQueryHandler.QueueQuery(UpdateUsername, Username, UsernameVerified)
                    break
