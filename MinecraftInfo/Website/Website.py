import sqlite3
from flask import Flask, request, render_template
from contextlib import closing

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('MinecraftInfo\DataStorage\DataStorage.db')
    conn.row_factory = sqlite3.Row
    return conn

def GetAutocompleteLists():
    Users = []
    Items = []
    Achievements = []
    Roles = []
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT Name FROM Users")
        rows = cursor.fetchall()
        for i in rows:
            Users.append(i[0])
        cursor.execute("SELECT Name FROM Items")
        rows = cursor.fetchall()
        for i in rows:
            Items.append(i[0].strip("[").strip("]"))
        cursor.execute("SELECT Achievement FROM Achievements")
        rows = cursor.fetchall()
        for i in rows:
            Achievements.append(i[0])

        cursor.execute("SELECT Role FROM Roles")
        rows = cursor.fetchall()
        for i in rows:
            Roles.append(i[0])

    Users = str(Users)
    Items = str(Items)
    Achievements = str(Achievements)
    Roles = str(Roles)
    return Users, Items, Achievements, Roles

@app.route("/")
def index():
    Users = []
    MessagesSent = []
    Playtime = []
    Kills = []
    Deaths = []
    Achievements = []
    Items = []
    Role = []
    Item = []

    Users, Items, Achievements, Roles = GetAutocompleteLists()
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT Name,MAX(MessagesSent) FROM Users")
        rows = cursor.fetchall()
        MessagesSent = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT Name,MAX(TotalPlayTime) FROM Users")
        rows = cursor.fetchall()
        Playtime = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT UserKiller,COUNT(UserKiller) FROM Deaths GROUP BY UserKiller ORDER BY COUNT(UserKiller) DESC LIMIT 1")
        rows = cursor.fetchall()
        Kills = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT UserDead,COUNT(UserDead) FROM Deaths GROUP BY UserDead ORDER BY COUNT(UserDead) DESC LIMIT 1")
        rows = cursor.fetchall()
        Deaths = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT User,COUNT(User) FROM AchievementLinks GROUP BY User ORDER BY COUNT(User) DESC LIMIT 1")
        rows = cursor.fetchall()
        TopUserAchievement = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT Achievement ,COUNT(Achievement) FROM AchievementLinks GROUP BY Achievement ORDER BY COUNT(Achievement) DESC LIMIT 1")
        rows = cursor.fetchall()
        TopAchievement = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT Role,COUNT(Role) FROM RoleLinks WHERE NOT Role='None' GROUP BY Role ORDER BY COUNT(Role) DESC LIMIT 1")
        rows = cursor.fetchall()
        Role = [rows[0][0],rows[0][1]]

        cursor.execute("SELECT ItemUsed,COUNT(ItemUsed) FROM Deaths GROUP BY ItemUsed ORDER BY COUNT(ItemUsed) DESC LIMIT 1")
        rows = cursor.fetchall()
        Item = [rows[0][0],rows[0][1]]

    Table = {"1":{"Title":"Top Statistics", "Headers":["Catagory","Username","Metric"],"Body":[
        ["Most Messages Sent",'<a href=/player?search='+MessagesSent[0]+'>'+MessagesSent[0]+'</a>',MessagesSent[1]],
        ["Most Playtime",'<a href=/player?search='+Playtime[0]+'>'+Playtime[0]+'</a>',str(float("{:.2f}".format(Playtime[1]/3600000)))+" Hours"],
        ["Top Kills",'<a href=/player?search='+Kills[0]+'>'+Kills[0]+'</a>',Kills[1]],
        ["Top Deaths",'<a href=/player?search='+Deaths[0]+'>'+Deaths[0]+'</a>',Deaths[1]],
        ["Most Achievements",'<a href=/player?search='+TopUserAchievement[0]+'>'+TopUserAchievement[0]+'</a>',TopUserAchievement[1]],
        ["Most Popular Achievement",'<a href=/achievement?search='+TopAchievement[0].replace(" ","+")+'>'+TopAchievement[0]+'</a>',TopAchievement[1]],
        ["Most Popular Role",'<a href=/role?search='+Role[0].replace(" ","+")+'>'+Role[0]+'</a>',Role[1]],
        ["Deadliest Item",'<a href=/item?search='+Item[0].strip("[").strip("]").replace(" ","+")+'>'+Item[0].strip("[").strip("]")+'</a>',Item[1]],
        ]}}

    return render_template('index.html', title = "Home",usernames = Users, items=Items, achievements=Achievements, roles=Roles,  Table = Table)

