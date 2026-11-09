select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_day,
    o.status,
    o.amount,
    o.is_revenue,
    c.state as customer_state
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c on c.customer_id = o.customer_id
