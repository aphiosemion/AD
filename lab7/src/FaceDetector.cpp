#include "FaceDetector.hpp"

FaceDetector::FaceDetector(const std::string& proto, const std::string& model) {
    net = cv::dnn::readNetFromCaffe(proto, model);
    workerThread = std::thread(&FaceDetector::worker, this);
}

FaceDetector::~FaceDetector() {
    running = false;
    if (workerThread.joinable()) workerThread.join();
}

void FaceDetector::updateFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    frame.copyTo(currentFrame);
    frameReady = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return detectedFaces;
}

void FaceDetector::worker() {
    while (running) {
        cv::Mat frame;
        {
            std::lock_guard<std::mutex> lock(mtx);
            if (frameReady && !currentFrame.empty()) {
                currentFrame.copyTo(frame);
                frameReady = false;
            }
        }

        if (!frame.empty()) {
            cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300), 
                                                 cv::Scalar(104.0, 177.0, 123.0));
            net.setInput(blob);
            
            cv::Mat detections = net.forward();

            std::this_thread::sleep_for(std::chrono::milliseconds(500));

            std::vector<cv::Rect> faces;
            float* data = (float*)detections.data;
            for (int i = 0; i < detections.size[2]; i++) {
                float confidence = data[i * 7 + 2];
                if (confidence > 0.5) { 
                    int x1 = static_cast<int>(data[i * 7 + 3] * frame.cols);
                    int y1 = static_cast<int>(data[i * 7 + 4] * frame.rows);
                    int x2 = static_cast<int>(data[i * 7 + 5] * frame.cols);
                    int y2 = static_cast<int>(data[i * 7 + 6] * frame.rows);
                    faces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
                }
            }

            {
                std::lock_guard<std::mutex> lock(mtx);
                detectedFaces = faces;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}
