# Finite difference coefficients estimator

Python implementation of the algorithm presented in:

> [Fornberg, B. (1988). Generation of finite difference formulas on arbitrarily
  spaced grids. Mathematics of computation, 51(184), 699-706.](https://www.ams.org/journals/mcom/1988-51-184/S0025-5718-1988-0935077-0/)

This algorithm can estimate the coefficients of the finite difference formula
used to estimate any derivative of an unidimensional function at a point `x_0`
given a grid of points (mostly neighbors of `x_0`). The accuracy level is
determined by the number of grid points used in each estimation.

### Highlights:

1. Grid points do not have to be equally spaced.
2. `x_0` does not have to be one of the grid points.
3. As a result of 2., the algorithm can also be used to interpolate a function
   at a point `x_0`, by using the coefficients of the derivative of order zero.
4. In a single `M` order derivative approximation the coefficients needed to
   estimate the derivative at any order from zero to `M` are calculated. 

