N Game Lookback
===============


This folder answers how many games prior to the one of interest corresponds to a team's performance in it's upcoming game. Essentially, I am trying to identify a proxy for what an upcoming game's box score will be based on previous game. My attempt at this is to try and correlate between the previous game splits, and the actual number in the game of interest. This code serves to answer this question of finding n by calculating the correlation of each box score statistic with the the game at time t by using an average over the previous t-1 to t-n games, and by maximizing this correlation, the proper n is identified. 



Results
-------


This plot is the correlation between all of the relevant statistics averaged over n games to the current game, as a function of n. 

<center>

![Project](https://github.com/nkasmanoff/NBA-Predictions/blob/master/splits_optimizer/lookback_correlations.png)


</center>


This plot shows diminishing returns after 20 or so games. In the end I decided to make this "proxy data" for the model be the team's splits over the previous 20 games, which also ends up being the best available option as I soon demonstrate using the NBA_py API, the options for scraping team splits via this method only goes back 20 games. If it was for say 30 games, I would have to develop a new scraper. How lucky! 


Furthermore, I also performa a little bit of EDA, and see that by using PCA and TSNE, there does appear to be a split in the data between home team wins and losses. Following this thread, I now move closer towards generating a model...