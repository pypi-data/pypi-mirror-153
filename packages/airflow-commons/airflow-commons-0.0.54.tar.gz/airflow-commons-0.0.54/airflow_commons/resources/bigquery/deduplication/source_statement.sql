SELECT
  *
FROM
  `{project_id}.{source_dataset}.{source_table}`
WHERE
    {source_where_statement}
QUALIFY ROW_NUMBER() OVER (PARTITION BY {partition_by_clause} ORDER BY {order_by_clause} ) = 1