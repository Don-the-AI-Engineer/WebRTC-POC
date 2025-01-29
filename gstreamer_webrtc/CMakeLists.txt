cmake_minimum_required(VERSION 3.14)
project(GStreamerWebRTC)

set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GSTREAMER REQUIRED gstreamer-1.0)
pkg_check_modules(LIBDATACHANNEL REQUIRED libdatachannel)

include_directories(${GSTREAMER_INCLUDE_DIRS} ${LIBDATACHANNEL_INCLUDE_DIRS})
link_directories(${GSTREAMER_LIBRARY_DIRS} ${LIBDATACHANNEL_LIBRARY_DIRS})

add_executable(gstreamer_webrtc src/main.cpp src/webrtc_handler.cpp src/gstreamer_pipeline.cpp src/stream_controls.cpp)
target_link_libraries(gstreamer_webrtc ${GSTREAMER_LIBRARIES} ${LIBDATACHANNEL_LIBRARIES})