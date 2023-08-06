import os

here = os.path.abspath(os.path.dirname(__file__))


ARCHIVE_DELETE_WHERE_STATEMENT_FILE = os.path.join(
    here, "archive/delete_where_statement.sql"
)
ARCHIVE_SOURCE_STATEMENT_FILE = os.path.join(here, "archive/source_statement.sql")
DEDUPLICATION_GET_AVAILABLE_PARTITIONS_FIELD_SQL_FILE = os.path.join(
    here, "deduplication/get_available_partitions_field.sql"
)
DEDUPLICATION_MERGE_KEYS_PARTITION_PRUNING_PARAMS = os.path.join(
    here, "deduplication/merge_keys_partition_pruning_params.sql"
)
DEDUPLICATION_SOURCE_STATEMENT_SQL_FILE = os.path.join(
    here, "deduplication/source_statement.sql"
)
DEDUPLICATION_SOURCE_WHERE_STATEMENT_SQL_FILE = os.path.join(
    here, "deduplication/source_where_statement.sql"
)
DEDUPLICATION_SOURCE_WHERE_STATEMENT_PARTITION_PRUNING_PARAMS_SQL_FILE = os.path.join(
    here, "deduplication/source_where_statement_partition_pruning_params.sql"
)
DELETE_SQL_FILE = os.path.join(here, "dml/delete.sql")
GET_COLUMN_NAMES_SQL_FILE = os.path.join(
    here, "information_schema/get_column_names.sql"
)
GET_PRIMITIVE_COLUMN_NAMES_SQL_FILE = os.path.join(
    here, "information_schema/get_primitive_column_names.sql"
)
GET_TABLE_NAMES_SQL_FILE = os.path.join(here, "information_schema/get_table_names.sql")
INSERT_SQL_FILE = os.path.join(here, "dml/insert.sql")
UPSERT_SQL_FILE = os.path.join(here, "dml/upsert.sql")
