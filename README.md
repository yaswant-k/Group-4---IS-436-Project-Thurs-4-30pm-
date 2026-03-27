# UMBC-ChatLink

## Overview
UMBC-ChatLink is a simple 1-to-1 TCP chat application built with Python sockets using only built-in Python libraries. The project includes one server and one client. After the server starts and the client connects, both sides can send and receive text messages through the terminal.

The chat supports UTF-8 text, which means users can send standard typed Unicode characters such as accented letters, symbols, and many emojis. Actual appearance may vary slightly depending on the operating system, terminal, and installed fonts.

## Features
- Accepts a TCP port number through the command line
- Validates that the port is within the allowed range (`1025–65535`)
- Accepts one client connection
- Displays a welcome message after connection
- Supports two-way real-time messaging
- Supports graceful exit using `/quit`
- Creates a server-side log file with timestamps (`server_chatlog.txt`)
- Includes a launcher script (`run_chat.py`) to make startup easier
- Supports UTF-8 text input and transmission for accents, symbols, and many emojis

## Included Files
- `server.py` — starts the chat server
- `client.py` — starts the chat client
- `run_chat.py` — starts the server and client automatically
- `README.md` — project overview and instructions

## Quick Start
The easiest way to run the project is with the launcher script.

From the project folder, run:

```bash
python3 run_chat.py
