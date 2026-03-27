# server.py
# UMBC-ChatLink — 1 server, 1 client, two-way console chat

import socket
import sys
import threading
from datetime import datetime

APP_TITLE = "UMBC-ChatLink"
QUIT_CMD = "/quit"
LOG_ENABLED = True
LOG_PATH = "server_chatlog.txt"


def ts_full() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(line: str) -> None:
    if not LOG_ENABLED:
        return
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        # Logging should never break the chat
        pass


def parse_port(argv) -> int:
    if len(argv) != 2:
        print("Usage: python3 server.py <port>")
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


def client_listener(conn: socket.socket, state: dict) -> None:
    # Receives messages from the client until quit or disconnect.
    while not state["stop"]:
        try:
            data = conn.recv(4096)
        except OSError:
            state["stop"] = True
            break

        if not data:
            print("\n[Client disconnected]")
            write_log(f"{ts_full()} | CLIENT_DISCONNECTED")
            state["stop"] = True
            break

        msg = data.decode("utf-8", errors="replace").strip()

        if msg.lower() == QUIT_CMD.lower():
            print("\n[Client ended chat]")
            write_log(f"{ts_full()} | CLIENT_QUIT")
            state["stop"] = True
            break

        line = f"{ts_full()} | Client: {msg}"
        print("\n" + line)
        write_log(line)


def main() -> None:
    port = parse_port(sys.argv)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    conn = None
    addr = None

    try:
        server_sock.bind(("0.0.0.0", port))
        server_sock.listen(1)
        print(f"{APP_TITLE} server is running on port {port} and waiting for 1 client...")

        conn, addr = server_sock.accept()
        print(f"Connected -> {addr[0]}:{addr[1]}")
        write_log(f"{ts_full()} | CONNECT {addr[0]}:{addr[1]}")

        welcome = (
            f"Welcome to {APP_TITLE}.\n"
            f"You can use standard UTF-8 text, including accents, symbols, and many emojis.\n"
            f"Type {QUIT_CMD} to exit.\n"
        )
        conn.sendall(welcome.encode("utf-8"))

        state = {"stop": False}
        listener_thread = threading.Thread(
            target=client_listener, args=(conn, state), daemon=True
        )
        listener_thread.start()

        while not state["stop"]:
            try:
                out = input("Server> ").strip()
            except (EOFError, KeyboardInterrupt):
                out = QUIT_CMD

            if out.lower() == QUIT_CMD.lower():
                try:
                    conn.sendall((QUIT_CMD + "\n").encode("utf-8"))
                except OSError:
                    pass
                write_log(f"{ts_full()} | SERVER_QUIT")
                state["stop"] = True
                break

            send_line = f"{ts_full()} | Server: {out}"
            write_log(send_line)

            try:
                conn.sendall((out + "\n").encode("utf-8"))
            except OSError:
                print("[Send failed: client not available]")
                state["stop"] = True
                break

    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass

        try:
            server_sock.close()
        except Exception:
            pass

        print("[Server closed cleanly]")


if __name__ == "__main__":
    main()

# Version updated
