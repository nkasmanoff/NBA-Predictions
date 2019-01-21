from datetime import datetime
from nba_py import Scoreboard
import numpy as np
import pandas as pd

today = datetime.now()
day = today.day
month = today.month
year = today.year
f = open("output.txt", "a")
f.write('\n')

f.write(str(month)+'/'+str(day)+'/'+str(year)+'\n')
f.write("----------"+'\n')
f.close()

def get_todays_games():
    """
    Get the game's going on today. 
    
    Parameters:
    -----------
    
    None
    
    
    Returns 
    -------
    
    matchups : arr
        array of all the matchups today. Note I skip the first element since it just denotes road, or home which is known
        now. 
        
        
    
    """
    
    
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
 
    ex = Scoreboard(month=month,day=day,year=year)
    games = ex.game_header()['GAMECODE']
    matchups = []
    matchups.append(['road','home'])
    for game in games:
        away_team = game[-6:-3]
        home_team = game[-3:]

        if away_team == 'BKN':
            away_team = 'BRK'
        if home_team == 'BKN':
            home_team = 'BRK'
        
        matchups.append([away_team,home_team])
        
    return matchups[1:]

def create_todays_data():
    """Creates a dataset identical to the one used for the ML modeling. This is done by scraping the ngames averages
    of the teams just listed, along with the spread, and cominbing. 
    
    Returns 
    -------
    
    today_matchups : arr
        In accordance with the designated format of how these team statistics will be shaped, I did that here. 
        For further explanation, please refer to the "relevant stats" and "splits_optimizer" repo's which explain why I 
        use certain values, this function simply puts them in that shape for the games I want to predict. 
    
    
    home_teams : arr
        Array of the home teams. Since I next have to obtain the spread of these games, I'll line them up based on the 
        name of the home team. 
    """
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    
    
    matchups = get_todays_games()
    
    #matchups
    import numpy as np
    from nba_py import team
    teams = team.TeamList()
    teamids = teams.info()
    #print('predicting matchups of ', teamids)
  #  print()
    teamids = teamids[:-15]
   # print(teamids)
    teamids = teamids[['TEAM_ID','ABBREVIATION']]
    teamids = teamids.rename(index=str, columns={"ABBREVIATION": "Team"})
    teamids = teamids.replace('BKN','BRK')
    teamids = teamids.sort_values('Team')
   # print(teamids)
    todays_matchups = []
    home_teams = []
    road_teams = []
    for matchup in matchups:
        home_teams.append(matchup[1])
        road_teams.append(matchup[0])
        game_array = []
        for team_ in matchup:
            TEAM_ID = teamids.loc[teamids['Team'] == team_].values[0,0]
         #   print(team_,TEAM_ID)
        
            TEAM_splits = team.TeamLastNGamesSplits(team_id=TEAM_ID,season='2018-19')
       # print(TEAM_splits.last20())
            df = TEAM_splits.last20()
        
            #retain (and create) the columns proven to be correlated to outcome. 
            df['AST/TO'] = df['AST']/df['TOV']

            df = df[['FGM','FG3M','FTM','DREB','AST','STL',
                     'TOV','BLK','PTS','AST/TO','FG3_PCT',
                     'FG_PCT','FT_PCT']]
           # df['AST/TO'] = df['AST']/df['TOV']
            game_array.append(df.values)
        
        matchup_array = np.concatenate((game_array[0],game_array[1]),axis=1)
        todays_matchups.append(matchup_array)

    #quick formating!
    todays_matchups = np.array(todays_matchups)
    todays_matchups = todays_matchups[:,0,:]
    return todays_matchups,home_teams,road_teams

#will use this cell to see if I can scrape Fox for a better result than ESPN. 