@app.route("/player")
def searchPlayer():
    player = request.args.get('search')
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT Name FROM Users WHERE Name=(?) LIMIT 1", (player,))
        rows = cursor.fetchall()
        try:
            User = rows[0][0]
        except:
            Table = {"1":{"Title":"User Not Found", "Headers":["Catagory","Metric"],"Body":[
            ["Messages Sent","N/A"],
            ["Playtime","N/A"],
            ["Kill Count", "N/A"],
            ["Death Count", "N/A"],
            ["Achievement Count","N/A"],
            ["Current Role","N/A"],
            ["Current Nickname","N/A"],
            ]}}
            return render_template('index.html',title = "User Info", Table = Table,usernames = Users, items=Items, achievements=Achievements, roles=Roles)

        try:
            cursor.execute("SELECT MessagesSent FROM Users WHERE Name = (?) LIMIT 1",(User,))
            rows = cursor.fetchall()
            MessagesSent = rows[0][0]
        except:
            MessagesSent = 0

        try:
            cursor.execute("SELECT TotalPlayTime FROM Users WHERE Name = (?) LIMIT 1", (User,))
            rows = cursor.fetchall()
            Playtime = rows[0][0]
        except:
            Playtime = 0

        try:
            cursor.execute("SELECT LoginTime,LastSeenOnline FROM Users WHERE Name = (?) LIMIT 1", (User,))
            rows = cursor.fetchall()
            LoginTime, LastSeenOnline = int(rows[0][0]), int(rows[0][1])
            LoginTimeIcon = "🔴"
            CurrentPlaytime =0
            if LoginTime:
                CurrentPlaytime = LastSeenOnline-LoginTime
                LoginTimeIcon = "🟢"
        except:
            LoginTimeIcon = "🔴"
            CurrentPlaytime = 0

        try:
            cursor.execute("SELECT COUNT(UserKiller) FROM Deaths WHERE UserKiller = (?) LIMIT 1",(User,))
            rows = cursor.fetchall()
            Kills = rows[0][0]
        except:
            Kills = 0

        try:
            cursor.execute("SELECT COUNT(UserDead) FROM Deaths WHERE UserDead= (?) LIMIT 1",(User,))
            rows = cursor.fetchall()
            Deaths = rows[0][0]
        except:
            Deaths = 0

        try:
            cursor.execute("SELECT Role FROM RoleLinks WHERE User=(?) LIMIT 1",(User,))
            rows = cursor.fetchall()
            Role = rows[0][0]
        except:
            Role = "None"

        try:
            cursor.execute("SELECT Nickname FROM NicknameLinks WHERE Name=(?) LIMIT 1",(User,))
            rows = cursor.fetchall()
            Nickname = rows[0][0]
        except:
            Nickname = "None"
        
        try:
            cursor.execute("SELECT COUNT(User) FROM AchievementLinks WHERE User=(?)",(User,))
            rows = cursor.fetchall()
            Achievement = rows[0][0]
        except Exception as e:
            Achievement = 0

        if Nickname == User:
            Nickname = "None"

        try:
            cursor.execute("SELECT UserDead, ItemUsed FROM Deaths WHERE UserKiller = (?)",(User,))
            rows = cursor.fetchall()
            KillList = []
            for i in rows:
                KillList.append(['<a href=/player?search='+i[0]+'>'+i[0]+'</a>','<a href=/item?search='+i[1].strip("[").strip("]").replace(" ","+")+'>'+i[1].strip("[").strip("]")+'</a>'])
        except:
            KillList = []

        try:
            cursor.execute("SELECT UserKiller, ItemUsed FROM Deaths WHERE UserDead = (?)",(User,))
            rows = cursor.fetchall()
            DeathList = []
            for i in rows:
                DeathList.append(['<a href=/player?search='+i[0]+'>'+i[0]+'</a>','<a href=/item?search='+i[1].strip("[").strip("]").replace(" ","+")+'>'+i[1].strip("[").strip("]")+'</a>'])
        except:
            DeathList = []

        try:
            cursor.execute("SELECT Achievement FROM AchievementLinks WHERE User=(?)",(User,))
            rows = cursor.fetchall()
            AchievementList = []
            for i in rows:
                AchievementList.append(['<a href=/achievement?search='+i[0].replace(" ","+")+'>'+i[0]+'</a>'])
        except Exception as e:
            AchievementList = []


        Table = {"1":{"Title":"Top Statistics", "Headers":["Catagory","Metric"],"Body":[
        ["Messages Sent",MessagesSent],
        ["Playtime",str(float("{:.2f}".format(Playtime/3600000)))+" Hours"],
        ["Kill Count", Kills],
        ["Death Count", Deaths],
        ["Achievement Count",Achievement],
        ["Current Role",'<a href=/role?search='+Role.replace(" ","+")+'>'+Role+'</a>'],
        ["Current Nickname",Nickname],
        ["Online",LoginTimeIcon],
        ["Current Playtime",CurrentPlaytime],
        ]},"2":{"Title":"Users Murdered", "Headers":["User Killed","Weapon"],"Body":KillList},
        "3":{"Title":"Users Been Murdred By", "Headers":["User Killed By","Weapon"],"Body":DeathList},
        "4":{"Title":"Achievement List", "Headers":["Achievement"],"Body":AchievementList}}

        return render_template('index.html',title = User, Table = Table, usernames = Users, items=Items, achievements=Achievements, roles=Roles)

