from pieces import Pawn, Knight, Square

class Game():
    def __init__(self):
        self.board = self.create_board()

    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.board[i][j].print_square()
            print()

    def create_board(self):
        new_board = [[Square('■') if (i + j) % 2 == 0 else Square('□')  for j in range(8)] for i in range(8)]

        #Pawns
        for i in range(8):
            new_board[1][i].piece = Pawn([1, i], 'black', new_board)
            new_board[6][i].piece = Pawn([6, i], 'white', new_board)

        return new_board

    def move_piece(self, old_coord, new_coord):
        selected_piece = self.board[old_coord[0]][old_coord[1]].piece

        if not selected_piece:
            print("No piece present.")
            return False
        elif new_coord in selected_piece.show_moves():
            print("ogey")
            self.board[old_coord[0]][old_coord[1]].piece = None
            self.board[new_coord[0]][new_coord[1]].piece = selected_piece
            return True
        else:
            print("Not a valid move.")
            return False

def test():
    game = Game()
    game.board[0][0].piece = Pawn([0, 0], 'black', game.board)
    game.board[5][6].piece = Pawn([5, 6], 'black', game.board)

    game.board[3][4].piece = Knight([3, 4], 'black', game.board)

    game.board[1][0].piece = None
    game.board[1][3].piece = None
    print(game.board[0][0].piece.show_moves())
    #game.move_piece([3, 4], [5, 5])

    game.print_board()

test()
