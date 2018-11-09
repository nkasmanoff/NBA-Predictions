from datetime import datetime
from nba_py import Scoreboard
import numpy as np
import pandas as pd

def get_yesterdays_games():
    today = datetime.now()

    try:
        day = today.day-1
        month = today.month
        year = today.year
    except:
        print("Error: Is it a new month or new year?")
 
    ex = Scoreboard(month=month,day=day,year=year)
    yesterdays_games = ex.line_score()[['TEAM_ABBREVIATION','PTS','GAME_ID']]
    teams = []
    scores = []
    for i, game in enumerate(yesterdays_games.values):
        teams.append(game[0])
        scores.append(game[1])
    road_teams = teams[0::2]
    home_teams = teams[1::2]
    road_scores = scores[0::2]
    home_scores = scores[1::2]
    f = open("output.txt", "a")
    f.write('\n')
    f.write("Winners from " + str(month)+'/'+str(day)+'/'+str(year)+'\n')

    for i in range(len(road_teams)):

        if road_scores[i] > home_scores[i]:
            f.write(road_teams[i]+'\n')
        else:
            f.write(home_teams[i]+'\n')
    print("Done!")
    
    return 

get_yesterdays_games()