@app.route("/item")
def searchItem():
    item = request.args.get('search')
    item = "["+item+"]"
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT Name FROM Items WHERE Name=(?) LIMIT 1", (item,))
        rows = cursor.fetchall()
        try:
            item = rows[0][0]
        except:
            Table = {"1":{"Title":"Item Not Found", "Headers":["Murderer","Victim"],"Body":[
            ["N/A","N/A"],
            ]}}
            return render_template('index.html',title = "Item Info", Table = Table,usernames = Users, items=Items, achievements=Achievements, roles=Roles)
        try:
            cursor.execute("SELECT UserKiller,UserDead FROM Deaths WHERE ItemUsed = (?)",(item,))
            rows = cursor.fetchall()
            KillList = []
            for i in rows:
                KillList.append(['<a href=/player?search='+i[0]+'>'+i[0]+'</a>','<a href=/player?search='+i[1]+'>'+i[1]+'</a>'])
        except:
            KillList = []
        Table = {"1":{"Title":"Item Statistics", "Headers":["Category", "Metric"],"Body":[["Number of murders using item",str(len(KillList))]]},"2":{"Title":"Deaths", "Headers":["Murderer","Victim"],"Body":KillList}}
        return render_template('index.html',title = item.strip("[").strip("]"), Table = Table, usernames = Users, items=Items, achievements=Achievements, roles=Roles)

@app.route("/achievement")
def searchAchievement():
    achievement = request.args.get('search')
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT User FROM AchievementLinks WHERE Achievement=(?)", (achievement,))
        rows = cursor.fetchall()
        try:
            
            AchievementList = []
            for i in rows:
                AchievementList.append(['<a href=/player?search='+i[0]+'>'+i[0]+'</a>'])
        except:
            Table = {"1":{"Title":"Achievement Not Found", "Headers":["Users with the Achievement"],"Body":[
            ["N/A"],
            ]}}
            return render_template('index.html',title = "Achievement Info", Table = Table,usernames = Users, items=Items, achievements=Achievements, roles=Roles)
        Table = {"1":{"Title":"Achievement Statistics", "Headers":["Category", "Metric"],"Body":[["Number of users holding achievement",str(len(AchievementList))]]},"2":{"Title":"Users holding Achievement", "Headers":["Users"],"Body":AchievementList}}
        return render_template('index.html',title = achievement, Table = Table, usernames = Users, items=Items, achievements=Achievements, roles=Roles)

@app.route("/role")
def searchRole():
    role = request.args.get('search')
    Users, Items, Achievements, Roles = GetAutocompleteLists()
    con = get_db_connection()
    with closing(con.cursor()) as cursor:
        cursor.execute("SELECT User FROM RoleLinks WHERE Role=(?)", (role,))
        rows = cursor.fetchall()
        try:
            
            RoleList = []
            for i in rows:
                RoleList.append(['<a href=/player?search='+i[0]+'>'+i[0]+'</a>'])
        except:
            Table = {"1":{"Title":"Role Not Found", "Headers":["Users with the Role"],"Body":[
            ["N/A"],
            ]}}
            return render_template('index.html',title = "Role Info", Table = Table,usernames = Users, items=Items, achievements=Achievements, roles=Roles)
        Table = {"1":{"Title":"Role Statistics", "Headers":["Category", "Metric"],"Body":[["Number of users holding achievement",str(len(RoleList))]]},"2":{"Title":"Users with Role", "Headers":["Users"],"Body":RoleList}}
        return render_template('index.html',title = role, Table = Table, usernames = Users, items=Items, achievements=Achievements, roles=Roles)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)