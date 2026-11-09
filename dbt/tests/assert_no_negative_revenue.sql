-- Fails if any day shows negative revenue
select * from {{ ref('mart_daily_sales') }} where revenue < 0
