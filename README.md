# UMBC-ChatLink (Option 1)

## What this is
A simple 1-to-1 TCP chat app using Python sockets. The server accepts one client connection. Both sides can send/receive console messages until the quit command is used.

## Requirements covered
- Port passed via command line and validated (1025–65535)
- Server sends a welcome message after accepting the client
- Two-way messaging (client ↔ server)
- Clean exit using a quit command + safe handling for disconnects
- Optional bonus: server-side chat logging with timestamps (server_chatlog.txt)

## How to run

Terminal 1 (server):
```bash
python3 server.py 5001
