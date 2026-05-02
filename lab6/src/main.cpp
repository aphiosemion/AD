#include <iostream>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "Display.hpp"

int main() {
    CameraProvider camera(0);
    FrameProcessor processor;
    KeyProcessor keys;
    Display display("OpenCV Lab 6");

    int brightness = 50;
    cv::createTrackbar("Brightness", "OpenCV Lab 6", &brightness, 100);

    cv::Mat frame;
    while (true) {
        if (!camera.getFrame(frame)) break;

        processor.process(frame, keys.getCurrentMode(), brightness);
        display.show(frame);

        int key = cv::waitKey(30);
        if (key == 27) break;
        keys.processKey(key);
    }
    return 0;
}
