## WebSocket Echo Server - Learning Project

### What I Built

A simple WebSocket echo server that receives messages from clients and sends them back with "Echo: " prefix. This is my first WebSocket project to understand the fundamentals of real-time, bidirectional communication.

### What are WebSockets?

WebSockets provide a persistent, two-way communication channel between a client and server. Unlike HTTP:

- **HTTP**: Client requests → Server responds → Connection closes
- **WebSocket**: Client ↔️ Server stay connected and can send messages anytime

Think of it like a phone call (WebSocket) vs sending letters (HTTP).

### Project Structure

```
.
├── echo_server.py   # The WebSocket server
├── test_client.py   # Interactive client
└── README.md        # This file
```

### How It Works

#### The Server (`echo_server.py`)

```python
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
```

**What each part does:**

- `handler(websocket)`: Handles each client connection
  - Prints when client connects
  - Loops through incoming messages (`async for message in websocket`)
  - Sends back each message with "Echo: " prefix
  - Loop automatically ends when client disconnects
- `main()`: Sets up the server
  - `websockets.serve()`: Starts listening on localhost:8765
  - `await asyncio.Future()`: Keeps server running forever (never completes)

#### The Client (`test_client.py`)

```python
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
```

**What each part does:**

- `websockets.connect(uri)`: Establishes connection to server
- `while True`: Keeps the client running for multiple messages
- `input()`: Gets message from user
- `websocket.send()`: Sends message to server
- `websocket.recv()`: Waits for and receives the echo
- Connection automatically closes when exiting the `async with` block

### Installation & Setup

1. **Install the WebSocket library:**

```bash
pip install websockets
```

2. **Run the server (Terminal 1):**

```bash
python echo_server.py
```

You should see: `Server started on ws://localhost:8765`

3. **Run the client (Terminal 2):**

```bash
python test_client.py
```

You should see: `Connected to the server`

4. **Test it:**

- Type messages in the client
- See them echoed back with "Echo: " prefix
- Type 'quit' to exit the client
- Server keeps running for new connections

### Example Session

```
Client Terminal:
Connected to the server
Enter message (or 'quit' to exit): Hello
Received: Echo: Hello
Enter message (or 'quit' to exit): WebSockets are cool!
Received: Echo: WebSockets are cool!
Enter message (or 'quit' to exit): quit

Server Terminal:
Server started on ws://localhost:8765
Client connected
Received message: Hello
Received message: WebSockets are cool!
```

### Key Concepts I Learned

1. **Asynchronous Programming**

   - `async def` creates async functions
   - `await` pauses execution until operation completes
   - `asyncio.run()` runs the async main function

2. **WebSocket Lifecycle**

   ```
   Client connects → Server accepts
   Client sends message → Server receives
   Server sends response → Client receives
   Client disconnects → Server continues running
   ```

3. **Message Loop Pattern**

   - Server uses `async for message in websocket` to continuously listen
   - Client uses `while True` with input() for interactive messaging

4. **Connection Management**

   - `async with` ensures proper connection cleanup
   - Server handles disconnections automatically (loop ends)
   - Multiple clients can connect to the same server

5. **Core WebSocket Methods**
   - `websockets.serve()` - Start a server
   - `websockets.connect()` - Connect to a server
   - `websocket.send()` - Send a message
   - `websocket.recv()` - Receive a message

### Common Issues & Solutions

**Issue**: "Connection refused" error

- **Solution**: Make sure the server is running before starting the client

**Issue**: Client exits immediately

- **Solution**: Add a loop or await to keep the connection open

**Issue**: Server exits after client disconnects

- **Solution**: Use `await asyncio.Future()` to keep server running

**Issue**: Messages not being received

- **Solution**: Make sure you're using `await` with send() and recv()

### What's Next?

Now that I understand the basics, I can build:

- Multi-client chat room (broadcast to all clients)
- Add usernames and timestamps
- Store message history
- Add different message types (JSON)
- Build a web-based client with JavaScript

### Skills Gained ✅

- ✅ WebSocket connection establishment
- ✅ Async programming with asyncio
- ✅ Bidirectional message passing
- ✅ Message loop implementation
- ✅ Clean disconnect handling
- ✅ Interactive CLI client
