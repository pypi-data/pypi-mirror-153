# https://github.com/pandas-profiling/pandas-profiling/blob/develop/src/pandas_profiling/controller/pandas_decorator.py
# https://github.com/scls19fr/pandas-helper-calc/blob/master/pandas_helper_calc/__init__.py
"""This file add the decorator on the DataFrame object."""

from collections.abc import Iterable
from typing import Union, Dict

from pandas import DataFrame
from MySQLdb import MySQLError

from banner.connection import RelationalConnection, Storage
from banner.queries import Queries

from banner.utils.web2py import JOINS, COLUMN_TO_LABEL
from banner.utils.pandas import assert_required_columns
from banner.utils.neware import (
    calculate_current, calculate_dqdv, calculate_neware_columns, 
    calculate_neware_timestamp, calculate_temperature, 
    calculate_voltage, group_by_auxchl, calculate_capacity, IS_CALCULATED_NEWARE_DF
)


def __split(df: DataFrame, size=100000):
    '''
        Split DataFrame into chunk_size list of DataFrames
    '''    
    return [df[i*size:(i+1)*size] for i in range(len(df) // size + 1)]

def __slope(df: DataFrame, x:str, y:str):
    '''
        Calculate Delta Y / Delta X
    '''
    return df[y].diff() / df[x].diff()
    
DataFrame.split = __split
DataFrame.slope = __slope

# Neware functions
DataFrame.calculate_current = calculate_current
DataFrame.calculate_neware_timestamp = calculate_neware_timestamp
DataFrame.calculate_temperature = calculate_temperature
DataFrame.calculate_voltage = calculate_voltage
DataFrame.calculate_neware_columns = calculate_neware_columns
DataFrame.calculate_dq_dv = calculate_dqdv
DataFrame.group_by_auxchl = group_by_auxchl
DataFrame.calculate_capacity = calculate_capacity
DataFrame.IS_CALCULATED_NEWARE_DF = IS_CALCULATED_NEWARE_DF


# Wrapper around Queries.table_query
def __join_table(
    df: DataFrame, table: str, columns: Union[list, str] = '*', condition: str = 'TRUE',
    left: Union[str, list, None] = None, right: Union[str, list, None] = None, how: Union[str, None] = None,
    connection: Union[RelationalConnection, str] = None, 
    raw: bool = False, cache: Storage=None, ttl: Union[bool, None] = None
):  
    _df = df.copy()
    
    try:
        assert(isinstance(df._tables, list)) # Is a list
        assert(df._tables) # Is not empty
 
    except (AssertionError, AttributeError):
        raise TypeError('DataFrame Does not represent a StoreDot Table')
    
    if len(df._tables) == 1: #First Join
        _df.columns = [f'{df._tables[0]}.{column}' for column in _df.columns] # Prefix columns

    for df_table in df._tables: # Iterate available tables
        join_params = JOINS.get(df_table, dict()).get(table, dict())

        how = how if how else join_params.get('how')
        left = left if left else join_params.get('left')
        right = right if right else join_params.get('right')
        
        if not all([left, right, how]):
            continue
        
        if not isinstance(left, list):
            left = [left]
    
        if not isinstance(right, list):
            right = [right]
        
        left = [
            f'{df_table}.{column}' if f'{df_table}.{column}' in _df else f'{df_table}.{COLUMN_TO_LABEL.get(column)}'
            for column in left
        ] #Add table prefix

        try:
            _keys_df = _df[left].dropna() # Keys cannot contain NA values
            
            _join_values = [f"({','.join([str(value) for value in values])})" for values in zip(*[_keys_df[column].values for column in left])] # List of tuples(str) for each entry
            _join_condition = f"({','.join(right)}) IN ({','.join(_join_values)})" # Mysql Condition(Where)
            
            table_df = Queries.table_query(
                table, columns=columns, condition=f'{_join_condition} AND {condition}',
                raw=raw, connection=connection, cache=cache, ttl=ttl
            )
            
            table_df.columns = [f'{table}.{column}' for column in table_df.columns] # Prefix columns
            
            right = [
                f'{table}.{column}' if f'{table}.{column}' in table_df else f'{table}.{COLUMN_TO_LABEL.get(column)}'
                for column in right
            ] #Add table prefix
            
            tables = df._tables + [table]
            
            for left_column, right_column in zip(left, right):
                table_df[right_column] = table_df[right_column].astype(_df[left_column].dtype) # Make sure right_column has same data type as left_column
              
            _df = _df.merge(
                table_df, how='inner', 
                left_on=left, right_on=right,
                # suffixes=(f'_{df_table}', f'_{table}')
            )
            
            _df._tables = tables # Set Current Tables
            
            return _df

        except (KeyError, MySQLError):
            continue
        
    raise TypeError(f'Failed to join {table} With {df._tables}')


# Queries
DataFrame.join_table = __join_table
DataFrame.table_query = Queries.table_query
