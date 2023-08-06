SELECT
  *
FROM
  `{project_id}.{source_dataset}.{source_table}`
WHERE
    {source_partition_field} <= '{archive_date}'