
Run with gui.py


# SpaceHole.

Solitaire card game based on: https://www.angelfire.com/games2/warpspawn/SHole.html .

## Description

Card game using a SQLite database as card manager. Both cards attributes and in game position (in hand, discarded, in play) are managed throught changes in the database. These changes are then load to the game and UI. User actions then implied a modification of the database, generating a response in the UI.

The UI was created over the PyQt5 library. This app was originally thought merely as an experiment over PyQt5's flexibility, as it is not meant to function as a game engine and it greatly limits the flexibility of the UI.

The game is a solitaire space colony builder and defender. The player must defend and build up his Space colony and accumulate the most megacredits possible. Cards repressent colony structures (buildings), colony defence forces (defenders), colony threats (invaders) and random events (events).


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

!![game UI with number codes](https://github.com/user-attachments/assets/f1d68ff5-9028-4953-a153-9d824d8c6b15)


1. Hand Area: cards` first possition once drawn from the deck.
2. Base Area: Where building cards are placed upon being played from hand
3. Defenders Area: This is the frame where defender cards are played
4. Invaders Area: Invader cards are played in this area

Finally, there is a frame dedicated to show information about the hoovered card ( 5 )

### How to play

The game consist in a common deck for all cards and is divided in phases

1. Space Karma Phase: draw a card
2. Event Phase: Event cards and Invader cards are played. In the case of events, the are resolved in this phase
3. Battle Phase: Invaders attack the base. This is repressented by the invader card's force. Each force point has a 1/6 chance of inflicting 1 damage. Defenders and lasers counterattack by the same criteria. This phase is itself divided in 4 subphases:
 * Invaders vs Defenders: Invaders deal damage to defendenders and vis-versa. Each damage dealt means 1 hit reduce for one card. Damage is assigned randomly. If hits are reduced to cero the card is discarded.
 * Invaders vs lasers: If invaders defeat all defenders, they are still in play and damage is left 



 




## Author

Leonardo Mario Mazzeo
leomazzeo@gmail.com
