class CreateBoard:
    """
    Create the gaming board
    """
    def __init__(self, board_size, bomb_num):
        """
        board size and bomb number variable assignemnt 
        """
        self.board_size = board_size
        self.bomb_num = bomb_num

        self.board = self.create_new_board()

    def create_new_board(self):
        """
        Creat board arrays with none values
        """
        board = [[None for a in range(self.board_size)] for b in range(self.board_size)]
        
        print(board)

CreateBoard(10, 10)


