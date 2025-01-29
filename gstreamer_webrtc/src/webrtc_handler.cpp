#include <rtc/rtc.hpp>
#include <iostream>
#include "webrtc_handler.h"

rtc::WebSocket ws("ws://localhost:8080");
rtc::PeerConnection pc;

void on_message(const std::string &message) {
    std::cout << "Message: " << message << std::endl;
}

void on_local_description(const rtc::Description &description) {
    ws.send(description);
}

void on_local_candidate(const rtc::Candidate &candidate) {
    ws.send(candidate);
}

void initialize_webrtc() {
    ws.onMessage(on_message);
    pc.onLocalDescription(on_local_description);
    pc.onLocalCandidate(on_local_candidate);
}

void cleanup_webrtc() {
    ws.close();
    pc.close();
}