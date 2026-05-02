#ifndef CAMERA_PROVIDER_HPP
#define CAMERA_PROVIDER_HPP

#include <opencv2/opencv.hpp>

class CameraProvider {
public:
    CameraProvider(int source = 0);
    bool getFrame(cv::Mat& frame);
private:
    cv::VideoCapture cap;
};

#endif
