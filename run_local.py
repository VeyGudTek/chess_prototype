from chess import Game

def main():
    game = Game()
    while True:
        game.print_board()
        game.move_piece(input(f"Turn: {game.turn} \nMake move: "))

main()