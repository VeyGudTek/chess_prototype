from chess import Game

game = Game()

game.board[0][0].piece = Pawn((0, 0), 'black', game.board)
game.board[5][6].piece = Pawn((5, 6), 'black', game.board)

game.board[3][4].piece = Knight((3, 4), 'black', game.board)
game.board[4][3].piece = Bishop((4, 3), 'white', game.board)
game.board[5][4].piece = Rook((5, 4), 'white', game.board)
game.board[3][3].piece = King((3, 3), 'white', game.board)
game.board[3][6].piece = Queen((3, 6), 'white', game.board)
game.board[1][0].piece = None
game.board[1][3].piece = None
print(game.board[7][1].piece.show_moves())
print(game.convert_input('b1 a3'))
game.print_board()
#print(game.convert_input(input()))