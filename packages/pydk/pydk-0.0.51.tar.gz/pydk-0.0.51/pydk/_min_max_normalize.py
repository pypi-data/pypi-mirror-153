
def _min_max_normalize(arr):
    
    """Min-max normalize array."""
    
    array_min =  arr.min()
    array_max = arr.max()
    
    return ((arr - array_min) / (array_max - array_min))