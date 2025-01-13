from confluent_kafka import Producer
import json
from kafka import KafkaProducer
import time

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