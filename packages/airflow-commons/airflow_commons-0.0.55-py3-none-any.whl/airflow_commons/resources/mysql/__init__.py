import os

here = os.path.abspath(os.path.dirname(__file__))

DELETE_SQL_FILE = os.path.join(here, "queries/delete.sql")

SELECT_ALL_SQL_FILE = os.path.join(here, "queries/select_all.sql")

SELECT_SQL_FILE = os.path.join(here, "queries/select.sql")

GET_ROW_COUNT_SQL_FILE = os.path.join(here, "queries/get_row_count.sql")
