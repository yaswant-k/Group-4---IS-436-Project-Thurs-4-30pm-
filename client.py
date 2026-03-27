# client.py
# UMBC-ChatLink — connect to server, two-way console chat

import socket
import sys
import threading
from datetime import datetime

APP_TITLE = "UMBC-ChatLink"
QUIT_CMD = "/quit"


def ts_short() -> str:
    return datetime.now().strftime("%H:%M:%S")


def parse_port(argv) -> int:
    if len(argv) != 2:
        print("Usage: python3 client.py <port>")
        sys.exit(1)

    raw = argv[1]
    try:
        port = int(raw)
    except ValueError:
        print(f"Error: port must be an integer (got '{raw}').")
        sys.exit(1)

    if port < 1025 or port > 65535:
        print("Error: port must be between 1025 and 65535.")
        sys.exit(1)

    return port


def server_listener(sock: socket.socket, state: dict) -> None:
    # Receives messages from the server until quit or disconnect.
    while not state["stop"]:
        try:
            data = sock.recv(4096)
        except OSError:
            state["stop"] = True
            break

        if not data:
            print("\n[Server disconnected]")
            state["stop"] = True
            break

        msg = data.decode("utf-8", errors="replace").strip()

        if msg.lower() == QUIT_CMD.lower():
            print("\n[Server ended chat]")
            state["stop"] = True
            break

        print(f"\n{ts_short()} | Server: {msg}")


def main() -> None:
    port = parse_port(sys.argv)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    state = {"stop": False}

    try:
        sock.connect(("127.0.0.1", port))

        try:
            welcome = sock.recv(4096).decode("utf-8", errors="replace").strip()
            if welcome:
                print(welcome)
        except OSError:
            pass

        print(f"{APP_TITLE} client ready. Type {QUIT_CMD} to exit.\n")

        listener_thread = threading.Thread(
            target=server_listener, args=(sock, state), daemon=True
        )
        listener_thread.start()

        while not state["stop"]:
            try:
                out = input("Client> ").strip()
            except (EOFError, KeyboardInterrupt):
                out = QUIT_CMD

            if out.lower() == QUIT_CMD.lower():
                try:
                    sock.sendall((QUIT_CMD + "\n").encode("utf-8"))
                except OSError:
                    pass
                state["stop"] = True
                break

            try:
                sock.sendall((out + "\n").encode("utf-8"))
            except OSError:
                print("[Send failed: server not available]")
                state["stop"] = True
                break

    except ConnectionRefusedError:
        print("Connection refused. Start server.py first, then run client.py.")
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print("[Client closed cleanly]")


if __name__ == "__main__":
    main()

# Version updated
