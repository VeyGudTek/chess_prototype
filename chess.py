from pieces import Pawn, Knight, Bishop, Rook, King, Queen, Square

class Game():
    def __init__(self):
        self.white_king = None
        self.black_king = None
        self.board = self.create_board()
        self.turn = 'white'
        self.x_conversion = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.class_conversion = {'queen': Queen, 'rook': Rook, 'bishop': Bishop, 'knight': Knight}
        self.response_code = {1: "Invalid Move Input", 2: "Invalid Piece Selection", 3: "Successful Move", 4: "Invalid Move", 5: "CheckMate",\
             6: "Check", 7: "No Event" , 8: "Pawn Conversion", 9: "No Pawn to Convert", 10: "Not Valid Class", 11: "Pawn Converted"}

    def print_board(self):
        for i in range(len(self.board)):
            print(8 - i, end=" ")
            for j in range(len(self.board)):
                self.board[i][j].print_square()
            print()
        print('  a b c d e f g h')

    def create_board(self):
        new_board = [[Square('■') if (i + j) % 2 == 0 else Square('□')  for j in range(8)] for i in range(8)]

        #Kings and Queens
        new_board[0][4].piece = King((0, 4), 'black', self)
        new_board[0][3].piece = Queen((0, 3), 'black', self)
        new_board[7][4].piece = King((7, 4), 'white', self)
        new_board[7][3].piece = Queen((7, 3), 'white', self)

        self.white_king = new_board[7][4].piece
        self.black_king = new_board[0][4].piece

        #Pawns
        for i in range(8):
            new_board[1][i].piece = Pawn((1, i), 'black', self)
            new_board[6][i].piece = Pawn((6, i), 'white', self)

        #Rooks
        new_board[0][0].piece = Rook((0, 0), 'black', self)
        new_board[0][7].piece = Rook((0, 7), 'black', self)
        new_board[7][0].piece = Rook((7, 0), 'white', self)
        new_board[7][7].piece = Rook((7, 7), 'white', self)

        #Knights
        new_board[0][1].piece = Knight((0, 1), 'black', self)
        new_board[0][6].piece = Knight((0, 6), 'black', self)
        new_board[7][1].piece = Knight((7, 1), 'white', self)
        new_board[7][6].piece = Knight((7, 6), 'white', self)

        #Bishops
        new_board[0][2].piece = Bishop((0, 2), 'black', self)
        new_board[0][5].piece = Bishop((0, 5), 'black', self)
        new_board[7][2].piece = Bishop((7, 2), 'white', self)
        new_board[7][5].piece = Bishop((7, 5), 'white', self)

        return new_board

    def move_piece(self, user_input):
        old_coord, new_coord = self.convert_input(user_input)
        if not old_coord:
            #Invalid Input
            return 1

        selected_piece = self.board[old_coord[0]][old_coord[1]].piece

        if (not selected_piece) or (selected_piece.color != self.turn):
            #Invalid Piece Selection
            return 2
        elif new_coord in selected_piece.show_moves(True):
            #Move and Update Piece
            self.board[old_coord[0]][old_coord[1]].piece = None
            self.board[new_coord[0]][new_coord[1]].piece = selected_piece
            selected_piece.coordinates = (new_coord[0], new_coord[1])
            if isinstance(selected_piece, Pawn):
                selected_piece.start = False

            #Update Turn
            if self.turn == "black":
                self.turn = "white"
            else:
                self.turn = "black"
            
            return 3
        else:
            #Invalid Move
            return 4

    def convert_input(self, user_input):
        user_input = user_input.strip().lower().split()
        #Check format and type
        if len(user_input) != 2:
            return False, ''
        
        input_1 = user_input[0]
        input_2 = user_input[1]

        if len(input_1) != 2 or not (input_1[0].isalpha()) or not(input_1[1].isdigit()):
            return False, ''
        if len(input_2) != 2 or not (input_2[0].isalpha()) or not(input_2[1].isdigit()):
            return False, ''

        #Check Range of Input
        if (not input_1[0] in self.x_conversion) or (not input_2[0] in self.x_conversion):
            return False, ''
        if (not int(input_1[1]) in range(1, 9)) or (not int(input_2[1]) in range(1, 9)):
            return False, ''

        return (8 - int(input_1[1]), self.x_conversion[input_1[0]]), (8 - int(input_2[1]), self.x_conversion[input_2[0]])
    
    def get_dangerous_squares(self, color, check_next=False):
        dangerous_squares = set()
        for row in self.board:
            for square in row:
                if square.piece and square.piece.color != color:
                    dangerous_squares = dangerous_squares.union(set(square.piece.show_moves(check_next)))
        return dangerous_squares

    def check_check(self):
        dangerous_squares = self.get_dangerous_squares(self.turn)

        if self.turn == 'black' and self.black_king.coordinates in dangerous_squares:
            return True
        if self.turn == 'white' and self.white_king.coordinates in dangerous_squares:
            return True
        return False

    def check_state(self):
        opp_turn = 'white'
        if self.turn == 'white':
            opp_turn = 'black'
        
        if self.check_check() and len(self.get_dangerous_squares(opp_turn, True)) == 0:
            #Checkmate
            return 5
        elif self.check_check():
            #Check
            return 6
        elif self.check_pawn():
            #Pawn Ready to Convert
            return 7
        else:
            #No event
            return 8
    
    def check_pawn(self):
        pawn = None
        for i in [0, 7]:
            for square in self.board[i]:
                if isinstance(square.piece, Pawn):
                    pawn = square.piece

        if not pawn:
            return False
        else:
            return pawn

    def convert_pawn(self, user_input):
        pawn = self.check_pawn()
        if not pawn:
            #No Pawn to Convert
            return 9

        user_input = user_input.strip().lower()
        if not user_input in self.class_conversion:
            #Not a valid Piece
            return 10
        else:
            #Pawn Converted
            self.board[pawn.coordinates[0]][pawn.coordinates[1]].piece = self.class_conversion[user_input]((pawn.coordinates), pawn.color, self)
            return 11
