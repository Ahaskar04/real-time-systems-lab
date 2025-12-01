# WebSocket Broadcast Chat (Asyncio + Python)

This project is a **simple broadcast chat application** built using Python’s `asyncio` and the `websockets` library.

It demonstrates:

- handling multiple WebSocket clients concurrently
- assigning **stable per-client IDs**
- broadcasting messages to all connected clients
- graceful handling of client disconnects
- proper async send/receive separation on the client side

---

## Features

- ✅ Multiple clients can connect simultaneously
- ✅ Each client gets a unique user ID
- ✅ Messages are broadcast to all connected clients
- ✅ Join and disconnect events are broadcast
- ✅ Safe cleanup of disconnected clients
- ✅ Non-blocking async client (no ping timeout issues)

---

## Project Structure

```
.
├── server.py   # WebSocket broadcast server
├── client.py   # Async WebSocket client
└── README.md
```

---

## Requirements

- Python 3.9+
- `websockets` library

Install dependencies:

```bash
pip install websockets
```

---

## How the Server Works

- A **dictionary** tracks connected clients:

  ```python
  connected_clients = {
      websocket: user_id
  }
  ```

- Each new connection:

  - gets a unique user ID
  - is stored in the registry
  - triggers a broadcast message

- Messages from any client are broadcast to all clients
- Disconnected clients are detected and cleaned up safely

This avoids:

- duplicate clients
- broken sockets
- identity mix-ups

---

## How the Client Works

The client runs **two concurrent tasks**:

1. ✅ **Receiving messages** from the server
2. ✅ **Reading user input and sending messages**

To avoid blocking the event loop:

- `input()` runs in a background thread using `run_in_executor`
- receiving runs continuously in an async task

This design prevents:

- missed messages
- ping timeout errors
- frozen clients

---

## Running the Server

```bash
python server.py
```

You should see:

```
Server started on ws://localhost:8765
```

---

## Running the Client

Open **multiple terminals** and run:

```bash
python client.py
```

Example output:

```
Connecting to ws://localhost:8765...
Connected successfully!
Enter message (or 'quit' to exit):
```

Anything you type will be broadcast to all connected clients.

---

## Example Interaction

```
User 1 has connected.
User 2 has connected.

User 1: hello
User 2: hi there!

User 1 has disconnected.
```

---

## Key Concepts Demonstrated

- Async concurrency with `asyncio`
- WebSocket lifecycle management
- Dictionary-based client registries
- Graceful error handling
- Broadcast messaging
- Clean shutdowns

---

## Notes / Limitations

- No authentication (IDs are assigned sequentially)
- Messages are text-only
- No persistence (messages are not stored)
- Designed for learning / experimentation

---

## Possible Extensions

- Add usernames instead of numeric IDs
- Implement chat rooms or channels
- Persist message history
- Add authentication
- Use structured JSON messages

---

## Summary

This project is a **minimal but correctly structured** WebSocket broadcast system that follows real-world async patterns and avoids common pitfalls like blocking input and improper connection cleanup.

It’s an excellent foundation for:

- chat systems
- multiplayer games
- real-time dashboards
- collaborative tools
