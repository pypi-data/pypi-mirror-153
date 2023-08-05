import sqlalchemy
from airflow_commons.logger import LOGGER
from sqlalchemy import text, column
from sqlalchemy import update as sql_update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker


def get_table_metadata(table_name: str, engine_connection: sqlalchemy.engine.Engine):
    """
    Gets the metadata of given table
    :param table_name: table name to get metadata
    :param engine_connection: database engine connection
    :return: sqlalchemy table.
    """
    return sqlalchemy.Table(
        table_name,
        sqlalchemy.MetaData(),
        autoload=True,
        autoload_with=engine_connection,
    )


def upsert(values: dict, conn, table_name: str):
    """
    :param values: values to write into database
    :param conn: database engine connection
    :param table_name: database table name to write
    :return:
    """
    table_metadata = get_table_metadata(table_name=table_name, engine_connection=conn)
    update_cols = {}
    insert_statement = insert(table_metadata).values(values)
    for col in insert_statement.table.columns:
        col_name = col.name
        if col_name not in table_metadata.primary_key:
            update_cols.update({col_name: getattr(insert_statement.inserted, col_name)})
    upsert_statement = insert_statement.on_duplicate_key_update(**update_cols)
    try:
        conn.execute(upsert_statement)
    except Exception as e:
        LOGGER.error(f"An exception occurred while upsert: {e}")
        raise


def update(table_name: str, values: list, engine, conn):
    """
    :param table_name: database table name to write
    :param values: list of values as dictionary with the optional where statetment as a text
    :param engine: database engine
    :param conn: database engine connection
    """
    session = sessionmaker(bind=engine)
    session = session(bind=conn)

    table_metadata = get_table_metadata(table_name=table_name, engine_connection=conn)
    try:
        for statement in values:
            try:
                where_clause = text(statement["where"])
            except KeyError:
                where_clause = text("1=1")

            values_formatted = {}
            [
                values_formatted.update({column(item["column"]): item["value"]})
                for item in statement["values"]
            ]
            session.execute(
                sql_update(
                    table_metadata, values=values_formatted, whereclause=where_clause
                )
            )
        session.commit()

    except Exception as e:
        LOGGER.info(f"An exeption {e} occured, session rollbacked. Noting is changed.")
        session.rollback()
        raise e

    LOGGER.info("Row columns are updated successfully.")
