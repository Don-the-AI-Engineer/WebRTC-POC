import asyncio
import json
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstWebRTC', '1.0')
from gi.repository import Gst, GstWebRTC, GLib
import websockets

Gst.init(None)

WS_URI = "ws://localhost:8765"
PEER_ID = "receiver"

pipeline_description = (
    f"webrtcbin name=webrtcbin ! "
    f"rtpvp8depay ! vp8dec ! videoconvert ! autovideosink"
)

pipeline = Gst.parse_launch(pipeline_description)

webrtcbin = pipeline.get_by_name("webrtcbin")

async def websocket_client():
    async with websockets.connect(WS_URI) as websocket:
        await websocket.send(PEER_ID)
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "offer":
                offer = GstWebRTC.WebRTCSessionDescription.new(
                    GstWebRTC.WebRTCSDPType.OFFER, data["sdp"]
                )
                promise = Gst.Promise.new()
                webrtcbin.emit("set-remote-description", offer, promise)
                promise.interrupt()

                promise = Gst.Promise.new_with_change_func(on_answer_created, None)
                webrtcbin.emit("create-answer", None, promise)
            elif data["type"] == "ice":
                webrtcbin.emit("add-ice-candidate", data["mlineindex"], data["candidate"])

def on_ice_candidate(webrtcbin, mlineindex, candidate):
    asyncio.run_coroutine_threadsafe(
        send_ice_candidate(mlineindex, candidate),
        loop
    )

async def send_ice_candidate(mlineindex, candidate):
    async with websockets.connect(WS_URI) as websocket:
        await websocket.send(json.dumps({
            "type": "ice",
            "mlineindex": mlineindex,
            "candidate": candidate
        }))

def on_answer_created(webrtcbin, promise, user_data):
    promise.wait()
    reply = promise.get_reply()
    answer = reply.get_value("answer")
    print("Answer created:", answer.sdp)

    promise = Gst.Promise.new()
    webrtcbin.emit("set-local-description", answer, promise)
    promise.interrupt()

    asyncio.run_coroutine_threadsafe(
        send_answer_to_sender(answer.sdp),
        loop
    )

async def send_answer_to_sender(answer_sdp):
    async with websockets.connect(WS_URI) as websocket:
        await websocket.send(json.dumps({
            "type": "answer",
            "sdp": answer_sdp
        }))

webrtcbin.connect("on-ice-candidate", on_ice_candidate)

pipeline.set_state(Gst.State.PLAYING)

loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_client())

main_loop = GLib.MainLoop()
try:
    print("WebRTC receiver started... Press Ctrl+C to stop.")
    main_loop.run()
except KeyboardInterrupt:
    print("Stopping WebRTC receiver...")

pipeline.set_state(Gst.State.NULL)