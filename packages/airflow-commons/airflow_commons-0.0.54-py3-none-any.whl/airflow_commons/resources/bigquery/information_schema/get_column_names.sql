SELECT column_name
FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS
WHERE table_name='{table_name}';
