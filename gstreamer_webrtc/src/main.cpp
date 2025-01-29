#include <iostream>
#include "gstreamer_pipeline.h"
#include "webrtc_handler.h"
#include "stream_controls.h"

int main() {
    // Initialize GStreamer pipeline
    create_pipeline();
    start_pipeline();

    // Initialize WebRTC connection
    initialize_webrtc();

    // Main loop for user input
    std::string command;
    while (true) {
        std::cout << "Enter command (mute/unmute/pause/resume/exit): ";
        std::cin >> command;

        if (command == "mute") {
            mute_audio();
        } else if (command == "unmute") {
            unmute_audio();
        } else if (command == "pause") {
            pause_video();
        } else if (command == "resume") {
            resume_video();
        } else if (command == "exit") {
            break;
        } else {
            std::cout << "Invalid command!" << std::endl;
        }
    }

    // Cleanup
    stop_pipeline();
    cleanup_webrtc();

    return 0;
}