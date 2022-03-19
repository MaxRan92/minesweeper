"""
random module -> imported for random number generation for placing bombs
import os --> needed for the ClearConsole function
from Colorama import Fore --> to colour the text in the console
"""
import random
import os
from colorama import Fore


# Assigning ASCII icons code to constants
BOMB = '\U0001F4A5'
BLANK_SQUARE = '\U0001F532'
CLOVER = '\U0001F340'
FLAG = '\U0001F6A9'


class Game():
    """
    Class that contains the following Methods:
    1) initial_screen()
        Welcome screen with logo and username input
    2) tutorial()
        Prints the rules of the game
    3) get_difficulty_level()
        Ask the level of difficulty
    4) create_new_board()
        Creates a board with random placed mines
    5) display_board()
        Function to display a properly formatted board
    6) insert_values()
        In free cells, insert number of adjacent bombs
    7) dig_or_flag_selector()
        Asks the user to dig or place a flag
    8) get_coordinates()
        Allows the user to insert coordinates of the chosen cell
    9) show()
        Discloses the cell underlying object
    10) get_near_bombs_num()
        Calculate the number of adjacent bombs for a cell
    11) run_game()
        Loop that keeps running until the user wins or loose
    12) restart_game()
        Allows user to restart the game once he wins or loose
    """

    def __init__(self):
        """
        Setting main parameters
        """
        self.username = ""
        self.board = ""
        self.board_size = ""
        self.bomb_num = ""
        self.ui_board = []
        self.board_to_show = []
        self.x_coordinates = []
        self.x_separation = []
        self.shown = set()
        self.gameover = False
        self.victory = False
        self.flag_alert = False
        self.flag = False

    def initial_screen(self):
        """"
        Displays banner and asks user to
        insert his name
        """
        print("""
                        ███╗   ███╗██╗███╗   ██╗███████╗
                        ████╗ ████║██║████╗  ██║██╔════╝
                        ██╔████╔██║██║██╔██╗ ██║█████╗
                        ██║╚██╔╝██║██║██║╚██╗██║██╔══╝
                        ██║ ╚═╝ ██║██║██║ ╚████║███████╗
                        ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
            ███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗
            ██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
            ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝
            ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
            ███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║
            ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
            """)
        # ask to enter a username until it is done
        print("Welcome to Minesweeper!\nPlease insert your name")
        self.username = input().strip()
        while len(self.username) == 0:
            ClearConsole.clear_display()
            print("It looks like you haven't typed anything, please enter your name!")  # noqa
            self.username = input().strip()
        ClearConsole.clear_display()
        # return hello message
        print("\nHi " + Fore.GREEN + f"{self.username}!" +
        Fore.WHITE + " Nice to meet you!\n")  # noqa

    def tutorial(self):
        """
        Prints tutorial text
        """
        # print the rules
        print(
            " - RULES OF THE GAME - \n\n\nThe field has several mines"
            " under its ground and your task is to identify and \nisolate them"
            ", digging only the safe spots! \n\nEvery time you dig in a safe"
            " spot, a number will appear representing the number of "
            "surrounding mines: with a little bit of logic, you will "
            "be able to localize them. \n\nWhen you localize a mine,"
            " place a flag over its cell as a reminder, so that you "
            "will not dig there by mistake! \n\nIf you dig all the "
            "safe spots in the field without any mistake, you win!\n\n ")
        # ask to start the game
        input("Press enter to start the game!\n")
        ClearConsole.clear_display()
        self.get_difficulty_level()
        ClearConsole.clear_display()
        self.run_game()

    def get_difficulty_level(self):
        """
        Assign board size and bomb num according to
        the difficulty level chosen by the user
        """
        # asks to insert difficulty level
        difficulty = input(
            "\nPlease select a difficulty level \n\nh: Hard \nm: Medium "
            "\ne: Easy\n").lower()
        while difficulty not in ["e", "easy", "m", "medium", "h", "hard"]:
            ClearConsole.clear_display()
            print(Fore.RED + "\nInput not recognized\n" + Fore.WHITE)
            difficulty = input(
                "Please select a difficulty level \n h: Hard \nm: Medium "
                "\ne: Easy\n").lower()

        # each difficulty level has increasing number of cells and bombs
        if difficulty in ["h", "hard"]:
            self.board_size = 14
            self.bomb_num = 30
        elif difficulty in ["m", "medium"]:
            self.board_size = 10
            self.bomb_num = 15
        elif difficulty in ["e", "easy"]:
            self.board_size = 5
            self.bomb_num = 4

    def create_new_board(self):
        """
        Create board arrays with none values
        Place bombs, at random coordinates in the board
        """
        # for loop that creates two boards, inserting for each coordinate:
        # - None value in the underlying board
        # - Blank Square Emoji for the User interface board
        board = [[None for a in range(self.board_size)]
                 for b in range(self.board_size)]
        self.ui_board = [[BLANK_SQUARE for a in range(
            self.board_size)] for b in range(self.board_size)]

        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size -
                                  1), random.randint(0, self.board_size - 1)
            # If the cell has already a bomb,
            # skip and go to the top of the while loop
            if board[x][y] == BOMB:
                continue
            # If the cell has no bomb, place it
            board[x][y] = BOMB
            bomb_counter += 1
        return board

    def display_board(self, board_to_show):
        """
        display board with format
        """
        self.board_to_show = board_to_show
        self.x_coordinates = []
        self.x_separation = []
        # print yellow x coordinates and separation lines
        # caring of the spaces taken by double digit coordinates for
        # better alignment
        for a in range(self.board_size):
            if a < 9:
                self.x_coordinates.append(
                    f"{'  ' + Fore.YELLOW + str(a+1) + Fore.WHITE}")
            else:
                self.x_coordinates.append(
                    f"{' ' + Fore.YELLOW + str(a+1) + Fore.WHITE}")
            self.x_separation.append('---')
        self.x_coordinates = ' '.join(self.x_coordinates)
        self.x_coordinates = '              ' + self.x_coordinates
        self.x_separation = ' '.join(self.x_separation)
        self.x_separation = '               ' + self.x_separation
        print(self.x_coordinates)
        print(self.x_separation)
        # print stacked board horizontal lines,
        # obtained appending cyan y coordinates
        # and spacing properly
        for r in range(self.board_size):
            if r < 9:
                line_to_print = f"          {Fore.CYAN + str(r+1) + Fore.WHITE + '  | ' + '   '.join(self.board_to_show[r]) + '  |  ' + Fore.CYAN + str(r+1) + Fore.WHITE}"  # noqa
            else:
                line_to_print = f"          {Fore.CYAN + str(r+1) + Fore.WHITE + ' | ' + '   '.join(self.board_to_show[r]) + '  |  ' + Fore.CYAN + str(r+1) + Fore.WHITE}"  # noqa
            print(line_to_print)
        print(self.x_separation)
        print(self.x_coordinates)

    def insert_values(self):
        """
        for each cell that has no bomb, calls the get_near_bombs_num()
        function that assignes a value representing
        the number of bombs in the cells next to it
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == BOMB:
                    continue
                self.board[x][y] = self.get_near_bombs_num(x, y)

    def dig_or_flag_selector(self):
        """
        Selection menu
        User decides to dig or place a flag
        """
        ClearConsole.clear_display()
        self.display_board(self.ui_board)
        starter = input(
            Fore.WHITE + "-  Press Enter to dig\n-  "
            "Press F to place/remove a flag\n")
        if starter in ["F", "f", "flag"]:
            self.flag = True
        else:
            self.flag = False

    def get_coordinates(self, flag):
        """
        Function to get the user's coordinates inputs
        Loops until a valid input is entered
        Allows to go back to dig_or_flag_selector
        """
        ClearConsole.clear_display()
        self.display_board(self.ui_board)
        # Print proper text according to the dig or flag user choice
        if flag:
            print(f"Let's place a flag! {FLAG}")
        else:
            print(f"Let's dig in! Watch out for mines and good luck! {CLOVER}")
        # insert row value or B to go back
        row_input = input(
            "insert the " + Fore.CYAN + "ROW NUMBER" + Fore.WHITE +
            " of the selected cell or " + Fore.RED +
            "B" + Fore.WHITE + " to go back:\n")
        # if input not valid (not a number or B), enter again
        while not (row_input.isdigit() or row_input.lower() in ["b", "back"]):
            ClearConsole.clear_display()
            self.display_board(self.ui_board)
            row_input = input(
                Fore.RED + "Value not recognized, please enter a valid"
                " number\n" +
                Fore.WHITE)
        # If value is B or Back, a new user choice sequence
        # starts while the current ends
        if row_input.lower() in ["b", "back"]:
            ClearConsole.clear_display()
            self.display_board(self.ui_board)
            self.dig_or_flag_selector()
            self.get_coordinates(self.flag)
        # else, the input must be a number
        else:
            x = int(row_input) - 1
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
            # insert column value or B to go back
            col_input = input(
                "insert the " + Fore.YELLOW + "COLUMN NUMBER" + Fore.WHITE +
                " of the selected cell or " + Fore.RED + "B" + Fore.WHITE +
                " to go back:\n")
            # if input not valid (not a number or B), enter again
            while not (col_input.isdigit() or col_input.lower() in ["b", "back"]):  # noqa
                ClearConsole.clear_display()
                self.display_board(self.ui_board)
                col_input = input(
                    Fore.RED + "Value not recognized, please enter a valid "
                    "number\n" + Fore.WHITE)
            # If value is B or Back, a new user choice sequence starts
            # while the current ends
            if col_input.lower() in ["b", "back"]:
                ClearConsole.clear_display()
                self.display_board(self.ui_board)
                self.dig_or_flag_selector()
                self.get_coordinates(self.flag)
            # else, the input must be a number
            else:
                y = int(col_input) - 1
                # if number out of board range, enter again,
                # otherwise we have our y coordinate
                while y < 0 or y > self.board_size - 1:
                    try:
                        ClearConsole.clear_display()
                        self.display_board(self.ui_board)
                        y = int(input(
                            Fore.RED + "The column does not exist, please enter a "  # noqa
                            "valid number\n" + Fore.WHITE)) - 1
                    except (TypeError, ValueError):
                        continue
                # if the user wants to dig
                if not flag:
                    # If there is a flag, print alert to remove it first
                    if self.ui_board[x][y] == FLAG:
                        ClearConsole.clear_display()
                        self.display_board(self.ui_board)
                        print(Fore.RED + "\nPlease remove the flag before digging")  # noqa
                        input("click Enter to continue")
                        self.flag_alert = True
                        ClearConsole.clear_display()
                        self.display_board(self.ui_board)
                        self.dig_or_flag_selector()
                        self.get_coordinates(self.flag)
                    # if there is not a flag, show underlying cell
                    # via self.show function
                    else:
                        self.flag_alert = False
                        ClearConsole.clear_display()
                        self.show(x, y, flag)
                # if the user wants to put a flag, do it via self.show function
                else:
                    ClearConsole.clear_display()
                    self.show(x, y, flag)

    def show(self, x, y, flag):
        """
        check the cell chosen by the user and shows it,
        enlarging the shown area on certain conditions
        """
        # if user is not placing/removing a flag
        if not flag:
            # if first cell, recreate table
            # until it is not a bomb
            if len(self.shown) == 0:
                while self.board[x][y] == BOMB:
                    # creates new random board
                    self.board = self.create_new_board()
                    # insert values in the underlying board
                    self.insert_values()
            # if cell already dug, notify the user and restart
            # the coordinates input
            if (x, y) in self.shown:
                self.display_board(self.ui_board)
                print(Fore.RED + "\nCell alread dug!" + Fore.WHITE)
                input("\nPress ENTER to continue")
                self.get_coordinates(flag)
            else:
                # Adds the shown cell as tuple in a set
                # Sets do not allow duplicate values, hence trying to dig
                # the same cell multiple times won't change it
                self.shown.add((x, y))
                # If there is a bomb, show it in the ui board. Game over.
                if self.board[x][y] == BOMB:
                    self.ui_board[x][y] = self.board[x][y]
                    self.gameover = True
                # If there is one or more adjacent bomb (>0 value in the
                # underlying board), show only that cell
                elif int(self.board[x][y]) > 0:
                    self.ui_board[x][y] = self.board[x][y]
                # If there is no adjacent bomb (0 value in the underlying
                # board), enlarge the shown area until you find a cell
                # with adjacent bombs
                elif int(self.board[x][y]) == 0:
                    # place a clover emoji
                    self.ui_board[x][y] = CLOVER
                    # loop through the 8 adjacent cells and show all
                    # of them if not already shown before
                    for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):  # noqa
                        for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):  # noqa
                            if (r, c) in self.shown:
                                continue
                            self.show(r, c, flag)
        # if user is placing(removing) a flag, place(remove) it
        # respectively if in that cell there is a blank_square(flag).
        else:
            if self.ui_board[x][y] == BLANK_SQUARE:
                self.ui_board[x][y] = FLAG
            elif self.ui_board[x][y] == FLAG:
                self.ui_board[x][y] = BLANK_SQUARE
            # else it means it is already dug. Notify it.
            else:
                self.display_board(self.ui_board)
                print(Fore.RED + "\nCannot place a flag in an already shown spot!\n" + Fore.WHITE)  # noqa
                input("Press enter to continue")

    def get_near_bombs_num(self, x, y):
        """
        iterate through the 8 adiacent cells
        and count the number of bombs
        """
        near_bombs_num = 0
        # two for loops to get the coordinates of all adjacent cells
        for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
            for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                # do not consider the dug cell
                if r == x and c == y:
                    continue
                # if adjacent cell has a bomb, add 1 to the counter
                if self.board[r][c] == BOMB:
                    near_bombs_num += 1
        return str(near_bombs_num)

    def run_game(self):
        """
        runs the game
        """
        # creates new random board
        self.board = self.create_new_board()
        # insert values in the underlying board
        self.insert_values()
        # loop that keeps running until all the cells that do not
        # contain bombs are shown
        while len(self.shown) < self.board_size ** 2 - self.bomb_num:
            # if there is not a flag_alert (see get_coordinates function),
            # show the ui board
            if not self.flag_alert:
                self.display_board(self.ui_board)
            # if gameover and not flag_alert, print it
            if self.gameover and not self.flag_alert:
                ClearConsole.clear_display()
                self.display_board(self.ui_board)
                print("Ouch, there was a mine!! \n" +
                      BOMB + BOMB + Fore.RED + " GAME OVER! " + Fore.WHITE +
                      BOMB + BOMB)
                self.restart_game()
                break
            # otherwise, let the user select dig/flag
            # and select the coordinates
            else:
                self.dig_or_flag_selector()
                ClearConsole.clear_display()
                self.get_coordinates(self.flag)
        # if all the cells that do not contain bombs are shown, you win
        if len(self.shown) == self.board_size ** 2 - self.bomb_num:
            self.display_board(self.ui_board)
            print("\n" + CLOVER + CLOVER + "  CONGRATULATIONS! You "
            "cleared all the field!  " + CLOVER + CLOVER)  # noqa
            self.victory = True
            self.restart_game()

    def restart_game(self):
        """
        If the user wins or loses, ask to restart
        """
        restart = input("\nDo you want to play again? (y/n)\n")
        if restart in ["y", "yes"]:
            # restart all the function needed for a new game
            ClearConsole.clear_display()
            self.gameover = False
            self.victory = False
            self.shown = set()
            ClearConsole.clear_display()
            self.get_difficulty_level()
            ClearConsole.clear_display()
            self.run_game()
        else:
            # exit the game
            ClearConsole.clear_display()
            self.display_board(self.ui_board)
            print(Fore.GREEN + f"\n\nThank you for playing {self.username}!\n\n" + Fore.WHITE)  # noqa


class ClearConsole():
    """
    Function that clears the console
    """
    # From https://www.delftstack.com/howto/python/python-clear-console/
    @staticmethod
    def clear_display():
        """"
        Clears the display
        """
        command = 'clear'
        if os.name in (
                'nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)


def main():
    """
    Runs initial screen
    Gives play/tutorial option
    Runs the function accordingly
    breaks once the game ends
    """
    game = Game()
    game.initial_screen()
    while True:
        user_selection = input(Fore.WHITE + "Please select 'Play' to start the game or 'Tutorial' for the guide.\n \t p: play \n \t t: tutorial\n")  # noqa
        if user_selection in ["play", "p", "yes", "y"]:
            ClearConsole.clear_display()
            game.get_difficulty_level()
            ClearConsole.clear_display()
            game.run_game()
        elif user_selection in ["tutorial", "t"]:
            ClearConsole.clear_display()
            game.tutorial()
        else:
            ClearConsole.clear_display()
            print(
                Fore.RED + f"Hey {game.username}, your input is not recognized! \n")  # noqa
        if game.gameover or game.victory:
            break


main()
