from looqbox.global_calling import GlobalCalling
from looqbox.objects.looq_table import ObjTable
from looqbox.utils.utils import base64_decode
from looqbox.database.database_exceptions import TimeOutException, alarm_handler
import pandas as pd
import jaydebeapi
import datetime
import signal
import json
import os
import re

__all__ = ["sql_in", "sql_close", "connect", "sql_execute", "sql_between"]

# The _set_connection_alias and _get_connection_alias function are used to save the
# connection alias in the log_query to improve readability. This change prevent log_query from
# save a jaydebeapi.Connection object as connection name, thus raise query trace difficulty
connection_alias = ""


def _set_connection_alias(connection: str) -> None:
    global connection_alias
    connection_alias = connection


def _get_connection_alias() -> str:
    global connection_alias
    return connection_alias


def connect(connection_name: list or str, parameter_as_json=False, use_all_jars=True) -> jaydebeapi.Connection:
    """
    Execute a connection in a database.

    :param connection_name: String or list of database names
    :param parameter_as_json: Set if the parameters will be in JSON format or not
    :param use_all_jars: If set as True, the connection will import all available jars, allowing connection with
                         different database within the same JVM.
                         If this flag is set as False only the connection required jar will be loaded, thus the
                         connection is going to become prone to error, in case another database technology
                         (e.g. another driver, use another version for the same driver) is used, the Looqbox Kernel
                         will crash due the lack of the correct jar(s) file(s).
                         Therefore, setting use_all_jars as False is recommended for tests purpose or for an advanced
                         user.
    :return: A Connection object
    """
    if isinstance(connection_name, str):
        connection_list = [connection_name]
    else:
        connection_list = connection_name

    _set_connection_alias(connection_name)

    connection_credential = _get_connection_credentials(connection_list, parameter_as_json)

    # build driver_args to enable connections that rather use or not user and password
    if _is_user_and_password_empty(connection_credential):
        driver_args = {}
    else:
        driver_args = {
            'user': connection_credential['user'],
            'password': base64_decode(connection_credential['pass'])
        }

    # Since jaydebeapi instantiate a JVM to perform the db connection, any kind of alteration (jar/drive insertion or
    # removing) are impossible, thus being essential to shut down the current JVM (create an error in Looqbox Kernel)
    # in this regard, all jars are imported into the JVM by default

    jars_path = _get_all_jar_files() if use_all_jars else connection_credential["jar"]

    conn = jaydebeapi.connect(
        connection_credential['driver'],
        connection_credential['connString'],
        driver_args,
        jars=jars_path,
    )

    return conn


def _is_user_and_password_empty(connection_credential: dict) -> bool:
    return connection_credential['user'] == '' and connection_credential['pass'] == ''


def sql_execute(connection, query, replace_parameters=None, close_connection=True, show_query=False,
                null_as=None, add_quotes=False):
    """
    Function to execute a query inside the connection informed. The result of the query will be
    transformed into a ObjTable to be used inside the response.


    :param connection: Connection name or object
    :param query: sql script to query result set
    :param replace_parameters: List of parameters to be used in the query. These parameters will replace the numbers
    wit h `` in the query.
        Example:
            replace_parameters = [par1, par2, par3, par4]
            query = "select * from bd where par1=`1` and par2=`2` and par3=`3` and par4=`4`

            In this case the values of `1`, `2`, `3`, `4` will be replaced by par1, par2, par3, par4 respectively (using
            the order of the list in replace_parameters).

    :param close_connection: Define if automatically closes the connection
    :param show_query: Print the query in the console
    :param null_as: Default value to fill null values in the result set
    :param add_quotes: Involves replaced parameters with quotes
    Example:
        replace_parameters = [par1]
            query = "select * from db where par1=`1`"
        For add_quotes = True
            query = "select * from db where par1='par1'"
        For add_quotes = False
            query = "select * from db where par1=par1"
    :return: A Looqbox ObjTable with the data retrieved from the query
    """

    if replace_parameters is not None:
        query = _sql_replace_parameters(query, replace_parameters, add_quotes)

    test_mode = GlobalCalling.looq.test_mode

    if show_query and test_mode:
        print(query)

    query_dataframe = ObjTable(null_as=null_as)

    sql_timeout = 0 if test_mode else _get_script_timeout()

    # Configure timeout features
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(sql_timeout)

    start_time = datetime.datetime.now()

    try:
        query_dataframe.data, query_dataframe.metadata = _get_query_result(connection, query, close_connection)
        total_sql_time = datetime.datetime.now() - start_time

    except jaydebeapi.DatabaseError as e:
        sql_close(connection)
        total_sql_time = datetime.datetime.now() - start_time

        GlobalCalling.log_query({"connection": str(_get_connection_alias()), "query": query,
                                 "time": str(total_sql_time), "success": False})

        print(str(e), "java.sql.SQLException: expected")

    except TimeOutException as ex:
        sql_close(connection)
        total_sql_time = datetime.datetime.now() - start_time

        GlobalCalling.log_query({"connection": str(_get_connection_alias()), "query": query,
                                 "time": str(total_sql_time), "success": False})

    finally:
        signal.alarm(0)
        if not test_mode:
            _update_sql_timeout(total_sql_time)

    GlobalCalling.log_query({"connection": str(_get_connection_alias()), "query": query,
                             "time": str(total_sql_time), "success": True})

    df_cols_and_rows = query_dataframe.data.shape
    query_dataframe.rows = df_cols_and_rows[0]
    query_dataframe.cols = df_cols_and_rows[1]

    if test_mode:
        total_sql_time = datetime.datetime.now() - start_time
        print("SQL fetch in...", total_sql_time.total_seconds(), "secs")

    if close_connection:
        sql_close(connection)

    return query_dataframe


