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


def NameParsing():
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())

    def ExtractNames(nameString: str):
        PlayerAccount, PlayerName = GetUsername(nameString.split(" ")[-1])
        if PlayerAccount == None:
            Nickname = ((nameString.split(" "))[-1]).strip()
            Account = GetExistingNicknameLink(Nickname)
            if Account != None:
                PlayerAccount = Account
            else:
                AddUser(Nickname)
                AddNickname(Nickname, Nickname)
                PlayerAccount = Nickname
        else:
            AddUser(PlayerAccount)
            AddNickname(PlayerAccount, PlayerName)
        if len(nameString.split(" ")) > 1:
            Nickname = (" ".join((nameString.split(" ")[:-1]))).strip()
        else:
            Nickname = None

        if Nickname == None:
            AddRole("None")
            AddRoleLink(PlayerAccount, "None")
        else:
            AddRole(Nickname)
            AddRoleLink(PlayerAccount, Nickname)

        return PlayerAccount

    def GetUsername(username: str):
        for player in UsernameJson["players"]:
            if player["name"] in username or player["account"] in username:
                return player["account"], player["name"]
        return None, username

    return ExtractNames


def ValidateUsers():
    UsernameJson = LoadWebJsonFile(GetUsernameUrl())
    Nicknames = GetNicknameLinks()
    for NicknameIndex in Nicknames:
        if Nicknames[NicknameIndex][0] == Nicknames[NicknameIndex][1]:
            Username = Nicknames[NicknameIndex][0]
            for player in UsernameJson["players"]:
                if player["account"] in Username:
                    UsernameVerified = player["account"]
                    UpdateUsername(Username, UsernameVerified)
                    break
