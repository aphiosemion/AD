#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int source) {
    cap.open(source, cv::CAP_V4L2);

    if (cap.isOpened()) {
        cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
        
        cap.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'));
    }
}

bool CameraProvider::getFrame(cv::Mat& frame) {
    if (!cap.isOpened()) {
        return false;
    }

    cap >> frame;
    
    return !frame.empty();
}
