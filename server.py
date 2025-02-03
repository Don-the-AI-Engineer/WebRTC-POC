import asyncio
import websockets

peers = {}

async def handler(websocket, path):
    peer_id = await websocket.recv()
    peers[peer_id] = websocket
    print(f"Peer {peer_id} connected.")

    try:
        async for message in websocket:
            for pid, ws in peers.items():
                if pid != peer_id:
                    await ws.send(message)
    finally:
        del peers[peer_id]
        print(f"Peer {peer_id} disconnected.")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Signaling server running on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())