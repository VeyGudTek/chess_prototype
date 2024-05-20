from chess import Game
from pieces import Pawn, Knight, Bishop, Rook, King, Queen


game = Game()

game.board[3][0].piece = Queen((3, 0), 'black', game.board)

game.white_king.coordinates = (3, 4)
game.board[7][4].piece = None
game.board[3][4].piece = game.white_king
game.print_board()

game.turn = 'white'
print(game.check_check())
#print(game.convert_input(input()))