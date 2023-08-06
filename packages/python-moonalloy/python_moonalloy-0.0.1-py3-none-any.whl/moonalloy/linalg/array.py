"""
Array wrappers for moonalloy
"""

import ctypes
from .ffi import moonalloy_ffi


class _Array_t(ctypes.Structure):
    """
    Internal class for representing an Array from moonalloy in python.
    """
    _fields_ = [('len', ctypes.c_size_t),
                ('arr', ctypes.POINTER(ctypes.c_double))]


# Initialize all functions in moonalloy
# array_print
moonalloy_ffi.array_print.argtypes = [ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_print.restype = None
array_print = moonalloy_ffi.array_print

# array_ones
moonalloy_ffi.array_ones.argtypes = [ctypes.c_int]
moonalloy_ffi.array_ones.restype = ctypes.POINTER(_Array_t)
array_ones = moonalloy_ffi.array_ones

# array_zeros
moonalloy_ffi.array_zeros.argtypes = [ctypes.c_int]
moonalloy_ffi.array_zeros.restype = ctypes.POINTER(_Array_t)
array_zeros = moonalloy_ffi.array_zeros

# array_sum
moonalloy_ffi.array_sum.argtypes = [ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_sum.restype = ctypes.c_double
array_sum = moonalloy_ffi.array_sum

# array_scalar
moonalloy_ffi.array_scalar.argtypes = [ctypes.POINTER(_Array_t),
                                       ctypes.c_double]
moonalloy_ffi.array_scalar.restype = ctypes.POINTER(_Array_t)
array_scalar = moonalloy_ffi.array_scalar

# array_add
moonalloy_ffi.array_add.argtypes = [ctypes.POINTER(_Array_t),
                                    ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_add.restype = ctypes.POINTER(_Array_t)
array_add = moonalloy_ffi.array_add

# array_sub
moonalloy_ffi.array_sub.argtypes = [ctypes.POINTER(_Array_t),
                                    ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_sub.restype = ctypes.POINTER(_Array_t)
array_sub = moonalloy_ffi.array_sub

# array_mult
moonalloy_ffi.array_mult.argtypes = [ctypes.POINTER(_Array_t),
                                     ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_mult.restype = ctypes.POINTER(_Array_t)
array_mult = moonalloy_ffi.array_mult

# array_dotp
moonalloy_ffi.array_dotp.argtypes = [ctypes.POINTER(_Array_t),
                                     ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_dotp.restype = ctypes.c_double
array_dotp = moonalloy_ffi.array_dotp

# array_concat
moonalloy_ffi.array_concat.argtypes = [ctypes.POINTER(_Array_t),
                                       ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_concat.restype = ctypes.POINTER(_Array_t)
array_concat = moonalloy_ffi.array_concat

# array_to_string
moonalloy_ffi.array_to_string.argtypes = [ctypes.POINTER(_Array_t)]
moonalloy_ffi.array_to_string.restype = ctypes.c_char_p
array_to_string = moonalloy_ffi.array_to_string


class ArithmeticError(BaseException):
    """
    Exception for arithmetic errors.
    """


class Array:
    """
    Wrapper class for arrays in moonalloy
    """
    _array_ptr: _Array_t
    _len: int

    def __init__(self, py_list: list[float]=None):
        if py_list is not None:
            self._init_array_pointer(py_list)
            self._len = len(py_list)

    def _init_array_pointer(self, py_list: list[float]):
        self._array_ptr = _Array_t()
        self._array_ptr.len = ctypes.c_size_t(len(py_list))

        internal_array = (ctypes.c_double * len(py_list))(*range(len(py_list)))

        for i, elem in enumerate(py_list):
            internal_array[i] = elem

        self._array_ptr.arr = internal_array

    def add(self, other):
        """
        Performs addition on this and another array.
        """
        if self._len != other._len:
            raise ArithmeticError("Moonalloy - Error: trying to add arrays with different lengths - operation is undefined.")
        new_arr = array_add(self._array_ptr, other._array_ptr)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len

        return result

    def sub(self, other):
        """
        Subtracts an another array from this array.
        """
        if self._len != other._len:
            raise ArithmeticError("Moonalloy - Error: trying to subtract arrays with different lengths - operation is undefined.")
        new_arr = array_sub(self._array_ptr, other._array_ptr)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len

        return result

    def mult(self, other):
        """
        Multiplies this array with another array.
        """
        if self._len != other._len:
            raise ArithmeticError("Moonalloy - Error: trying to multiply arrays with different lengths - operation is undefined.")
        new_arr = array_mult(self._array_ptr, other._array_ptr)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len

        return result

    def dotp(self, other):
        """
        Calculates the dot product from this and another array.
        """
        if self._len != other._len:
            raise ArithmeticError("Moonalloy - Error: trying to calculate the dot product of arrays with different lengths - operation is undefined.")
        new_arr = array_dotp(self._array_ptr, other._array_ptr)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len

        return result

    def concat(self, other):
        """
        Returns the concatenation of this and another array.
        """
        new_arr = array_concat(self._array_ptr, other._array_ptr)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len + other._len

        return result

    def scalar(self, scal: float):
        """
        Returns a new Array that has been multiplied by a scalar value.
        """
        new_arr = array_scalar(self._array_ptr, scal)

        result = Array()
        result._array_ptr = new_arr
        result._len = self._len

        return result

    def sum(self):
        """
        Returns the sum of the internal array
        """
        return array_sum(self._array_ptr)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mult(other)

    def __str__(self):
        array_as_char_p = array_to_string(self._array_ptr)
        return array_as_char_p.decode('utf-8')
