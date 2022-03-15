import colorama
from colorama import Fore
import random
from mixins import ClearConsole


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
        #self.display_board(self.board)
        self.shown = set()
        self.gameover = False
        self.flag_alert = False
        #self.show(5,5)
        #self.display_board(self.ui_board)
        
        
    def get_difficulty_level(self):
        """
        Assign board size and bomb num according to
        the difficulty level chosen by the user
        """
        self.board_size = 15
        self.bomb_num = 15

    def create_new_board(self):
        """
        Create board arrays with none values
        Place bombs, represented by character *, at random coordinates in the board 
        """
        board = [[None for a in range(self.board_size)] for b in range(self.board_size)]
        self.ui_board = [["\U0001F532" for a in range(self.board_size)] for b in range(self.board_size)]
 

        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            # If the cell has already a bomb, skip and go to the top of the while loop
            if board[x][y] == "\U0001F4A5":
                continue
            # If the cell has no bomb, place it
            board[x][y] = "\U0001F4A5"
            bomb_counter += 1
        return board
  
    def insert_values(self):
        """
        for each cell that has no bomb, assign a value representing
        the number of bombs in the cells next to it
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == '\U0001F4A5':
                    continue
                self.board[x][y] = self.get_near_bombs_num(x,y)
        
    def get_near_bombs_num(self,x,y):
        """
        iterate through the 8 adiacent cells 
        """        
        near_bombs_num = 0
        for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
            for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                if r == x and c == y:
                    continue
                if self.board[r][c] == '\U0001F4A5':
                    near_bombs_num += 1
        return str(near_bombs_num)

    def display_board(self, board_to_show):
        """
        display board with format
        """
        self.board_to_show = board_to_show
        self.x_coordinates = []
        for a in range(self.board_size):
            if a < 9:
                self.x_coordinates.append('  ' + str(a+1))
            else:
                self.x_coordinates.append(' ' + str(a+1))
        self.x_coordinates = ' '.join(self.x_coordinates)
        print(self.x_coordinates)
        # stack board arrays
        for r in range(self.board_size):
            if r < 9:
                line_to_print = f"{str(r+1) + '  | ' + '  '.join(self.board_to_show[r])}"
            else:
                line_to_print = f"{str(r+1) + ' | ' + '  '.join(self.board_to_show[r])}"
            print(line_to_print)


    def show(self, x, y, flag):
        """
        check the cell chosen by the user:
        """
        if flag == False:
            self.shown.add((x,y))
            # If there is a bomb, game over
            if self.board[x][y] == "\U0001F4A5":
                self.ui_board[x][y] = self.board[x][y]
                self.gameover = True
            # If there is one or more adjacent bomb, show only that cell
            # in the displayed board
            elif int(self.board[x][y]) > 0:
                self.ui_board[x][y] = " " + self.board[x][y]
            # If there is no adjacent bomb, enlarge the shown area until
            # you find a cell with adjacent bombs
            elif int(self.board[x][y]) == 0:
                self.ui_board[x][y] = "\U0001F340"
                for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
                    for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                        if (r, c) in self.shown:
                            continue
                        self.show(r, c, flag)
        else:
            if self.ui_board[x][y] == "\U0001F532": # ascii white square
                self.ui_board[x][y] = "\U0001F6A9" # ascii Flag
            elif self.ui_board[x][y] == "\U0001F6A9": # ascii Flag
                self.ui_board[x][y] = "\U0001F532" # ascii white square
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
                print("\nGame Over!")
                self.restart_game()
                break
            else:   
                starter = input(Fore.WHITE + "\n-  Press Enter to dig\n-  Press F to place/remove a flag\n")
                if starter == "F":
                    flag = True
                    self.flag_alert = False
                    self.clear_display()
                    self.display_board(self.ui_board)
                    x = int(input("\ninsert the row number of the selected cell: ")) - 1
                    if x < 0 or x > self.board_size + 1:
                        print("The row does not exist")
                        continue
                    y = int(input("insert the column number of the selected cell: ")) - 1
                    if y < 0 or y > self.board_size + 1:
                        print("The column does not exist")
                        continue
                    self.clear_display()
                    self.show(x,y,flag)
                else:
                    flag = False
                    self.clear_display()
                    self.display_board(self.ui_board)
                    x = int(input("\ninsert the row number of the selected cell: ")) - 1
                    if x < 0 or x > self.board_size + 1:
                        print("The row does not exist")
                        continue
                    y = int(input("insert the column number of the selected cell: ")) - 1
                    if y < 0 or y > self.board_size + 1:
                        print("The column does not exist")
                        continue
                    # If there is a flag, print alert
                    if self.ui_board[x][y] == "\U0001F6A9":
                        print(Fore.RED + "\nPlease remove the flag before digging")
                        self.flag_alert = True 
                    else:
                        self.flag_alert = False
                        self.clear_display()
                        self.show(x,y,flag)


    def restart_game(self):
        """
        If the user wins or loses, ask to restart
        """
        restart = input("Do you want to play again) (y/n)\n")
        if restart == "y":
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
    print("Hello! What is your name?")
    username = input().strip()
    print("Hi " + Fore.GREEN + f"{username}!")
    while True:
        user_selection = input(Fore.WHITE + "Please select 'Play' to start the game or 'Tutorial' for the guide.\n \t p: play \n \t t: tutorial\n")
        if user_selection in ["play", "p", "yes", "y"]:
            game.clear_display()
            game.run_game()
        elif user_selection in ["tutorial", "t"]:
            print("Tutorial to be inserted")
        else:
            print(Fore.RED + f"Hey {username}, your input is not recognized, please try again!")
        if game.gameover == True:
            break

"""
def main():
    #insert if you want to play or not
    game = Game()
"""
    
#main()
main()




