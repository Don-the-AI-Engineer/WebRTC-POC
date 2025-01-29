import asyncio
import websockets

clients = {}  # Dictionary to store connected clients

async def handler(websocket):  # Ensure handler accepts two arguments
    try:
        client_type = await websocket.recv()  # Expect "A" or "B" as identifier
        clients[client_type] = websocket
        print(f"Client {client_type} connected")

        async for message in websocket:
            print(f"Received from {client_type}: {message}")
            if client_type == "A" and "B" in clients:
                await clients["B"].send(message)  # Forward command to B
    except websockets.ConnectionClosed:
        print(f"Client {client_type} disconnected")
    finally:
        if client_type in clients:
            del clients[client_type]

async def main():
    server = await websockets.serve(handler, "localhost", 8765)  # Await WebSocket server
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()  # Keeps the server running

# Ensure compatibility with asyncio
if __name__ == "__main__":
    asyncio.run(main())
