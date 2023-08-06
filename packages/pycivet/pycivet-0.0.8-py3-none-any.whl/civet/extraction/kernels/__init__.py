from importlib.resources import files

_data = files(__package__) / 'data'
ngh_count_kernel = _data / 'ngh_count.kernel'

assert ngh_count_kernel.is_file()
