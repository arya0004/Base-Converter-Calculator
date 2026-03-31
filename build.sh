#!/bin/bash

# Compile NASM code
echo "Compiling NASM code..."
nasm -f win64 -o conversions.obj conversions.asm
nasm -f win64 -o calculator.obj calculator.asm

# Create DLL
echo "Creating DLL..."
gcc -shared -o conversions.dll conversions.obj calculator.obj

# Clean up
echo "Cleaning up..."
rm conversions.obj calculator.obj

echo "Build complete! Run the Python application with: python base_converter.py" 