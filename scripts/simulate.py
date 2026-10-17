from faker import Faker
import random
import json
import uuid
from datetime import datetime

fake = Faker()

# Coordonnées GPS de Casablanca
CASABLANCA_ZONES = {
    "Maarif": (33.5892, -7.6336),
    "Ain Diab": (33.5978, -7.6956),
    "Hay Hassani": (33.5545, -7.6723),
    "Sidi Moumen": (33.5823, -7.5234),
    "Anfa": (33.5731, -7.6598),
    "Derb Sultan": (33.5912, -7.6012),
    "Bourgogne": (33.5867, -7.6234),
    "Ain Sebaa": (33.6012, -7.5456)
}

def generate_trip():
    """Génère un trajet Uber réaliste à Casablanca"""
    
    # Choisir zone de départ et d'arrivée
    pickup_zone = random.choice(list(CASABLANCA_ZONES.keys()))
    dropoff_zone = random.choice(list(CASABLANCA_ZONES.keys()))
    
    # Coordonnées avec légère variation
    pickup_lat = CASABLANCA_ZONES[pickup_zone][0] + random.uniform(-0.01, 0.01)
    pickup_lon = CASABLANCA_ZONES[pickup_zone][1] + random.uniform(-0.01, 0.01)
    dropoff_lat = CASABLANCA_ZONES[dropoff_zone][0] + random.uniform(-0.01, 0.01)
    dropoff_lon = CASABLANCA_ZONES[dropoff_zone][1] + random.uniform(-0.01, 0.01)
    
    # Distance et durée
    distance_km = round(random.uniform(1.0, 25.0), 2)
    duration_min = int(distance_km * random.uniform(3, 6))
    
    # Prix dynamique (surge pricing)
    hour = datetime.now().hour
    surge = 1.5 if (7 <= hour <= 9 or 17 <= hour <= 20) else 1.0
    price = round((5 + distance_km * 3.5) * surge, 2)
    
    trip = {
        "trip_id": str(uuid.uuid4()),
        "driver_name": fake.name(),
        "passenger_name": fake.name(),
        "pickup_zone": pickup_zone,
        "dropoff_zone": dropoff_zone,
        "pickup_lat": pickup_lat,
        "pickup_lon": pickup_lon,
        "dropoff_lat": dropoff_lat,
        "dropoff_lon": dropoff_lon,
        "distance_km": distance_km,
        "duration_min": duration_min,
        "price_mad": price,
        "surge_multiplier": surge,
        "status": random.choice(["completed", "in_progress", "cancelled"]),
        "timestamp": datetime.now().isoformat()
    }
    
    return trip

if __name__ == "__main__":
    # Générer 5 trajets de test
    for i in range(5):
        trip = generate_trip()
        print(json.dumps(trip, indent=2))
        print("---")