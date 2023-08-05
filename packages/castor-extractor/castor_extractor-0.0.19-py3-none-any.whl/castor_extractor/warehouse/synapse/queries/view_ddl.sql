SELECT
    DB_NAME() AS database_id,
    DB_NAME() AS database_name,
    DB_NAME() + '.' + table_schema AS schema_id,
    table_schema AS schema_name,
    table_name AS view_name,
    view_definition AS view_definition
FROM INFORMATION_SCHEMA.VIEWS
