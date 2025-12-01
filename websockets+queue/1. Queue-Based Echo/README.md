# Queue-Based WebSocket Server (Asyncio)

This project implements a **queue-based WebSocket server** using Python’s `asyncio` and `websockets` library.
It demonstrates a **producer–consumer architecture**, proper **decoupling**, **backpressure**, and **clean task cancellation** — patterns used in real-world async systems.

---

## 🚀 Overview

Instead of processing WebSocket messages directly inside the receive loop, this server:

- **Receives messages quickly**
- **Buffers them in an asyncio queue**
- **Processes and sends responses in a separate task**
- **Handles slow clients safely**
- **Shuts down cleanly when clients disconnect**

This avoids common async pitfalls like blocking receives, memory bloat, and zombie tasks.

---

## 🧠 Architecture

```
Client
  │
  ▼
WebSocket recv
  │
  ▼
Producer Task ──────► asyncio.Queue ──────► Consumer Task
 (receive)                                   (send)
   fast                                     can be slow
```

### Key Concepts

- **Producer–Consumer pattern**
- **Decoupling** network IO from processing
- **Backpressure** via bounded queues
- **Coordinated cancellation** on disconnect
- **Per-connection isolation**

---

## ✅ Features

- One queue per client connection
- Bounded queue to prevent unbounded memory usage
- Separate async tasks for receiving and sending
- Proper `queue.task_done()` usage
- Clean task cancellation on client disconnect
- Graceful shutdown with no leaked tasks

---

## 📦 Requirements

- Python 3.9+
- `websockets` library

Install dependencies:

```bash
pip install websockets
```

---

## ▶️ Running the Server

```bash
python server.py
```

Server starts on:

```
ws://localhost:8765
```

---

## 🧪 Example Client

A simple interactive client is included:

```python
import asyncio
import websockets

async def echo():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server")

        while True:
            message = input("Enter message (or 'quit' to exit): ")

            if message.lower() == "quit":
                break

            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(echo())
```

Run it in another terminal:

```bash
python client.py
```

---

## 🔐 Clean Shutdown Behavior

When the client disconnects:

1. `recv()` or `send()` fails
2. One task exits
3. The handler cancels the sibling task
4. Both tasks terminate cleanly
5. Queue and connection are released

This prevents:

- Zombie async tasks
- Hanging handlers
- Memory leaks

---

## 🎯 Why This Design Matters

This pattern is foundational for building:

- Chat servers
- Multiplayer game servers
- Real-time dashboards
- Job queues
- Streaming pipelines
- AI inference servers

It scales far better than naïve “recv → process → send” loops.

---

## 🛠 Possible Extensions

- Multiple consumer workers per queue
- Broadcast / fan-out messaging
- Room-based queues
- Rate limiting per client
- Structured message formats (JSON)
- Graceful server-wide shutdown

---

## ✅ Learning Outcome

This project focuses on **understanding async systems**, not just making code work:

- Why queues exist
- Where backpressure belongs
- Who owns task lifetimes
- How async cancellation actually works

---

## 🧑‍💻 Author

Built as a learning project to deeply understand **asyncio**, **WebSockets**, and **real-world concurrency patterns**.
