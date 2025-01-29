# WebRTC-POC with Stream Control


## Overview

This project demonstrates a WebRTC-based application that allows a broadcaster to stream audio/video (pre-recorded footage) to a viewer over a secure peer-to-peer (P2P) connection. The broadcaster has controls to mute/unmute audio and pause/resume video, with changes reflecting in real time for the viewer.

## Features

- Secure WebRTC-based P2P communication

- Stream audio/video from the broadcaster to the viewer

- Stream controls: mute/unmute audio and pause/resume video

- Real-time stream control updates for the viewer

- WebSocket-based signaling server for exchanging WebRTC offer/answer and ICE candidates

## Technologies Used

- WebRTC for P2P streaming

- GStreamer/NVIDIA DeepStream for video processing (GStreamer pipeline)

- WebSockets (Socket.IO) for signaling server

- C++ for WebRTC implementation

- Python (Aiohttp, Socket.IO) for the signaling server

## Setup and Installation

### Prerequisites

- Ensure you have the following installed:

- C++ Compiler (GCC/Clang/MSVC)

- GStreamer/NVIDIA DeepStream

- WebRTC development libraries

- Python 3.7+

- Required Python dependencies (aiohttp, python-socketio)

### Building and Running

1. Install Dependencies

```bash
    pip install -r requirements.txt
```

2. Run the Signaling Server

```bash
    python server.py
```

3. Compile and Run the WebRTC Client

```bash
g++ -o webrtc_app main.cpp gstreamer_pipeline.cpp webrtc_handler.cpp stream_controls.cpp -lwebrtc -lgstreamer-1.0
./webrtc_app
```

## Usage

1. Start the signaling server (server.py).

2. Run the WebRTC application (webrtc_app).

3. The broadcaster will start streaming video.

4. Use the provided controls to mute/unmute audio and pause/resume video.

5. The viewer will see changes in real time.

