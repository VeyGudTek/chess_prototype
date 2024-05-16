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