import base64
import os
import sys

from flask import send_from_directory
from flask import Flask, render_template, request
from werkzeug.serving import run_simple
from werkzeug.middleware.proxy_fix import ProxyFix


sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from MinecraftInfo.Util.FileProcessing import GetMap, GenerateMap, GetUserModel
from MinecraftInfo.Util.WebsiteSqlQueries import (
    GetAchievementList,
    GetAllAchievements,
    GetAllClaims,
    GetAllItems,
    GetAllNations,
    GetAllRoles,
    GetAllUsers,
    GetClaimInfo,
    GetClaimNation,
    GetItem,
    GetItemMurderList,
    GetLargestClaimByChunks,
    GetLargestClaimByUsers,
    GetLargestNationByChunks,
    GetLargestNationByClaims,
    GetLargestNationByUsers,
    GetNationCapital,
    GetNationClaimList,
    GetNationInfo,
    GetRoleList,
    GetTop50Achievement,
    GetTop50Items,
    GetTop50Roles,
    GetTop50UserTotalPlayTime,
    GetTopAchievementCount,
    GetTopItem,
    GetTopUserAchievementCount,
    GetTopUserDeaths,
    GetTopUserKiller,
    GetTopUserMessagesCount,
    GetTopUserRole,
    GetTopUserTotalPlayTime,
    GetUserAchievementCount,
    GetUserAchievementList,
    GetUserClaimList,
    GetUserCurrentPlayTime,
    GetUserDeathCount,
    GetUserDeathList,
    GetUserMessageCount,
    GetUserMurderCount,
    GetUserMurderList,
    GetUsername,
    GetUserNickname,
    GetUserNicknameList,
    GetUserRole,
    GetUserRoleList,
    GetUserTotalPlayTime,
    Top50LargestClaimByChunks,
    Top50LargestClaimByUsers,
    Top50LargestNationByChunks,
    Top50LargestNationByClaims,
    Top50LargestNationByUsers,
)

app = Flask(__name__)
MAP = GetMap()


