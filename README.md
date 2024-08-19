
Run with gui.py


# SpaceHole.

Solitaire card game based on: https://www.angelfire.com/games2/warpspawn/SHole.html .

## Description

Card game using a SQLite database as card manager. Both cards attributes and in game position (in hand, discarded, in play) are managed throught changes in the database. These changes are then load to the game and UI. User actions then implied a modification of the database, generating a response in the UI.

The UI was created over the PyQt5 library. This app was originally thought merely as an experiment over PyQt5's flexibility, as it is not meant to function as a game engine and it greatly limits the flexibility of the UI.

The game is a solitaire space colony builder and defender. The player must defend and build up his Space colony. Cards repressent colony structures (buildings), colony defence forces (defenders), colony threats (invaders) and random events (events).


## Usage

### Dependencies

Libraries:
* PyQt5
* sys
* functools
* sqlite3
* csv
* random

### Executing program

Run gui.py. The game consist of 4 frames each representing different possible positions of the cards in play. 

!

1. Hand Area: cards` first possition once drawn from the deck.
2. Base Area: Where building cards are placed upon being played from hand
3. Defenders Area: This is the frame where defender cards are played
4. Invaders Area: Invader cards are played in this area

Finally, there is a frame dedicated to show information about the hoovered card ( 5 )



 

### Configuring the Neural Network

config.py includes all the possible options for configuration:



### Running the Neural Network

Upon running net.py it may look like this, depending on the configuration:

![Screenshot of the Neural Network](synapsis.png)



## Author

Leonardo Mario Mazzeo
leomazzeo@gmail.com
