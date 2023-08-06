import numpy as np
from setuptools import Extension, find_packages, setup

long_description = """
Finite difference coefficients estimator
========================================

Python implementation of the algorithm presented in:

  Fornberg, B. (1988). Generation of finite difference formulas on arbitrarily
  spaced grids. Mathematics of computation, 51(184), 699-706.

This algorithm can estimate the coefficients of the finite difference formula
used to estimate any derivative of an unidimensional function at a point `x_0`
given a grid of points (mostly neighbors of `x_0`). The accuracy level is
determined by the number of grid points used in each estimation.

Highlights
----------

1. Grid points do not have to be equally spaced.
2. `x_0` does not have to be one of the grid points.
3. As a result of 2., the algorithm can also be used to interpolate a function
   at a point `x_0`, by using the coefficients of the derivative of order zero.
4. In a single `M` order derivative approximation the coefficients needed to
   estimate the derivative at any order from zero to `M` are calculated. 
""" 

setup(
    name="fdce",
    version="0.1.1a5",
    description="Finite difference coefficient estimator",
    long_description=long_description,
    author="Jorge Morgado Vega",
    author_email="jorge.morgadov@gmail.com",
    requires=["numpy"],
    packages=find_packages(),
    python_requires=">=3.8",
    ext_modules=[
        Extension(
            "fdce._extension._fdce",
            ["fdce/_extension/_fdce.c"],
            include_dirs=[np.get_include()],
        )
    ]
)