def GetAutocompleteLists() -> tuple:
    """Retrieve the lists of searchable terms within the website.

    Returns:
        str: The string list of the searchable terms.
    """
    Users = str(GetAllUsers())
    Items = str(GetAllItems())
    Achievements = str(GetAllAchievements())
    Roles = str(GetAllRoles())
    return Users, Items, Achievements, Roles


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
def Index() -> object:
    """Display the index webpage containing the top statistics.

    Returns:
        HTML: index.html template with top statistics.
    """
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    try:
        MessagesSent = GetTopUserMessagesCount()
        Playtime = GetTopUserTotalPlayTime()
        Kills = GetTopUserKiller()
        Deaths = GetTopUserDeaths()
        TopUserAchievement = GetTopUserAchievementCount()
        TopAchievement = GetTopAchievementCount()
        Role = GetTopUserRole()
        Item = GetTopItem()
        LargestClaimChunks = GetLargestClaimByChunks()
        LargestClaimUsers = GetLargestClaimByUsers()
        LargestNationChunks = GetLargestNationByChunks()
        LargestNationUsers = GetLargestNationByUsers()
        LargestNationClaims = GetLargestNationByClaims()
        Table = {
            "1": {
                "Title": "Top Statistics",
                "Headers": ["Catagory", "Name", "Metric"],
                "Body": [
                    [
                        "Most Messages Sent",
                        "<a href=/player?search="
                        + MessagesSent[0]
                        + ">"
                        + MessagesSent[0]
                        + "</a>",
                        MessagesSent[1],
                    ],
                    [
                        "Most Playtime",
                        "<a href=/player?search="
                        + Playtime[0]
                        + ">"
                        + Playtime[0]
                        + "</a>",
                        str(float("{:.2f}".format(Playtime[1] / 3600000))) + " Hours",
                    ],
                    [
                        "Top Kills",
                        "<a href=/player?search=" + Kills[0] + ">" + Kills[0] + "</a>",
                        Kills[1],
                    ],
                    [
                        "Top Deaths",
                        "<a href=/player?search="
                        + Deaths[0]
                        + ">"
                        + Deaths[0]
                        + "</a>",
                        Deaths[1],
                    ],
                    [
                        "Most Achievements",
                        "<a href=/player?search="
                        + TopUserAchievement[0]
                        + ">"
                        + TopUserAchievement[0]
                        + "</a>",
                        TopUserAchievement[1],
                    ],
                    [
                        "Most Popular Achievement",
                        "<a href=/achievement?search="
                        + TopAchievement[0].replace(" ", "+")
                        + ">"
                        + TopAchievement[0]
                        + "</a>",
                        TopAchievement[1],
                    ],
                    [
                        "Most Popular Role",
                        "<a href=/role?search="
                        + str(Role[0]).replace(" ", "+")
                        + ">"
                        + str(Role[0])
                        + "</a>",
                        Role[1],
                    ],
                    [
                        "Deadliest Weapon",
                        "<a href=/weapon?search="
                        + Item[0].strip("[").strip("]").replace(" ", "+")
                        + ">"
                        + Item[0].strip("[").strip("]")
                        + "</a>",
                        Item[1],
                    ],
                    [
                        "Largest Claim (Chunks)",
                        LargestClaimChunks[0],
                        LargestClaimChunks[1],
                    ],
                    [
                        "Largest Claim (Users)",
                        LargestClaimUsers[0],
                        LargestClaimUsers[1],
                    ],
                    [
                        "Largest Nation (Chunks)",
                        LargestNationChunks[0],
                        LargestNationChunks[1],
                    ],
                    [
                        "Largest Nation (Users)",
                        LargestNationUsers[0],
                        LargestNationUsers[1],
                    ],
                    [
                        "Largest Nation (Claims)",
                        LargestNationClaims[0],
                        LargestNationClaims[1],
                    ],
                ],
            }
        }

        return render_template(
            "index.html",
            title="Home",
            list=Users,
            searchbox="Search Users...",
            Table=Table,
            uri="player",
        )
    except:
        return render_template(
            "index.html",
            title="Home",
            list=Users,
            searchbox="Search Users...",
            Table=[],
            uri="player",
        )


