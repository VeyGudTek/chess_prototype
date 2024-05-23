import asyncio
from chess import Game

class Session():
    def __init__(self):
        self.game = Game()
        self.turn_white = asyncio.Event()
        self.turn_white.set()
        self.turn_black = asyncio.Event()
        self.game_start = asyncio.Event()
        self.player = 'white'
        self.prev_move = None

    def set_player(self):
        if self.player == 'white':
            self.player = 'black'
            return 'white'
        else:
            self.player = 'done'
            return 'black'

    def get_event(self, player_color):
        if player_color == 'white':
            return self.turn_white
        else:
            return self.turn_black

    def switch_turns(self):
        if self.turn_white.is_set():
            self.turn_white.clear()
            self.turn_black.set()
        else:
            self.turn_white.set()
            self.turn_black.clear()

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
        session.game_start.set()
    
    #Wait for game to start
    await session.game_start.wait()
    print('Game started')
    
    #Gameplay Loop
    while True:
        #SEND MESSAGE TO CLIENT TO INITIATE TURN
        await wait_turn.wait()
        writer.write(str(session.prev_move).encode())
        await writer.drain()
        print('sent prev move to', player_color)

        #GET MOVE FROM CLIENT
        data = await reader.read(100)
        print('Received Move:', data.decode())
        session.game.move_piece(data.decode())
        session.prev_move = data.decode()
        session.switch_turns()

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(new_client, '127.0.0.1', 9999)
    
    print('Server Started')

    async with server:
        await server.serve_forever()

asyncio.run(server())