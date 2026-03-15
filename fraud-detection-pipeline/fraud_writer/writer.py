from kafka import KafkaConsumer
import psycopg2
import json 

consumer = KafkaConsumer(
    'fraud_alerts',
    bootstrap_servers = 'kafka:9092',
    value_deserializer = lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset = 'earliest'
)

conn = psycopg2.connect(
    host = 'postgres',
    database = 'fraud_db',
    user = 'admin',
    password = 'admin'
)

cursor = conn.cursor()

for message in consumer:
    transaction = message.value

    cursor.execute("""
        insert into fraud_alerts(user_id, amount, merchant, country, event_time)  
        values(%s, %s, %s, %s, %s, %s)             
    """,(
        transaction['user_id'],
        transaction['amount'],
        transaction['merchant'],
        transaction['country'],
        transaction['event_time']
        )
    )

    conn.commit()

    print('Inserted fraud alert:', transaction)
    
