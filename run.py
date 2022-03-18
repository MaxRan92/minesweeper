from colorama import Fore
import random
from mixins import ClearConsole

"""
Assign ASCII icons code to variables 
"""
BOMB = '\U0001F4A5'
BLANK_SQUARE = '\U0001F532'
CLOVER = '\U0001F340'
FLAG = '\U0001F6A9'


class Game(ClearConsole):
    """
    Create the gaming board
    """

    def __init__(self):
        """
        Setting variables 
        """
        self.ui_board = []
        self.x_coordinates = []
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
                     __  __ _                         
                    |  \/  (_)                        
                    | \  / |_ _ __   ___              
               _____| |\/| | | '_ \ / _ \             
              / ____| |  | | | | | |  __/             
             | (____|_|  |_|_|_| |_|\___|_   ___ _ __ 
              \___ \ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
              ____) \ V  V /  __/  __/ |_) |  __/ |   
             |_____/ \_/\_/ \___|\___| .__/ \___|_|   
                                     | |              
                                     |_|               
            """)
        global username
        # ask to enter a username until it is done
        print("Welcome to Minesweeper!\nPlease insert your name")
        username = input().strip()
        while len(username) == 0:
            print("It looks like you haven't typed anything, please enter your name!")  # noqa
            username = input().strip()
        self.clear_display()
        print("\nHi " + Fore.GREEN + f"{username}!")

    def tutorial(self):
        #print the rules
        print(" - RULES OF THE GAME - \n\n\n The field has several mines under its ground and your task is to identify and isolate them, digging only the safe spots! \n\n Every time you dig in a safe spot, a number will appear representing the number of surrounding mines: with a little bit of logic, you will be able to localize them. \n\n When you localize a mine, place a flag over its cell as a reminder, so that you will not dig there by mistake. \n\n If you dig all the safe spots in the field without any mistake, you win!\n\n ")
        # ask to start the game
        start_game = input("Click enter to start the game!\n")
        self.clear_display()
        self.get_difficulty_level()
        self.clear_display()
        self.run_game()

    def get_difficulty_level(self):
        """
        Assign board size and bomb num according to
        the difficulty level chosen by the user
        """
        difficulty = input(
                "Please select a difficulty level \nh:hard \nm:medium \ne:easy\n")
        while difficulty not in ["e", "easy", "m", "medium", "h", "hard"]:
            difficulty = input(
                Fore.RED + "Input not recognized\n" + Fore.WHITE).lower()

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
        Place bombs, represented by character *, at random coordinates in the board 
        """
        board = [[None for a in range(self.board_size)]
                 for b in range(self.board_size)]
        self.ui_board = [[BLANK_SQUARE for a in range(
            self.board_size)] for b in range(self.board_size)]

        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size -
                                  1), random.randint(0, self.board_size - 1)
            # If the cell has already a bomb, skip and go to the top of the while loop
            if board[x][y] == BOMB:
                continue
            # If the cell has no bomb, place it
            board[x][y] = BOMB
            bomb_counter += 1
        return board

    def insert_values(self):
        """
        for each cell that has no bomb, assign a value representing
        the number of bombs in the cells next to it
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == BOMB:
                    continue
                self.board[x][y] = self.get_near_bombs_num(x, y)

    def get_near_bombs_num(self, x, y):
        """
        iterate through the 8 adiacent cells 
        """
        near_bombs_num = 0
        for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
            for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                if r == x and c == y:
                    continue
                if self.board[r][c] == BOMB:
                    near_bombs_num += 1
        return str(near_bombs_num)

    def display_board(self, board_to_show):
        """
        display board with format
        """
        self.board_to_show = board_to_show
        self.x_coordinates = []
        self.x_separation = []
        for a in range(self.board_size):
            if a < 9:
                self.x_coordinates.append(
                    f"{'  ' + Fore.YELLOW + str(a+1) + Fore.WHITE}")
            else:
                self.x_coordinates.append(
                    f"{' ' + Fore.YELLOW + str(a+1) + Fore.WHITE}")
            self.x_separation.append('---')
        self.x_coordinates = ' '.join(self.x_coordinates)
        self.x_coordinates = '    ' + self.x_coordinates
        self.x_separation = ' '.join(self.x_separation)
        self.x_separation = '     ' + self.x_separation
        print(self.x_coordinates)
        print(self.x_separation)
        # stack board arrays
        for r in range(self.board_size):
            if r < 9:
                line_to_print = f"{Fore.CYAN + str(r+1) + Fore.WHITE + '  | ' + '   '.join(self.board_to_show[r]) + '  |  ' + Fore.CYAN + str(r+1) + Fore.WHITE}"
            else:
                line_to_print = f"{Fore.CYAN + str(r+1) + Fore.WHITE + ' | ' + '   '.join(self.board_to_show[r]) + '  |  ' + Fore.CYAN + str(r+1) + Fore.WHITE}"
            print(line_to_print)
        print(self.x_separation)
        print(self.x_coordinates)

    def show(self, x, y, flag):
        """
        check the cell chosen by the user:
        """
        if flag == False:
            self.shown.add((x, y))
            # If there is a bomb, game over
            if self.board[x][y] == BOMB:
                self.ui_board[x][y] = self.board[x][y]
                self.gameover = True
            # If there is one or more adjacent bomb, show only that cell
            # in the displayed board
            elif int(self.board[x][y]) > 0:
                self.ui_board[x][y] = self.board[x][y]
            # If there is no adjacent bomb, enlarge the shown area until
            # you find a cell with adjacent bombs
            elif int(self.board[x][y]) == 0:
                self.ui_board[x][y] = CLOVER
                for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
                    for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                        if (r, c) in self.shown:
                            continue
                        self.show(r, c, flag)
        else:
            if self.ui_board[x][y] == BLANK_SQUARE:  # ascii white square
                self.ui_board[x][y] = FLAG  # ascii Flag
            elif self.ui_board[x][y] == FLAG:  # ascii Flag
                self.ui_board[x][y] = BLANK_SQUARE  # ascii white square
            else:
                print("Cannot place a flag in an already shown spot!")

    def run_game(self):
        """
        runs the game
        """
        self.board = self.create_new_board()
        self.insert_values()
        while len(self.shown) < self.board_size ** 2 - self.bomb_num:
            if self.flag_alert == False:
                self.display_board(self.ui_board)
            if self.gameover:
                print("\nOuch, there was a mine!! \n" +
                      Fore.RED + "Game Over!" + Fore.WHITE)
                self.restart_game()
                break
            else:
                self.dig_or_flag_selector()
                self.clear_display()
                self.display_board(self.ui_board)
                self.get_coordinates(self.flag)
        if len(self.shown) == self.board_size ** 2 - self.bomb_num:
            self.display_board(self.ui_board)
            print("\nCONGRATULATIONS! You cleared the field!")
            self.victory = True
            self.restart_game()

    def dig_or_flag_selector(self):
        starter = input(
            Fore.WHITE + "-  Press Enter to dig\n-  Press F to place/remove a flag\n")
        if starter in ["F", "f", "flag"]:
            self.flag = True
            self.flag_alert = False
        else:
            self.flag = False
        


    def get_coordinates(self, flag):
        """
        Docstring to be inserted
        """
        self.clear_display()
        self.display_board(self.ui_board)
        if flag:
            print(f"Let's place a flag! {FLAG}")
        else:
            print(f"Let's dig in! Watch out for mines and good luck! {CLOVER}")
        # insert row value
        row_input = input(
            "insert the " + Fore.CYAN + "ROW NUMBER" + Fore.WHITE + " of the selected cell or " + Fore.RED + "B" + Fore.WHITE +" to go back:\n")
        # if value not a digit or B, enter again
        while not (row_input.isdigit() or row_input.lower() in ["b", "back"]):
            row_input = input(
                Fore.RED + "Value not recognized, please enter a number\n" + Fore.WHITE)
        if row_input.lower() in ["b", "back"]:
            self.clear_display()
            self.display_board(self.ui_board)
            self.dig_or_flag_selector()
            self.get_coordinates(self.flag)
        x = int(row_input) - 1
        # if value out of range, enter again
        while x < 0 or x > self.board_size - 1:
            x = int(input(
                Fore.RED + "The row does not exist, please enter a valid number\n" + Fore.WHITE)) - 1
        # insert row value
        col_input = input(
            "insert the " + Fore.YELLOW + "COLUMN NUMBER" + Fore.WHITE + " of the selected cell or " + Fore.RED + "B" + Fore.WHITE +" to go back:\n")
        # if value not a digit or B, enter again
        while not (col_input.isdigit() or col_input.lower() in ["b", "back"]):
            col_input = input(
                Fore.RED + "Value not recognized, please enter a number\n" + Fore.WHITE)
        if col_input.lower() in ["b", "back"]:
            self.clear_display()
            self.display_board(self.ui_board)
            self.dig_or_flag_selector()
            self.get_coordinates(self.flag)
        y = int(col_input) - 1
        # if value out of range, enter again
        while y < 0 or y > self.board_size - 1:
            y = int(input(
                Fore.RED + "The column does not exist, please enter a valid number\n" + Fore.WHITE)) - 1
        if not flag:
            # If there is a flag, print alert
            if self.ui_board[x][y] == FLAG:
                print(Fore.RED + "\nPlease remove the flag before digging")
                self.flag_alert = True
            else:
                self.flag_alert = False
        self.clear_display()
        self.show(x, y, flag)

    def restart_game(self):
        """
        If the user wins or loses, ask to restart
        """
        restart = input("\nDo you want to play again? (y/n)\n")
        if restart in ["y", "yes"]:
            self.clear_display()
            self.__init__()
            self.get_difficulty_level()
            self.clear_display()
            self.run_game()
        else:
            print(f"Thank you for playing {username}!")


def main():
    """
    Runs game
    """
    game = Game()
    game.initial_screen()
    while True:
        user_selection = input(Fore.WHITE + "Please select 'Play' to start the game or 'Tutorial' for the guide.\n \t p: play \n \t t: tutorial\n")  # noqa
        if user_selection in ["play", "p", "yes", "y"]:
            game.clear_display()
            game.get_difficulty_level()
            game.clear_display()
            game.run_game()
        elif user_selection in ["tutorial", "t"]:
            game.clear_display()
            game.tutorial()
        else:
            game.clear_display()
            print(
                Fore.RED + f"Hey {username}, your input is not recognized! \n")
        if game.gameover or game.victory:
            break


main()
