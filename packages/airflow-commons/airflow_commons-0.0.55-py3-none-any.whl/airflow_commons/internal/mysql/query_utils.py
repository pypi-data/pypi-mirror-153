from airflow_commons.internal.util.file_utils import read_sql
from airflow_commons.resources.mysql import DELETE_SQL_FILE
from airflow_commons.resources.mysql import SELECT_ALL_SQL_FILE
from airflow_commons.resources.mysql import SELECT_SQL_FILE
from airflow_commons.resources.mysql import GET_ROW_COUNT_SQL_FILE


def get_delete_sql(
    table_name: str,
    where_statement: str,
):
    """
    Returns a delete dml query

    :param table_name: table name
    :param where_statement: delete condition
    :return: sql statement as a string
    """
    return read_sql(
        sql_file=DELETE_SQL_FILE,
        table_name=table_name,
        where_statement=where_statement,
    )


def get_select_all_sql(
    table_name: str,
    where_statement: str,
):
    """
    Returns a select sql query

    :param table_name: table name
    :param where_statement: select condition
    :return: sql statement as a string
    """
    return read_sql(
        sql_file=SELECT_ALL_SQL_FILE,
        table_name=table_name,
        where_statement=where_statement,
    )


def get_select_sql(
    table_name: str,
    column_names: list,
    where_statement: str,
):
    """
    Returns a select sql query

    :param table_name: table name
    :param column_names: column name
    :param where_statement: select condition
    :return: sql statement as a string
    """
    return read_sql(
        sql_file=SELECT_SQL_FILE,
        table_name=table_name,
        column_names=", ".join(column_names),
        where_statement=where_statement,
    )


def get_row_count_sql(
    table_name: str,
    where_statement: str,
):
    """
    Returns a row count sql query

    :param table_name: table name
    :param where_statement: select condition
    :return: sql statement as a string
    """

    where_clause = ""
    if len(where_statement):
        where_clause = "WHERE"

    return read_sql(
        sql_file=GET_ROW_COUNT_SQL_FILE,
        table_name=table_name,
        where_clause=where_clause,
        where_statement=where_statement,
    )
