
import os

def _get_parent_directory(path, levels=1, verbose=False):
    
    """
    Parameters:
    -----------
    path
        input path
        type: str
    
    levels
        number of levels `os.path.dirname` should be called.
        type: int
        default: 1
    
    verbose
        if True, prints the resulting directory of each iteration.
        type: bool
        default: False
    
    Returns:
    --------
    path to parent directory
    """
    
    path_ = path
    for i in range(levels):
        path_ = os.path.dirname(path_)
        if verbose:
            print(i, path_)
            
    return path_
