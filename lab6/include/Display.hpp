#ifndef DISPLAY_HPP
#define DISPLAY_HPP

#include <opencv2/opencv.hpp>
#include <string>

class Display {
public:
    Display(std::string name);
    void show(cv::Mat& frame);
private:
    std::string windowName;
};

#endif
