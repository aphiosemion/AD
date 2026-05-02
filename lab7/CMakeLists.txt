cmake_minimum_required(VERSION 3.10)
project(lab_7)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

find_package(Threads REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS} include)

add_executable(lab_7 
    src/main.cpp 
    src/CameraProvider.cpp 
    src/FrameProcessor.cpp 
    src/KeyProcessor.cpp 
    src/Display.cpp
    src/FaceDetector.cpp
)

target_link_libraries(lab_7 ${OpenCV_LIBS} Threads::Threads)
