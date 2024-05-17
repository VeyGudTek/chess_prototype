class Square():
    def __init__(self, color):
        self.piece = None
        self.color = color

    def print_square(self):
        if self.piece:
            self.piece.print_piece()
        else:
            print(self.color, end=' ')

class Piece():
    def __init__(self, coordinates, color, board):
        self.coordinates = coordinates
        self.color = color
        self.board = board

class Pawn(Piece):
    def show_moves(self):
        moves = []
        increment = 1 if self.color == 'black' else -1

        #Check in bounds
        if not (self.coordinates[0] + increment <= 7) and (self.coordinates[0] + increment >= 0):
            return moves

        #Check in front
        if not self.board[self.coordinates[0] + increment][self.coordinates[1]].piece:
            moves.append([self.coordinates[0] + increment, self.coordinates[1]])
        
        #Check Diagonal
        if self.board[self.coordinates[0] + increment][self.coordinates[1] + 1].piece and self.board[self.coordinates[0] + increment][self.coordinates[1] + 1].piece.color != self.color:
            moves.append([self.coordinates[0] + increment, self.coordinates[1] + 1])
        if self.board[self.coordinates[0] + increment][self.coordinates[1] - 1].piece and self.board[self.coordinates[0] + increment][self.coordinates[1] - 1].piece.color != self.color:
            moves.append([self.coordinates[0] + increment, self.coordinates[1] - 1])
        
        return moves

    def print_piece(self):
        if self.color == 'black':
            print('♙', end=' ')
        else:
            print('♟︎', end=' ')


class Knight(Piece):
    def show_moves(self):
        moves = []

        #Check L movement
        if self.check_valid(1, 2):
            moves.append([self.coordinates[0] + 2, self.coordinates[1] + 1])
        if self.check_valid(2, 1):
            moves.append([self.coordinates[0] + 1, self.coordinates[1] + 2])
        if self.check_valid(-1, 2):
            moves.append([self.coordinates[0] + 2, self.coordinates[1] - 1])
        if self.check_valid(-2, 1):
            moves.append([self.coordinates[0] + 1, self.coordinates[1] - 2])
        if self.check_valid(-1, -2):
            moves.append([self.coordinates[0] - 2, self.coordinates[1] - 1])
        if self.check_valid(-2, -1):
            moves.append([self.coordinates[0] - 1, self.coordinates[1] - 2])
        if self.check_valid(1, -2):
            moves.append([self.coordinates[0] - 2, self.coordinates[1] + 1])
        if self.check_valid(2, -1):
            moves.append([self.coordinates[0] - 1, self.coordinates[1] + 2])

        return moves

    def check_valid(self, x_offset, y_offset):
        #Check in bounds
        if not ((self.coordinates[0] + y_offset <= 7) and (self.coordinates[0] + y_offset >= 0)):
            return False
        if not ((self.coordinates[1] + x_offset <= 7) and (self.coordinates[1] + x_offset >= 0)):
            return False

        #Check for same colored pieces
        if not self.board[self.coordinates[0] + y_offset][self.coordinates[1] + x_offset].piece:
            return True
        elif self.board[self.coordinates[0] + y_offset][self.coordinates[1] + x_offset].piece.color != self.color:
            return True
        else:
            return False

    def print_piece(self):
        if self.color == "black":
            print('♘', end=" ")
        else:
            print('♞', end=" ")