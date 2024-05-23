import asyncio

async def run():
    reader, writer = await asyncio.open_connection('127.0.0.1', 9999)

    print('Created Connection')

    message = input('Enter Message: ')
    writer.write(message.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()


asyncio.run(run())