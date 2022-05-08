# Drafts on server

# Check server socket is accepting connections:
import socket
import time

s = socket.create_server(("", 8080))

for _ in range(3):
    try:
        if s.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN):
            break
    except (OSError,):  # maybe others like AttributeError if s has to be initiated somewhere
        continue
else:
    raise RuntimeError(f"Failed to start server {s}")
