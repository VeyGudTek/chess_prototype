import asyncio
from chess import Game

class Session():
    def __init__(self):
        self.game = Game()
        self.turn_1 = asyncio.Event()
        self.turn_1.set()
        self.turn_2 = asyncio.Event()
        self.player = 'white'

    def set_player(self):
        if self.player == 'white':
            self.player = 'black'
            return 'white'
        else:
            self.player = 'done'
            return 'black'

    def get_event(self, player_color):
        if player_color == 'white':
            return self.turn_1
        else:
            return self.turn_2

waiting = None

async def new_client(reader, writer):
    global waiting
    print("New Client:", writer.get_extra_info('peername'))

    #if no session waiting, create new one
    if not  waiting:
        waiting = Session()

    session = waiting
    player_color = session.set_player()
    wait_turn = session.get_event(player_color)

    writer.write(str(player_color).encode())
    await writer.drain()

    #Reset waiting if you are second player
    if session.player == 'done':
        waiting = None

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(new_client, '127.0.0.1', 9999)
    
    print('Server Started')

    async with server:
        await server.serve_forever()

asyncio.run(server())