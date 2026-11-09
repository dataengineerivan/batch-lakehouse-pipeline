select
    order_id,
    customer_id,
    order_date,
    cast(order_date as date) as order_day,
    status,
    amount,
    -- cancelled and pending orders don't count as revenue
    status in ('completed', 'shipped') as is_revenue,
    updated_at
from {{ source('raw', 'orders') }}
