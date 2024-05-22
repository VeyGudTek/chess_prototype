from chess import Game
from pieces import Pawn, Knight, Bishop, Rook, King, Queen


game = Game()

game.board[3][0].piece = Queen((3, 0), 'black', game)
game.board[4][0].piece = Queen((4, 0), 'black', game)
#game.board[2][3].piece = Bishop((2, 3), 'white', game)

game.board[7][3].piece = Pawn((7, 3), 'white', game)
game.print_board()
if game.check_pawn():
    print('pawn needs to be converted')
    game.convert_pawn('biShop ')
game.print_board()

'''TEST CHECK_CHECK
game.white_king.coordinates = (3, 4)
game.board[7][4].piece = None
game.board[3][4].piece = game.white_king
game.print_board()

game.turn = 'black'
print(game.check_check())
print('kings moves:')
print(game.white_king.show_moves())
print(game.white_king.show_moves(True))

print('Bishop moves:')
print(game.board[2][3].piece.show_moves())
print(game.board[2][3].piece.show_moves(True))
print(game.board[7][6].piece.show_moves(True))
game.print_board()
game.check_state()

print(game.move_piece(input("move: ")))
game.print_board()
'''

