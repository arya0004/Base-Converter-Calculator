import sys
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QRadioButton, QPushButton,
                            QLabel, QButtonGroup, QTabWidget)
from PyQt6.QtCore import Qt

# Load the NASM library
try:
    lib = ctypes.CDLL('./conversions.dll')
except Exception as e:
    print(f"Error loading DLL: {e}")
    sys.exit(1)

# Define the function signatures
lib.StringToNumber.argtypes = [ctypes.c_char_p, ctypes.c_uint64]
lib.StringToNumber.restype = ctypes.c_uint64

lib.NumberToString.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p]
lib.NumberToString.restype = None

lib.ConvertBase.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p]
lib.ConvertBase.restype = None

lib.ToGrayCode.argtypes = [ctypes.c_uint64]
lib.ToGrayCode.restype = ctypes.c_uint64

lib.FromGrayCode.argtypes = [ctypes.c_uint64]
lib.FromGrayCode.restype = ctypes.c_uint64

lib.ToExcess3.argtypes = [ctypes.c_uint64]
lib.ToExcess3.restype = ctypes.c_uint64

lib.FromExcess3.argtypes = [ctypes.c_uint64]
lib.FromExcess3.restype = ctypes.c_uint64

# Add calculator function signatures
lib.AddNumbers.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
lib.AddNumbers.restype = ctypes.c_uint64

lib.SubtractNumbers.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
lib.SubtractNumbers.restype = ctypes.c_uint64

lib.MultiplyNumbers.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
lib.MultiplyNumbers.restype = ctypes.c_uint64

lib.DivideNumbers.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
lib.DivideNumbers.restype = ctypes.c_uint64

# Calculator operation constants
OP_ADD = 0
OP_SUBTRACT = 1
OP_MULTIPLY = 2
OP_DIVIDE = 3

class BaseConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base Converter & Calculator")
        self.setGeometry(100, 100, 800, 600)
        
        # Calculator state
        self.first_number = 0
        self.second_number = 0
        self.current_operation = None
        self.is_first_number = True
        self.clear_on_next_input = False
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Base conversion tab
        base_tab = QWidget()
        base_layout = QVBoxLayout(base_tab)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter number...")
        self.input_field.textChanged.connect(self.update_output)
        base_layout.addWidget(self.input_field)
        
        # Output fields
        output_layout = QHBoxLayout()
        
        # Binary output
        binary_layout = QVBoxLayout()
        binary_label = QLabel("Binary:")
        self.binary_output = QLineEdit()
        self.binary_output.setReadOnly(True)
        binary_layout.addWidget(binary_label)
        binary_layout.addWidget(self.binary_output)
        output_layout.addLayout(binary_layout)
        
        # Decimal output
        decimal_layout = QVBoxLayout()
        decimal_label = QLabel("Decimal:")
        self.decimal_output = QLineEdit()
        self.decimal_output.setReadOnly(True)
        decimal_layout.addWidget(decimal_label)
        decimal_layout.addWidget(self.decimal_output)
        output_layout.addLayout(decimal_layout)
        
        # Hexadecimal output
        hex_layout = QVBoxLayout()
        hex_label = QLabel("Hexadecimal:")
        self.hex_output = QLineEdit()
        self.hex_output.setReadOnly(True)
        hex_layout.addWidget(hex_label)
        hex_layout.addWidget(self.hex_output)
        output_layout.addLayout(hex_layout)
        
        # Octal output
        octal_layout = QVBoxLayout()
        octal_label = QLabel("Octal:")
        self.octal_output = QLineEdit()
        self.octal_output.setReadOnly(True)
        octal_layout.addWidget(octal_label)
        octal_layout.addWidget(self.octal_output)
        output_layout.addLayout(octal_layout)
        
        base_layout.addLayout(output_layout)
        
        # Base selection radio buttons
        base_group = QButtonGroup()
        self.decimal_radio = QRadioButton("Decimal")
        self.binary_radio = QRadioButton("Binary")
        self.hex_radio = QRadioButton("Hexadecimal")
        self.octal_radio = QRadioButton("Octal")
        
        base_group.addButton(self.decimal_radio)
        base_group.addButton(self.binary_radio)
        base_group.addButton(self.hex_radio)
        base_group.addButton(self.octal_radio)
        
        self.decimal_radio.setChecked(True)
        
        base_layout = QHBoxLayout()
        base_layout.addWidget(self.decimal_radio)
        base_layout.addWidget(self.binary_radio)
        base_layout.addWidget(self.hex_radio)
        base_layout.addWidget(self.octal_radio)
        base_layout.addLayout(base_layout)
        
        # Gray code tab
        gray_tab = QWidget()
        gray_layout = QVBoxLayout(gray_tab)
        
        # Gray code input
        gray_input_layout = QHBoxLayout()
        gray_input_label = QLabel("Input:")
        self.gray_input = QLineEdit()
        self.gray_input.setPlaceholderText("Enter number...")
        self.gray_input.textChanged.connect(self.update_gray_output)
        gray_input_layout.addWidget(gray_input_label)
        gray_input_layout.addWidget(self.gray_input)
        gray_layout.addLayout(gray_input_layout)
        
        # Gray code outputs
        gray_output_layout = QHBoxLayout()
        
        # To Gray code
        to_gray_layout = QVBoxLayout()
        to_gray_label = QLabel("To Gray Code:")
        self.to_gray_output = QLineEdit()
        self.to_gray_output.setReadOnly(True)
        to_gray_layout.addWidget(to_gray_label)
        to_gray_layout.addWidget(self.to_gray_output)
        gray_output_layout.addLayout(to_gray_layout)
        
        # From Gray code
        from_gray_layout = QVBoxLayout()
        from_gray_label = QLabel("From Gray Code:")
        self.from_gray_output = QLineEdit()
        self.from_gray_output.setReadOnly(True)
        from_gray_layout.addWidget(from_gray_label)
        from_gray_layout.addWidget(self.from_gray_output)
        gray_output_layout.addLayout(from_gray_layout)
        
        gray_layout.addLayout(gray_output_layout)
        
        # Excess-3 tab
        excess3_tab = QWidget()
        excess3_layout = QVBoxLayout(excess3_tab)
        
        # Excess-3 input
        excess3_input_layout = QHBoxLayout()
        excess3_input_label = QLabel("Input:")
        self.excess3_input = QLineEdit()
        self.excess3_input.setPlaceholderText("Enter number...")
        self.excess3_input.textChanged.connect(self.update_excess3_output)
        excess3_input_layout.addWidget(excess3_input_label)
        excess3_input_layout.addWidget(self.excess3_input)
        excess3_layout.addLayout(excess3_input_layout)
        
        # Excess-3 outputs
        excess3_output_layout = QHBoxLayout()
        
        # To Excess-3
        to_excess3_layout = QVBoxLayout()
        to_excess3_label = QLabel("To Excess-3:")
        self.to_excess3_output = QLineEdit()
        self.to_excess3_output.setReadOnly(True)
        to_excess3_layout.addWidget(to_excess3_label)
        to_excess3_layout.addWidget(self.to_excess3_output)
        excess3_output_layout.addLayout(to_excess3_layout)
        
        # From Excess-3
        from_excess3_layout = QVBoxLayout()
        from_excess3_label = QLabel("From Excess-3:")
        self.from_excess3_output = QLineEdit()
        self.from_excess3_output.setReadOnly(True)
        from_excess3_layout.addWidget(from_excess3_label)
        from_excess3_layout.addWidget(self.from_excess3_output)
        excess3_output_layout.addLayout(from_excess3_layout)
        
        excess3_layout.addLayout(excess3_output_layout)
        
        # Add tabs
        tab_widget.addTab(base_tab, "Base Conversion")
        tab_widget.addTab(gray_tab, "Gray Code")
        tab_widget.addTab(excess3_tab, "Excess-3")
        
        layout.addWidget(tab_widget)
        
        # Calculator buttons
        calculator_layout = QVBoxLayout()
        
        # Operation buttons
        operations_layout = QHBoxLayout()
        self.add_button = QPushButton("+")
        self.subtract_button = QPushButton("-")
        self.multiply_button = QPushButton("×")
        self.divide_button = QPushButton("÷")
        self.equals_button = QPushButton("=")
        self.clear_button = QPushButton("C")
        
        self.add_button.clicked.connect(lambda: self.set_operation(OP_ADD))
        self.subtract_button.clicked.connect(lambda: self.set_operation(OP_SUBTRACT))
        self.multiply_button.clicked.connect(lambda: self.set_operation(OP_MULTIPLY))
        self.divide_button.clicked.connect(lambda: self.set_operation(OP_DIVIDE))
        self.equals_button.clicked.connect(self.calculate_result)
        self.clear_button.clicked.connect(self.clear_calculator)
        
        operations_layout.addWidget(self.add_button)
        operations_layout.addWidget(self.subtract_button)
        operations_layout.addWidget(self.multiply_button)
        operations_layout.addWidget(self.divide_button)
        operations_layout.addWidget(self.equals_button)
        operations_layout.addWidget(self.clear_button)
        
        calculator_layout.addLayout(operations_layout)
        
        # Number buttons
        button_grid = QWidget()
        button_grid_layout = QVBoxLayout(button_grid)
        
        # Create rows of buttons
        for i in range(4):
            row_layout = QHBoxLayout()
            for j in range(4):
                value = i * 4 + j
                if value < 10:
                    text = str(value)
                else:
                    text = chr(ord('A') + value - 10)
                button = QPushButton(text)
                button.clicked.connect(lambda checked, t=text: self.append_digit(t))
                row_layout.addWidget(button)
            button_grid_layout.addLayout(row_layout)
        
        calculator_layout.addWidget(button_grid)
        layout.addLayout(calculator_layout)
        
        # Connect radio button signals
        self.decimal_radio.toggled.connect(self.update_output)
        self.binary_radio.toggled.connect(self.update_output)
        self.hex_radio.toggled.connect(self.update_output)
        self.octal_radio.toggled.connect(self.update_output)
    
    def get_current_base(self):
        if self.decimal_radio.isChecked():
            return 10
        elif self.binary_radio.isChecked():
            return 2
        elif self.hex_radio.isChecked():
            return 16
        else:
            return 8
    
    def append_digit(self, digit):
        if self.clear_on_next_input:
            self.input_field.clear()
            self.clear_on_next_input = False
        
        current_text = self.input_field.text()
        self.input_field.setText(current_text + digit)
    
    def set_operation(self, operation):
        if self.input_field.text():
            self.first_number = self.get_current_number()
            self.current_operation = operation
            self.is_first_number = False
            self.clear_on_next_input = True
    
    def calculate_result(self):
        if self.current_operation is not None and self.input_field.text():
            self.second_number = self.get_current_number()
            
            # Convert numbers to decimal for calculation
            base = self.get_current_base()
            input_bytes = str(self.first_number).encode('utf-8')
            output_buffer = ctypes.create_string_buffer(32)
            lib.ConvertBase(input_bytes, base, 10, output_buffer)
            first_decimal = int(output_buffer.value.decode('utf-8'))
            
            input_bytes = str(self.second_number).encode('utf-8')
            lib.ConvertBase(input_bytes, base, 10, output_buffer)
            second_decimal = int(output_buffer.value.decode('utf-8'))
            
            # Perform calculation using assembly function
            try:
                if self.current_operation == OP_ADD:
                    result = lib.AddNumbers(first_decimal, second_decimal)
                elif self.current_operation == OP_SUBTRACT:
                    result = lib.SubtractNumbers(first_decimal, second_decimal)
                elif self.current_operation == OP_MULTIPLY:
                    result = lib.MultiplyNumbers(first_decimal, second_decimal)
                elif self.current_operation == OP_DIVIDE:
                    if second_decimal == 0:
                        self.input_field.setText("Error: Division by zero")
                        return
                    result = lib.DivideNumbers(first_decimal, second_decimal)
                
                # Convert result back to current base
                input_bytes = str(result).encode('utf-8')
                lib.ConvertBase(input_bytes, 10, base, output_buffer)
                self.input_field.setText(output_buffer.value.decode('utf-8'))
                
                self.is_first_number = True
                self.current_operation = None
                self.clear_on_next_input = True
            except Exception as e:
                print(f"Error in calculation: {e}")
                self.input_field.setText("Error: Calculation failed")
    
    def clear_calculator(self):
        self.input_field.clear()
        self.first_number = 0
        self.second_number = 0
        self.current_operation = None
        self.is_first_number = True
        self.clear_on_next_input = False
        self.clear_outputs()
    
    def get_current_number(self):
        input_text = self.input_field.text()
        if not input_text:
            return 0
        
        input_base = self.get_current_base()
        input_bytes = input_text.encode('utf-8')
        return lib.StringToNumber(input_bytes, input_base)
    
    def update_output(self):
        input_text = self.input_field.text()
        if not input_text:
            self.clear_outputs()
            return
        
        input_base = self.get_current_base()
        
        try:
            # Convert input to bytes for C interface
            input_bytes = input_text.encode('utf-8')
            output_buffer = ctypes.create_string_buffer(32)
            
            # Convert to binary
            lib.ConvertBase(input_bytes, input_base, 2, output_buffer)
            self.binary_output.setText(output_buffer.value.decode('utf-8'))
            
            # Convert to decimal
            lib.ConvertBase(input_bytes, input_base, 10, output_buffer)
            self.decimal_output.setText(output_buffer.value.decode('utf-8'))
            
            # Convert to hexadecimal
            lib.ConvertBase(input_bytes, input_base, 16, output_buffer)
            self.hex_output.setText(output_buffer.value.decode('utf-8'))
            
            # Convert to octal
            lib.ConvertBase(input_bytes, input_base, 8, output_buffer)
            self.octal_output.setText(output_buffer.value.decode('utf-8'))
        except Exception as e:
            print(f"Error in conversion: {e}")
            self.clear_outputs()
    
    def update_gray_output(self):
        input_text = self.gray_input.text()
        if not input_text:
            self.to_gray_output.clear()
            self.from_gray_output.clear()
            return
        
        try:
            # Convert input to number
            input_base = 10  # Gray code conversions work with decimal numbers
            input_bytes = input_text.encode('utf-8')
            number = lib.StringToNumber(input_bytes, input_base)
            
            # Convert to Gray code
            gray_code = lib.ToGrayCode(number)
            
            # Display Gray code in binary
            output_buffer = ctypes.create_string_buffer(32)
            lib.NumberToString(gray_code, 2, output_buffer)
            binary_gray = output_buffer.value.decode('utf-8')
            
            # Display only binary representation
            self.to_gray_output.setText(binary_gray)
            
            # Convert from Gray code back to decimal
            original = lib.FromGrayCode(gray_code)
            lib.NumberToString(original, input_base, output_buffer)
            self.from_gray_output.setText(output_buffer.value.decode('utf-8'))
        except Exception as e:
            print(f"Error in Gray code conversion: {e}")
            self.to_gray_output.clear()
            self.from_gray_output.clear()
    
    def update_excess3_output(self):
        input_text = self.excess3_input.text()
        if not input_text:
            self.to_excess3_output.clear()
            self.from_excess3_output.clear()
            return
        
        try:
            # Convert input to number
            input_base = 10  # Excess-3 conversions work with decimal numbers
            input_bytes = input_text.encode('utf-8')
            number = lib.StringToNumber(input_bytes, input_base)
            
            if number < 0 or number > 9:
                self.to_excess3_output.setText("Error: Please enter a single digit (0-9)")
                self.from_excess3_output.clear()
                return
            
            # Convert to Excess-3
            excess3 = lib.ToExcess3(number)
            
            # Display Excess-3 in binary
            output_buffer = ctypes.create_string_buffer(32)
            lib.NumberToString(excess3, 2, output_buffer)
            binary_excess3 = output_buffer.value.decode('utf-8')
            
            # Pad with leading zeros to make it 4 bits
            binary_excess3 = binary_excess3.zfill(4)
            
            # Display only binary representation
            self.to_excess3_output.setText(binary_excess3)
            
            # Convert from Excess-3 back to decimal
            original = lib.FromExcess3(excess3)
            lib.NumberToString(original, input_base, output_buffer)
            self.from_excess3_output.setText(output_buffer.value.decode('utf-8'))
        except Exception as e:
            print(f"Error in Excess-3 conversion: {e}")
            self.to_excess3_output.setText("Error: Invalid input")
            self.from_excess3_output.clear()
    
    def clear_outputs(self):
        self.binary_output.clear()
        self.decimal_output.clear()
        self.hex_output.clear()
        self.octal_output.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BaseConverter()
    window.show()
    sys.exit(app.exec()) 