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
        
    return matchups


def create_todays_dataset_p1():
    """Creates a dataset identical to the one used for the ML modeling. This is done by scraping the ngames averages
    of the teams just listed, along with the spread, and cominbing. 
    """
    
    
    """Find teams. 
    """
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    
    
    matchups = get_todays_games()[1:]
    
    #matchups
    import numpy as np
    from nba_py import team
    teams = team.TeamList()
    teamids = teams.info()
    teamids = teamids[:-15]
    teamids = teamids[['TEAM_ID','ABBREVIATION']]
    teamids = teamids.rename(index=str, columns={"ABBREVIATION": "Team"})
    teamids = teamids.replace('BKN','BRK')
    teamids = teamids.sort_values('Team')

    todays_dataframe = []
    for matchup in matchups:
        game_array = []
        for team_ in matchup:
            TEAM_ID = teamids.loc[teamids['Team'] == team_].values[0,0]
            #print(team_,TEAM_ID)
        
            TEAM_splits = team.TeamLastNGamesSplits(team_id=TEAM_ID,season='2018-19')
       # print(TEAM_splits.last20())
            df = TEAM_splits.last20()
        
            #retain (and create) the columns already proven to be statistically correlated to outcome. 
            df['AST/TO'] = df['AST']/df['TOV']

            df = df[['FGM','FG3M','FTM','DREB','AST','STL',
                     'TOV','BLK','PTS','AST/TO','FG3_PCT',
                     'FG_PCT','FT_PCT']]
           # df['AST/TO'] = df['AST']/df['TOV']
            game_array.append(df.values)
        
        matchup_array = np.concatenate((game_array[0],game_array[1]),axis=1)
        todays_dataframe.append(matchup_array)

    #quick formating!
    todays_dataframe = np.array(todays_dataframe)
    todays_dataframe = todays_dataframe[:,0,:]
    return todays_dataframe

def scrape_espn_for_today_spreads(todays_dataframe):
    """Scrape and clean from ESPN, which has the info of all NBA games today and their lines. 
    """
    from bs4 import BeautifulSoup
    import pandas as pd
    import urllib
    matchups = get_todays_games()[1:]


    url  = "http://www.espn.com/nba/lines/_/date"
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")
    tables = soup.find_all('table')
    table_df = pd.DataFrame([])
    for table in tables:
        table_df =table_df.append(pd.read_html(str(table)))

    team_that_plays = []
    spread_of_that_team = []
    for i, row in enumerate(table_df[1]):
        if row == 'SPREAD':
           # print(row)
            try:
           #     print(table_df[1][i+1])
        
                eh = table_df[1][i+1]
            except: 
                eh = table_df[1][i+2]
          #      print(eh)

            sign = eh[0]
            try:
                spread, _ = eh[1:6].split('-')
            except:
                spread, _ = eh[1:6].split('+')

       # spread, _ = eh[0:5].split('-')
       # print(spread)
           # print(sign + spread)
            for i, char in enumerate(eh): 
                team = eh[i:i+3]

                if char.isalpha():
                    team = eh[i:i+3]
                    if team[-1].isalpha() == False:
                        if team == 'SA:':
                            team = 'SAS'
                        if team == 'NY:':
                            team = 'NYK'
                        if team == 'GS:':
                            team = 'GSW'
                    else:
                        if team == 'WSH':
                            team = 'WAS'
                        if team  == 'UTAH':
                            team = 'UTA'
                        if team == 'BKN':
                            team = 'BRK'
                    #print(team)

                    break
    
              #  if eh[i+3].isalpha() == False:
              #      print(team)
              #      print("BAD!!")
               # team = eh[i:i+3]
             ##   if team =='SA':
             #       team = 'SAS'

               # break
                
        
        
       # print("Spread of the game? " , team, sign+spread)
            team_that_plays.append(team)
            spread_of_that_team.append(sign+spread)
            
    home_spread = []
   # print("TEAM THAT PLAYS:")
   # print(team_that_plays)
    for s,team in enumerate(team_that_plays):
      #  print(team)
        for game in matchups:
            try:
                ind = game.index(team)
                if ind == 0:
                  #  print(team + " is on the road")
                 #   print("home spread is therefore opposite of ",float(spread_of_that_team[s]))
                 #  print("home spread is therefore ",-float(spread_of_that_team[s]))
                    home_spread.append(-float(spread_of_that_team[s]))

                else:
                 #   print(team + " is at home")
                    home_spread.append(-float(spread_of_that_team[s]))
    

            except:
                pass
        
    ready_for_it = []
    for i in range(len(todays_dataframe)):
        ready = list(todays_dataframe[i])
        ready.append(home_spread[i])
        ready_for_it.append(ready)
  # todays_dataframe[i] = list(todays_dataframe[i]).append(home_spread[i])

    ready_for_it = np.array(ready_for_it)
    
    return matchups,ready_for_it



todays_splits = create_todays_dataset_p1()


matchups, data = scrape_espn_for_today_spreads(todays_splits)


import pickle 

#print("Loading in models...")

model_path = '../models/finalized_model.sav'
# load the model from disk
loaded_model = pickle.load(open(model_path, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

scaler_path = '../models/finalized_scaler.sav'
loaded_scaler = pickle.load(open(scaler_path, 'rb'))

X_today = data


X_today = loaded_scaler.transform(X_today)

for i,game in enumerate(X_today):
    prediction = loaded_model.predict([game])[0]
    
    print("Game: ", matchups[i])
    print("Winner: ",matchups[i][prediction])





def spread2ML(spread):
    """Converts spread into a moneyline value using the equation I calculated. 
    """
    if spread <=1.5:
        
        ML = 1.71409498 * spread**3 + 10.90008433 * spread **2 + 22.40247106 * spread - 138.20112341
    else: 

        ML = 1.66494668 * spread**3 -20.03302374 * spread**2 + 101.20347437 * spread - 34.68833849
    
    return ML


f = open("output.txt", "a")
spreads = data[:,-1]
for i,game in enumerate(X_today):
    prediction = loaded_model.predict([game])[0]
    

    f.write("Game: " + str(matchups[i][0]) + ' @ ' + str(matchups[i][1])+'\n')
    f.write("Predicted Winner: " + str(matchups[i][prediction])+'\n')
    f.write("Home Team Spread: " + str(matchups[i][1]) + str(spreads[i])+'\n')
    f.write("Approximate Moneyline Odds: " + str(matchups[i][0])+str(spread2ML(-spreads[i]))+" "+str(matchups[i][1])+str(spread2ML(spreads[i]))+'\n')
    #f.write()

f.close()

