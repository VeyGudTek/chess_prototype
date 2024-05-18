from pieces import Pawn, Knight, Bishop, Rook, King, Queen, Square

class Game():
    def __init__(self):
        self.board = self.create_board()
        self.x_conversion = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def print_board(self):
        for i in range(len(self.board)):
            print(8 - i, end=" ")
            for j in range(len(self.board)):
                self.board[i][j].print_square()
            print()
        print('  a b c d e f g h')

    def create_board(self):
        new_board = [[Square('■') if (i + j) % 2 == 0 else Square('□')  for j in range(8)] for i in range(8)]

        #Pawns
        for i in range(8):
            new_board[1][i].piece = Pawn([1, i], 'black', new_board)
            new_board[6][i].piece = Pawn([6, i], 'white', new_board)

        return new_board

    def move_piece(self, old_coord, new_coord, color):
        selected_piece = self.board[old_coord[0]][old_coord[1]].piece

        if (not selected_piece) or (selected_piece.color != color):
            print("No valid piece selected.")
            return False
        elif new_coord in selected_piece.show_moves():
            print("ogey")
            self.board[old_coord[0]][old_coord[1]].piece = None
            self.board[new_coord[0]][new_coord[1]].piece = selected_piece
            return True
        else:
            print("Not a valid move.")
            return False

    def convert_input(self, user_input):
        user_input = user_input.strip().split()
        #Check format and type
        if len(user_input) != 2:
            return False
        
        input_1 = user_input[0]
        input_2 = user_input[1]

        if len(input_1) != 2 or not (input_1[0].isalpha()) or not(input_1[1].isdigit()):
            return False
        if len(input_2) != 2 or not (input_2[0].isalpha()) or not(input_2[1].isdigit()):
            return False

        #Check Range of Input
        if (not input_1[0] in self.x_conversion) or (not input_2[0] in self.x_conversion):
            return False
        if (not int(input_1[1]) in range(1, 9)) or (not int(input_2[1]) in range(1, 9)):
            return False

        return [8 - int(input_1[1]), self.x_conversion[input_1[0]]], [8 - int(input_2[1]), self.x_conversion[input_2[0]]]

def test():
    game = Game()
    game.board[0][0].piece = Pawn([0, 0], 'black', game.board)
    game.board[5][6].piece = Pawn([5, 6], 'black', game.board)

    game.board[3][4].piece = Knight([3, 4], 'black', game.board)
    game.board[4][3].piece = Bishop([4, 3], 'white', game.board)
    game.board[5][4].piece = Rook([5, 4], 'white', game.board)
    game.board[3][3].piece = King([3, 3], 'white', game.board)
    game.board[3][6].piece = Queen([3, 6], 'white', game.board)

    game.board[1][0].piece = None
    game.board[1][3].piece = None
    print(game.board[3][4].piece.show_moves())
    game.move_piece([3, 5], [3, 5], 'black')

    game.print_board()
    #print(game.convert_input(input()))

test()
