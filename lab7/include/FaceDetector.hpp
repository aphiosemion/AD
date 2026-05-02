#ifndef FACE_DETECTOR_HPP
#define FACE_DETECTOR_HPP

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
public:
    FaceDetector(const std::string& proto, const std::string& model);
    ~FaceDetector();
    
    void updateFrame(const cv::Mat& frame);
    
    std::vector<cv::Rect> getFaces();

private:
    void worker();

    cv::dnn::Net net;
    std::thread workerThread;
    std::mutex mtx;
    std::atomic<bool> running{true};

    cv::Mat currentFrame;
    std::vector<cv::Rect> detectedFaces;
    bool frameReady = false;
};

#endif
