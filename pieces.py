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
    def __init__(self, coordinates, color, game):
        self.coordinates = coordinates
        self.color = color
        self.game = game

    def check_fork(self, moves):
        valid_moves = []
        original_coordinates = self.coordinates
        
        for move in moves:
            #Make the move
            self.game.board[original_coordinates[0]][original_coordinates[1]].piece = None
            old_piece = self.game.board[move[0]][move[1]].piece
            self.game.board[move[0]][move[1]].piece = self
            self.coordinates = move

            if not self.game.check_check():
                valid_moves.append(move)

            #Revert Move
            self.game.board[original_coordinates[0]][original_coordinates[1]].piece = self
            self.game.board[move[0]][move[1]].piece = old_piece
            self.coordinates = original_coordinates
        
        return valid_moves

    def add_direction(self, moves, x_offset, y_offset, recursive = False, x_base = 0, y_base = 0):
        #Check in bounds
        if not self.check_in_bounds(x_offset + x_base, y_offset + y_base):
            return

        #Check for same colored pieces
        if not self.game.board[self.coordinates[0] + y_offset + y_base][self.coordinates[1] + x_offset + x_base].piece:
            moves.append((self.coordinates[0] + y_offset + y_base, self.coordinates[1] + x_offset + x_base))
        elif self.game.board[self.coordinates[0] + y_offset + y_base][self.coordinates[1] + x_offset + x_base].piece.color != self.color:
            moves.append((self.coordinates[0] + y_offset + y_base, self.coordinates[1] + x_offset + x_base))
            return
        else:
            return

        if recursive:
            self.add_direction(moves, x_offset, y_offset, True, x_base + x_offset, y_base + y_offset)

    def check_in_bounds(self, x_offset, y_offset):
        if not ((self.coordinates[0] + y_offset <= 7) and (self.coordinates[0] + y_offset >= 0)):
            return False
        if not ((self.coordinates[1] + x_offset <= 7) and (self.coordinates[1] + x_offset >= 0)):
            return False
        return True

class Pawn(Piece):
    def __init__(self, coordinates, color, game):
        super().__init__(coordinates, color, game)
        self.start = True

    def show_moves(self, check_next=False):
        moves = []
        increment = 1 if self.color == 'black' else -1

        #Check in bounds
        if not (self.check_in_bounds(0, increment)):
            return moves

        #Check in front
        if not self.game.board[self.coordinates[0] + increment][self.coordinates[1]].piece:
            moves.append((self.coordinates[0] + increment, self.coordinates[1]))

        #Check long start
        if (self.start) and (self.check_in_bounds(0, increment * 2)) and (not self.game.board[self.coordinates[0] + increment * 2][self.coordinates[1]].piece):
            moves.append((self.coordinates[0] + increment * 2, self.coordinates[1]))
        
        #Check Diagonal
        if (self.check_in_bounds(1, increment)) and (self.game.board[self.coordinates[0] + increment][self.coordinates[1] + 1].piece) and (self.game.board[self.coordinates[0] + increment][self.coordinates[1] + 1].piece.color != self.color):
            moves.append((self.coordinates[0] + increment, self.coordinates[1] + 1))
        if (self.check_in_bounds(-1, increment)) and (self.game.board[self.coordinates[0] + increment][self.coordinates[1] - 1].piece) and (self.game.board[self.coordinates[0] + increment][self.coordinates[1] - 1].piece.color != self.color):
            moves.append((self.coordinates[0] + increment, self.coordinates[1] - 1))

        if check_next:
            moves = self.check_fork(moves)
        
        return moves

    def print_piece(self):
        if self.color == 'black':
            print('♙', end=' ')
        else:
            print('♟︎', end=' ')


class Knight(Piece):
    def show_moves(self, check_next = False):
        moves = []

        #Add L movement
        self.add_direction(moves, 1, 2)
        self.add_direction(moves, 2, 1)
        self.add_direction(moves, -1, 2)
        self.add_direction(moves, -2, 1)
        self.add_direction(moves, -1, -2)
        self.add_direction(moves, -2, -1)
        self.add_direction(moves, 1, -2)
        self.add_direction(moves, 2, -1)

        if check_next:
            moves = self.check_fork(moves)

        return moves

    def print_piece(self):
        if self.color == "black":
            print('♘', end=" ")
        else:
            print('♞', end=" ")


class King(Piece):
    def show_moves(self, check_next = False):
        moves = []

        self.add_direction(moves, 0, 1)
        self.add_direction(moves, 1, 0)
        self.add_direction(moves, 0, -1)
        self.add_direction(moves, -1, 0)
        self.add_direction(moves, 1, 1)
        self.add_direction(moves, -1, 1)
        self.add_direction(moves, -1, -1)
        self.add_direction(moves, 1, -1)

        if check_next:
            moves = self.check_fork(moves)

        return moves

    def print_piece(self):
        if self.color == "black":
            print("♔", end=" ")
        else:
            print("♚", end=" ")


class Bishop(Piece):
    def show_moves(self, check_next = False):
        moves = []

        self.add_direction(moves, 1, 1, True)
        self.add_direction(moves, -1, 1, True)
        self.add_direction(moves, -1, -1, True)
        self.add_direction(moves, 1, -1, True)

        if check_next:
            moves = self.check_fork(moves)

        return moves
    
    def print_piece(self):
        if self.color == "black":
            print("♗", end=" ")
        else:
            print("♝", end=" ")


class Rook(Piece):
    def show_moves(self, check_next = False):
        moves = []

        self.add_direction(moves, 0, 1, True)
        self.add_direction(moves, 1, 0, True)
        self.add_direction(moves, 0, -1, True)
        self.add_direction(moves, -1, 0, True)

        if check_next:
            moves = self.check_fork(moves)

        return moves
    
    def print_piece(self):
        if self.color == "black":
            print("♖", end=" ")
        else:
            print("♜", end=" ")


class Queen(Piece):
    def show_moves(self, check_next=False):
        moves = []

        self.add_direction(moves, 0, 1, True)
        self.add_direction(moves, 1, 0, True)
        self.add_direction(moves, 0, -1, True)
        self.add_direction(moves, -1, 0, True)
        self.add_direction(moves, 1, 1, True)
        self.add_direction(moves, -1, 1, True)
        self.add_direction(moves, -1, -1, True)
        self.add_direction(moves, 1, -1, True)

        if check_next:
            moves = self.check_fork(moves)

        return moves
    
    def print_piece(self):
        if self.color == "black":
            print("♕", end=" ")
        else:
            print("♛", end=" ")