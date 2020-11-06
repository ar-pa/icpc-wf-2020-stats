import json
import urllib.request
from math import log10
from time import time

import tabulate


def get_win_probability(ra, rb):
    return 1.0 / (1.0 + pow(10.0, (rb - ra) / 400.0))


def aggregate_ratings(team_ratings):
    if len(team_ratings) == 0:
        return 0

    left = 1
    right = 1E4

    for tt in range(100):
        r = (left + right) / 2.0

        rWinsProbability = 1.0
        for i in range(len(team_ratings)):
            rWinsProbability *= get_win_probability(r, team_ratings[i])

        rating = log10(1 / rWinsProbability - 1) * 400 + r

        if rating > r:
            left = r
        else:
            right = r

    return (left + right) / 2.0


def get_rating(handle):
    cached_ratings = json.loads(open('cached_ratings', 'r').read())
    for row in cached_ratings:
        if row[0] == handle:
            return row[1]
    try:
        res = json.loads(urllib.request.urlopen("https://codeforces.com/api/user.info?handles=" + handle).read())
        if res['status'] == 'OK':
            if not ('rating' in res['result'][0]):
                res['result'][0]['rating'] = 1500
            cached_ratings.append([handle, res['result'][0]['rating']])
            to_write = open('cached_ratings', 'w')
            to_write.write(json.dumps(cached_ratings))
            to_write.close()
            print(handle, res['result'][0]['rating'])
            return res['result'][0]['rating']
        else:
            print("user " + handle + " error")
            return 0
    except Exception as e:
        print(e)


def get_number_of_submissions(handle):
    SECONDS_PER_MONTH = 30 * 24 * 60 * 60
    cached_status = json.loads(open('cached_status', 'r').read())
    for row in cached_status:
        if row[0] == handle:
            return row[1]
    try:
        res = json.loads(
            urllib.request.urlopen("https://codeforces.com/api/user.status?count=1000&handle=" + handle).read())
        if res['status'] == 'OK':
            res = res['result']
            cnt = 0
            for submission in res:
                if time() - submission["creationTimeSeconds"] > SECONDS_PER_MONTH:
                    break
                if submission["verdict"] == "OK":
                    cnt += 1
            cached_status.append([handle, cnt])
            to_write = open('cached_status', 'w')
            to_write.write(json.dumps(cached_status))
            to_write.close()
            print(handle + " accepted ", cnt)
            return cnt
        else:
            print("user " + handle + " error")
            return 0
    except Exception as e:
        print(e)


def get_team_rating(team_members):
    team_members_rating = []
    for member in team_members:
        team_members_rating.append(int(get_rating(member)))
    return aggregate_ratings(team_members_rating)


def get_team_list():
    plain_team_list_lines = open('plain_team_list', 'r').readlines()
    teams = []
    for team in plain_team_list_lines:
        teams.append(team[:-1].split('\t'))
    return teams


teams = get_team_list()
for team in teams:
    if len(team[1]) > 20:
        team[1] = team[1][0:18] + "..."
    team.append(get_team_rating([team[2], team[3], team[4]]))
    team.append(sum(get_number_of_submissions(member) for member in team[2:5]))
teams.sort(key=lambda t: t[5], reverse=True)
print(tabulate.tabulate(teams, showindex=True))
