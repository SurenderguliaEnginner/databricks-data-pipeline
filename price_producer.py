import requests
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

try:
  while True:
    response = requests.get(url)
    data = response.json()

    for coin,price_info in data.items():
        message = {
            "coin":coin,
            "price_usd": price_info.get('usd', None),
            "timestamp":time.time()
        }
        producer.send("crypto-prices", json.dumps(message).encode('utf-8'))
        producer.flush()
        print(message)
    time.sleep(5)
except KeyboardInterrupt:
    print("stopped by user")
    producer.flush()
