select
    customer_state,
    count(distinct customer_id) as customers,
    count(*) as orders,
    sum(case when is_revenue then amount else 0 end) as revenue
from {{ ref('fct_orders') }}
group by customer_state
