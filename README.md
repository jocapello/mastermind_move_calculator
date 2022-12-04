# CISC/CMPE 204 Modelling Project

Welcome to the major project for CISC/CMPE 204!

Mastermind move calculator 

Our project is designed to run and calculate the set of possible codes given informationm the player knows in a game of mastermind. 
	Rules = (https://en.wikipedia.org/wiki/Mastermind_(board_game))
Whenever the player makes a guess, they recieve feedback that helps them narrow down the possible codes
Our project will assist the player by deducing all the possible codes that match the information the player is given

utils.py contains most of the constraint forming functions, while run.py contains the game class and the gameloop class. when run.py is run, a game loop is started using the gameloop class



## Structure

* `utils.py`: Contains most of the constraint forming functions.
* `run.py`: Contains the game class and the gameloop class. when run.py is run, a game loop is started
* `config.py`: sets the colors and slots that are included. avoid adding colors that start with the same letter. for testing purposes, it is reccomended to reduce the list of colors to 4 and decrease the code length to 3, as using the full range of colors and code length 4 will result in the assist action taking ~40 mins to compute
