
# _update_python_class_attr.py
__module_name__ = "_training_preflight.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


def _update_python_class_attr(class_object, parameter, value):

    """Update a python class object with a new {key, value} pair."""

    class_object.__setattr__(parameter, value)