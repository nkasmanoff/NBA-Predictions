Today's Games
--------------


After determining the optimal features and optimal model, the challenge now is to apply these methods to games going on NOW. Scraping the same sources used to obtain games from older seasons, I can now do the same thing with games going on today.  This allows for well-informed guesses as to who is supposed to win games going on today. Scraping methods are necessary to obtain the spreads of the games of today, but a slight flaw in this tool is that lines may move as the day goes on, and depending on when the scrape is done the line may no longer be accurate. Regardless, a pipeline is done that means after simply typing "python predict_today.py", a running list of games and expected results will be added to the "output.txt" document. 

The day after, just run "python update_results.py" to see how the model performed. 
