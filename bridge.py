import ctypes
import math
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
library_path = os.path.join(current_directory, 'lib2048.so')
# Define the C data types
c_uint16 = ctypes.c_uint64
c_size_t = ctypes.c_size_t

# Load the shared library
lib = ctypes.CDLL(library_path)  # Replace "path/to/your/library.so" with the actual path to your library

# Define the C function signature
lib.find_best_move.argtypes = [ctypes.c_uint64]
lib.find_best_move.restype = c_uint16


def reverse_array(array):
    return array[::-1]


def convert_to_binary_exponent(arr):
    binary_exponents = ""
    for num in arr:
        if num == 0:
            binary_exponents += '0000'
        else:
            try:
                exponent = int(math.log2(num))
                binary_exponents += bin(exponent)[2:].zfill(4)
            except ValueError:
                binary_exponents += '0000'
    return binary_exponents


def convert_to_uint64(array):
    # Create a 64-bit unsigned integer type
    uint64_t = ctypes.c_uint64

    # Create a union structure to interpret the bytes of the array as a uint64_t value
    class Union(ctypes.Union):
        _fields_ = [("array", ctypes.c_ubyte * 16),
                    ("value", uint64_t)]

    # Create an instance of the union
    union = Union()

    # Convert the binary string to a uint64_t value
    union.value = int(array, 2)

    # Access the union's value field to get the uint64_t value
    uint64_value = union.value

    return uint64_value

def call_algoritm(result):
    lib.init_tables()
    best_move = lib.find_best_move(result)
    return best_move

def convert_array(arr):
    result = []
    for row in arr:
        for item in row:
            result.append(item)        
    return result

# Example usage
#c
# array = [[2048, 0, 0, 0], [2048, 0, 2, 0], [0, 0, 0, 0], [0, 0, 256, 128]]
# result=convert_to_uint64(convert_to_binary_exponent(reverse_array(array)))
# print(output)


def getbestmove(grid):
    print("got inside bridge")
    result=convert_to_uint64(convert_to_binary_exponent(reverse_array(grid)))
    print("the converted array is ",result) 
    move=call_algoritm(result) 
    # print("the move is gvgfjc",move)
    return move
# Example array of 16 elements
# array = [4, 8, 32, 128, 4, 8, 8, 4, 4, 0, 2, 0, 0, 2, 0, 0]
# reversed_array = reverse_array(array)

# # Convert the array to binary exponent representation
# binary_exponents = convert_to_binary_exponent(reversed_array)

# # Pad the binary_exponents string with zeros if its length is less than 64
# binary_exponents = binary_exponents.zfill(64)

# # Convert the binary_exponents to uint64_t
# result = convert_to_uint64(binary_exponents)

# print(result)

# Example usage

# grid = [2, 0, 2, 4, 4, 2, 8, 16, 2, 4, 8, 2, 4, 0, 0, 0]
# board_representation = convert_grid_to_board(grid)
# print(board_representation)
# # Call the C function
# lib.init_tables()
# best_move = lib.find_best_move(result)

# print("the best move is hi " ,best_move)
