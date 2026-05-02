#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    void process(cv::Mat& frame, ProcessingMode mode, int brightness);
private:
    void applyGlitch(cv::Mat& frame);
};

#endif
