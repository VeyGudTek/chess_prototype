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
        print('Waiting for other player to move...')
        data = await reader.read(100)
        print('Received Move:', data.decode())

        #Game End from Server
        if data.decode() == 'quit' or not data.decode():
            print('Connection Lost')
            break

        #Check State of Game
        game.move_piece(data.decode())
        game.print_board()
        match game.check_state():
            case 5:
                print('CheckMate!')
                print('You Lost')
                break
            case 6:
                print('Check!')

        user_input = input('Move Piece: ').lower().strip()

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

        writer.write(user_input.encode())
        await writer.drain()

        if user_input == 'quit':
            break    

        #Check for Win
        if game.check_state() == 5:
            print('CheckMate\n')
            print('You Won!')
            break

    writer.close()
    await writer.wait_closed()


asyncio.run(run())