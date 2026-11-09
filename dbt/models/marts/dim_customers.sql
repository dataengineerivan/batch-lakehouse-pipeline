with order_summary as (
    select
        customer_id,
        min(order_day) as first_order_day,
        max(order_day) as last_order_day,
        count(*) as total_orders,
        sum(case when is_revenue then amount else 0 end) as lifetime_revenue
    from {{ ref('stg_orders') }}
    group by customer_id
)

select
    c.customer_id,
    c.full_name,
    c.email,
    c.state,
    c.signup_date,
    o.first_order_day,
    o.last_order_day,
    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.lifetime_revenue, 0) as lifetime_revenue,
    case
        when o.total_orders is null then 'No orders'
        when o.lifetime_revenue >= 1500 then 'High value'
        when o.lifetime_revenue >= 500 then 'Mid value'
        else 'Low value'
    end as customer_segment
from {{ ref('stg_customers') }} c
left join order_summary o on o.customer_id = c.customer_id