@app.route("/player")
def SearchPlayer() -> object:
    """Search for an indivigual player.

    Returns:
        HTML: index.html template with a players statistics
    """
    player = request.args.get("search")
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    if User := GetUsername(player):
        MessagesSent = GetUserMessageCount(User)
        Playtime = GetUserTotalPlayTime(User)
        LoginTime, LastSeenOnline = GetUserCurrentPlayTime(User)
        Kills = GetUserMurderCount(User)
        Deaths = GetUserDeathCount(User)
        Role = GetUserRole(User)
        Nickname = GetUserNickname(User)
        Achievement = GetUserAchievementCount(User)
        KillList = GetUserMurderList(User)
        DeathList = GetUserDeathList(User)
        AchievementList = GetUserAchievementList(User)
        NicknameList = GetUserNicknameList(User)
        RoleList = GetUserRoleList(User)
        ClaimList = GetUserClaimList(User)
        ClaimNationList = []
        if len(ClaimList) > 0:
            Map = GenerateMap(MAP, ClaimList, False)
            for claim in ClaimList:
                Nation = GetClaimNation(claim)
                ClaimNationList.append(
                    [
                        "<a href=/claim?search=" + str(claim) + ">" + claim + "</a>",
                        Nation,
                    ]
                )

        LoginTimeIcon = "🔴"
        CurrentPlaytime = 0
        CurrentPlaytimeInt = 0
        if LoginTime:
            CurrentPlaytimeInt = LastSeenOnline - LoginTime
            CurrentPlaytime = (
                str(float("{:.2f}".format(CurrentPlaytimeInt / 3600000))) + " Hours"
            )
            LoginTimeIcon = "🟢"

        if Nickname == User:
            Nickname = "None"

        Table = {
            "1": {
                "Title": "Top Statistics",
                "Headers": ["Catagory", "Metric"],
                "Body": [
                    ["Messages Sent", MessagesSent],
                    [
                        "Playtime",
                        str(
                            float(
                                "{:.2f}".format(
                                    (Playtime + CurrentPlaytimeInt) / 3600000
                                )
                            )
                        )
                        + " Hours",
                    ],
                    ["Kill Count", Kills],
                    ["Death Count", Deaths],
                    ["Achievement Count", Achievement],
                    [
                        "Current Role",
                        "<a href=/role?search="
                        + str(Role).replace(" ", "+")
                        + ">"
                        + str(Role)
                        + "</a>",
                    ],
                    ["Current Nickname", Nickname],
                    ["Online", LoginTimeIcon],
                    ["Current Playtime", CurrentPlaytime],
                ],
            }
        }
        if len(ClaimList) > 0:
            Table["7"] = {
                "Title": "Member Claims",
                "Headers": ["Claim", "Nation"],
                "Body": ClaimNationList,
            }
            Table["Map"] = {
                "Title": "Member Claims Locations",
                "Headers": ["Claim Locations"],
                "Body": [[Map]],
            }
        if len(KillList) > 0:
            Table["2"] = {
                "Title": "Users Murdered",
                "Headers": ["User Killed", "Weapon"],
                "Body": KillList,
            }

        if len(DeathList) > 0:
            Table["3"] = {
                "Title": "Users Been Murdred By",
                "Headers": ["User Killed By", "Weapon"],
                "Body": DeathList,
            }
        if len(AchievementList) > 0:
            Table["4"] = {
                "Title": "Achievement List",
                "Headers": ["Achievement"],
                "Body": AchievementList,
            }

        if len(NicknameList) > 0:
            Table["5"] = {
                "Title": "Nickname List",
                "Headers": ["Nickname"],
                "Body": NicknameList,
            }
        if len(RoleList) > 0:
            Table["6"] = {
                "Title": "Role List",
                "Headers": ["Role"],
                "Body": RoleList,
            }

        UserModel = GetUserModel(User)

        return render_template(
            "index.html",
            title=UserModel + User,
            Table=Table,
            searchbox="Search Users...",
            list=Users,
            uri="player",
        )

    else:
        PlayTimeList = GetTop50UserTotalPlayTime()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific user."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Playtimes",
                "Headers": ["Index", "User", "Playtime"],
                "Body": PlayTimeList,
            },
        }
        return render_template(
            "index.html",
            title="User Info",
            Table=Table,
            searchbox="Search Users...",
            list=Users,
            uri="player",
        )


@app.route("/weapon")
def SearchWeapon() -> object:
    """Search for an indivigual weapon.

    Returns:
        HTML: index.html template with an items statistics
    """
    Item = request.args.get("search")
    if Item and Item != "None":
        Item = "[" + Item + "]"
    Users, Items, Achievements, Roles = GetAutocompleteLists()

    if Item := GetItem(Item):
        KillList = GetItemMurderList(Item)
        Table = {
            "1": {
                "Title": "Weapon Statistics",
                "Headers": ["Category", "Metric"],
                "Body": [["Number of murders using item", str(len(KillList))]],
            },
            "2": {
                "Title": "Deaths",
                "Headers": ["Murderer", "Victim"],
                "Body": KillList,
            },
        }
        return render_template(
            "index.html",
            title=Item.strip("[").strip("]"),
            Table=Table,
            searchbox="Search Weapons...",
            list=Items,
            uri="weapon",
        )

    else:
        ItemList = GetTop50Items()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific weapon."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Items",
                "Headers": ["Index", "Item", "Kills"],
                "Body": ItemList,
            },
        }

        return render_template(
            "index.html",
            title="Weapon Info",
            Table=Table,
            searchbox="Search Items...",
            list=Items,
            uri="weapon",
        )


