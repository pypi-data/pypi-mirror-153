from google.cloud import bigquery


MEGABYTES_BILLED_DENOMINATOR = 2**20
AVAILABLE_COLUMN_NAMES = ["column_name", "table_name"]
SELECT_RETURN_TYPES = ["dict", "json", "dataframe", "pyarrow"]
PRIMITIVE_DATA_TYPES = [
    "BOOL",
    "BYTES",
    "STRING",
    "DATE",
    "DATETIME",
    "TIME",
    "TIMESTAMP",
    "INT64",
    "FLOAT64",
    "NUMERIC",
    "BIGNUMERIC",
    "STRUCT",
]
JOB_PRIORITIES = ["INTERACTIVE", "BATCH"]
WRITE_DISPOSITIONS = ["WRITE_APPEND", "WRITE_TRUNCATE", "WRITE_EMPTY"]

JOB_CONFIGS = {
    "LoadJobConfig": bigquery.LoadJobConfig(),
    "QueryJobConfig": bigquery.QueryJobConfig(),
}
