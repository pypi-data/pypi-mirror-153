from snowcatcher.connect import connect
from snowcatcher.execute_query import execute_query

def connect_and_query(config_dict = None, config_path = None, secret_sa_username = None, secret_sa_password = None, sso_username = None, account = None, role = None, warehouse = None, query = None, query_path = None):
    """ Function which connects to snowfake and executes a query. The query 
    can be provied directly or via a path to the query string. This function
    returns a pandas dataframe 

    Args:
        see connect() and execute_query()

    Returns:
        pandas.dataframe: data frame of query execution.
    """
    con = connect(config_dict, config_path, secret_sa_username, secret_sa_password, sso_username, account, role, warehouse)
    df = execute_query(con, query, query_path)
    return df