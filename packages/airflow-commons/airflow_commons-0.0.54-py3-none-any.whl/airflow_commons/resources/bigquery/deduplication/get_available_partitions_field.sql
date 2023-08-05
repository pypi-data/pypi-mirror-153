SELECT
  STRING_AGG(DISTINCT CONCAT("'" , format_timestamp("%Y-%m-%d", {target_partition_field}), "'")) AS available_partitions
FROM
  `{project_id}.{source_dataset}.{source_table}`
WHERE
    {source_partition_field} BETWEEN '{start_date}'
    AND '{end_date}' AND {target_partition_field} >= '{oldest_allowable_target_partition}';