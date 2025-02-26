import os
import time
import asyncio
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from websockets.server import serve

# Global variables
active_connections = set()
start_time = time.time()

# WebSocket handler
async def handle_client(websocket, path):
    global active_connections
    active_connections.add(websocket)
    print(f"New connection. Active connections: {len(active_connections)}")

    try:
        while True:
            message = await websocket.recv()
            if message == "status":
                uptime = time.time() - start_time
                status = f"Active Connections: {len(active_connections)}, Uptime: {int(uptime)}s"
                await websocket.send(status)
            elif message == "stop":
                await websocket.send("Server shutting down...")
                os._exit(0)
    except:
        pass
    finally:
        active_connections.remove(websocket)

# Start WebSocket server
async def start_websocket_server():
    async with serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Run forever

# Start HTTP server
def start_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("HTTP server running on port 8000...")
    httpd.serve_forever()

# Main function
if __name__ == "__main__":
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    # Start WebSocket server
    asyncio.run(start_websocket_server())