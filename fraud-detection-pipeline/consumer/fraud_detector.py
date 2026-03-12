from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest"
)

for message in consumer:
    transaction = message.value

    if "amount" not in transaction:
        print("Skipping invalid message:", transaction)
        continue

    if transaction["amount"] > 1000:
        print("Fraud Alert:", transaction)
    else:
        print("Normal transaction:", transaction)