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
    bootstrap_servers = 'localhost:9092',
    value_deserializer = lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset = 'earliest'
)

for message in consumer:
    transaction = message.value

    if 'amount' not in transaction:
        print('Skip invalid message:', transaction)
        continue

    if transaction['amount'] > 1000:
        print('Fraud Alert:', transaction)

        cursor.execute("""
            insert into fraud_alerts(user_id, amount, merchant, country)
            values(%s, %s, %s, %s)
        """, (
            transaction['user_id'], transaction['amount'], transaction['merchant'], transaction['country']
        )
        )

        conn.commit()

    else:
        print('Normal transaction:', transaction)

    