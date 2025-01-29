#include <gst/gst.h>
#include <iostream>
#include "stream_controls.h"

extern GstElement *pipeline;

void mute_audio() {
    GstElement *audio_sink = gst_bin_get_by_name(GST_BIN(pipeline), "audio_sink");
    if (audio_sink) {
        g_object_set(audio_sink, "mute", TRUE, NULL);
        std::cout << "Audio muted" << std::endl;
    } else {
        std::cerr << "Failed to find audio sink" << std::endl;
    }
}

void unmute_audio() {
    GstElement *audio_sink = gst_bin_get_by_name(GST_BIN(pipeline), "audio_sink");
    if (audio_sink) {
        g_object_set(audio_sink, "mute", FALSE, NULL);
        std::cout << "Audio unmuted" << std::endl;
    } else {
        std::cerr << "Failed to find audio sink" << std::endl;
    }
}

void pause_video() {
    gst_element_set_state(pipeline, GST_STATE_PAUSED);
    std::cout << "Video paused" << std::endl;
}

void resume_video() {
    gst_element_set_state(pipeline, GST_STATE_PLAYING);
    std::cout << "Video resumed" << std::endl;
}