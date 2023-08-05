WITH dashboard_view_log AS
(
    SELECT
        model_id,
        COUNT(id) AS view_count,
        MAX("timestamp") AS last_viewed_at
    FROM
        {schema}.view_log
    WHERE
        model = 'dashboard'
    GROUP BY
        1
)

SELECT
    rd.*,
    vl.last_viewed_at AS last_viewed_at,
    COALESCE(vl.view_count, 0) AS view_count
FROM
    {schema}.report_dashboard AS rd
    LEFT JOIN dashboard_view_log AS vl ON rd.id = vl.model_id
