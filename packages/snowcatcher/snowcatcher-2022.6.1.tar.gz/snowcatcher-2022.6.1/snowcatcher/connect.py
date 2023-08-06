import os
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import yaml
import snowflake.connector as sfc

def connect(config_dict = None, config_path = None, secret_sa_username = None, secret_sa_password = None, sso_username = None, account = None, role = None, warehouse = None):
    """
    Create connection to snowflake per configuration. This function uses
    service account credentials defined by environment variables if available,
    otherwise it defaults to using SSO authentication. This function also sets
    the default warehouse/role that are to be used for queries made by this
    connection.

    Args:
        config_dict (dict, optional): dictionary with connection parameters as keys. Defaults to None.
        config_path (str, optional): path to a config.yaml file which has the connection parameters. Defaults to None.
        secret_sa_username (str, optional): service account username secret. Defaults to None.
        secret_sa_password (str, optional): service account password secret. Defaults to None.
        sso_username (str, optional): user's snowflake login username. Defaults to None.
        account (str, optional): snowflake account to be accessed. Defaults to None.
        role (str, optional): snowflake account role to be used. Defaults to None.
        warehouse (str, optional): snowflake warehouse to be used. Defaults to None.

    Returns:
        snowflake.connector.Connection: Snowflake connection object
    """    

    if config_dict is not None:
        for key, value in config_dict.items():
            key = key.strip()
            key = key.lower()
            if key == 'secret_sa_username':
                secret_sa_username = value
            elif key == 'secret_sa_password':
                secret_sa_password = value
            elif key == 'sso_username':
                sso_username = value
            elif key == 'account':
                account = value
            elif key == 'role':
                role = value
            elif key == 'warehouse':
                warehouse = value
        # set config_path to None as config_dict takes priority if both provided
        config_path = None
    
    if config_path is not None:
        #! Config file must be in the following format:
        """ 
        snowflake:
            account: X
            role: Y 
            warehouse: Z
            sa:
                username: T
                password: J
            sso:
                username: Q
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        # Parse config file, only take what is needed
        config = config['snowflake']

        secret_sa_username = config['sa']['username']
        secret_sa_password = config['sa']['password']
        sso_username = config['sso']['username']
        account = config['account']
        role = config['role']
        warehouse = config['warehouse']

    try:
        if secret_sa_username is None or secret_sa_password is None:
            raise KeyError('Secrets not provided')
        username = os.environ[secret_sa_username]
        password = os.environ[secret_sa_password]
        #* switched to sqlalchemy
        #con = __connect_sa(username, password, account)
        engine = create_engine(URL(
                account = account,
                user = username,
                password = password,
                warehouse = warehouse,
                role = role,
                ))
        con = engine.connect()
    except KeyError as e:
        #* Note sso generates a pandas warning
        # TODO Fix this. 
        username = sso_username
        con = __connect_sso(username, account)
        con = __set_role(con, role)
        con = __set_warehouse(con, warehouse)
        print('here')

    return con

def __connect_sa(user, password, account):
    """Create connection to snowflake with specified credentials

    Args:
        user (str): Snowflake account username
        password (str): Snowflake account password
        account (str): Snowflake account organization name

    Returns:
        snowflake.connector.Connection: Snowflake connection object
    """

    con = sfc.connect(
        user=user,
        password=password,
        account=account
    )
    return con

def __connect_sso(user, account):
    """Create snowflake connection via single-sign-on authentication

    Args:
        user (str): Snowflake account username (paccar email)
        account (str): Snowflake account organization name

    Returns:
        snowflake.connector.Connection: Snowflake connection object
    """
    con = sfc.connect(
        user=user,
        password='',
        account=account,
        authenticator='externalbrowser'
    )
    return con


def __set_role(con, role):
    """Set default role for Snowflake connection

    Args:
        con (snowflake.connector.Connection): Snowflake connection object
        role (str): Snowflake role

    Returns:
        (snowflake.connector.Connection): Snowflake connection object
    """

    con.execute_string(f'USE ROLE {role};')
    return con



def __set_warehouse(con, warehouse):
    """Set default warehouse for Snowflake connection

    Args:
        con (snowflake.connector.Connection): Snowflake connection object
        warehouse (str): Snowflake warehouse

    Returns:
        (snowflake.connector.Connection): Snowflake connection object
    """

    con.execute_string(f'USE WAREHOUSE {warehouse};')
    return con
