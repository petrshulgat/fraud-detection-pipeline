from kafka import KafkaConsumer
import psycopg2
import json 

conn = psycopg2.connect(
    host = 'localhost',
    database = 'fraud_db',
    user = 'admin',
    password = 'admin'
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers = 'kafka:9092',
    value_deserializer = lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset = 'earliest'
)

for message in consumer:
    transaction = message.value

    event_time = transaction.get("timestamp") or transaction.get("created_at")

    if 'amount' not in transaction:
        print('Skip invalid message:', transaction)
        continue

    if transaction['amount'] > 1000:
        print('Fraud Alert:', transaction)

        cursor.execute("""
            insert into fraud_alerts(user_id, amount, merchant, country, event_time)
            values(%s, %s, %s, %s, %s)
        """, (
            transaction['user_id'], transaction['amount'], transaction['merchant'], transaction['country'], event_time
        )
        )

        conn.commit()

    else:
        print('Normal transaction:', transaction)

    