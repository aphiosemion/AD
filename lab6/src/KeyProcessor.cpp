#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessingMode::NORMAL) {}

void KeyProcessor::processKey(int key) {
    if (key >= '0' && key <= '5') {
        currentMode = static_cast<ProcessingMode>(key - '0');
    }
}

ProcessingMode KeyProcessor::getCurrentMode() const {
    return currentMode;
}
