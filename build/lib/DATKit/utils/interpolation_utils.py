import numpy as np


def zeros(*args, **kwargs):
    """
    Create a function for extrapolation that assigns a value of zero outside the range.

    Parameters
    ----------
    *args : tuple
        Additional positional arguments (not used, included for compatibility).
    **kwargs : dict
        Additional keyword arguments (not used, included for compatibility).

    Returns
    ----------
    callable
        A function that takes an array `x` as input and returns an array of zeros
        with the same shape as `x`.
    """
    return lambda x: np.zeros_like(x)


def nearest(kDa, values, **kwargs):
    """
    Create a function for extrapolation that assigns the nearest available value
    from the input data.

    Parameters
    ----------
    kDa : array-like
        Array of known `kDa` values from the original dataset.
    values : array-like
        Array of corresponding values to the `kDa` values.
    **kwargs : dict
        Additional keyword arguments (not used, included for compatibility).

    Returns
    ----------
    callable
        A function that takes an array `x` as input and returns an array of values
        corresponding to the nearest `kDa` value for each point in `x`.

    Notes
    ----------
    - The function uses the absolute difference between each value in `x` and the
      known `kDa` values to determine the nearest value.
    - If `x` contains values outside the range of `kDa`, the nearest edge value
      in `kDa` will be assigned.
    """

    def nearest_func(x):
        # Find the index of the nearest `kDa` value for each point in `x`
        nearest_indices = np.abs(kDa.values[:, None] - x).argmin(axis=0)
        return values.iloc[nearest_indices]

    return nearest_func
