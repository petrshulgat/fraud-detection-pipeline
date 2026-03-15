from kafka import KafkaProducer
from faker import Faker
from datetime import datetime
import json
import random
import time

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers = "kafka:9092",
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
    )

while True:
    transaction = {
        'user_id': random.randint(1, 1000),
        'amount': round(random.uniform(5, 2000), 2),
        'merchant': fake.company(),
        'country': fake.country_code(),
        'timestamp': datetime.utcnow().isoformat()
    }

    producer.send("transactions", transaction)
    producer.flush()

    print(transaction)

    time.sleep(1)
