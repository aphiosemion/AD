cmake_minimum_required(VERSION 3.10)
project(lab_6)

set(CMAKE_CXX_STANDARD 17)

# Пошук OpenCV
find_package(OpenCV REQUIRED)

# Вказуємо шлях до заголовочних файлів
include_directories(${OpenCV_INCLUDE_DIRS} include)

# Збираємо всі файли з папки src
file(GLOB SOURCES "src/*.cpp")

add_executable(lab_6 ${SOURCES})

target_link_libraries(lab_6 ${OpenCV_LIBS})
