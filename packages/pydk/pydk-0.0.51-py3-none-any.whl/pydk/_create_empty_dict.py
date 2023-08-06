
# _create_empty_dict.py

__module_name__ = "_create_empty_dict.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


def _create_empty_dict(keys):

    """
    Create an empty python Dictionary given a set of keys.
    
    Parameters:
    -----------
    keys
    
    Returns:
    --------
    Dict
    """

    Dict = {}
    for key in keys:
        Dict[key] = {}

    return Dict