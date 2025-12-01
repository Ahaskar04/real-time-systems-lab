import asyncio
import websockets


async def receive_message(websocket, queue):
    try:
        while True:
            msg = await websocket.recv()
            await queue.put(msg)
    except asyncio.CancelledError:
        # Task cancelled → exit cleanly
        pass


async def send_message(websocket, queue):
    try:
        while True:
            msg = await queue.get()
            await websocket.send(msg)
            queue.task_done()
    except asyncio.CancelledError:
        # Task cancelled → exit cleanly
        pass


async def handler(websocket):
    queue = asyncio.Queue(maxsize=10)  # bounded queue = backpressure
    print("Client connected")

    receive_task = asyncio.create_task(
        receive_message(websocket, queue)
    )
    send_task = asyncio.create_task(
        send_message(websocket, queue)
    )

    done, pending = await asyncio.wait(
        {receive_task, send_task},
        return_when=asyncio.FIRST_EXCEPTION,
    )

    # If either task finishes or crashes → cancel the other
    for task in pending:
        task.cancel()

    # Ensure all tasks fully exit
    await asyncio.gather(*pending, return_exceptions=True)

    print("Client disconnected, cleanup complete")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # run forever


asyncio.run(main())
