insert into warehouse.dim_customer (customer_id, full_name, email, country, created_at)
select customer_id, first_name || ' ' || last_name as full_name, email, country, created_at
from staging.customers on conflict(customer_id) do nothing;

insert into warehouse.dim_product (product_id, product_name, category, price)
select product_id, product_name, category, price 
from staging.products on conflict(product_id) do nothing;



insert into warehouse.dim_date (date_key, full_date, year, month, day)
select
    TO_CHAR(order_date, 'YYYYMMDD')::int as date_key,
    order_date::DATE as full_date,
    extract(year from order_date)::int as year,
    extract(month from order_date)::int as month,
    extract(day from order_date)::int as day
from staging.orders
group by order_date
on conflict (date_key) do nothing;