import asyncio
import websockets

clients = {}

async def handler(websocket):
    try:
        client_type = await websocket.recv()
        clients[client_type] = websocket
        print(f"Client {client_type} connected")

        async for message in websocket:
            print(f"Received from {client_type}: {message}")
            if client_type == "A" and "B" in clients:
                await clients["B"].send(message)
    except websockets.ConnectionClosed:
        print(f"Client {client_type} disconnected")
    finally:
        if client_type in clients:
            del clients[client_type]

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
