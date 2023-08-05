SELECT column_name as primitive_column_name, data_type
FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS
WHERE table_name='{table_name}'
AND data_type IN ({primitive_data_types});