from kafka import KafkaConsumer
from kafka import KafkaProducer
import psycopg2
import json 

conn = psycopg2.connect(
    host = 'localhost',
    database = 'fraud_db',
    user = 'admin',
    password = 'admin'
)
cursor = conn.cursor()

fraud_producer = KafkaProducer(
    bootstrap_server = 'kafka:9092',
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

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

    if transaction["amount"] > 1000:
        print("Fraud Alert:", transaction)

        fraud_producer.send("fraud_alerts", transaction)
        fraud_producer.flush()

        conn.commit()

    else:
        print('Normal transaction:', transaction)

    