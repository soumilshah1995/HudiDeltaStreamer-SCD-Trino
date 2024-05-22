WITH updated_records AS (
    SELECT
        a.customer_id,
        a.name AS customer_name,
        a.state,
        a.city,
        a.email,
        a.created_at,
        a.ts
    FROM
   <SRC> a
    ),
    existing_records AS (
SELECT
    e.customer_id,
    e.customer_name,
    e.state,
    e.city,
    e.email,
    e.created_at,
    e.ts,
    e.is_current,
    e.customer_dim_key
FROM
    hudi_db.customer_dim e
    INNER JOIN
    updated_records u
ON
    e.customer_id = u.customer_id
    )
SELECT
    uuid() AS customer_dim_key,
    customer_id,
    customer_name,
    state,
    city,
    email,
    created_at,
    ts,
    true AS is_current
FROM
    updated_records
UNION ALL
SELECT
    customer_dim_key,
    customer_id,
    customer_name,
    state,
    city,
    email,
    created_at,
    ts,
    false AS is_current
FROM
    existing_records;
