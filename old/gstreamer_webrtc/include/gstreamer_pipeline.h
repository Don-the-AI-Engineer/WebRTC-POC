#ifndef GSTREAMER_PIPELINE_H
#define GSTREAMER_PIPELINE_H

extern GstElement *pipeline;

void create_pipeline();
void start_pipeline();
void stop_pipeline();

#endif