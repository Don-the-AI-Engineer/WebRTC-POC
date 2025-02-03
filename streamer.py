import asyncio
import json
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstWebRTC', '1.0')
from gi.repository import Gst, GstWebRTC, GLib
import websockets

Gst.init(None)

WS_URI = "ws://localhost:8765"
PEER_ID = "sender"

pipeline_description = (
    f"filesrc location=test_video/friends.mp4 ! "
    f"qtdemux ! h264parse ! avdec_h264 ! "
    f"videoconvert ! vp8enc ! rtpvp8pay ! "
    f"webrtcbin name=webrtcbin"
)

pipeline = Gst.parse_launch(pipeline_description)

webrtcbin = pipeline.get_by_name("webrtcbin")

async def websocket_client():
    async with websockets.connect(WS_URI) as websocket:
        await websocket.send(PEER_ID)
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "answer":
                answer = GstWebRTC.WebRTCSessionDescription.new(
                    GstWebRTC.WebRTCSDPType.ANSWER, data["sdp"]
                )
                promise = Gst.Promise.new()
                webrtcbin.emit("set-remote-description", answer, promise)
                promise.interrupt()

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

webrtcbin.connect("on-ice-candidate", on_ice_candidate)

pipeline.set_state(Gst.State.PLAYING)

loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_client())

main_loop = GLib.MainLoop()
try:
    print("WebRTC streaming started... Press Ctrl+C to stop.")
    main_loop.run()
except KeyboardInterrupt:
    print("Stopping WebRTC stream...")

pipeline.set_state(Gst.State.NULL)