def _get_query_result(connection, query, close_connection):
    """
    Function to get the table resulting from the query

    :param connection: Connection name or class
    :param query: Query to get the table
    :param close_connection: Define if automatically closes the connection
    :return: Return the data frame resulting from the query.
    """

    try:
        if isinstance(connection, str):
            connection = connect(connection)

        conn_curs = connection.cursor()

    except:
        if close_connection and not isinstance(connection, str):
            conn_curs.close()
            sql_close(conn_curs)

        raise Exception("Error to connect in database.")

    try:
        conn_curs.execute(query)
        col_names = [i[0] for i in conn_curs.description]
        fetch_tuple = conn_curs.fetchall()

        metadata = get_column_types(conn_curs)

        # Fix error when fetch brings one None row
        query_df = pd.DataFrame()
        if fetch_tuple or len(fetch_tuple) > 0:
            if len(fetch_tuple[0]) == 1:
                if fetch_tuple[0][0] is not None:
                    query_df = pd.DataFrame(fetch_tuple, columns=col_names)
            else:
                query_df = pd.DataFrame(fetch_tuple, columns=col_names)

        sql_close(conn_curs)

        return query_df, metadata
    except:
        if close_connection and not isinstance(connection, str):
            conn_curs.close()
            sql_close(conn_curs)

        raise Exception("Error to execute query.")


def get_column_types(cursor):
    metadata = dict()
    for column in cursor.description:
        column_name = column[0]
        column_type = filter_types(column[1].values)
        metadata[column_name] = {
            "type": column_type
        }
    return metadata


def filter_types(type_list):
    type_dict = {
        'CHAR': ('CHAR', 'NCHAR', 'NVARCHAR', 'VARCHAR', 'OTHER'),
        'LONGVARCHAR': ('CLOB', 'LONGVARCHAR', 'LONGNVARCHAR', 'NCLOB', 'SQLXML'),
        'BINARY': ('BINARY', 'BLOB', 'LONGVARBINARY', 'VARBINARY'),
        'INTEGER': ('BOOLEAN', 'BIGINT', 'BIT', 'INTEGER', 'SMALLINT', 'TINYINT'),
        'FLOAT': ('FLOAT', 'REAL', 'DOUBLE'),
        'NUMERIC': ('DECIMAL', 'NUMERIC'),
        'DATE': ('DATE',),
        'TIME': ('TIME',),
        'TIMESTAMP': ('TIMESTAMP',),
        'ROWID': ('ROWID',)
    }
    column_type = None
    for db_type, aliases in type_dict.items():
        if type_list == aliases:
            column_type = db_type
    return column_type


def _sql_replace_parameters(query, replace_parameters, replace_with_quotes=False):
    """
    This function get the query and replace all the values between backticks to the values in the replace_parameters
    list, the values are substituted using the order in replace parameters, for example, the `1` in the query will be
    substituted by the value replace_parameters[0] and so goes on.
    Example:
        query = "select * from database where x = `1` and z = `3` and y = `2`"
        replace_parameters = [30, 50, 60}

        returns = "select * from database where x = 30 and z = 60 and y = 50"

    :param query: Query to be changed
    :param replace_parameters: List that contains the values to be substitute
    :param replace_with_quotes=False: Involves replaced parameters with quotes
    :return: Query with the values changed
    """
    separator = '"' if replace_with_quotes else ""

    for replace in range(len(replace_parameters)):
        query = query.replace('`' + str((replace + 1)) + '`', separator + str(replace_parameters[replace]) + separator)
    print(query)
    return query


