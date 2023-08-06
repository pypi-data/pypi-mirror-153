from airflow_commons.logger import LOGGER

from airflow_commons.internal.util.file_utils import read_sql

from airflow_commons.internal.mysql.auth import get_session
from airflow_commons.internal.mysql.core import upsert
from airflow_commons.internal.mysql.core import update as update_util
from airflow_commons.internal.mysql.query_utils import get_delete_sql
from airflow_commons.internal.mysql.query_utils import get_select_all_sql
from airflow_commons.internal.mysql.query_utils import get_select_sql
from airflow_commons.internal.mysql.query_utils import get_row_count_sql
import pandas as pd


def write_to_mysql(
    username: str,
    password: str,
    host: str,
    db_name: str,
    values: dict,
    chunk_size: int,
    table_name: str,
):
    """

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param values: values to write into database
    :param chunk_size: data size to upload at a time
    :param table_name: database table name to write
    :return:
    """
    Session = get_session(username, password, host, db_name)
    chunks = [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]
    LOGGER.info(f"Chunk size is {chunk_size}.")
    with Session.begin() as session:
        i = 0
        for chunk in chunks:
            i += 1
            upsert(values=chunk, session=session, table_name=table_name)
            LOGGER.info(f"Chunk {i} uploaded")
    LOGGER.info("Data uploaded to MySql.")


def delete(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str,
    where_statement_params: dict = None,
):
    """
    Runs a delete query on given table, and removes rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: table name
    :param where_statement_file: relative location of where statement sql file
    :param where_statement_params: parameters of where statements
    """
    Session = get_session(username, password, host, db_name)

    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_delete_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    with Session.begin() as session:
        session.execute(sql)
        LOGGER.info(f"The below sql statement is executed \n {sql}")


def select_all(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str,
    where_statement_params: dict = None,
    return_type: str = "resultProxy",
):
    """
    Runs a select query on given table and returns the rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: database table name
    :param where_statement_params: relative location of where statement sql file
    :param where_statement_file: parameters of where statements
    :param return_type: parameter which determines return type
    :return: iterable ResultProxy object that stores results of the select query
    """
    Session = get_session(username, password, host, db_name)
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_select_all_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    with Session.begin() as session:
        if return_type == "dataframe":
            result = session.execute(sql).fetchall()
        else:
            result = pd.read_sql(sql, session.bind)
    LOGGER.info(f"The below sql statement is executed \n {sql}")
    LOGGER.info(f"Number of records retrieved = {str(len(result))}")
    return result


def select(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    column_names: list,
    where_statement_file: str,
    where_statement_params: dict = None,
    return_type: str = "resultProxy",
):
    """
    Runs a select query on given table and returns the rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: database table name
    :param column_names: column name from the table
    :param where_statement_params: relative location of where statement sql file
    :param where_statement_file: parameters of where statements
    :param return_type: parameter which determines return type
    :return: iterable ResultProxy object that stores results of the select query
    """
    Session = get_session(username, password, host, db_name)
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_select_sql(
        table_name=table_name,
        column_names=column_names,
        where_statement=where_statement,
    )
    with Session.begin() as session:
        if return_type == "dataframe":
            result = session.execute(sql).fetchall()
        else:
            result = pd.read_sql(sql, session.bind)

    LOGGER.info(f"The below sql statement is executed \n {sql}")
    LOGGER.info(f"Number of records retrieved = {str(len(result))}")
    return result


def get_row_count(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str = None,
    where_statement_params: dict = None,
):
    Session = get_session(username, password, host, db_name)

    if where_statement_file is not None:
        if where_statement_params is None:
            where_statement_params = dict()
        where_statement = read_sql(
            sql_file=where_statement_file, **where_statement_params
        )
    else:
        where_statement = ""

    sql = get_row_count_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    with Session.begin() as session:
        LOGGER.info(f"The below sql statement will be executed: \n {sql}")
        cursor = session.execute(sql)
        row_count = cursor.fetchone()[0]
        LOGGER.info("The sql statement is executed successfully\n")
    return row_count


def update(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    values: list,
):
    """
    Runs a update query on given table, and updates row columns that conform where condition if given

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: database table name to write
    :param values: list of values as dictionary with the optional where statetment as a text
    exp: [{"values": [{"column": "column_name", "value": value_to_be_updated}],
         "where": "id = 1234"}]
    """
    session = get_session(username, password, host, db_name)
    update_util(table_name, values, session)

    LOGGER.info("Data updated on MySql.")
