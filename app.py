import ctypes

# Load the 64-bit DLL
base_calc = ctypes.CDLL('./base_calc.dll')

# Define the function signatures
# Add Numbers: int add_numbers(int a, int b)
base_calc._add_numbers.argtypes = [ctypes.c_int, ctypes.c_int]
base_calc._add_numbers.restype = ctypes.c_int

# Subtract Numbers: int subtract_numbers(int a, int b)
base_calc._subtract_numbers.argtypes = [ctypes.c_int, ctypes.c_int]
base_calc._subtract_numbers.restype = ctypes.c_int

# Multiply Numbers: int multiply_numbers(int a, int b)
base_calc._multiply_numbers.argtypes = [ctypes.c_int, ctypes.c_int]
base_calc._multiply_numbers.restype = ctypes.c_int

# Divide Numbers: int divide_numbers(int a, int b)
base_calc._divide_numbers.argtypes = [ctypes.c_int, ctypes.c_int]
base_calc._divide_numbers.restype = ctypes.c_int

# Convert Decimal to Binary: char* convert_decimal_to_binary(int num)
base_calc._convert_decimal_to_binary.argtypes = [ctypes.c_int]
base_calc._convert_decimal_to_binary.restype = ctypes.POINTER(ctypes.c_char)

# Test functions
def test_operations():
    # Addition
    add_result = base_calc._add_numbers(5, 3)
    print("Addition Result: ", add_result)
    
    # Subtraction
    subtract_result = base_calc._subtract_numbers(10, 3)
    print("Subtraction Result: ", subtract_result)
    
    # Multiplication
    multiply_result = base_calc._multiply_numbers(4, 2)
    print("Multiplication Result: ", multiply_result)
    
    # Division
    divide_result = base_calc._divide_numbers(10, 2)
    print("Division Result: ", divide_result)

    # Convert Decimal to Binary
    num = 10
    binary_result = base_calc._convert_decimal_to_binary(num)
    print(f"Binary of {num}: {binary_result.contents.value.decode('utf-8')}")

# Run the test
if __name__ == "__main__":
    test_operations()
