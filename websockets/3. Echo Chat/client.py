import asyncio
import websockets

async def echo():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server")
        
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            
            if message.lower() == 'quit':
                break
                
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(echo())