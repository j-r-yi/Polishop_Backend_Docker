from confluent_kafka import Consumer
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from models import Product
from database import get_db
import json





TOPIC_NAME = "demo_topic"
BROKER = "localhost:9092"

def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id="demo-group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def consume_messages(consumer):
    print("Listening for messages...")
    for message in consumer:
        print(f"Consumed: {message.value}")

if __name__ == "__main__":
    consumer = create_consumer()
    consume_messages(consumer)


















'''
# "productconsumer.py" listens to the product topic, processes incoming data, and stores in db

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "products"

# Kafka Config
consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "product-consumer-group",
    "auto.offset.reset": "latest"
})
consumer.subscribe([KAFKA_TOPIC])

def process_messages():
    db = next(get_db())
    try:
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                
                # Parse message from KAFKA
                product_data = json.loads(msg.value())
                try:
                    # Log product to check process of producing and consuming
                    print("Received product data from Kafka:")
                    print(json.dumps(product_data, indent=4))

                    # Check if product already exists in the database
                    existing_product = db.query(Product).filter(
                        Product.name == product_data.name,
                        Product.category == product_data.category
                    ).first()

                    if existing_product:
                        print(
                                f"Product '{product_data['name']}' in category '{product_data['category']}' already exists."
                        )
                        continue

                    # Creating a new product object
                    new_product = Product(
                        img=product_data["img"],
                        name=product_data["name"],
                        price=product_data["price"],
                        discount=product_data["discount"],
                        description=product_data["description"],
                        quantity=product_data["quantity"],
                        product_details=product_data["product_details"],
                        gallery_1=product_data["gallery_1"],
                        gallery_2=product_data["gallery_2"],
                        category=product_data["category"],
                        subcategory=product_data["subcategory"],
                    )

                    # adding and committing product to db
                    db.add(new_product)
                    db.commit()
                    db.refresh(new_product)
                    print(f"Stored product: {product_data['name']} in MySQL")
                    
                except Exception as e:
                    # db.rollback()
                    print(f"Error storing product: {e}")
                    
            except Exception as e:
                print(f"Error processing message: {e}")
    except KeyboardInterrupt:
        print("Consumer shutting down")
    finally:
        db.close()
        consumer.close()


if __name__ == "__main__":
    process_messages()

'''

# def create_product(product: ProductSchema, db: Session = Depends(get_db)):
#     existing_product = db.query(Product).filter(
#         Product.name == product.name,
#         Product.category == product.category
#     ).first()

#     if existing_product:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Product '{product.name}' in category '{product.category}' already exists."
#         )

#     # Create and add the new product to the database
#     new_product = Product(
#         img=product.img,
#         name=product.name,
#         price=product.price,
#         discount=product.discount,
#         description=product.description,
#         quantity=product.quantity,
#         product_details=product.product_details,
#         gallery_1=product.gallery_1,
#         gallery_2=product.gallery_2,
#         category=product.category,
#         subcategory=product.subcategory,
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)

#     return {
#         "message": "Product added successfully",
#         "product": {
#             "productId": new_product.productId,
#             "name": new_product.name,
#             "category": new_product.category
#         }
#     }