SELECT DISTINCT
    s.catalog_name AS database_id,
    s.catalog_name AS database_name,
    s.schema_name AS schema_name,
    s.schema_owner AS schema_owner,
    s.catalog_name + '.' + s.schema_name AS schema_id
FROM INFORMATION_SCHEMA.SCHEMATA AS s
