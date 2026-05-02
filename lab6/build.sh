#!/bin/bash
echo "Starting build process..."
mkdir -p build
cd build
cmake ..
make
