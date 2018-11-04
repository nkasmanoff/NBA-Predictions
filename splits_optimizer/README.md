N Game Lookback
===============


This folder answers how many games of lookback time correspond to a team's performance in it's upcoming game. In order to create a proxy for the input data of a team's box score, a correlation needs to be found between that team's performance in it's previous n games. This code serves to ansewr this question of finding n by calculating the correlation of each box score statistic with the the game at time t by using an average over the previous t-1 to t-n games, and by maximizing this correlation, the proper n is identified. 



Results
-------


This plot is the correlation between all of the relevant statistics averaged over n games to the current game, as a function of n. 

<center>

![Project](https://github.com/nkasmanoff/NBA-Predictions/blob/master/splits_optimizer/lookback_correlations.png)


</center>


