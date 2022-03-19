# MineSweeeper

## Author 
Massimo Ranalli

## Project Overview 

MineSweeper is a single-player puzzle video game. The objective of the game is to clear a square board containing hidden mines or bombs without detonating any of them, with the help from clues about the number of neighbouring mines in each field. The game originates from the 1960s and it has been written for many computing platforms in use today.

![Website Display](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/landing-page.png)


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

![Name Input](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/insert-name.png)

#### Difficulty Level
The user can pick between three difficulty levels:
- Easy: 5x5 board with 4 mines
- Medium: 10x10 board with 15 mines
- Hard: 14x14 board with 30 mines

![Difficulty Level](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/difficulty-level.png)

#### Choice between dig and flag

Just like the original game, the user can decide to dig or flag the chosen cell
This leads to a series of logical steps to take care of, such as:
- If the user wants to dig(flag) an undisclosed cell, the cell will be dug(flagged)
- If the user wants to dig or flag an already dug cell, return alert message
- If the user wants to dig an already flagged cell, return alert proposing to de-flag it first
- If the user wants to flag an already flagged cell, the cell will be de-flagged

![Dig or Flag](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/dig-or-flag.png)

Cells can be selected entering first the Row index, then the Column one. At each one of these steps, the user can press B ad go back to the dig or flag choice.

#### Fully updating display
With the use of ClearDisplay method, the screen updates and there will not be old data left on the top of the command line

#### User input made easier, with complete error handling
- Case insensitivity
- Users can type both full order words or the initial letter
- While entering coordinates, Row and Columns number not included in the board are signalled, and the user is pushed to insert valid ones
- General user input error handling is taken cared of and fully tested

![Error Handling](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/input-handling.png)

#### Game restart
Whether the game is terminated with a victory or not, the user is offered to play another game or leave. 

![Game Restart](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/game-over.png)

#### User interface
With all the limits that a simple command line has, basic but clear UI has been implemented.
Colors help the user to focus his attention on the actions (keys to press to continue, row/column coordinates to insert etc).
Moreover, use of ASCII logo and emoji help to improve the aseptic black and white outlook.

## Flow Chart 

![FlowChart](https://github.com/MaxRan92/minesweeper/blob/main/docs/flowchart/flowchart.png)

## Main Methods
1) **initial_screen()**: Welcome screen with logo and username input
2) **tutorial()**: Prints the rules of the game
3) **get_difficulty_level()**: Asks to the user the level of difficulty
4) **create_new_board()**: Creates a board with random placed mines
5) **display_board()**: Function to display a properly formatted board
6) **insert_values()**: In free cells, inserts number of adjacent bombs
7) **dig_or_flag_selector()**: Asks the user to dig or place a flag
8) **get_coordinates()**: Allows the user to insert coordinates of the chosen cell
9) **show()**: Discloses the cell underlying object on the UI board
10) **get_near_bombs_num()**: Calculates the number of adjacent bombs for a given cell
11) **run_game()**: Loop that keeps running until the user wins or loses
12) **restart_game()**: Allows the user to restart the game once he wins or loose

## Testing

## Validator Testing - PEP8 

- The code is PEP8 validated, however manual intervention was necessary to meet all the requirements.
  Most of the alerts were regarding the number of blank lines between methods, trailing whitespaces to be deleted and too long lines.
  About this last alert, I included '  # noqa' on those parts in which shorter than 79 characters lines may lead to bad readibility
![Validation Errors](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/pep8.png)

## Manual Testing
Manual testing has been implemented in all the phases of the project. Here I summarize and document the most significant issues encountered:

1) **Row/Column input handling**
  The code below comes from the 8) **get_coordinates()** method. As explained by the comments, the code does the following steps:
  - takes a row input
  - If the input is B (back), the code leads to the dir_or_flag_selection method.
  - If the input is a number, that number should be the row index.
  
  When the user inputs a number that is out of the board index range, an alert pops up, asking for a number included between the ranges.
  The main issue was that, if in this second input request the user simply writes a word or just press enter, it would compare a str with "<" and ">" operator conditions (which ensure the number is between the range). And this leads to ValueError and TypeError.
  The issue was solved including a try: except: condition as follows:

            # if number out of board range, enter again,
            # otherwise we have our x coordinate
            while x < 0 or x > self.board_size - 1:
                try:
                    ClearConsole.clear_display()
                    self.display_board(self.ui_board)
                    x = int(input(
                        Fore.RED + "The row does not exist, please enter a valid "  # noqa
                        "number\n" + Fore.WHITE)) - 1
                except (TypeError, ValueError):
                    continue
                
