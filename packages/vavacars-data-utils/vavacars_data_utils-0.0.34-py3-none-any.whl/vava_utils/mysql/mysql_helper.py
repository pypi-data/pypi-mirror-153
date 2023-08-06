from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL
import subprocess
import pandas as pd


def _get_auth_token():
    cmd = "az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken"
    token = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE).stdout.decode("utf-8")
    return token


class MySQL_Helper:
    def __init__(self, host, user, port=3306, database=None, password=None):
        """
        MySQL helper constructor.

        Parameters:
            host: host to connect
            user: username to connect as
            port: TCP/IP port to connect to
            database: database name
        """
        self._engine = self._create_engine(host, user, port, database, password)

    def _create_engine(self, host, user, port, database, password=None):
        engine_url = URL.create(
            drivername="mysql+pymysql", host=host, username=user, database=database, password=password
        )
        engine = create_engine(engine_url, connect_args={"ssl": {"ssl_check_hostname": False}}, pool_pre_ping=True)

        if not password:

            @event.listens_for(engine, "do_connect")  # https://docs.sqlalchemy.org/en/14/core/engines.html
            def provide_token(dialect, conn_rec, cargs, cparams):
                cparams["password"] = _get_auth_token()

        return engine

    def from_table(self, table, **kwargs):
        """
        Given a table name, returns a Pandas DataFrame.

        Parameters:
            table (string): table name
            **kwargs: additional keyword parameters passed to pd.read_sql_table

        Returns:
            result (pd.DataFrame): SQL table in pandas dataframe format
        """
        return pd.read_sql_table(table, self._engine, **kwargs)

    def from_file(self, filename, query_args={}, limit=None, **kwargs):
        """
        Read SQL query from .sql file into a Pandas DataFrame.

        Parameters:
            filename (string): path to file containing the SQL query
            query_args (dict): query string is formatted with those params: string.format(**query_args)
                               example: {'max_date': '2020-01-01'}
            limit (int): maximum number of results
            **kwargs: additional keyword parameters passed to pd.read_sql_query

        Returns:
            result (pd.DataFrame): query results in  Pandas DataFrame format
        """
        if (limit is not None) and (not isinstance(limit, int)):
            raise ValueError("Limit must be of type int")

        with open(filename, "r") as f:
            query_unformated = f.read().rstrip()
        query = query_unformated.format(**query_args)
        query = query if not limit else query.replace(";", f" LIMIT {limit};")
        return self.from_query(query, **kwargs)

    def from_query(self, query, **kwargs):
        """
        Read SQL query into a Pandas DataFrame.

        Parameters:
            query (string): query string
            **kwargs: additional keyword parameters passed to pd.read_sql_query

        Returns:
            result (pd.DataFrame): query results in  Pandas DataFrame format
        """
        return pd.read_sql_query(query, self._engine, **kwargs)
