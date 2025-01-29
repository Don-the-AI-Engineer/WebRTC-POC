from aiohttp import web
import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def offer(sid, data):
    print(f"Offer received from {sid}")
    await sio.emit('answer', data, room=sid)

@sio.event
async def ice_candidate(sid, data):
    print(f"ICE candidate received from {sid}")
    await sio.emit('ice_candidate', data, room=sid)

if __name__ == '__main__':
    web.run_app(app, port=8080)