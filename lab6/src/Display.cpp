#include "Display.hpp"

Display::Display(std::string name) : windowName(name) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
}

void Display::show(cv::Mat& frame) {
    cv::imshow(windowName, frame);
}
