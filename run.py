import random

class CreateBoard:
    """
    Create the gaming board
    """
    def __init__(self, board_size, bomb_num):
        """
        Board size and bomb number variable assignment 
        """
        self.board_size = board_size
        self.bomb_num = bomb_num

        self.board = self.create_new_board()

    def create_new_board(self):
        """
        Create board arrays with none values
        Place bombs, represented by character "*", at random coordinates in the board 
        """
        board = [[None for a in range(self.board_size)] for b in range(self.board_size)]
        
        bomb_counter = 0
        while bomb_counter < self.bomb_num:
            # Generate two random coordinates considering the size of the board
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            # If the cell of the board has already a bomb, continue (skip and go at the top of the while loop)
            if board[x][y] == "*":
                continue
            # If the cell has no bomb, place it
            board[x][y] = "*"
            bomb_counter += 1
        
        print(board)


        


CreateBoard(10, 10)


