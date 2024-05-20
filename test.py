from chess import Game
from pieces import Pawn, Knight, Bishop, Rook, King, Queen


game = Game()

game.board[3][0].piece = Queen((3, 0), 'black', game)
game.board[2][3].piece = Knight((2, 3), 'white', game)

game.white_king.coordinates = (3, 4)
game.board[7][4].piece = None
game.board[3][4].piece = game.white_king
game.print_board()

game.turn = 'white'
print(game.check_check())
print('kings moves:')
print(game.white_king.show_moves())
print(game.white_king.check_fork(game.white_king.show_moves()))
print('knight moves:')
print(game.board[2][3].piece.show_moves())
print(game.board[2][3].piece.check_fork(game.board[2][3].piece.show_moves()))
#print(game.convert_input(input()))