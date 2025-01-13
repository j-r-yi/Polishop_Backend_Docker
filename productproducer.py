from confluent_kafka import Producer
import json
from kafka import KafkaProducer
import time

TOPIC_NAME = "demo_topic"
BROKER = "localhost:9092"

def create_producer():
    return KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def produce_messages(producer):
    for i in range(10):
        message = {"id": i, "message": f"Hello Kafka! Message {i}"}
        producer.send(TOPIC_NAME, message)
        print(f"Produced: {message}")
        time.sleep(1)  # Sleep to simulate delay

if __name__ == "__main__":
    producer = create_producer()
    produce_messages(producer)
    producer.close()



'''
# "productproducer.py" sends product to Kafka topic called products

# Kafka Config
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "products"

# Initialize Kafka Producer, points to Kafka broker
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

# Callback function to log result of each delivery attempt
def delivery_report(err, msg):
    if err:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} partition {msg.partition()} @ offset {msg.offset()}")

# Method to send to kafka
# Serializes product_data to json
def send_to_kafka(product_data: dict):
    try:
        producer.produce(
            # Create new event
            # Event has key, value, and timestamp, and optional meta data
            KAFKA_TOPIC,
            key=str(product_data.get("name")), # Product name
            value=json.dumps(product_data),    # Serialized json
            callback=delivery_report,          # Callback function
        )
        producer.flush()
    # Error handling
    except Exception as e:
        print(f"Error Sending To Kafka: {e}")
'''