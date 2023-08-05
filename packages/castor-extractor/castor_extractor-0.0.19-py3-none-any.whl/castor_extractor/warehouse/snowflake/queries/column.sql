SELECT
    c.column_id,
    c.column_name,
    c.table_id,
    c.table_name,
    c.table_schema_id AS schema_id,
    c.table_schema AS "schema_name",
    c.table_catalog_id AS database_id,
    c.table_catalog AS database_name,
    c.ordinal_position,
    c.column_default,
    c.is_nullable,
    c.data_type,
    c.maximum_cardinality,
    c.character_maximum_length,
    c.character_octet_length,
    c.numeric_precision,
    c.numeric_precision_radix,
    c.numeric_scale,
    c.datetime_precision,
    c.interval_type,
    c.interval_precision,
    c.comment,
    c.deleted
FROM snowflake.account_usage.columns AS c
    JOIN snowflake.account_usage.schemata AS s ON s.schema_id = c.table_schema_id
    JOIN snowflake.account_usage.tables AS t ON t.table_id = c.table_id
WHERE TRUE
    AND COALESCE(c.column_name, '') != ''
    AND UPPER(c.table_catalog) NOT IN ('SNOWFLAKE', 'UTIL_DB')
    AND (
        c.deleted IS NULL
        OR c.deleted > CURRENT_TIMESTAMP - INTERVAL '1 day'
    )
    {database_allowed}
    {database_blocked}
    AND CASE {has_fetch_transient} WHEN FALSE THEN NOT t.is_transient::BOOLEAN ELSE TRUE END
