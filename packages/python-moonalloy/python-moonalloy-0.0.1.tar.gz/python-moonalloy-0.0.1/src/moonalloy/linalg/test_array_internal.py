"""
Tests for internal array classes.
"""
import ctypes
from array import (array_ones,
                   array_print,
                   array_scalar,
                   array_sum,
                   array_zeros)

# Test
print("----- Initiating Test -----\n\n")

arr = array_ones(ctypes.c_int(3))
print("Result: ")
array_print(arr)
print()

arr2 = array_zeros(ctypes.c_int(2))
print("Result: ")
array_print(arr2)
print()

sum_result = array_sum(arr)
print(f"Result: {sum_result}")
print()

scalar_result = array_scalar(arr, ctypes.c_double(2.5))
print("Result: ")
array_print(scalar_result)
print("\n----- Test Successful -----")
