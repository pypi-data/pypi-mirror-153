MERGE
    `{project_id}.{target_dataset}.{target_table}` T
USING
  ({source_statement}) AS S
ON
  {merge_keys}
  WHEN MATCHED THEN UPDATE SET {update_statements}
  WHEN NOT MATCHED
  THEN
INSERT
  ({columns})
VALUES
  ({columns});
