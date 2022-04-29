"""
Read tabular data from disk. A single table can naturally represent examples
with many features along a single dimension as rows. Examples can be labeled as
belonging to distinct domains, subjects, and categories with additional columns.
"""

import numpy as np
import pandas as pd


class UnbalancedDesignError(Exception):
    def __init__(self, value_counts_dict: dict):
        info_string = " ".join([f"{k}: {v}" for k, v in value_counts_dict.items()])
        super().__init__(f"Data is not balanced across domains, subjects, and categories.\n{info_string}")


def read_csv_tabular(csv_path: str, index_col: list) -> np.array:
    """Read numeric data from comma separated text.

    Args:
        csv_path (str): Path to comma separated text file, with one row per example.
        index_col (list): Columns that should be treated as levels of a Pandas
            Dataframe MultiIndex. There should be an level for each subject,
            domain, and example (in that order).

    Returns:
        [array-like]: [description]
    """
    dataframe = pd.read_csv(csv_path, index_col=index_col)
    dataframe.sort_index(level=index_col, inplace=True)
    value_counts_by_level = [dataframe.index.get_level_values(level).nunique() for level in index_col]

    if not all(value_counts_by_level[0] == x for x in value_counts_by_level):
        value_counts_dict = {k: v for k, v in zip(index_col, value_counts_by_level)}
        raise UnbalancedDesignError(value_counts_dict)

    # The values from the table are reshaped into an an array because other
    # functions within PyKale know how to accept this kind of input. Ultimately,
    # it will be better to handle tablular data directly and prehaps allow
    # imbalanced designs.
    nfeatures = dataframe.shape[1]
    dims = value_counts_by_level + [nfeatures]
    images = np.reshape(dataframe.to_numpy(), dims)

    return images
