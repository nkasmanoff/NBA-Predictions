NBA Forecasting 
===============

<center>

![Project Cover](https://github.com/nkasmanoff/NBA-Predictions/blob/master/nbapic.png:large)

</center>


Contained in this and the nested repositories are the tools used to forecast the winners of NBA games with ~70% accuracy. 

The steps done in this study are split into corresponding folders, but the overlying objective is as follows. To take the avaialbe game information of previously played games in the NBA, and identify what features, if any, and can be used to successfully translate into a model that can pick enough correct games to translate into a lucrative system of picking NBA games. 


First the data is scraped from available sources via NBA.com and oddshark.com, providing the box scores and spreads of previously played games from the 2013-2014 NBA season up to today's games. 

Next, the box scores are studied, and used to identify the relevant statistics that would correlate to the outcome of that played game. 

Furthermore, if you could bet on an already played game, there would be no purpose for such a study, as we would all be millionaires. With that being the case, the next goal is to determine if there is such a proxy that could be inserted that when used, could effectively correspond to a team's performance over that game. For this study, the decided tool to use is that team's previous N game averages prior to the game of interest. For this purpose, a tool is created that identifies this optimal value of N, and serves to figure out whether or not a classifier is feasible. 

Lastly, after creating the relevant dataset, various machine learning models are implemented, and in addition to the accuracy metric used, the betting odds and lines are also applied to see if such a prediction method would generate positive returns. 


For futher documentation and descriptions of these objectives, please see the corresponding repositories linked. 

Please email me or describe any issues with this data if any questions arise.

