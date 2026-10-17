from kafka import KafkaProducer
import json
import time
from simulate import generate_trip

# Connexion à Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

TOPIC = "uber_trips"

def send_trips():
    """Envoie les trajets Uber vers Kafka en continu"""
    print("Producer démarré — envoi des trajets vers Kafka...")
    
    while True:
        # Générer un trajet
        trip = generate_trip()
        
        # Envoyer vers Kafka
        producer.send(TOPIC, value=trip)
        
        print(f"Trajet envoyé: {trip['trip_id']} | {trip['pickup_zone']} → {trip['dropoff_zone']} | {trip['price_mad']} MAD")
        
        # Attendre 1 seconde avant le prochain trajet
        time.sleep(1)

if __name__ == "__main__":
    send_trips()