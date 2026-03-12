create table fraud_alerts (
    id integer generated always as identity primary key,
    user_id int,
    amount float,
    merchant varchar(255),
    country varchar(100),
    created_at TIMESTAMP default current_timestamp
);