# MineSweeper

## Game Link
The project is published on Heroku at the following [Link](https://mine-sweeper-app.herokuapp.com/)

## Author 
Massimo Ranalli

## Project Overview 

MineSweeper is a single-player puzzle video game. The objective of the game is to clear a square board containing hidden mines or bombs without detonating any of them, with the help from clues about the number of neighbouring mines in each field. The game originates from the 1960s and it has been written for many computing platforms in use today.

![Website Display](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/landing-page.png)


## How To Play
- Mines are scattered throughout a board, which is divided into cells. Cells have three states: non displayed, displayed and flagged. 
- A non displayed cell is blank and can be displayed, while an already displayed cell is exposed. 
- Flagged cells are those marked by the player to indicate a potential mine location.
- The player select a cell to display it. If a player displays a mined cell, the game ends. Otherwise, the cell displays either a number, indicating the number of mines adjacent to it, or a black tile (here represented by a clover emoji), and all adjacent non-mined cells will automatically be uncovered.
The first dig is always safe.
- The player can also flag a cell, causing a flag to appear on it. Flagged cells are still considered covered, and a player can select them to display them, although they must first be unflagged.
- To win the game, players must uncover all non-mine cells, at which point, the timer is stopped. Flagging all the mined cells is not required.


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

These proportions make sure that approximately 15% of the cells contain a mine.

![Difficulty Level](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/difficulty-level.png)

#### Choice between dig and flag

Just like the original game, the user can decide to dig or flag the chosen cell. This leads to a series of logical steps to be cared of, such as:
- If the user wants to dig(flag) an undisclosed cell, the cell will be dug(flagged)
- If the user wants to dig or flag an already dug cell, return alert message
- If the user wants to dig an already flagged cell, return alert proposing to de-flag it first
- If the user wants to flag an already flagged cell, the cell will be de-flagged

![Dig or Flag](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/dig-or-flag.png)

Cells can be selected entering first the Row index, then the Column one. At each one of these steps, the user can press B ad go back to the dig or flag choice.

![Enter Coordinates](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/board-display.png)

#### Fully updating display
With the use of ClearDisplay method, the screen updates and there will not be old or useless data output left at the top of the command line

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
Colors help the user to focus his attention on the actions (keys to press, row/column coordinates to insert etc).
Moreover, the use of ASCII logo and emoji helps to enhance the old fashioned black and white look.

## Flow Chart 
The rules of the game described above are put into practice via the following flowchart.

![FlowChart](https://github.com/MaxRan92/minesweeper/blob/main/docs/flowchart/full-flowchart.png)

## Main Methods
Below you may find a brief description of the main function used to implement the flow above.

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
  Most of the alerts were about the number of blank lines between methods, trailing whitespaces to be deleted and too long lines.
  About this last alert type, '  # noqa' string were included on those parts in which shorter than 79 characters lines may lead to bad readibility.
![Validation Errors](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/pep8.png)

## Manual Testing and Interesting Code Logics
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
                
2) **To loop through the 8 adjacent cell if dug cell is empty**


  As per flowchart, if a cell with no adjacent mine is dug, a recursive function should enlarge to the neighbouring cells until a close-to-mine cell (hence with a number) is met and shown.
  Heach loop of the recursive function should loop through all the adjacent cells, and is made via a duble "for" loop which combines left and right cells with up and down ones. 
  At first the code would break and not enlarge, since the if-condition in the last rows was not inserted: the for loops iterates all the adjacent cells but also the cell dug at first, and this would trigger the "already dug cell" alert and stop the code.
  
        # loop through the 8 adjacent cells and show all of them
        # if not already shown before
        for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
            for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):  # noqa
                if (r, c) in self.shown:
                    continue
                self.show(r, c, flag)

3) **To define a victory**


  While for losing you just need to dig in the wrong place (quite easy to code), for victory the logic is more interesting.
  Win comes when all the "safe" cells are dug. This is obtained storing in a set (which hosts unique values) a series of tuple with two numbers representing the coordinates of already dug cells.
  The set lenght (which corresponds to the number of cells dug) was at first compared to the total number of the cells: if they were equal, means that we uncovered all the cells safely! ... but that is not possible! 
  
  
  The total number of cells contains also those with a mine, hence it is impossible to win digging every cell.
  The solution is in the code below: a while loop that makes the user play and dig until the number of shown cells equals the total number of cells of the board, minus the number of bombs.
  
        # loop that keeps running until all the cells that do not
        # contain bombs are shown
        while len(self.shown) < self.board_size ** 2 - self.bomb_num:

4) **To avoid a bomb at the first dig**


  As per official rules, the first dig should not return a bomb. That would be frustrating!
  However, this feature was easily implemented adding the code below: if the shown set has a lenght of zero, meaning no cells have been dug, and the player is so unfortunate to dig a bomb at his first trial, the code keep recreating a complete table until that first chosen cell is safe.
  
        if len(self.shown) == 0:
          while self.board[x][y] == BOMB:
              # creates new random board
              self.board = self.create_new_board()
              # insert values in the underlying board
              self.insert_values()

## Deployments

### Heroku
The game is deployed on Heroku and the process involved is the following:
  - Log in and create a new app with proper name and region
  
  ![Create App](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-create-app.png)
  
  - Click on the app and go to settings tab

  ![Settings](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-settings.png)

  - Go to the Config Vars section and insert PORT with a value of 8000

  ![Config Vars](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-config-vars.png)

  - In the section below, called Buildpack, you must add Python and Nodejs (in this precise order)

  ![Buildpack](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-buildpacks.png)

  - Go to Deploy Tab. In the Deployment method section connect your Github account. Entering your repository name, your project will automatically be connected to Heroku

  ![Connect Github](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-connect-github.png)

  - From here you can decide if deploy automatically on Heroku (i.e. each time you commit a change) or manually. I chose the second one for better control over the final output
  - Click on deploy and wait some seconds: a view button will appear and clicking on it you will see your program deployed!

  ![Deploy](https://github.com/MaxRan92/minesweeper/blob/main/docs/screenshots/heroku-deploy.png)



### Gitpod
Is it also possible to deploy the project on Github and make it run on its terminal.
To do so, first type ```pip3 install -r requirements.txt```, so that all the required installation are done.
Then, type ```python3 run.py``` to run the program on the terminal.


## Credits and Ackowledgments

- First of all, I have to thank my mentor Malia: as always her experience, competence and fast thinking are very useful and inspirational. 
- The code structure and logic is inspired to this short but useful [Video](https://www.youtube.com/watch?v=Fjw7Lc9zlyU).
- Flowchart is made thank to this very intuitive and easy to use [Site](https://app.diagrams.net/).
