import psycopg2
import json
from kafka import KafkaConsumer
import os

conn = psycopg2.connect(
    host="172.31.0.1",
    database="market_pipeline",
    user="postgres",
    password= os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history(
            id SERIAL PRIMARY KEY,
            coin TEXT,
            price_usd REAL,
            timestamp REAL
    )
''')
conn.commit()

consumer = KafkaConsumer(
    'crypto-prices',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='price-consumer-group',
    enable_auto_commit=True
)

print("Listening for message and saving to database...")

for message in consumer:
    data = json.loads(message.value.decode('utf-8'))

    cursor.execute(
    'INSERT INTO raw_prices (coin, price_usd, timestamp) VALUES (%s, %s, %s)',
    (data['coin'], data['price_usd'], data['timestamp'])
)
    
    
    conn.commit()
    print(f"Saved: {data}")
       