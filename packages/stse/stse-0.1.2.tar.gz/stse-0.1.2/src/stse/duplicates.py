import pandas as pd
import numpy as np


"""
    File name: duplicates.py
    Author: Jacob Gerlach
    Description: Assortment of pandas DataFrame operations for handling duplicates.
    Notes:
        * = Function has associated unit test.
"""

def filter(df, subsets, return_duplicates=False, how='all'):  # *
    """Filters duplicates to either return DataFrame subset of duplicates or non-duplicates.

    Args:
        df (pandas DataFrame): DataFrame to perform duplicate search on.
        subsets (list): List of column names to compare in duplicate search.
                        All must match to be considered a duplicate.
        return_duplicates (bool, optional): If True, returns non-duplicate df else returns duplicate df.
                                            Defaults to False.
        how (str): 

    Returns:
        pandas DataFrame: Filtered df.
    """
    if how == 'any' and len(subsets) > 1:
        # Checks for occurances in ANY column of 'subsets'
        index_arr = np.array([])
        for col in subsets:     
            index_arr = np.concatenate((index_arr, indices(df, col)))
        
        index_arr = np.unique(index_arr)
        
        return df.loc[df.index.isin(index_arr)] if return_duplicates else df.loc[~df.index.isin(index_arr)]
    
    elif how == 'all':
        # Duplicates in ALL columns of 'subsets' must agree
        duplicates = pd.DataFrame.duplicated(df, subset=subsets)
        
    else:
        # Raise error of how is not 'any' or 'all'
        raise ValueError('how argument must be either \'any\' or \'all\'')
    
    return df[duplicates] if return_duplicates else df[~duplicates]

def remove(df, subsets):  # *
    """Removes duplicates from df. Keeps first occurance in df.

    Args:
        df (pandas DataFrame): DataFrame to perform dupicate search on.
        subsets (list): List of column names to compare in duplicate search.
                        All must match to be considered a duplicate.

    Returns:
        pandas DataFrame: DataFrame with duplicates removed.
    """
    return filter(df, subsets=subsets)

def indices(df, column):  # *
    """Finds indices of rows in df column that hold duplicate values.

    :param df: Dataframe to perform duplicate search on
    :type df: pandas DataFrame
    :param column: Name of column in df
    :type column: str
    :return: Indices
    :rtype: list
    """
    return list(df[pd.DataFrame.duplicated(df, subset=[column])].index)

def average(df, subsets, average_by):  # *
    """Averages duplicates from df.

    Args:
        df (pandas DataFrame): DataFrame to perform duplicate search on.
        subsets (list): List of column names to compare in duplicate search. 
                        All must match to be considered a duplicate.
        average_by (str): Column name to average along.

    Returns:
        pandas DataFrame: DataFrame with duplicates averaged.
    """
    df_copy = df.copy()
    
    # Filter out duplicates for merge df
    out = filter(df_copy, subsets)
    orig_index = out.index
        
    # Ensure average_by exists in the dataframe
    if average_by not in df.columns:
        raise ValueError('average_by column not found in DataFrame')
    
    # Cast value column to float (for avg computation)
    try:
        df_copy[average_by] = df_copy[average_by].astype(float)
    except ValueError:
        raise ValueError('average_by column does not contain float castable values')
    
    # Group duplicate rows and aggregate by mean (adds mean to end of value column)
    avg_value = df_copy.groupby(by=subsets).agg({average_by: ['mean']})
    avg_value.columns = [col[0] for col in avg_value.columns.values]

    # Drop original value column ('value' --> 'valuemean')
    out = out.drop(columns=[average_by])  # drop original values

    # Add averaged values to dataframe and preserve original index
    out = pd.merge(out, avg_value, on=subsets).set_index(orig_index)
    out = out[df_copy.columns]
    
    return out
