Here’s the same content rewritten as a **clean, structured README** with proper headings, spacing, and a clear mental model. You can drop this directly into a `README.md`.

---

# Multiplayer WebSockets: Shared Game State Explained

This document explains **why and how multiple WebSocket connections share the same game**, using a Connect-4–style example.

---

## Step 1: What problem are we solving?

In a WebSocket server:

- Each client connection runs in its **own handler**
- Handlers **do not automatically know about each other**
- But multiplayer games, chats, or rooms require **shared state**

### The core problem

> How do two **independent WebSocket connections** agree that they belong to the **same game**?

---

## Step 2: The identifier (“Game ID” / Join Key)

When **Player 1** starts a game:

1. The server creates a new game object
2. The server assigns it a **unique identifier**

   - short code
   - UUID
   - random token

3. The server sends that identifier back to Player 1

### Example

```
Game ID: A9F3Q
```

Player 1 then shares this identifier with Player 2:

- copy/paste
- invite link
- `?join=A9F3Q` in the URL

---

## Step 3: Player 2 uses the identifier to find the same game

When **Player 2** connects:

1. They send the identifier to the server
2. The server looks it up
3. If it exists → Player 2 joins the game
4. If it doesn’t → the server rejects the request

This is how **two separate handlers reach the same object in memory**.

---

## Step 4: The module-level dictionary (shared server memory)

### What is it?

A **module-level dictionary** is data that:

- Is created **once** when the server starts
- Is shared by **all WebSocket connections**
- Persists across incoming connections

Example:

```python
games = {}
```

This is **not per client**.
This is **global server memory**.

---

### Intuition (important)

Imagine the server as a building:

- Each WebSocket connection = **one room**
- The module-level dict = **a notice board in the lobby**

Everyone can:

- read it
- write to it
- look things up from it

That notice board is how isolated rooms coordinate.

---

## Step 5: Why do we need a module-level dict?

> **“A module-level dict enables lookups by identifier.”**

This is the key sentence.

Because:

- Handlers start independently
- They need a central place to say
  “Does a game with ID `A9F3Q` exist?”

Without a shared lookup:

- Every handler lives in isolation
- Multiplayer is impossible

---

## Step 6: What goes inside the dictionary?

Each entry represents **one game**:

```python
games = {
    "A9F3Q": game_object
}
```

Each `game_object` contains:

- Game state (board, turn, score, etc.)
- A set of connected WebSocket clients
- Logic to broadcast events to those clients

---

## Step 7: How this works inside the WebSocket handler

### Player 1 (creates a game)

```python
game_id = create_game()
game = games[game_id]
game.players.add(ws)
send(game_id)   # send join key to Player 1
```

### Player 2 (joins a game)

```python
game = games.get(game_id)
game.players.add(ws)
```

✅ Both handlers now interact with the **same game object**

That’s the entire trick.

---

## Core mental model (memorize this)

```
WebSocket handler  = wire + events
Game/session object = truth + state
Dictionary          = meeting point
```

---

## What is `connected` / `players`?

`connected` (usually a set) contains **only the WebSocket connections that belong to ONE game**.

Initially:

- It contains only the creator’s WebSocket

When another player joins:

- Their WebSocket is added to the _same set_

Now the server can:

- broadcast moves
- broadcast wins
- broadcast errors

to everyone in that game.

---

## Why do we need JOIN at all?

Because **each WebSocket connection runs in isolation**.

Without JOIN:

- Player 1 creates a game
- Player 2 connects
- Player 2 has no way to find Player 1’s game

With JOIN:

1. Player 1: “Here’s the join key”
2. Player 2 sends that key to the server
3. Server does:

```python
game, connected = JOIN[join_key]
```

✅ Both handlers now touch:

- the same game
- the same connection set

That is **multiplayer**.

---

## Final takeaway

> Multiplayer WebSocket systems work by routing independent connections to shared objects using identifiers and a module-level dictionary.

If you understand this, you understand:

- multiplayer games
- chat rooms
- collaborative editors
- interview platforms
- real-time dashboards

You’ve crossed an important architectural milestone.
