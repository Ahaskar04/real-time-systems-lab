import asyncio
import websockets

connected_clients = {}   # websocket -> user_id
user_counter = 0         # global counter to assign IDs


async def handler(websocket):
    global user_counter

    # Assign a unique ID to this client
    user_counter += 1
    user_id = user_counter
    connected_clients[websocket] = user_id

    # Notify everyone (with error handling!)
    disconnected = []
    for client in connected_clients:
        try:
            await client.send(f"User {user_id} has connected. Total: {len(connected_clients)}")
        except:
            disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        if client in connected_clients:
            del connected_clients[client]

    print(f"User {user_id} connected. Total:", len(connected_clients))

    try:
        async for message in websocket:
            sender_id = connected_clients[websocket]  # WHO sent it
            
            # Broadcast with error handling
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send(f"User {sender_id}: {message}")
                except:
                    print(f"Failed to send to a client")
                    disconnected.append(client)
            
            # Clean up disconnected clients
            for client in disconnected:
                if client in connected_clients:
                    del connected_clients[client]

    finally:
        # Get ID before removal
        if websocket in connected_clients:
            left_user_id = connected_clients[websocket]
            del connected_clients[websocket]
            
            print(f"User {left_user_id} disconnected. Total:", len(connected_clients))
            
            # Notify remaining clients (with error handling!)
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send(
                        f"User {left_user_id} has disconnected. Total: {len(connected_clients)}"
                    )
                except:
                    disconnected.append(client)
            
            # Clean up any failed sends
            for client in disconnected:
                if client in connected_clients:
                    del connected_clients[client]


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())