"""
Matrix wrappers for moonalloy
"""

import ctypes
from .array import _Array_t, ArithmeticError
from .ffi import moonalloy_ffi


class _Matrix_t(ctypes.Structure):
    """
    Internal class for representing a Matrix from moonalloy in python.
    """
    _fields_ = [('rows', ctypes.c_size_t),
                ('cols', ctypes.c_size_t),
                ('arrays', ctypes.POINTER(_Array_t))]


# Initialize all functions in moonalloy
# matrix_print
moonalloy_ffi.matrix_print.argtypes = [ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_print.restype = None
matrix_print = moonalloy_ffi.matrix_print

# matrix_ones
moonalloy_ffi.matrix_ones.argtypes = [ctypes.c_int, ctypes.c_int]
moonalloy_ffi.matrix_ones.restype = ctypes.POINTER(_Matrix_t)
matrix_ones = moonalloy_ffi.matrix_ones

# matrix_zeros
moonalloy_ffi.matrix_zeros.argtypes = [ctypes.c_int, ctypes.c_int]
moonalloy_ffi.matrix_zeros.restype = ctypes.POINTER(_Matrix_t)
matrix_zeros = moonalloy_ffi.matrix_zeros

# matrix_identity
moonalloy_ffi.matrix_identity.argtypes = [ctypes.c_int]
moonalloy_ffi.matrix_identity.restype = ctypes.POINTER(_Matrix_t)
matrix_identity = moonalloy_ffi.matrix_identity

# matrix_scalar
moonalloy_ffi.matrix_scalar.argtypes = [ctypes.POINTER(_Matrix_t),
                                        ctypes.c_double]
moonalloy_ffi.matrix_scalar.restype = ctypes.POINTER(_Matrix_t)
matrix_scalar = moonalloy_ffi.matrix_scalar

# matrix_add
moonalloy_ffi.matrix_add.argtypes = [ctypes.POINTER(_Matrix_t),
                                     ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_add.restype = ctypes.POINTER(_Matrix_t)
matrix_add = moonalloy_ffi.matrix_add

# matrix_sub
moonalloy_ffi.matrix_sub.argtypes = [ctypes.POINTER(_Matrix_t),
                                     ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_sub.restype = ctypes.POINTER(_Matrix_t)
matrix_sub = moonalloy_ffi.matrix_sub

# matrix_elem_mult
moonalloy_ffi.matrix_elem_mult.argtypes = [ctypes.POINTER(_Matrix_t),
                                           ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_elem_mult.restype = ctypes.POINTER(_Matrix_t)
matrix_elem_mult = moonalloy_ffi.matrix_elem_mult

# matrix_transpose
moonalloy_ffi.matrix_transpose.argtypes = [ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_transpose.restype = ctypes.POINTER(_Matrix_t)
matrix_transpose = moonalloy_ffi.matrix_transpose

# matrix_mult
moonalloy_ffi.matrix_mult.argtypes = [ctypes.POINTER(_Matrix_t),
                                      ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_mult.restype = ctypes.POINTER(_Matrix_t)
matrix_mult = moonalloy_ffi.matrix_mult

# matrix_to_string
moonalloy_ffi.matrix_to_string.argtypes = [ctypes.POINTER(_Matrix_t)]
moonalloy_ffi.matrix_to_string.restype = ctypes.POINTER(_Matrix_t)
matrix_to_string = moonalloy_ffi.matrix_to_string


class Matrix:
    """
    Wrapper class for matrices in moonalloy
    """
    _matrix_ptr: _Matrix_t
    _rows: int
    _cols: int

    def __init__(self, py_list: list[list[float]]=None):
        if py_list is not None:
            self._init_matrix_pointer(py_list)
            self._rows = len(py_list)
            self.cols = len(py_list[0])

    def _init_matrix_pointer(self, py_list: list[list[float]]):
        self._matrix_ptr = _Matrix_t()
        self._matrix_ptr.rows = ctypes.c_size_t(len(py_list))
        self._matrix_ptr.cols = ctypes.c_size_t(len(py_list[0]))

        internal_matrix = (ctypes.POINTER(_Array_t) * len(py_list))(*range(len(py_list)))
        for i, array in enumerate(py_list):
            internal_array = (ctypes.c_double * len(array))(*range(len(array)))
            for j, elem in enumerate(array):
                internal_array[j] = elem

            internal_matrix[i] = internal_array

        self._matrix_ptr = internal_matrix

    def add(self, other):
        """
        Performs addition on this and another array.
        """
        if self._rows != other._rows and self._cols != other._cols:
            raise ArithmeticError("Moonalloy - Error: trying to add matrices with incompatible dimensions - operation is undefined.")
        new_mat = matrix_add(self._matrix_ptr, other._matrix_ptr)

        result = Matrix()
        result._matrix_ptr = new_mat
        result._rows = self._rows
        result._cols = other._cols

        return result

    def sub(self, other):
        """
        Subtracts another matrix from this matrix.
        """
        if self._rows != other._rows and self._cols != other._cols:
            raise ArithmeticError("Moonalloy - Error: trying to subtract matrices with incompatible dimensions - operation is undefined.")
        new_mat = matrix_sub(self._matrix_ptr, other._matrix_ptr)

        result = Matrix()
        result._matrix_ptr = new_mat
        result._rows = self._rows
        result._cols = other._cols

        return result

    def mult(self, other):
        """
        Multiplies this matrix with another matrix.
        """
        if self._cols != other._rows:
            raise ArithmeticError("Moonalloy - Error: trying to multiply matrices with incompatible dimensions - operation is undefined.")
        new_mat = matrix_mult(self._matrix_ptr, other._matrix_ptr)

        result = Matrix()
        result._matrix_ptr = new_mat
        result._rows = self._rows
        result._cols = other._cols

        return result

    def elem_mult(self, other):
        """
        Performs Element-wise multiplication on this matrix and another matrix.
        """
        if self._rows != other._rows and self._cols != other._cols:
            raise ArithmeticError("Moonalloy - Error: trying to do element-wise multiplication for matrices with incompatible dimensions - operation is undefined.")
        new_mat = matrix_elem_mult(self._matrix_ptr, other._matrix_ptr)

        result = Matrix()
        result._matrix_ptr = new_mat
        result._rows = self._rows
        result._cols = other._cols

        return result

    def transpose(self):
        """
        Transposes this matrix.
        """
        new_mat = matrix_transpose(self._matrix_ptr)

        result = Matrix()
        result._rows = self._cols
        result._cols = self._rows

        return result

    def scalar(self, scal: float):
        """
        Multiplies every element with a scalar.
        """
        new_mat = matrix_scalar(self._matrix_ptr, ctypes.c_double(scal))

        result = Matrix()
        result._matrix_ptr = new_mat
        result._rows = self._rows
        result._cols = self._cols

        return result

    def dimensions(self):
        """
        Returns a tuple with the dimensions of the matrix (rows, columns).
        """
        return (self._rows, self._cols)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mult(other)

    def __str__(self):
        matrix_as_char_p = matrix_to_string(self._matrix_ptr)
        return matrix_as_char_p.decode('utf-8')
