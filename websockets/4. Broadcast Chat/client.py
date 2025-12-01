import asyncio
import websockets

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
        return
    except Exception as e:
        print(f"Error receiving: {e}")
        return
    
async def send_messages(websocket):
    # handle user input and sending
    while True:
        # Run input in a thread so it doesn't block the event loop
        message = await asyncio.get_event_loop().run_in_executor(
            None, 
            input, 
            "Enter message (or 'quit' to exit): "
        )
        
        if message.lower() == 'quit':
            break
            
        await websocket.send(message)

async def main():
    uri = "ws://localhost:8765"
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected successfully!")
            
            receive_task = asyncio.create_task(receive_messages(websocket))
            
            # Run send_messages directly (not as a task)
            await send_messages(websocket)
            
            # When send completes (user quit), cancel receive
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())