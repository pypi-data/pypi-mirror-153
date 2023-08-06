def read_query(query_path):
    """Read SQL query from specified path

    Args:
        path (str): Path to file containing query

    Returns:
        str: Contents of query from file
    """
    with open(query_path, 'r') as f:
        query = f.read()
    return query