import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Define the pipeline
pipeline_description = (
    f"udpsrc port=5001 ! "
    f"application/x-rtp,media=video,encoding-name=H264,payload=96 ! "
    f"rtph264depay ! avdec_h264 ! "
    f"videoconvert ! autovideosink"
)

# Create the pipeline
pipeline = Gst.parse_launch(pipeline_description)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Create a main loop to keep the script running
main_loop = GLib.MainLoop()
try:
    print("Receiving and playing video... Press Ctrl+C to stop.")
    main_loop.run()
except KeyboardInterrupt:
    print("Stopping playback...")

# Clean up
pipeline.set_state(Gst.State.NULL)