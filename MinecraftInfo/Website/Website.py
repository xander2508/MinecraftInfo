from flask import Flask, render_template, request

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from MinecraftInfo.Util.SqlQueries import (
    GetAchievementList,
    GetAllAchievements,
    GetAllItems,
    GetAllRoles,
    GetAllUsers,
    GetItem,
    GetItemMurderList,
    GetRoleList,
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
    GetUserCurrentPlayTime,
    GetUserDeathCount,
    GetUserDeathList,
    GetUserMessageCount,
    GetUserMurderCount,
    GetUserMurderList,
    GetUsername,
    GetUserNickname,
    GetUserRole,
    GetUserTotalPlayTime,
)

app = Flask(__name__)


def GetAutocompleteLists() -> tuple(str, str, str, str):
    """Retrieve the lists of searchable terms within the website.

    Returns:
        str: The string list of the searchable terms.
    """
    Users = str(GetAllUsers())
    Items = str(GetAllItems())
    Achievements = str(GetAllAchievements())
    Roles = str(GetAllRoles())
    return Users, Items, Achievements, Roles


@app.route("/")
def Index() -> object:
    """Display the index webpage containing the top statistics.

    Returns:
        HTML: index.html template with top statistics.
    """
    Users, Items, Achievements, Roles = GetAutocompleteLists()

    MessagesSent = GetTopUserMessagesCount()
    Playtime = GetTopUserTotalPlayTime()
    Kills = GetTopUserKiller()
    Deaths = GetTopUserDeaths()
    TopUserAchievement = GetTopUserAchievementCount()
    TopAchievement = GetTopAchievementCount()
    Role = GetTopUserRole()
    Item = GetTopItem()

    Table = {
        "1": {
            "Title": "Top Statistics",
            "Headers": ["Catagory", "Username", "Metric"],
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
                    "<a href=/player?search=" + Deaths[0] + ">" + Deaths[0] + "</a>",
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
                    + Role[0].replace(" ", "+")
                    + ">"
                    + Role[0]
                    + "</a>",
                    Role[1],
                ],
                [
                    "Deadliest Item",
                    "<a href=/item?search="
                    + Item[0].strip("[").strip("]").replace(" ", "+")
                    + ">"
                    + Item[0].strip("[").strip("]")
                    + "</a>",
                    Item[1],
                ],
            ],
        }
    }

    return render_template(
        "index.html",
        title="Home",
        usernames=Users,
        items=Items,
        achievements=Achievements,
        roles=Roles,
        Table=Table,
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

        LoginTimeIcon = "🔴"
        CurrentPlaytime = 0
        if LoginTime:
            CurrentPlaytime = LastSeenOnline - LoginTime
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
                        str(float("{:.2f}".format(Playtime / 3600000))) + " Hours",
                    ],
                    ["Kill Count", Kills],
                    ["Death Count", Deaths],
                    ["Achievement Count", Achievement],
                    [
                        "Current Role",
                        "<a href=/role?search="
                        + Role.replace(" ", "+")
                        + ">"
                        + Role
                        + "</a>",
                    ],
                    ["Current Nickname", Nickname],
                    ["Online", LoginTimeIcon],
                    ["Current Playtime", CurrentPlaytime],
                ],
            },
            "2": {
                "Title": "Users Murdered",
                "Headers": ["User Killed", "Weapon"],
                "Body": KillList,
            },
            "3": {
                "Title": "Users Been Murdred By",
                "Headers": ["User Killed By", "Weapon"],
                "Body": DeathList,
            },
            "4": {
                "Title": "Achievement List",
                "Headers": ["Achievement"],
                "Body": AchievementList,
            },
        }

        return render_template(
            "index.html",
            title=User,
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )

    else:
        Table = {
            "1": {
                "Title": "User Not Found",
                "Headers": ["Catagory", "Metric"],
                "Body": [
                    ["Messages Sent", "N/A"],
                    ["Playtime", "N/A"],
                    ["Kill Count", "N/A"],
                    ["Death Count", "N/A"],
                    ["Achievement Count", "N/A"],
                    ["Current Role", "N/A"],
                    ["Current Nickname", "N/A"],
                ],
            }
        }
        return render_template(
            "index.html",
            title="User Info",
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )


@app.route("/item")
def SearchItem() -> object:
    """Search for an indivigual item.

    Returns:
        HTML: index.html template with an items statistics
    """
    Item = request.args.get("search")
    Item = "[" + Item + "]"
    Users, Items, Achievements, Roles = GetAutocompleteLists()

    if Item := GetItem(Item):
        KillList = GetItemMurderList(Item)
        Table = {
            "1": {
                "Title": "Item Statistics",
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
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )

    else:
        Table = {
            "1": {
                "Title": "Item Not Found",
                "Headers": ["Murderer", "Victim"],
                "Body": [
                    ["N/A", "N/A"],
                ],
            }
        }
        return render_template(
            "index.html",
            title="Item Info",
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
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
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )
    else:
        Table = {
            "1": {
                "Title": "Achievement Not Found",
                "Headers": ["Users with the Achievement"],
                "Body": [
                    ["N/A"],
                ],
            }
        }
        return render_template(
            "index.html",
            title="Achievement Info",
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
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
                "Body": [["Number of users holding achievement", str(len(RoleList))]],
            },
            "2": {"Title": "Users with Role", "Headers": ["Users"], "Body": RoleList},
        }
        return render_template(
            "index.html",
            title=role,
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )
    else:
        Table = {
            "1": {
                "Title": "Role Not Found",
                "Headers": ["Users with the Role"],
                "Body": [
                    ["N/A"],
                ],
            }
        }
        return render_template(
            "index.html",
            title="Role Info",
            Table=Table,
            usernames=Users,
            items=Items,
            achievements=Achievements,
            roles=Roles,
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
