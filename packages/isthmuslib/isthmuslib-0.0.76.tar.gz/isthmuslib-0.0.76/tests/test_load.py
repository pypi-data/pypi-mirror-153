import isthmuslib as isli
import pathlib

timeseries: isli.VectorSequence = isli.VectorSequence().read_csv(
    pathlib.Path.cwd() / '..'/'data' / 'version_controlled' / 'example_vector_sequence_data.csv', inplace=False,
    basis_col_name='timestamp', name_root='Experiment gamma', disable_auto_conversion_to_numeric=True)