@app.route("/achievement")
def SearchAchievement() -> object:
    """Search for a Achievement.

    Returns:
        HTML: index.html template with achievement statistics.
    """
    achievement = request.args.get("search")
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    if AchievementList := GetAchievementList(achievement):
        Table = {
            "1": {
                "Title": "Achievement Statistics",
                "Headers": ["Category", "Metric"],
                "Body": [
                    ["Number of users holding achievement", str(len(AchievementList))]
                ],
            },
            "2": {
                "Title": "Users holding Achievement",
                "Headers": ["Users"],
                "Body": AchievementList,
            },
        }
        return render_template(
            "index.html",
            title=achievement,
            Table=Table,
            searchbox="Search Achievements...",
            list=Achievements,
            uri="achievement",
        )
    else:
        AchievementList = GetTop50Achievement()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific achievement."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Achievements Earned",
                "Headers": ["Index", "Achievement", "Count"],
                "Body": AchievementList,
            },
        }
        return render_template(
            "index.html",
            title="Achievement Info",
            Table=Table,
            searchbox="Search Achievements...",
            list=Achievements,
            uri="achievement",
        )


@app.route("/role")
def SearchRole() -> object:
    """Search for a role.

    Returns:
        HTML: index.html template with role statistics.
    """
    role = request.args.get("search")
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    if RoleList := GetRoleList(role):
        Table = {
            "1": {
                "Title": "Role Statistics",
                "Headers": ["Category", "Metric"],
                "Body": [["Number of users holding role", str(len(RoleList))]],
            },
            "2": {"Title": "Users with Role", "Headers": ["Users"], "Body": RoleList},
        }
        return render_template(
            "index.html",
            title=role,
            Table=Table,
            searchbox="Search Roles...",
            list=Roles,
            uri="role",
        )
    else:
        RoleList = GetTop50Roles()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific role."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Roles Used",
                "Headers": ["Index", "Role", "Count"],
                "Body": RoleList,
            },
        }
        return render_template(
            "index.html",
            title="Role Info",
            Table=Table,
            searchbox="Search Roles...",
            list=Roles,
            uri="role",
        )


@app.route("/claim")
def SearchClaim() -> object:
    """Search for a claim.

    Returns:
        HTML: index.html template with claim statistics.
    """
    claim = request.args.get("search")
    Claims = GetAllClaims()
    ClaimLevel, ClaimCoords, ClaimChunks, ClaimNation, UserList = GetClaimInfo(claim)
    Map = GenerateMap(MAP, [claim], False)
    if ClaimLevel:
        Table = {
            "1": {
                "Title": "Claim Statistics",
                "Headers": ["Category", "Metric"],
                "Body": [
                    ["Level", str(ClaimLevel)],
                    ["Coords", str(ClaimCoords)],
                    ["Chunks", str(ClaimChunks)],
                    ["Nation", str(ClaimNation)],
                    ["Players", len(UserList)],
                ],
            },
            "2": {
                "Title": "Claim Location",
                "Headers": ["Location"],
                "Body": [[Map]],
            },
            "3": {
                "Title": "Users Registered to Claim",
                "Headers": ["Users"],
                "Body": UserList,
            },
        }
        return render_template(
            "index.html",
            title=claim,
            Table=Table,
            searchbox="Search Claims...",
            list=Claims,
            uri="claim",
        )
    else:
        ClaimUserList = Top50LargestClaimByUsers()
        ClaimChunkList = Top50LargestClaimByChunks()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific claim."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Claims by Users",
                "Headers": ["Index", "Claim", "Users"],
                "Body": ClaimUserList,
            },
            "3": {
                "Title": "Top 50 Claims by Chunks",
                "Headers": ["Index", "Claim", "Chunks"],
                "Body": ClaimChunkList,
            },
        }
        return render_template(
            "index.html",
            title="Claim Info",
            Table=Table,
            searchbox="Search Claims...",
            list=Claims,
            uri="claim",
        )


