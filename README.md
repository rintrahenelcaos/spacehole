
# SpaceHole.

Solitaire card game based on: https://www.angelfire.com/games2/warpspawn/SHole.html .

## Description

Card game using a SQLite database as card manager. Both cards attributes and in game position (in hand, discarded, in play) are managed through changes in the database. These changes are then loaded into the game and UI. User actions then imply a modification of the database, generating a response in the UI.

The UI was created from the PyQt5 library. This app was originally thought merely as an experiment of PyQt5's flexibility, as it is not meant to function as a game engine, and it greatly limits the flexibility of the UI.

The game is a solitaire space colony builder and defender. The player must defend and build up his Space colony and accumulate the most megacredits ( 8 ) possible. Cards represent colony structures (buildings), colony defense forces (defenders), colony threats (invaders) and random events (events). The game ends if the colony base is destroyed (defeat) or the deck runs out of cards (victory).


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

Run gui.py. The game consists of 4 frames, each representing different possible positions of the cards in play.

!![game UI with number codes](https://github.com/user-attachments/assets/f1d68ff5-9028-4953-a153-9d824d8c6b15)


1. Hand Area: cards` first position once drawn from the deck.
2. Base Area: Where building cards are placed upon being played by hand
3. Defenders Area: This is the frame where defender cards are played
4. Invaders Area: Invader cards are played in this area

Finally, there is a frame dedicated to showing information about the hoovered card ( 5 )

### How to play

The game consists of a common deck for all cards and is divided into phases.

1. Space Karma Phase: draw a card
2. Event Phase: Event cards and Invader cards are played. In the case of events, they are resolved in this phase.
3. Battle Phase: Invaders attack the base. This is represented by the invader card's force. Each force point has a 1/6 chance of inflicting 1 damage. Defenders and lasers counterattack by the same criteria. This phase is itself divided into 4 subphases in which invaders try to pass through defenders, lasers and domes to deal damage to the base while defenders and lasers deal damage back.  
4. Build Phase: Building and defenders cards are played in this phase. It can be skipped to completely heal any building or defender.
5. Income Phase: Megacredits number is updated
6. Discard Phase: Hand has a maximum (5 or 7 depending on buildings). Excess cards are discarded

To pass from phase to phase, click on the Next Phase button ( 7 ) or press Space.

The current game phase is informed in the top left corner ( 6 ) and important happenings in the game are shown on the bottom left ( 9 )



## Author

Leonardo Mario Mazzeo
leomazzeo@gmail.com
