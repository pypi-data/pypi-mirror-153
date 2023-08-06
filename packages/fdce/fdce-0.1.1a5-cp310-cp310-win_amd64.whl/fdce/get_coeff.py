import numpy as np


def get_coeff(
    x_0: float, a: np.ndarray, M: int, coeff_matrix: np.ndarray
) -> np.ndarray:
    """
    Returns the coefficients of the finite difference formula for the given
    grid.

    Parameters
    ----------
    x_0 : float
        Point at which the coefficients are evaluated.
    a : np.ndarray
        Grid points.
    M : int
        Degree of the derivative.
    coeff_matrix : np.ndarray
        If given, the coeffitients are calculated in the given matrix.

        This matrix must have shape MxNxN, where N is the number of grid
        points. This is useful for memory efficiency.

    Returns
    -------
    np.ndarray
        Coeffitient matrix.

        The matrix in [m_i, N-1, :] gives the coeffitients to estimate the
        derivative of order m_i. Where N is the number of grid points.
    """
    # pylint: disable=invalid-name
    # The variables where named as in the original algorithm.

    N = a.shape[0]
    M += 1
    coeff_arr = np.zeros((M, N, N)) if coeff_matrix is None else coeff_matrix
    coeff_arr[0, 0, 0] = 1
    c1 = 1

    for n in range(1, N):
        c2 = 1
        for v in range(n):
            c3 = a[n] - a[v]
            c2 = c2 * c3
            if n < M:
                coeff_arr[n, n - 1, v] = 0
            for m in range(min(n + 1, M)):
                d_1 = coeff_arr[m, n - 1, v]
                d_2 = coeff_arr[m - 1, n - 1, v] if m != 0 else 0
                coeff_arr[m, n, v] = ((a[n] - x_0) * d_1 - m * d_2) / c3
        for m in range(min(n + 1, M)):
            d_1 = coeff_arr[m - 1, n - 1, n - 1] if m != 0 else 0
            d_2 = coeff_arr[m, n - 1, n - 1]
            coeff_arr[m, n, n] = (c1 / c2) * (m * d_1 - (a[n - 1] - x_0) * d_2)
        c1 = c2

    return coeff_arr
