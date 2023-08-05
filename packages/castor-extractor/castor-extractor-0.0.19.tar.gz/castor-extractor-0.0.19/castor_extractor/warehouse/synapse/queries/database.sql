SELECT
    d.name AS database_id,
    d.name AS database_name,
    NULL AS "comment"
FROM sys.databases AS d
    WHERE d.name != 'master'
