# Makefile for Base Converter Calculator

# Compiler and linker settings
ML = ml
ML_FLAGS = /c /coff
LINK = link
LINK_FLAGS = /subsystem:windows

# Output files
TARGET = base_converter.exe
OBJS = base_converter.obj conversions.obj calculator.obj

# Default target
all: $(TARGET)

# Main target
$(TARGET): $(OBJS)
    $(LINK) $(LINK_FLAGS) $(OBJS)

# Object files
base_converter.obj: base_converter.asm
    $(ML) $(ML_FLAGS) base_converter.asm

conversions.obj: conversions.asm conversions.inc
    $(ML) $(ML_FLAGS) conversions.asm

calculator.obj: calculator.asm calculator.inc
    $(ML) $(ML_FLAGS) calculator.asm

# Clean target
clean:
    del *.obj
    del *.exe