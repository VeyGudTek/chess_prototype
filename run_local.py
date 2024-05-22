from chess import Game

class Interface():
    def __init__(self):
        self.game = None

    def print_game(self):
        self.game.print_board()
        print(f'Turn: {self.game.turn}')

    def move_input(self):
        while True:
            user_input = input('Enter move in the form: <starting_coordinates> <destination_coordinates>\n Coordinates should be in form <letter><number> (i.e "a6 a5")\n Enter "back" to go back\n Command: ')
            user_input = user_input.strip().lower()

            if user_input == 'back':
                break

            match self.game.move_piece(user_input):
                case 1:
                    print('Invalid Input')
                case 2:
                    print("Not a valid piece")
                case 3:
                    print("Moved", user_input)
                    break
                case 4:
                    print('Invalid Move')

    def pawn_input(self):
        while True:
            
            user_input = input('Enter a piece to convert to (Options are [queen], [rook], [bishop], [knight]): ')
            user_input = user_input.strip().lower()

            match self.game.convert_pawn(user_input):
                case 9:
                    break
                case 10:
                    print('Please enter a valid Piece')
                case 11:
                    print('Pawn Converted to', user_input.capitalize())
                    break

    def run(self):
        self.game = Game()

        while True:
            self.print_game()
            user_input = input('Enter a Command:\n\
                [move]\n\
                [show]\n\
                [quit]\n')

            match user_input.lower().strip():
                case 'move':
                    self.move_input()
                case 'show':
                    self.print_game()
                case 'quit':
                    break
            
            match self.game.check_state():
                case 5:
                    print('CheckMate')
                    break
                case 6:
                    print('Check')
                case 7:
                    self.game.print_board()
                    print("Pawn has reached the end of the board.")
                    self.pawn_input()
                case 8:
                    print('No Event')

def main():
    interface = Interface()
    interface.run()

main()