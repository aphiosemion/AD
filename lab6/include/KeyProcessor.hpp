#ifndef KEY_PROCESSOR_HPP
#define KEY_PROCESSOR_HPP

enum class ProcessingMode {
    NORMAL,      // 0
    INVERSION,   // 1
    CANNY,       // 2
    SEPIA,       // 3
    PIXELATE,    // 4
    POSTERIZE    // 5
};

class KeyProcessor {
public:
    KeyProcessor();
    void processKey(int key);
    ProcessingMode getCurrentMode() const;
private:
    ProcessingMode currentMode;
};

#endif
