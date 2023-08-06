import pandas as pd
from snowcatcher.read_query import read_query

def execute_query(con, query = None, query_path = None):
    """Execute snowflake SQL statement and retreive results as pandas dataframe

    Args:
        con (snowflake.connector.Connection): Snowflake connection object
    Optional 1 of 2 arguments needed
        query (str): SQL statement to be executed
        path (str): Path to file containing query 

    Returns:
        pandas.DataFrame: Pandas DataFrame containing query results
    """
    if query is None and query_path is None:
        raise TypeError('query or query_path required. No query or query_path string provided')
    
    if query is not None:
        df = pd.read_sql_query(query, con)
        return df
    
    query = read_query(query_path)
    df = pd.read_sql_query(query, con)
    return df