from kafka import KafkaConsumer
import json

# Connexion à Kafka
consumer = KafkaConsumer(
    "uber_trips",
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='uber_consumer_group'
)

def consume_trips():
    """Reçoit les trajets depuis Kafka"""
    print("Consumer démarré — en attente des trajets...")
    
    for message in consumer:
        trip = message.value
        print(f"Trajet reçu: {trip['trip_id']} | {trip['pickup_zone']} → {trip['dropoff_zone']} | {trip['price_mad']} MAD")

if __name__ == "__main__":
    consume_trips()