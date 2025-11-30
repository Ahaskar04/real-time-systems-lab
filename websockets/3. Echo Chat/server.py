import asyncio
import websockets

async def handler(websocket):
    print("Client connected")
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # This waits forever

asyncio.run(main())