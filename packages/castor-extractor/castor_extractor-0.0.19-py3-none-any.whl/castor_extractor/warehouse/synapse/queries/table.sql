WITH users AS (
    SELECT DISTINCT
        uid,
        name
    FROM sys.sysusers
)

SELECT
    DB_NAME() as database_id,
    DB_NAME() AS database_name,
    DB_NAME() + '.' + s.name AS schema_id,
    s.name AS schema_name,
    DB_NAME() + '.' + s.name + '.' + o.name AS table_id,
    o.name AS table_name,
    CASE UPPER(REPLACE(o.type, ' ', ''))
        WHEN 'U' THEN 'TABLE'
        WHEN 'V' THEN 'VIEW'
        ELSE 'UNKNOWN'
    END AS table_type,
    -- Normally schema owner is table owner, but we can
    -- change table owner with ALTER AUTHORIZATION command
    -- in this case we have to look up for the owner
    -- in sys.objects table
    COALESCE(su.name, pu.name) AS table_owner,
    COALESCE(su.uid, pu.uid) AS table_owner_id,
    NULL AS comment
FROM sys.objects AS o
    JOIN sys.schemas AS s
        ON o.schema_id = s.schema_id
    LEFT JOIN users AS pu
        ON s.principal_id = pu.uid
    LEFT JOIN users AS su
        ON o.principal_id = su.uid
WHERE
-- SYNAPSE NOTATION: U for TABLE, V for VIEW
    o.type IN ('U', 'V')
