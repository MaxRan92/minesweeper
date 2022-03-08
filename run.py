import random

class CreateBoard:
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
        self.board = self.create_new_board()
        self.insert_values()
        #self.display_board(self.board)
        self.shown = set()
        #self.show(5,5)
        #self.display_board(self.ui_board)
        
        
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
        Place bombs, represented by character "*", at random coordinates in the board 
        """
        board = [[None for a in range(self.board_size)] for b in range(self.board_size)]
        self.ui_board = [['x' for a in range(self.board_size)] for b in range(self.board_size)]

        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            # If the cell has already a bomb, skip and go to the top of the while loop
            if board[x][y] == "*":
                continue
            # If the cell has no bomb, place it
            board[x][y] = "*"
            bomb_counter += 1
        return board
  
    def insert_values(self):
        """
        for each cell that has no bomb, assign a value representing
        the number of bombs in the cells next to it
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == "*":
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
                if self.board[r][c] == '*':
                    near_bombs_num += 1
        return str(near_bombs_num)

    def display_board(self, board_to_show):
        """
        display board with format
        """
        self.board_to_show = board_to_show
        #stack board arrays
        for r in range(self.board_size):
            #print(self.board[r])
            line_to_print = ' '.join(self.board_to_show[r])
            print(line_to_print) 

    def show(self, x, y):
        """
        check the cell chosen by the user:
        """
        self.shown.add((x,y))
        #If there is a bomb, game over
        if self.board[x][y] == "*":
            print("Game Over")
        #If there is one or more adjacent bomb, show only that cell
        #in the displayed board 
        elif int(self.board[x][y]) > 0:
            self.ui_board[x][y] = self.board[x][y]   
        #If there is no adjacent bomb, enlarge the shown area until
        #you find a cell with adjacent bombs 
        elif int(self.board[x][y]) == 0:
            self.ui_board[x][y] = "-"
            for r in range(max(0, x-1), min(self.board_size-1, x+1)+1):
                for c in range(max(0, y-1), min(self.board_size-1, y+1)+1):
                    if (r,c) in self.shown:
                        continue
                    self.show(r, c)

def run_game():
    board = CreateBoard()
    while len(board.shown) < board.board_size ** 2 - board.bomb_num:
        board.display_board(board.ui_board)
        x = int(input("input the row number of the selected cell: ")) - 1
        if x < 0 or x > board.board_size + 1:
            print("The row does not exist")
            continue
        y = int(input("input the column number of the selected cell: ")) - 1
        if y < 0 or y > board.board_size + 1:
            print("The column does not exist")
            continue
        board.show(x,y)

"""
def main():
    #insert if you want to play or not
    game = CreateBoard()
"""
    
#main()
run_game()




