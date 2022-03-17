from colorama import Fore
import random
from mixins import ClearConsole

WHITE_BOX = "\U0001F532"
BOMB = "\U0001F4A5"
CLOVER = "\U0001F340"


class Game(ClearConsole):
    """
    Create the gaming board
    """

    def __init__(self):
        """
        Board size and bomb number variable assignment 
        """
        self.board_size = 0
        self.bomb_num = 0
        self.get_difficulty_level()
        self.ui_board = []
        self.x_coordinates = []
        self.board = self.create_new_board()
        self.insert_values()
        self.shown = set()
        self.gameover = False
        self.victory = False
        self.flag_alert = False
        self.x_separation = ""

    def get_difficulty_level(self):
        """
        Assign board size and bomb num according to
        the difficulty level chosen by the user
        """
        self.board_size = 10
        self.bomb_num = 15

    def create_new_board(self):
        """
        Create board arrays with none values
        Place bombs, represented by character *, at random coordinates in the board 
        """
        board = [[None for a in range(self.board_size)]
                 for b in range(self.board_size)]
        self.ui_board = [[WHITE_BOX for a in range(
            self.board_size)] for b in range(self.board_size)]

        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)  # noqa
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
        if not flag:
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
            if self.ui_board[x][y] == "\U0001F532":  # ascii white square
                self.ui_board[x][y] = "\U0001F6A9"  # ascii Flag
            elif self.ui_board[x][y] == "\U0001F6A9":  # ascii Flag
                self.ui_board[x][y] = "\U0001F532"  # ascii white square
            else:
                print("Cannot place a flag in an already shown spot!")

    def run_game(self):
        """
        runs the game
        """
        while len(self.shown) < self.board_size ** 2 - self.bomb_num:
            if self.flag_alert == False:
                self.display_board(self.ui_board)
            if self.gameover == True:
                print("\nOuch, there was a mine!! \n" +
                      Fore.RED + "Game Over!" + Fore.WHITE)
                self.restart_game()
                break
            else:
                starter = ""
                flag = False
                print("\n-  Press D to dig\n-  Press F to place/remove a flag\n")
                while starter not in ["f", "flag", "d", "dig"]:
                    starter = input(Fore.WHITE + "Please enter D or F").lower()
                    print(f"starter is {starter}")
                if "f" in starter.lower():
                    flag = True
                    self.flag_alert = False
                self.get_coordinates(flag)
        if len(self.shown) == self.board_size ** 2 - self.bomb_num:
            self.display_board(self.ui_board)
            print("\nCONGRATULATIONS! You cleared the field!")
            self.victory = True
            self.restart_game()

    def get_coordinates(self,flag):
        """
        Docstring to be inserted
        """
        self.clear_display()
        self.display_board(self.ui_board)
        if flag:
            print("\nLet's place a flag! \U0001F6A9")
        else:
            print("\nLet's dig in! Whatch out for mines and good luck! \U0001F340")
        x = 0
        y = 0
        print("insert the " + Fore.CYAN + "ROW NUMBER" + Fore.WHITE + " of the selected cell:\n")
        while not x > 0 and not x < self.board_size + 1:
            x = int(input(f"it should be a number between 1 and {self.board_size + 1}\n")) - 1
        print("insert the " + Fore.YELLOW + "COLUMN NUMBER" +
                Fore.WHITE + " of the selected cell:\n")
        while not y > 0 and not y < self.board_size + 1:
            y = int(input(f"it should be a number between 1 and {self.board_size + 1}\n")) - 1    
        if not flag:
            # If there is a flag, print alert
            if self.ui_board[x][y] == "\U0001F6A9":
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
            self.run_game()
        else:
            print(f"Thank you for playing {username}!")


def main():
    """
    Runs game
    """
    game = Game()
    global username
    # ask to enter a username until it is done
    print("Hello! What is your name?")
    username = input().strip()
    while len(username) == 0:
        print("It looks like you haven't typed anything, please enter your name!")
        username = input().strip()
    game.clear_display()
    print("\nHi " + Fore.GREEN + f"{username}!")
    while True:
        user_selection = input(
            Fore.WHITE + "Please select 'Play' to start the game or 'Tutorial' for the guide.\n \t p: play \n \t t: tutorial\n")
        if user_selection in ["play", "p", "yes", "y"]:
            game.clear_display()
            game.run_game()
        elif user_selection in ["tutorial", "t"]:
            print("Tutorial to be inserted")
        else:
            game.clear_display()
            print(
                Fore.RED + f"Hey {username}, your input is not recognized! \n")
        if game.gameover or game.victory:
            break


"""
def main():
    #insert if you want to play or not
    game = Game()
"""

main()
