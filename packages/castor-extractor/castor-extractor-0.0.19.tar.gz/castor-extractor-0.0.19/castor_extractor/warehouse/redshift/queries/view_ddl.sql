-- This query was inspired from this thread:
-- https://github.com/awslabs/amazon-redshift-utils/blob/master/src/AdminViews/v_generate_view_ddl.sql
SELECT
    CURRENT_DATABASE() AS database_name,
    n.nspname AS schema_name,
    c.relname AS view_name,
    CASE
     	WHEN c.relnatts > 0 THEN 'CREATE OR REPLACE VIEW ' + QUOTE_IDENT(n.nspname) + '.' + QUOTE_IDENT(c.relname) + ' AS\n' + COALESCE(pg_get_viewdef(c.oid, TRUE), '')
     	ELSE COALESCE(pg_get_viewdef(c.oid, TRUE), '')
     END AS view_definition
FROM
    pg_catalog.pg_class AS c
INNER JOIN
    pg_catalog.pg_namespace AS n
    ON c.relnamespace = n.oid
WHERE
    TRUE
    AND relkind = 'v'
    AND n.nspname NOT IN ('information_schema', 'pg_catalog');
