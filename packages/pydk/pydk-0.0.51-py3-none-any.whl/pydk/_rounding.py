import numpy as np


def _ceil(x, precision=0):

    """
    Round to the nearest lower bound within the given precision.

    Parameters:
    -----------
    x
    array or value
    type: numpy.ndarray or int or float

    precision
    positions left (negative) or right (positive) of the decimal point to round.

    Returns:
    --------
    rounded_value
    type: numpy.ndarray or int or float

    """
  
    return np.true_divide(np.ceil(x * 10**precision), 10**precision)


def _floor(x, precision=0):
  
    """
    Round to the nearest upper bound within the given precision.

    Parameters:
    -----------
    x
    array or value
    type: numpy.ndarray or int or float

    precision
    positions left (negative) or right (positive) of the decimal point to round.

    Returns:
    --------
    rounded_value
    type: numpy.ndarray or int or float
    """
  
    return np.true_divide(np.floor(x * 10**precision), 10**precision)
