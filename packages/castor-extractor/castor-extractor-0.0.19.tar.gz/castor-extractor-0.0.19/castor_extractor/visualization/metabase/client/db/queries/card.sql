WITH card_view_log AS
(
    SELECT
        model_id,
        COUNT(id) AS view_count,
        MAX("timestamp") AS last_viewed_at
    FROM
        {schema}.view_log
    WHERE
        model = 'card'
    GROUP BY
        1
)

SELECT
    rc.*,
    vl.last_viewed_at AS last_viewed_at,
    COALESCE(vl.view_count, 0) AS view_count
FROM
    {schema}.report_card AS rc
    LEFT JOIN card_view_log AS vl ON rc.id = vl.model_id
