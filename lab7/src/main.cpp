#include <iostream>
#include <vector>
#include <string>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

int main() {
    CameraProvider camera(0);
    FrameProcessor processor;
    KeyProcessor keys;
    Display display("OpenCV Lab 7: AI & Multithreading");

    FaceDetector faceDet("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");

    int brightness = 50;
    cv::createTrackbar("Brightness", "OpenCV Lab 7: AI & Multithreading", &brightness, 100);
    
    bool showFaces = false;
    cv::Mat frame;
    
    double t = 0;
    double fps = 0;

    std::cout << "Програма запущена. Керування:" << std::endl;
    std::cout << "0-5: Зміна фільтрів" << std::endl;
    std::cout << "F: Увімкнути/Вимкнути детекцію облич (AI)" << std::endl;
    std::cout << "ESC: Вихід" << std::endl;

    while (true) {
        double t_start = (double)cv::getTickCount();

        if (!camera.getFrame(frame)) {
            std::cerr << "Помилка: не вдалося отримати кадр!" << std::endl;
            break;
        }

        if (showFaces) {
            faceDet.updateFrame(frame);
            
            std::vector<cv::Rect> faces = faceDet.getFaces();
            
            for (const auto& rect : faces) {
                cv::rectangle(frame, rect, cv::Scalar(0, 255, 0), 2);
                cv::putText(frame, "FACE (SSD)", cv::Point(rect.x, rect.y - 10),
                            cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
            }
        }

        processor.process(frame, keys.getCurrentMode(), brightness);

        std::string status = "Mode: " + std::to_string(static_cast<int>(keys.getCurrentMode())) + 
                             " | AI: " + (showFaces ? "ON" : "OFF") + 
                             " | FPS: " + std::to_string((int)fps);
        cv::putText(frame, status, cv::Point(10, frame.rows - 20), 
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 255, 255), 2);

        display.show(frame);

        int key = cv::waitKey(1);
        if (key == 27) break;
        
        if (key == 'f' || key == 'F' || key == 'а' || key == 'А') {
            showFaces = !showFaces;
            std::cout << "AI Detection: " << (showFaces ? "ENABLED" : "DISABLED") << std::endl;
        }
        
        keys.processKey(key);

        t = ((double)cv::getTickCount() - t_start) / cv::getTickFrequency();
        fps = 1.0 / t;
    }

    return 0;
}
