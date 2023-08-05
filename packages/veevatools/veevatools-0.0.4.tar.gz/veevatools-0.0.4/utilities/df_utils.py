import pandas as pd
from collections import OrderedDict
from typing import Union, Iterable


def unpack_column(result: pd.DataFrame, column: str='errors'):
    return pd.concat([result, result[column].apply(lambda row: pd.Series(row[0]) if len(row) >0 else pd.Series(dtype='int64')).fillna("")], axis=1).drop(columns=[column])

def metadata_parse(metadata_value: Union[pd.DataFrame, Iterable, OrderedDict, bool, list, int, None]) -> Union[Iterable, OrderedDict, dict, bool, list, int, None]:
    """
    Function recursively traverses down a set of nested DataFrame, Dict, List, Ordered Dict iterables until
    it reaches a str, bool, empty list, or None value to return a dict comprising of the original hierarchical data.
    """
    if type(metadata_value) == str:
        return metadata_value
    elif type(metadata_value) == bool:
        return metadata_value
    elif metadata_value is None:
        return None
    elif type(metadata_value) == int:
        return metadata_value
    elif type(metadata_value) == list:
        if len(metadata_value) == 0:
            return []
        else:
            working_list = []
            for item in metadata_value:
                working_list.append(metadata_parse(item))
            return working_list
    elif type(metadata_value) == OrderedDict:
        working_dict = {}
        for key in metadata_value.keys():
            working_dict[key] = metadata_parse(metadata_value[key])
        return working_dict
    elif type(metadata_value) == pd.DataFrame:
        working_df_dict = {}
        for column in metadata_value.columns:
            if len(metadata_value[column]) == 0:
                working_df_dict[column] = None
            elif len(metadata_value[column]) > 1:
                for item in metadata_value[column]:
                    working_df_dict[column] = metadata_parse(item)
            elif len(metadata_value[column]) == 1:
                working_df_dict[column] = metadata_parse(metadata_value[column][0])
        return working_df_dict
