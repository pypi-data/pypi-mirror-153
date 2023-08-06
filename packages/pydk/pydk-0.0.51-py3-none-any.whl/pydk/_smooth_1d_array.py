import numpy as np

def _get_window(window_size):
    return np.ones(int(window_size)) / float(window_size)
def _add_back_edges(x, x_smooth, edge_size):
    
    return np.hstack(
        [x[:edge_size], x_smooth[edge_size:-edge_size], x[-edge_size:]]
    )

def _smooth_1d_array(x, window_size, edge_size):
    
    """
    Calculate the moving average over a given window of an array.
    
    Parameters:
    -----------
    x
        1-d array
        type: numpy.ndarray
        
    window_size
        Number of items over which values should be smoothed.
        type: int
    
    edge_size
        type: int
        
    Returns:
    --------
    Array of a moving average of array values using the given window.
    """
    
    window = _get_window(window_size)
    x_smooth = np.convolve(x, window, "same")
    return _add_back_edges(x, x_smooth, edge_size)