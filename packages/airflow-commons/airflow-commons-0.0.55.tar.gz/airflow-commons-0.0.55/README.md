# airflow-commons
A python package that contains common functionalities for airflow

## Installation
Use the package manager pip to install airflow-commons.
```bash
pip install airflow-commons
```
## Modules
* bigquery_operator: With this module you can manage your Google BigQuery operations.
* mysql_operator: Using this module, you can connect to your MySQL data source and manage your data operations.
* s3_operator: This operator connects to your s3 bucket and lets you manage your bucket.
* glossary: This module consists of constants used across project
* sql_resources: Template BigQuery and MySQL queries such as merge, delete, select etc. are located here.
* utils: Generic methods like connection, querying etc. are implemented in this module.

## Usage
* Sample deduplication code works like:
```python
from airflow_commons import bigquery_operator

bigquery_operator.deduplicate(
        service_account_file="path_to_file",
        start_date="01-01-2020 14:00:00",
        end_date="01-01-2020 15:00:00",
        project_id="bigquery_project_id",
        source_dataset="source_dataset",
        source_table="source_table",
        target_dataset="target_dataset",
        target_table="target_table",
        oldest_allowable_target_partition="01-01-2015 00:00:00",
        primary_keys=["primary_keys"],
        time_columns=["time_columns"],
        allow_partition_pruning=True,
    )
```
