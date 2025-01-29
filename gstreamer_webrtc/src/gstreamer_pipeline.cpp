#include <gst/gst.h>
#include <iostream>
#include "gstreamer_pipeline.h"

GstElement *pipeline;

void create_pipeline() {
    pipeline = gst_parse_launch(
        "filesrc location=friends.mp4 ! qtdemux name=demux "
        "demux.video_0 ! queue ! decodebin ! videoconvert ! x264enc ! rtph264pay ! queue ! appsink name=video_sink "
        "demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! opusenc ! rtpopuspay ! queue ! appsink name=audio_sink",
        NULL
    );

    if (!pipeline) {
        std::cerr << "Failed to create pipeline" << std::endl;
        exit(1);
    }
}

void start_pipeline() {
    gst_element_set_state(pipeline, GST_STATE_PLAYING);
}

void stop_pipeline() {
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(pipeline);
}