Models
======


This repo applies various machine learning models to the dataset of 20 game splits, plus the winner of that game, and attempts to create a model which can generate positive returns based on the vegas odds of those games. 


The attached pictures demonstrate the relationship between the designated spread of a game, and that team's corresponding moneyline odds. The spread is available online going back, but moneyline odds are not. By creating this equation, it allows me to essentially convert my outright predictions into what the corresponding returns would have been. 

A good example demonstrating this is if the Warriors were to play the New York Knicks. If the Warriors are heavy favorites, their spread would be -10 (expected to win by 10 points) and the related money line odds of -450, meaning risk $45 to win $10. A clear deterrent for always picking favorites. 

The data used to create these conversions comes from https://www.predictem.com/nfl/point-spread-to-moneyline-odds-conversion-chart/. 


Concurrently, a model must be created that maximizes the testing accuracy of choosing this data. This involves a long and computational search along different algorithms, and tuning the hyperparameters of said algorithms. While the most effective tool for doing such a grid search is sklearn and the many models it has built into it, a tensorflow implementation is also included as a sanity check and quick demonstration of tensorflows capabilities. For the purposes of maximizing accuracy, sklearn is the better package at this stage. 



<center>

![Project](https://github.com/nkasmanoff/NBA-Predictions/blob/master/models/lossgraph.png)


</center>

