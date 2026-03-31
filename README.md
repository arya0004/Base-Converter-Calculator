# Base Converter Calculator

A powerful calculator application that combines number base conversions, Gray code, Excess-3 code conversions, and arithmetic operations. Built with Python and NASM assembly for optimal performance.

## Features

1. **Base Conversions**
   - Convert numbers between Binary, Decimal, Hexadecimal, and Octal
   - Real-time conversion as you type
   - Supports all common number bases

2. **Gray Code Conversion**
   - Convert decimal digits (0-9) to Gray code
   - Display results in binary format
   - Convert back to original decimal

3. **Excess-3 Code Conversion**
   - Convert decimal digits (0-9) to Excess-3 code
   - Display results in binary format
   - Convert back to original decimal

4. **Calculator**
   - Basic arithmetic operations (+, -, ×, ÷)
   - Works in any number base
   - Division by zero protection
   - Clear and equals functions

## Technical Details

- **Frontend**: Python with PyQt6 for the graphical interface
- **Backend**: NASM assembly for high-performance conversions and calculations
- **Platform**: Windows (64-bit)

## Requirements

1. Python 3.x
2. PyQt6 (`pip install PyQt6`)
3. NASM (Netwide Assembler)
4. GCC (GNU Compiler Collection)

## How to Run

1. **Install Requirements**
   ```bash
   pip install PyQt6
   ```

2. **Build the Assembly Code**
   ```bash
   ./build.sh
   ```
   This will:
   - Compile the NASM code
   - Create the DLL
   - Clean up temporary files

3. **Run the Application**
   ```bash
   python base_converter.py
   ```

## How to Use

1. **Base Conversion**
   - Enter a number in any base
   - Select the input base (Binary, Decimal, Hex, Octal)
   - See conversions in all other bases

2. **Gray Code**
   - Enter a single digit (0-9)
   - See the Gray code in binary
   - See the conversion back to decimal

3. **Excess-3 Code**
   - Enter a single digit (0-9)
   - See the Excess-3 code in binary
   - See the conversion back to decimal

4. **Calculator**
   - Enter first number
   - Click operation (+, -, ×, ÷)
   - Enter second number
   - Click equals (=) to see result
   - Use clear (C) to reset

## Example Usage

1. **Base Conversion**
   - Input: "1010" (Binary)
   - Output: "10" (Decimal), "A" (Hex), "12" (Octal)

2. **Gray Code**
   - Input: "5"
   - Output: "0111" (Gray code)

3. **Excess-3 Code**
   - Input: "5"
   - Output: "1000" (Excess-3)

4. **Calculator**
   - Input: "10" + "5"
   - Output: "15" (in current base)

## Error Handling

- Invalid inputs are clearly indicated
- Division by zero is prevented
- Single-digit restrictions for Gray and Excess-3 codes
- Clear error messages for all operations

This project demonstrates the integration of high-level Python programming with low-level assembly code, providing both a user-friendly interface and efficient number processing capabilities. 