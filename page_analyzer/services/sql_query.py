GET_ITEMS = """SELECT
    json_build_object(
        'id', urls.id,
        'name', urls.name,
        'created_at', urls.created_at,
        'url_checks', COALESCE(json_agg(json_build_object(
            'id', latest_url_checks.id,
            'url_id', latest_url_checks.url_id,
            'status_code', latest_url_checks.status_code,
            'h1', latest_url_checks.h1,
            'title', latest_url_checks.title,
            'description', latest_url_checks.description,
            'created_at', latest_url_checks.created_at
        )) FILTER (WHERE latest_url_checks.id IS NOT NULL), '[]'::json)
    ) AS result
FROM urls
LEFT JOIN LATERAL (
    SELECT *
    FROM url_checks
    WHERE url_checks.url_id = urls.id
    ORDER BY url_checks.created_at DESC
    LIMIT 1
) AS latest_url_checks ON true
GROUP BY urls.id;"""
GET_JSON_BY_ID = """SELECT
    json_build_object(
        'id', urls.id,
        'name', urls.name,
        'created_at', urls.created_at,
        'url_checks', COALESCE(json_agg(json_build_object(
            'id', url_checks.id,
            'url_id', url_checks.url_id,
            'status_code', url_checks.status_code,
            'h1', url_checks.h1,
            'title', url_checks.title,
            'description', url_checks.description,
            'created_at', url_checks.created_at
        )) FILTER (WHERE url_checks.id IS NOT NULL) , '[]'::json)
    ) AS result
FROM urls
LEFT JOIN url_checks ON urls.id = url_checks.url_id
WHERE urls.id = (%s)
GROUP BY urls.id;"""
GET_JSON_BY_URL = """SELECT
    json_build_object(
        'id', id,
        'name', name,
        'created_at', created_at
) AS result
FROM urls WHERE name = (%s)"""
INSERT_ITEM_RETURN_JSON = """INSERT INTO
    urls (name, created_at)
    VALUES (%s,%s)
    RETURNING json_build_object(
        'id', id,
        'name', name,
        'created', created_at
    ) AS result;"""