def scrape_fox():
    """
    
    Scrape fox sports website for today's games and spreads. For variations, use average? 
    
    Parameters
    ----------
    
    None
    
    Returns 
    -------
    
    todays_spreads : dict
        Dictionary of the home team, and what their line is (road team has the opposite spread)
    
    """
    from numpy import mean

    url = "https://www.foxsports.com/nba/odds"
    from bs4 import BeautifulSoup
  #  import pandas as pd
    import urllib
    from urllib.request import urlopen



    client = urlopen(url)
    page_html = client.read()
    page_soup = BeautifulSoup(page_html,'html.parser')
    todays_spreads = {}

    for game in page_soup.find_all('div',class_ = 'wisbb_gameWrapper'):
        new = game.findAll('div')[3].findAll('table')[0]
        #class="wisbb_runLinePtsCol"
       # print(new.findAll(class_='wisbb_teamsCol')[0].text)
        #print(new.findAll(class_='wisbb_runLinePtsCol')[0].text)
        road_team = new.findAll(class_='wisbb_teamsCol')[0].text[0:3]
        home_team = new.findAll(class_='wisbb_teamsCol')[0].text[3:]
        if home_team == 'BKN':
            home_team = 'BRK'
        spreads = new.findAll(class_='wisbb_runLinePtsCol')

        home_spreads_floats = []
        for spread in spreads:
            #There are multiple books, just average them!
            home_spreads_floats.append(float(list(spread.children)[-1]))
    
        home_spread = mean(home_spreads_floats)
        
        
        road_spread = new.findAll(class_='wisbb_teamsCol')[0].text.split
       # print("Road team: ", road_team)
       # print("home team " , home_team)
       # print("home spread ", home_spread)
        #print("Road spread:", new.findAll(class_='wisbb_runLinePtsCol')[0].text[0:2])
        todays_spreads[home_team] = home_spread
#tables = soup.find_all('table')
    return todays_spreads

def model_ready_data():
    """Combine the data acquisition tools already made, and combine into an array capable of being fed into and used
    for an insight regarding the expected winner of today's games. 
    
    
    Returns
    -------
    
    todays_matchups_with_spreads : arr
        The input ready format of the game's going on today. 
        
    """
    
    from numpy import array
    todays_matchups,home_teams,road_teams = create_todays_data()
    todays_spreads = scrape_fox()
    
    todays_matchups_with_spreads = []
    for t, m in zip(home_teams, todays_matchups):
   # print(m.extend((todays_spreads[t])))
        m = np.append(m,todays_spreads[t])
        todays_matchups_with_spreads.append(m)# np.append(todays_matchups_with_spreads,m)t
    todays_matchups_with_spreads = array(todays_matchups_with_spreads)
    
    return todays_matchups_with_spreads,home_teams,road_teams
X,home_teams,road_teams = model_ready_data()
import pickle 
model_path = '../models/finalized_model.sav'
# load the model from disk
loaded_model = pickle.load(open(model_path, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

scaler_path = '../models/finalized_scaler.sav'
loaded_scaler = pickle.load(open(scaler_path, 'rb'))

X_today = loaded_scaler.transform(X)


def spread2ML(spread):
    """Converts spread into a moneyline value using the equation I calculated. 
    """
    if spread <=1.5:
        
        ML = 1.71409498 * spread**3 + 10.90008433 * spread **2 + 22.40247106 * spread - 138.20112341
    else: 

        ML = 1.66494668 * spread**3 -20.03302374 * spread**2 + 101.20347437 * spread - 34.68833849
    
    return ML

f = open("output.txt", "a")

for i,game in enumerate(X_today):
    f.write("Game: " + road_teams[i] +' @ ' + home_teams[i])

    prediction = loaded_model.predict([game])
    if prediction == 0:
        
        f.write("Predicted winner is " + road_teams[i])
    else: 
        f.write("Predicted winner is " + home_teams[i])

   # print("Game: ", matchups[i][0], ' @ ', matchups[i][0])
    f.write("Home Team Spread: " + str(X[i][-1]))
    #print("Approximate Moneyline Odds: ",matchups[i][0],spread2ML(-spreads[i]),matchups[i][1],spread2ML(spreads[i]))

f.close()
