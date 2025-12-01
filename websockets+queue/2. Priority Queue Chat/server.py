import asyncio
import websockets
import itertools


async def receive_messages(websocket, queue, seq_counter):
    try:
        while True:
            data = await websocket.recv()

            # Format: "priority:message"
            try:
                priority_str, message = data.split(":", 1)
                priority = int(priority_str)
            except ValueError:
                # Default priority if not provided
                priority = 5
                message = data

            seq = next(seq_counter)

            item = (priority, seq, message)

            # Queue full → drop lowest-priority item
            if queue.full():
                dropped = queue.get_nowait()
                queue.task_done()

            await queue.put(item)

    except asyncio.CancelledError:
        pass


async def send_messages(websocket, queue):
    try:
        while True:
            priority, seq, message = await queue.get()
            await websocket.send(f"[p={priority}] {message}")
            queue.task_done()
    except asyncio.CancelledError:
        pass


async def handler(websocket):
    print("Client connected")

    queue = asyncio.PriorityQueue(maxsize=10)
    seq_counter = itertools.count()

    recv_task = asyncio.create_task(
        receive_messages(websocket, queue, seq_counter)
    )
    send_task = asyncio.create_task(
        send_messages(websocket, queue)
    )

    done, pending = await asyncio.wait(
        {recv_task, send_task},
        return_when=asyncio.FIRST_EXCEPTION,
    )

    for task in pending:
        task.cancel()

    await asyncio.gather(*pending, return_exceptions=True)

    print("Client disconnected")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
