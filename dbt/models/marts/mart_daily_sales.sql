-- One row per day: the main table behind the Superset sales dashboard
select
    order_day,
    count(*) as orders,
    sum(case when is_revenue then amount else 0 end) as revenue,
    round(avg(case when is_revenue then amount end), 2) as avg_order_value,
    round(100.0 * avg(case when status = 'cancelled' then 1 else 0 end), 1) as cancel_rate_pct,
    count(distinct customer_id) as active_customers
from {{ ref('fct_orders') }}
group by order_day
