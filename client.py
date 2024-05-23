import asyncio

async def run():
    reader, writer = await asyncio.open_connection('127.0.0.1', 9999)

    print('Created Connection')

    print('Getting ID...')
    data = await reader.read()
    
    print('You are player', data.decode())

    writer.close()
    await writer.wait_closed()


asyncio.run(run())