# CISC/CMPE 204 Modelling Project

Welcome to the major project for CISC/CMPE 204!

Mastermind move calculator 

Our project is designed to calculate the worst possible move in a game of mastermind. 
	Rules = (https://en.wikipedia.org/wiki/Mastermind_(board_game))
A "worst guess" is defined by us to be the guess that shares the least new information. For example, while guessing the 
same thing twice would be the worse by this definition, we remove all guesses that provide NO new information.

Thus far we have a system in place to calculate all of the possibilities based on the proposistions provided. The game.py 
file has a method to figure out if a red or white peg is suitable based on a guess. This only provides the guesser with 
the amount of red or white pegs and does not share which part of their guess produced these results. 



Our next steps include combining the methods inside game.py and implimenting the algorithm. The algorithm will work by 
eliminating all the possible guesses that are not possible given previous guesses. An example being a guess of 
WBRR with 1 white peg would imediatly eliminate all possible solutions that contained soley the remaining colours. Because 
this result ensures us that at least one of the colours of the code masters code is W,B ir R. 

## Structure

* `game.py`: Contains temporary methods awaiting implimentation into run.py.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
