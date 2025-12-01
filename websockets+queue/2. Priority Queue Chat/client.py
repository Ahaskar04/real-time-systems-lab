import asyncio
import websockets


async def chat():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        print("Send messages as: priority:message (lower = higher priority)")
        print("Type 'quit' to exit\n")

        async def sender():
            while True:
                msg = input("> ")
                if msg.lower() == "quit":
                    break
                await websocket.send(msg)

        async def receiver():
            while True:
                response = await websocket.recv()
                print("Received:", response)

        await asyncio.gather(sender(), receiver())


asyncio.run(chat())
