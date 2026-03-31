@echo off
REM Compile the NASM code
nasm -f win64 -o conversions.obj conversions.asm

REM Create DLL
gcc -shared -o conversions.dll conversions.obj

REM Clean up object file
del conversions.obj

echo Build complete! Run the Python application with: python base_converter.py 