import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Define the pipeline
pipeline_description = (
    f"filesrc location=friends.mp4 ! "
    f"qtdemux ! h264parse ! avdec_h264 ! "
    f"videoconvert ! x264enc ! "
    f"rtph264pay ! udpsink host=127.0.0.1 port=5001"
)

# Create the pipeline
pipeline = Gst.parse_launch(pipeline_description)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Create a main loop to keep the script running
main_loop = GLib.MainLoop()
try:
    print("Streaming video... Press Ctrl+C to stop.")
    main_loop.run()
except KeyboardInterrupt:
    print("Stopping stream...")

# Clean up
pipeline.set_state(Gst.State.NULL)