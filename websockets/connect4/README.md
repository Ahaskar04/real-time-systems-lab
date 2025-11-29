# Connect 4 WebSocket Server – Architecture Notes

This project demonstrates a **server-authoritative Connect 4 game** implemented using **async WebSockets in Python**.
The focus is on understanding **handlers**, **async lifecycles**, and **proper server cleanup**.

---

## 1. What a `handler` Is

A **handler** is the logic the server runs while communicating with **one WebSocket client**.

### Key ideas

- `handler(websocket)` is an **async coroutine**
- It represents the **entire lifetime of a single client connection**
- You **never call `handler` yourself**
- The WebSocket server automatically starts a new handler **for every client that connects**

Conceptually:

```
Browser connects ──▶ server creates task ──▶ handler(websocket)
Browser disconnects ──▶ handler exits
```

---

### How handlers run concurrently

Inside `handler`, you typically see something like:

```python
async for message in websocket:
    ...
```

This loop:

- waits for incoming messages using `await`
- **pauses without blocking** the event loop
- allows other handlers (other clients) to run at the same time

Even though there’s a single event loop:

- each client gets its **own handler coroutine**
- each handler progresses independently
- concurrency is achieved via `await`, not threads

This is how one server can handle many clients simultaneously.

---

### What belongs in a handler

A handler should only:

- receive messages from the client
- forward input to core logic (game, engine, state)
- send events back to the client
- clean up when the client disconnects

A handler should **not**:

- contain game rules
- decide turns
- validate business logic
- own shared state

Think of it as a **communication pipe**, not the brain.

---

## 2. Server Startup and Cleanup

### Using `async with serve(...)` (recommended)

```python
async with serve(handler, "", 8001):
    await asyncio.Future()
```

When you use `async with serve(...)`, the WebSockets library automatically:

- closes the listening socket
- stops accepting new clients
- closes all active WebSocket connections
- cancels all running handler tasks
- releases the port cleanly
- ensures the event loop shuts down without pending tasks

This is the **safest and simplest** way to run a server.

---

## 3. Manual Cleanup Logic (What This Means in Practice)

If you **do not** use `async with serve(...)`, then **you are responsible for cleanup**.

Example:

```python
server = await serve(handler, "", 8001)
await server.serve_forever()
```

In this case, you must manually handle shutdown.

---

### What you must do manually

1. **Catch termination signals**

   - `KeyboardInterrupt` (Ctrl+C)
   - task cancellation
   - runtime exceptions

2. **Stop accepting new connections**

   ```python
   server.close()
   ```

3. **Wait for the server to shut down**

   ```python
   await server.wait_closed()
   ```

4. **Close existing client connections**

   - track active WebSockets
   - call `.close()` on each

5. **Cancel running handler tasks**

   - maintain a set of tasks
   - cancel them explicitly
   - `await` their cancellation

6. **Ensure no pending tasks remain**

   - otherwise you will see:

     ```
     Task was destroyed but it is pending!
     ```

7. **Handle partial shutdowns correctly**

   - e.g. stop new clients
   - allow current operations to finish cleanly

---

### What breaks if you skip manual cleanup

- Port remains occupied (`Address already in use`)
- Zombie WebSocket connections persist
- Event loop refuses to terminate
- Resource leaks and warnings
- Unpredictable shutdown behavior

---

## Summary

- **Handlers** are per-connection async coroutines
- Each client gets its own independent handler
- Async `await` enables concurrency without threads
- `async with serve(...)` handles cleanup safely
- Without it, **cleanup is your responsibility**

This repo is intentionally simple to make these concepts clear and observable.
