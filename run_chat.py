# run_chat.py
# Cross-platform launcher for UMBC-ChatLink

import subprocess
import sys
import time

PORT = "5000"


def main() -> None:
    python_cmd = sys.executable

    print(f"Starting server on port {PORT}...")
    server_process = subprocess.Popen([python_cmd, "server.py", PORT])

    try:
        time.sleep(1)
        print(f"Starting client on port {PORT}...")
        subprocess.run([python_cmd, "client.py", PORT])
    finally:
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()


if __name__ == "__main__":
    main()

# Version updated