@app.route("/nation")
def SearchNation() -> object:
    """Search for a nation.

    Returns:
        HTML: index.html template with nation statistics.
    """
    nation = request.args.get("search")
    Nations = GetAllNations()
    (
        NationLevel,
        CaptialCoords,
        Captial,
        NationChunks,
        NationPlayers,
        NationClaims,
    ) = GetNationInfo(nation)

    ClaimList = GetNationClaimList(nation)
    NationCaptial = GetNationCapital(nation)
    Map = GenerateMap(MAP, ClaimList, True, NationCaptial)

    if NationLevel:
        Table = {
            "1": {
                "Title": "Nation Statistics",
                "Headers": ["Category", "Metric"],
                "Body": [
                    ["Level", str(NationLevel)],
                    ["Chunks", str(NationChunks)],
                    ["Players", str(NationPlayers)],
                    ["Capital", str(Captial)],
                    ["Capital Coords", str(CaptialCoords)],
                ],
            },
            "2": {
                "Title": "Map of Claims Registered to the Nation",
                "Headers": ["Locations"],
                "Body": [[Map]],
            },
            "3": {
                "Title": "Claims Registered to the Nation",
                "Headers": ["Claim", "Users"],
                "Body": NationClaims,
            },
        }
        return render_template(
            "index.html",
            title=nation,
            Table=Table,
            searchbox="Search Nations...",
            list=Nations,
            uri="nation",
        )
    else:
        NationUserList = Top50LargestNationByUsers()
        NationChunkList = Top50LargestNationByChunks()
        NationClaimList = Top50LargestNationByClaims()
        Table = {
            "1": {
                "Title": "INFO",
                "Headers": [""],
                "Body": [
                    [
                        "Use the search box at the top of the page to search for a specific nation."
                    ]
                ],
            },
            "2": {
                "Title": "Top 50 Nations by Users",
                "Headers": ["Index", "Nation", "Users"],
                "Body": NationUserList,
            },
            "3": {
                "Title": "Top 50 Nations by Chunks",
                "Headers": ["Index", "Nation", "Chunks"],
                "Body": NationChunkList,
            },
            "4": {
                "Title": "Top 50 Nations by Claims",
                "Headers": ["Index", "Nation", "Claims"],
                "Body": NationClaimList,
            },
        }
        return render_template(
            "index.html",
            title="Nation Info",
            Table=Table,
            searchbox="Search Nations...",
            list=Nations,
            uri="nation",
        )


@app.route("/info")
def info() -> object:
    Users, Items, Achievements, Roles = GetAutocompleteLists()

    Table = {
        "1": {
            "Title": "Plz",
            "Headers": [""],
            "Body": [
                [
                    "This is a personal project and only updates while the website is running. If you try and break it, it will break."
                ],
                [
                    "IF you wish to attempt to break it please message me on discord prior (xander2508#8106) so I can fix it."
                ],
                [""],
                ["WHEN you spot a bug message me on discord (xander2508#8106)."],
                [""],
                [
                    "This website is run off a free cloud server and therefore is vulnerable to outages. I will do my best to maintain it but be aware."
                ],
                [""],
                [
                    "Database can be made avalable on request if there is a good use case. Also if you are good at front-end dev hit me up."
                ],
                [""],
                ["Feel free to donate to xander2508 however much you can."],
                ["/pay xander2508 1000"],
            ],
        }
    }
    return render_template(
        "index.html",
        title="Info Page",
        Table=Table,
        searchbox="Search Players...",
        list=Users,
        uri="player",
    )


def RunDebugWebsite():
    app.run(host="127.0.0.1", port=80, debug=True)


def RunWebsite():
    app.run(host="0.0.0.0", port=80, debug=False)
    return app


if __name__ == "__main__":
    RunDebugWebsite()
