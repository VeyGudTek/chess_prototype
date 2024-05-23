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

    #game = Game()
    #game.print_board()

    while True:
        print('Waiting for other player to move...')
        data = await reader.read(100)
        print('Received Move:', data.decode())

        writer.write(input('Move: ').encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


asyncio.run(run())