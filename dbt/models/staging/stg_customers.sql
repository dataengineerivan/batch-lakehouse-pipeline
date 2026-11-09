select
    customer_id,
    first_name,
    last_name,
    first_name || ' ' || last_name as full_name,
    email,
    state,
    cast(created_at as date) as signup_date,
    updated_at
from {{ source('raw', 'customers') }}
