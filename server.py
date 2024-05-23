import asyncio
from chess import Game

async def new_client(reader, writer):
    print("New Client:", writer.get_extra_info('peername'))

    data = await reader.read()
    print('Message:', data.decode())

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(new_client, '127.0.0.1', 9999)
    
    async with server:
        await server.serve_forever()

asyncio.run(server())