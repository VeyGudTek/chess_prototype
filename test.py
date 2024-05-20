from chess import Game
from pieces import Pawn, Knight, Bishop, Rook, King, Queen


game = Game()

game.board[3][0].piece = Queen((3, 0), 'black', game)

game.white_king.coordinates = (4, 4)
game.board[7][4].piece = None
game.board[4][4].piece = game.white_king
game.print_board()

game.turn = 'white'
print(game.check_check())
print(game.white_king.show_moves())
print(game.white_king.check_fork(game.white_king.show_moves()))
#print(game.convert_input(input()))