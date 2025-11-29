Step 1: What problem are we solving?

In WebSockets:

Each client connection gets its own handler function

Handlers do not automatically know about each other

But for a game/chat/room, multiple handlers must act on shared state

So we need a way for:

Two independent WebSocket connections to agree they belong to the same game.

Step 2: The identifier (the “game id”)

When Player 1 starts a game:

The server creates a game object

Assigns it a unique identifier (string / UUID / short code)

Sends that identifier back to Player 1

Example:

Game ID: "A9F3Q"

Player 1 then:

Gives this ID to Player 2 (copy, invite link, etc.)

Step 3: Player 2 uses the identifier to find the same game

When Player 2 connects:

They send the identifier

The server looks it up

If it exists → join the game

If not → reject

This is how two handlers reach the same shared object.

Module level dict:
Think of module-level dict as shared memory

Imagine your server like a building:

Each WebSocket connection = one room

The module-level dict = the notice board in the lobby

Everyone can:

read it

write to it

look things up from it
A module-level dict is data created once when the server starts, shared by all connections, and used to let independent handlers see the same state.

Step 4: Why a module-level dict?

“A module-level dict enables lookups by identifier”

This line is extremely important.

What it means

A module-level dict:

Lives once per server process

Is shared across all WebSocket handlers

Persists between incoming connections

Example:

games = {}

This is not per-client.
This is global server memory.

Step 5: What goes inside the dict?

Each entry represents one game:

games = {
"A9F3Q": game_object
}

The game_object contains:

Game state (board, score, turn, etc.)

Connected WebSockets

Methods to broadcast events

Step 7: How this plays out in the WebSocket handler
Player 1
game_id = create_game()
game = games[game_id]
game.players.add(ws)
send(game_id)

Player 2
game = games.get(game_id)
game.players.add(ws)

✅ Both handlers now touch the same object

That’s the key.

Core mental model (memorize this)
connection handler = wire + events
game/session object = truth + state
dictionary = meeting point

connected is a set of WebSocket connections that belong to ONE game

Right now, it contains:

only the creator’s WebSocket

Later, when another player joins:

their WebSocket is added to this same set

Why do we need JOIN at all?

Because each WebSocket connection runs in isolation.

Without JOIN:

Player 1 creates a game

Player 2 connects

Player 2 has no way to find Player 1’s game

With JOIN:

Player 1 says “here’s the join key”

Player 2 sends that key to the server

Server does:

game, connected = JOIN[join_key]

✅ Both handlers touch the same game and same connection set
