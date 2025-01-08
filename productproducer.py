from confluent_kafka import Producer
import json

# Kafka Config
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "products"

# Initialize Kafka Producer
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} partition {msg.partition()} @ offset {msg.offset()}")

def send_to_kafka(product_data: dict):
    try:
        producer.produce(
            KAFKA_TOPIC,
            key=str(product_data.get("name")),
            value=json.dumps(product_data),
            callback=delivery_report,
        )
        producer.flush()
    except Exception as e:
        print(f"Error Sending To Kafka: {e}")