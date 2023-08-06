# moonalloy

Smelting moonstone and corroded metal to forge a powerful alloy! (Rust + Lua)

## What is moonalloy?

Moonalloy is a library for scientific computing and data analysis.
It contains functionality for manipulating mathematical objects
like Arrays (Vectors) and Matrices.

It also has structures for handling data tables and functions to analyze that data.

## Goals

The aim of the project is to a all-in-one, go-to library for scientific computing
and data analysis. The functionality should include:

* Tools for numeric linear algebra
* Tools for computational science
* Tools for statistics and machine learning for data analysis

In short, it aims to have similar functionality as NumPy/SciPy and Pandas.
It will not be an exact clone of the mentioned libraries.

## Why moonalloy

Moonalloy is written with speed and ease of use in mind.
Rust was chosen as the backend language since it is fast (similar to C/C++),
but it has more safety features and a more modern toolchain than C/C++
that works out-of-box. It also has a built-in FFI that is compatible with C/C++.

Lua was chosen as the frontend language since it is a fast,
interpreted scripting language similar to python.
It also supports operator overloading and object-oriented programming,
which makes it pleasant to implement a library with an intuitive syntax.
