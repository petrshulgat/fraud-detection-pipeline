from kafka import KafkaConsumer
import psycopg2
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="fraud_db",
    user="admin",
    password="admin"
)
cursor = conn.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest"
)

for message in consumer:
    transaction = message.value

    # skip invalid messages
    if "amount" not in transaction:
        print("Skipping invalid message:", transaction)
        continue

    # Fraud detection rule
    if transaction["amount"] > 1000:
        print("FRAUD ALERT:", transaction)

        # Insert into database
        cursor.execute("""
            INSERT INTO fraud_alerts (user_id, amount, merchant, country)
            VALUES (%s, %s, %s, %s)
        """, (
            transaction["user_id"],
            transaction["amount"],
            transaction["merchant"],
            transaction["country"]
        ))

        conn.commit()

    else:
        print("Normal transaction:", transaction)