def sql_in(query=None, values_list=None):
    """
    Transform the list in values_list to be used inside a IN statement of the SQL.
    Example:
        values_list = [1,2,3,4,5]
        query = 'select * from database where' + sql_in(" col in", values_list)

        "select * from database where col in (1, 2, 3, 4, 5)"


    :param query: Query header with the first part of the query
    :param values_list: list to be transformed as a IN format
    :return: query concatenated with values_list as a IN format
    """
    if values_list is None:
        return ""

    if not isinstance(values_list, list):
        values_list = [values_list]

    separated_list = str(values_list).replace('[', '(').replace(']', ')')

    if query is None:
        return separated_list
    else:
        return query + " " + separated_list


def sql_between(query=None, values_list=None):
    """
    Transform the list in values_list to be used as a between statement of the SQL.
    Example:
        values_list = ['2018-01-01', '2018-02-02']
        query = 'select * from database where sql_between(' date', date_int)'

        "select * from database where date between '2018-01-01' and '2018-02-02')"


    :param query: Query header with the first part of the query
    :param values_list: list to be used in a between statement
    :return: query concatenated with values_list as a between statement
    """
    if values_list is None:
        return ""

    if len(values_list) != 2:
        raise Exception("To use sql_between values_list must be of two positions")

    if not isinstance(values_list, list):
        values_list = [values_list]

    if isinstance(values_list[0], int) or isinstance(values_list[1], int):
        between_query = query + " between " + str(values_list[0]) + " and " + str(values_list[1])
    else:
        between_query = query + " between '" + values_list[0] + "' and '" + values_list[1] + "'"

    return between_query


def sql_close(conn):
    """
    Close a connection
    :param conn: Connection of the type JayBeDeApi
    """

    if isinstance(conn, jaydebeapi.Cursor):
        conn.close()


def reload_database_connection(conn_file_path=GlobalCalling.looq.connection_file):
    if os.path.isfile(conn_file_path):
        GlobalCalling.looq.connection_config = json.loads(conn_file_path)
    else:
        print("Missing connection file: " + GlobalCalling.looq.connection_file)
        GlobalCalling.looq.connection_config = None


def _update_sql_timeout(time_used: float = 0):
    """
    Subtract the amount of time used in script timeout
    """
    GlobalCalling.looq.response_timeout -= int(round(time_used.total_seconds(), 0))
    return None


def _get_script_timeout() -> float:
    """
    Retrieve the remaining script run time
    """
    # Starts script timeout counting
    return GlobalCalling.looq.response_timeout


def _get_all_jar_files() -> list:
    """
    Get and append all jar files required for each entry in connection.json
    """

    jar_list = list()
    file_connections = _get_connection_file()

    # get the jar files for each connection
    for connections in file_connections:

        # Avoid errors due some wrong connection register
        try:
            connection_jar = _get_connection_credentials([connections])["jar"]
        except:
            connection_jar = []

        jar_list.extend(connection_jar)
    return jar_list


def _is_jar(file: str) -> bool:
    return not file.startswith('.') and '.jar' in file


def _get_connection_file() -> dict:
    try:
        if isinstance(GlobalCalling.looq.connection_config, dict):
            file_connections = GlobalCalling.looq.connection_config
        else:
            file_connections = open(GlobalCalling.looq.connection_config)
            file_connections = json.load(file_connections)
    except FileNotFoundError:
        raise Exception("File connections.json not found")
    return file_connections


def _get_connection_credentials(connection: list, parameter_as_json=False) -> dict:
    """
    Get credentials for a list of connections.

    :param connection: String or list of database names
    :param parameter_as_json: Set if the parameters will be in JSON format or not
    :return: A Connection object
    """

    driver_path = []
    connection_credential = _get_connection_file()
    for conn_name in connection:
        try:
            if not parameter_as_json:
                connection_credential = GlobalCalling.looq.connection_config[conn_name]
            else:
                connection_credential = connection_credential[conn_name]
        except KeyError:
            raise Exception("Connection " + conn_name + " not found in the file " + GlobalCalling.looq.connection_file)

        conn_file_name, conn_file_extension = os.path.splitext(connection_credential['driverFile'])

        old_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name + conn_file_extension)
        new_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name)

        if new_driver_folder_path:
            for file in os.listdir(new_driver_folder_path):
                if _is_jar(file):
                    driver_path.append(new_driver_folder_path + '/' + file)

        elif old_driver_folder_path:
            driver_path = old_driver_folder_path

        connection_credential["jar"] = driver_path
    return connection_credential
