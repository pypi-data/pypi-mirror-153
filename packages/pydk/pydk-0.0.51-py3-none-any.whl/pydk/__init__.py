# __init__.py

from ._create_empty_dict import _create_empty_dict as create_empty_dict
from ._flexible_multilevel_mkdir import _flexible_multilevel_mkdir as mkdir_flex
from ._get_parent_directory import _get_parent_directory as parent_dir
from ._smooth_1d_array import _smooth_1d_array as smooth
from ._mk_GCP_command import _mk_GCP_command as gcp
from ._load_pickled import _load_pickled as load_pickled
from ._class_attributes import _class_attributes as class_attributes
from ._to_list import _to_list as to_list
from ._update_python_class_attr import _update_python_class_attr as update_class
from ._dynamical_import_of_function_from_string import _dynamical_import_of_function_from_string as func_from_str
from ._rounding import _floor as floor
from ._rounding import _ceil as ceil
from ._current_time import _current_time as time
from ._GIF import _GIF as GIF
from ._GIF import _make_GIF as make_GIF
from ._min_max_normalize import _min_max_normalize as min_max_normalize
from ._filter_overlapping import _filter_overlapping as unique
from ._find_overlapping import _find_overlapping as overlap