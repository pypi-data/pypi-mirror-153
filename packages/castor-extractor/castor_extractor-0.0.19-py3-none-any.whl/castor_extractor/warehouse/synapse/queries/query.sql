WITH query_execution AS (
    SELECT
        plan_id,
        CASE execution_type_desc
            WHEN 'Aborted' THEN 1
            WHEN 'Exception' THEN 1
            ELSE 0
        END AS aborted,
        MIN(CAST(first_execution_time AS DATETIME)) AS start_time,
        MAX(CAST(last_execution_time AS DATETIME)) AS end_time
    FROM sys.query_store_runtime_stats
    WHERE CAST(first_execution_time AS DATE) = CAST(DATEADD(day, -1, getdate()) AS DATE)
    -- Filtering on hour will be needed when running that query out of notebooks
    GROUP BY plan_id, execution_type_desc
)

SELECT
    q.query_id,
    qt.query_sql_text AS query_text,
    DB_NAME() AS database_id,
    DB_NAME() AS database_name,
    'SYNAPSE' AS user_name,
    qp.plan_id AS process_id,
    qe.aborted AS aborted,
    qe.start_time AS start_time,
    qe.end_time AS end_time
FROM sys.query_store_query AS q
    JOIN sys.query_store_query_text AS qt
        ON q.query_text_id = qt.query_text_id
    JOIN sys.query_store_plan AS qp
        ON q.query_id = qp.query_id
    JOIN query_execution AS qe
        ON qp.plan_id = qe.plan_id
