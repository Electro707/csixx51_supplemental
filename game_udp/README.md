# Python Multiplayer Game Client Example
By Jamal Bouajjaj

This is an example code developed to demonstrate a game running under PyGame, with a server that handles all of the
player's positions.

The "game" itself are just dots (the players) moving in a window.

# Disclaimer
This is a game I made in a couple of hours, with little knowledge beforehand of UDP sockets and PyGame as a class
demonstration of how to make a basic networked game.
So take this game example as just that: **an example**.
The code or protocol implementation probably can be further optimized or be better designed.

# Protocol
The game multiplayer protocol is a server-client model. Thus, a server must be running before the clients are
able to be used.

The link protocol used is UDP.

There is NO ENCRYPTION occurring for this demo, thus opening it up to man-in-the-middle and spoofing attacks.

## Commands
The command will be escaped code, with `0xFF` as the escape sequence

The following commands are available for the client to send to the server:
- `0xFF | 0xA0`: A client requests to join the server
  - Responds from the server will be `0xFF | 0xA1 | (playerId, 2 bytes)`
  - or `0xFF | 0xA2` for a rejection code, i.e too many players
- `0xFF | 0x01 | (x pos, 2 bytes) | (y pos, 2 bytes)`: Update the player's position
- `0xFF | 0xF0`: End the session for that player
  - Server responds with `0xFF | 0xF1`


The following commands can get sent by the server to the client:
- `0xFF | 0x10 | pn | DATA*pn`: The information for all players, where
  - `pn` is the number of players
  - `DATA` is `(ID, 2 bytes), (x pos, 2 bytes), (y pos, 2 bytes)`. The amount of `DATA` depends on the player number
- `0xFF - 0xE0`: Server Shutdown, it is expected for the clients to close
- `0xFF - 0x20 - (ID, 2 bytes) - (color - 2 bytes)`: A new player joined, the following ID and color
- `0xFF - 0x21 - (ID, 2 bytes)`: A player un-joined
