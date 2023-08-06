
__module_name__ = "_filter_overlapping.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# import packages #
# --------------- #
import numpy as np


def _filter_overlapping(set_01, set_02, labels=[0, 1]):

    set_01_only = [clone for clone in set_01 if not clone in set_02]
    set_02_only = [clone for clone in set_02 if not clone in set_01]

    unique_clones = {
        labels[0]: np.array(set_01_only).astype(float),
        labels[1]: np.array(set_02_only).astype(float),
    }

    return unique_clones
