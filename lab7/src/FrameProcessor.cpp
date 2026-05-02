#include "FrameProcessor.hpp"

void FrameProcessor::process(cv::Mat& frame, ProcessingMode mode, int brightness) {
    frame.convertTo(frame, -1, 1, brightness - 50);

    switch (mode) {
        case ProcessingMode::INVERSION:
            cv::bitwise_not(frame, frame);
            break;

        case ProcessingMode::CANNY: {
            cv::Mat gray;
            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
            cv::Canny(gray, gray, 100, 200);
            cv::cvtColor(gray, frame, cv::COLOR_GRAY2BGR);
            break;
        }

        case ProcessingMode::SEPIA: {
            cv::Mat kernel = (cv::Mat_<float>(3, 3) << 
                0.272, 0.534, 0.131,
                0.349, 0.686, 0.168,
                0.393, 0.769, 0.189);
            cv::transform(frame, frame, kernel);
            break;
        }

        case ProcessingMode::PIXELATE: {
            int width = frame.cols;
            int height = frame.rows;
            int pixelSize = 20;
            cv::Mat temp;
            cv::resize(frame, temp, cv::Size(width/pixelSize, height/pixelSize), 0, 0, cv::INTER_LINEAR);
            cv::resize(temp, frame, cv::Size(width, height), 0, 0, cv::INTER_NEAREST);
            break;
        }

        case ProcessingMode::POSTERIZE: {
            int div = 64;
            frame = (frame / div) * div + div / 2;
            break;
        }

        default: break;
    }

    std::string modeText = "Mode: " + std::to_string(static_cast<int>(mode));
    cv::putText(frame, modeText, cv::Point(20, 40), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 255, 0), 2);
}
