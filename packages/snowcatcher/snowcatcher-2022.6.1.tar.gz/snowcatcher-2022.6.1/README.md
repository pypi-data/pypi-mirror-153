# snowcatcher
snowcatcher package
pip install snowcatcher
https://pypi.org/project/snowcatcher/
## Purpose
The snowcatcher package can setup up a snowflake connection and execute a sql query to return a pandas df. 

The snowflake connection is setup via a Service Account (SA) login, or via Single sign-on (SSO) web browser authentication. 

The SA login uses secrets and can be utilized on cloud computing systems, while the SSO login requires local web browser authentication and can only be used locally. SA login can also be used for local development by placing the secrets in the .bashrc file (if using WSL, or a linux environment). 
## Directory Structure

```markdown
├── .gitignore
├── .gitattributes
├── README.md
├── LICENSE
│
├── setup.py                    # snowcatcher package setup file
│
├── snowcatcher
│   ├── connect.py              # sets up connection to snowflake, returns connection object
│   ├── read_query.py           # reads file path containing a sql query, returns query string
│   ├── execute_query.py        # executes query on snowflake, returns pandas data frame
│   └── connect_and_query.py    # single function combining all of the above
│
├── test                # directory for testing. contents are gitignored by default.
│   └── sample.py       # test file



## Documentation

## connect.py
sets up the snowflake connection; returns a connection object.

snowcatcher.connect(config_dict = None, config_path = None, secret_sa_username = None, secret_sa_password = None, sso_username = None, account = None, role = None, warehouse = None)

The snowflake connection can be setup via a config_dict, a config_path, or by providing each connection parameter (secret_sa_username , secret_sa_password , sso_username, account, role, warehouse) individually.

Parameters:
    - config_dict: dict
        connection parameters as keys (secret_sa_username , secret_sa_password , sso_username, account, role, warehouse) and their coresponding values as strings.

        config_dict_example = {'secret_sa_username' : '', 'secret_sa_password' : '', 'sso_username' : '', 'account' : '', 'role' : '', 'warehouse' : ''}

    - config_path: str
        the config path points towards a config.yaml file which contains connection parameters. 

        Note: The config file must be a .yaml file and of the format

        snowflake:
            account: X
            role: Y 
            warehouse: Z
            sa:
                username: T
                password: J
            sso:
                username: Q

    - secret_sa_username: str
        service account username secret

    - secret_sa_password: str
        service account password secret

    - sso_username: str
        user's snowflake login username

    - account: str
        snowflake account to be accessed

    - role: str
        snowflake account role to be used

    - warehouse: str
        snowflake warehouse to be used

Note: If multiple conflicting inputs are provided the use hierarchy is config_dict > config_path > individual parameters

## read_query.py
Reads a sql query from the specified path; returns a string with the query.

snowcatcher.read_query(query_path)

Note: the sql query must end in a ';'

## execute_query.py
Executes a sql query on snowflake; returns a pandas data frame of the query results.

snowcatcher.execute_query(con, query = None, query_path = None)

execute_query can take in an sql query string, or a path string to the query. 

If the path to the query is provided read_query is called to read the query. 

Note: if both a query and a query_path are provided the query will take priority


## connect_and_query.py
Connects to snowflake and executes an sql query; returns a pandas data frame of the query results.

snowcatcher.connect_and_query(config_dict = None, config_path = None, secret_sa_username = None, secret_sa_password = None, sso_username = None, account = None, role = None, warehouse = None, query = None, query_path = None)

connect_and_query utilizes snowcatcher.connect and snowcatcher.execute_query, see those funcitons for input discussion.










<p align="center">
    <img width="248" height="250" src="https://pre00.deviantart.net/4619/th/pre/f/2012/045/2/e/2ecf95c43defd7b12976da54743a4e6d-d4prbsn.png" alt="snowcatcher">
</p>
