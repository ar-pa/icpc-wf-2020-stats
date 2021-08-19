import urllib3

changed = ["GiannisAntetokounmpo",
           "retrograd",
           "Reiketsu",
           "Light",
           "omar42",
           "Captain_Knuckles",
           "RedNova",
           "apiadu",
           "I_love_Y_UME",
           "_franz_",
           "Fischer",
           "Monogon",
           "emma",
           "chenvictor1999",
           "sincerity",
           "kolyukkonen",
           "pikmike",
           "Ne0n25",
           "ShavelV",
           "Sealionheart",
           "FlNALIST"]
http = urllib3.PoolManager()


def get_new(user):
    url = "https://www.codeforces.com/profile/" + user
    http.request('Get', url)
    page = http.request('Get', url)
    url = page.geturl()
    return url[url.rfind('/') + 1:]


teams = open('plain_team_list', 'r').read()
for user in changed:
    teams = teams.replace(user, get_new(user))

print(teams)
