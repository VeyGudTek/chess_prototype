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

        game.move_piece(data.decode())
        game.print_board()

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

        if user_input == 'quit':
            break    

        writer.write(user_input.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


asyncio.run(run())