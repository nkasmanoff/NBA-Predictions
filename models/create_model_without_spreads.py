
import pandas as pd
import numpy as np

df = pd.read_csv('../splits_optimizer/model_ready_data.csv')


outcome = df['PLUS_MINUS'] #df['home_SPREAD'] + df['PLUS_MINUS'] 
y = []
for val in outcome:
    if val>0: 
        y.append(1) #home team wins. 
    else:
        y.append(0)
        
del df['PLUS_MINUS']


X = df
del X['Unnamed: 0']
del X['Home Team Won?']  #This was the problem from earlier :) 
#del X['road_SPREAD']
#del X['home_SPREAD']


#ready for data normalization and splitting


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

#Split all into training and testing
X_train,X_test,y_train,y_test = train_test_split(X,y,shuffle=True,test_size = .3)
test_spreads = X_test['home_SPREAD']

#prior to normalization, I want to retrieve a list of all of the spreads of the testing data. 
#This will be used further down the pipeline for converting to moneyline odds. 
#est_spreads = X_test['home_SPREAD']

del X_test['road_SPREAD'],X_test['home_SPREAD']
del X_train['road_SPREAD'],X_train['home_SPREAD']

scaler = MinMaxScaler()
#Normalization of dataset. 
scaler.fit(X_train.values)
X_train = scaler.transform(X_train.values)
X_test = scaler.transform(X_test.values)


#Here's a vanilla neural network courtesy of Sklearn. Let's see how well it does. 
#I can always tune this model, or apply other ones. 



from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import cross_val_score
model = MLPClassifier()

model.fit(X_train,y_train)


cvs = cross_val_score(model,X_test,y_test,cv=5)

print("Model Accuracy: ", 100*np.mean(cvs), "% +/- " , 100 * 2*np.std(cvs), "%. ")

def spread2ML(spread):
    """Converts spread into a moneyline value using the equation I calculated. 
    """
    if spread <=1.5:
        
        ML = 1.71409498 * spread**3 + 10.90008433 * spread **2 + 22.40247106 * spread - 138.20112341
    else: 

        ML = 1.66494668 * spread**3 -20.03302374 * spread**2 + 101.20347437 * spread - 34.68833849
    
    return ML


def ML2Payout(ML,bet,win=True):
    """Convert Moneyline odds to a payout. 
    """
    if win:
        if ML < 0: # - moneyline, 
        # PAYOUT = BET AMOUNT / (-1 *MONEYLINE ODDS / 100)

            payout = bet / (-1*ML/100)

        elif ML > 0:   #now for the underdog
        #PAYOUT = BET AMOUNT * ODDS / 100
            payout = (bet * ML) / 100

            
        else:
            payout = bet
    else:
        if ML > 0: 
            payout = -bet
        elif ML < 0:
            #in the circumstances where its a favorite, the computer makes you put down more. ie -190 means 19 to win 10. 
            payout = -bet
            
        else:
            payout = -bet
    
    return payout 

def risk2payout(ML,bet,win=True):
    """Depending on the moneyline, the risk reward formula changes. 
    """
    
    if ML < 0: # if betting on a favorite. 
        
        risk = -ML/bet
        reward = bet
        if win:
            payout = reward
        else:
            payout = -risk
        
    if ML > 0: #if betting on an underdog. 
        risk = bet
        reward = ML/bet
        
        if win:
            payout = reward #this is your risked money back, plus the reward. 
        else:
            payout = -risk  #this is how much you risked, and it's gone. 
    
    return risk, payout
        
        
predictions = model.predict(X_test) #predicted winners of all the test data. 

money_made = 0
acc_count = 0
total_winings = 0
total_losings = 0
init_bet = 10

for i,prediction in enumerate(predictions):
       
     
    
    spread = test_spreads.values[i]
    ML_odds = spread2ML(spread)
 #   print()
 #   print("Approx. Odds of Game: ", ML_odds)

   # ML * 

    if y_test[i] == prediction:
        acc_count+=1
        risk , winnings = risk2payout(ML_odds,init_bet,win=True)
     #   print("Correct! Win $", winnings)
     #   print("You risked $",risk)
       # print('$',winnings)
        
        money_made += winnings
        total_winings += winnings
       # if ML_odds < -
    else:
        _ , losings = risk2payout(ML_odds,init_bet,win=False)
     #   print("Wrong! Lose $", -losings)

        money_made += losings
        total_losings += losings


print("# of games selected: ", len(predictions))
print("Total money made: $", money_made)
print("Numbers of games chosen correctly: " ,acc_count)



import pickle

print("exporting tools...")

model_filename = 'finalized_model_wo_spread.sav'
print("model exported as ", model_filename)
pickle.dump(model, open(model_filename, 'wb'))


scaler_filename = 'finalized_scaler_wo_spread.sav'
print("scaler exported as ", scaler_filename)
pickle.dump(scaler, open(scaler_filename, 'wb'))

        
        
