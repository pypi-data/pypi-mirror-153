def get_reduce_memory(dataset, verbose=True):
    """This method is for reduce memory dataframe

    :param dataset: Dataframe
    :param verbose: Boolean
    :return: Dataframe
    """

    import numpy as np
    import pandas as pd

    ds_tmp = dataset.copy()
    start_mem = ds_tmp.memory_usage().sum() / 1024 ** 2
    int_columns = ds_tmp.select_dtypes(include=[np.int8, np.int16, np.int32, np.int64]).columns.tolist()
    for col in int_columns:
        ds_tmp[col] = pd.to_numeric(arg=ds_tmp[col], downcast='integer')

    float_columns = ds_tmp.select_dtypes(include=[np.float32, np.float64]).columns.tolist()
    for col in float_columns:
        ds_tmp[col] = pd.to_numeric(arg=ds_tmp[col], downcast='float')

    end_mem = ds_tmp.memory_usage().sum() / 1024 ** 2
    ds_tmp = ds_tmp.replace([np.inf, -np.inf], np.nan)
    if verbose:
        print(f'Memory usage after optimization is: {end_mem:.2f} MB')
        print(f'Decreased by {100 * (start_mem - end_mem) / start_mem:.2f}%')
    del dataset
    return ds_tmp
