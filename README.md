# MineSweeeper

## Author 
Massimo Ranalli

## Project Overview 

MineSweeper is a single-player puzzle video game. The objective of the game is to clear a square board containing hidden mines or bombs without detonating any of them, with the help from clues about the number of neighbouring mines in each field. The game originates from the 1960s and it has been written for many computing platforms in use today.

![Website Display]()

### Flow Chart 

![FlowChart]()

## How To Play
- Insert username
- The user can view the rules or directly play
- The user chooses a difficulty level (easy, medium, hard)
- The user can decide to place a flag or dig a cell
- Once all the empty cells (without mines) are dug, the player wins

## Features 

### Implemented Features 

#### Name Input
- We collect the username to add a personal touch to the game and have a basic and friendly interaction with him. 

![Name Input]()

#### Difficulty Level
The user can pick between three difficulty levels:
- Easy: 5x5 board with 4 mines
- Medium: 10x10 board with 15 mines
- Hard: 14x14 board with 30 mines

![Difficulty Level]()

#### Choice between dig and flag

Just like the original game, the user can decide to dig or flag the chosen cell
This leads to a series of logical steps to take care of, such as:
- If the user wants to dig(flag) an undisclosed cell, the cell will be dug(flagged)
- If the user wants to dig or flag an already dug cell, return alert message
- If the user wants to dig an already flagged cell, return alert proposing to de-flag it first
- If the user wants to flag an already flagged cell, the cell will be de-flagged

![Dig or Flag]()

Cells can be selected entering first the Row index, then the Column one. At each one of these steps, the user can press B ad go back to the dig or flag choice.

#### Fully updating display
With the use of ClearDisplay method, the screen updates and there will not be old data left on the top of the command line

#### User input made easier, with complete error handling
- Case insensitivity
- Users can type both full order words or the initial letter
- While entering coordinates, Row and Columns number not included in the board are signalled, and the user is pushed to insert valid ones
- General user input error handling is taken cared of and fully tested

![Error Handling]()

#### Game restart
Whether the game is terminated with a victory or not, the user is offered to play another game or leave. 

![Game Restart]()

#### User interface
With all the limits that a simple command line has, basic but clear UI has been implemented.
Colors help the user to focus his attention on the actions (keys to press to continue, row/column coordinates to insert etc).
Moreover, use of ASCII logo and emoji help to improve the aseptic black and white outlook.

![User Interface]()


