import asyncio
from chess import Game

async def run():
    reader, writer = await asyncio.open_connection('127.0.0.1', 9999)

    #Initial Connection and Color Set
    print('Created Connection')
    print('Finding Match...')
    data = await reader.read(100)
    color = data.decode()
    print('You are player', data.decode())

    game = Game()
    game.print_board()

    while True:
        #Turn is initiated with message from server
        print('Waiting for other player...')
        data = await reader.read(100)
        print('Received Move:', data.decode())

        #Game End from Server
        if data.decode() == 'quit' or not data.decode():
            print('Connection Lost')
            break

        game.move_piece(data.decode())
        
        #Check State of Game       
        match game.check_state():
            case 5:
                #Checkmate
                print('CheckMate!')
                print('You Lost')
                break
            case 6:
                #Check
                print('Check!')
            case 7:
                #Pawn Conversion
                data = await reader.read(100)
                print('Pawn Converted:', data.decode())

                if data.decode() == 'quit' or not data.decode():
                    print('Connection Lost')
                    break
                
                game.convert_pawn(data.decode())

        game.print_board()
        user_input = input('Move Piece in format: [start coordinates] [end coordinates] (i.e "c4 c6")\nMove Piece: ').lower().strip()

        #Move Piece Loop
        while user_input != 'quit':
            match game.move_piece(user_input):
                case 1:
                    print('Invalid Input')
                case 2:
                    print("Not a valid piece")
                case 3:
                    print("Moved", user_input)
                    break
                case 4:
                    print('Invalid Move')
            user_input = input('Move Piece: ').lower().strip()

        game.print_board()

        #Send move to server
        writer.write(user_input.encode())
        await writer.drain()

        if user_input == 'quit':
            break    

        #Check game state
        match game.check_state():
            case 7:
                #Pawn Conversion Loop
                user_input = input('Convert Pawn(Options are [queen], [rook], [bishop], [knight]): ').lower().strip()

                while user_input != 'quit':
                    match game.convert_pawn(user_input):
                        case 10:
                            print('Please enter a valid Piece')
                        case 11:
                            print('Pawn Converted to', user_input.capitalize())
                            break
                    user_input = input('Convert Pawn: ').lower().strip()

                #Send conversion to server
                writer.write(user_input.encode())
                await writer.drain()

                if user_input == 'quit':
                    break   

                game.print_board()
            case 5: 
                #Checkmate
                print('CheckMate\n')
                print('You Won!')
                break

    writer.close()
    await writer.wait_closed()


asyncio.run(run())