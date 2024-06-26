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
        self.game_ended = False
        self.pawn_conversion = 'hold'

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
        #SEND MOVE TO CLIENT TO INITIATE TURN
        await wait_turn.wait()
        writer.write(str(session.prev_move).encode())
        await writer.drain()
        print('sent prev move to', player_color)

        #IF A PAWN CONVERSION WAS MADE, SEND IT
        if session.pawn_conversion != 'hold':
            writer.write(str(session.pawn_conversion).encode())
            await writer.drain()
            session.pawn_conversion = 'hold'
            print('sent pawn_conversion to', player_color)

        #END GAME
        if session.game_ended:
            break

        #GET MOVE FROM CLIENT
        data = await reader.read(100)
        print('Received Move:', data.decode())

        '''Get move loop for error checking
        while data.decode() != 'quit' and data.decode():
            match session.game.move_piece(data.decode()):
                case 3:
                    break
                case _:
                    writer.write('fail_move'.encode())
                    await writer.drain()
            data = await reader.read(100)
            print('Received Move:', data.decode())
        '''

        #Move Piece without Error Checking
        if session.game.move_piece(data.decode()) != 3:
                #Quit Game Check
                print('Game Ended from Quit')
                session.game_ended = True

        session.prev_move = data.decode()

        print(session.game.check_state())

        if session.game.check_state() == 7:
            #Get Pawn Conversion
            data = await reader.read(100)
            print('Received Pawn Conversion: ', data.decode())
            
            '''Loop for Error Checking
            while data.decode() != 'quit' and data.decode():
                match session.game.convert_pawn(data.decode()):
                    case 11:
                        break
                    case _:
                        writer.write('fail_pawn'.encode())
                        await writer.drain()
                data = await reader.read(100)
                print('Received Pawn Conversion: ', data.decode())
            
            session.pawn_conversion = data.decode()
            if not data.decode() in session.game.class_conversion.keys():
                #Quit Game Check
                print('Game Ended from Quit')
                session.game_ended = True
            '''
            
            session.pawn_conversion = data.decode()
            if session.game.convert_pawn(data.decode()) != 11:
                #Quit Game Check
                print('Game Ended from Quit')
                session.game_ended = True

        if session.game.check_state() == 5:
            #Checkmate check
            print('Game Ended from Checkmate')
            session.game_ended = True
        elif session.prev_move == 'quit' or not session.prev_move:
            #Quit game check
            print('Game Ended from Quit')
            session.game_ended = True

        session.switch_turns()

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(new_client, '127.0.0.1', 9999)
    
    print('Server Started')

    async with server:
        await server.serve_forever()

asyncio.run(server())