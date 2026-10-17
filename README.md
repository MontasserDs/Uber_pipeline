# 🚗 Uber Casablanca — Real-Time Data Pipeline

A production-grade, end-to-end data engineering pipeline that simulates and processes Uber ride data in real-time across Casablanca neighborhoods.

##  Architecture

Faker → Kafka → PySpark → PostgreSQL → Streamlit
↑
Airflow (Orchestration)
Docker (Containerization)


##  Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Simulation | Python + Faker | Generate realistic Uber trips |
| Streaming | Apache Kafka | Real-time data transport |
| Processing | Apache PySpark | Data transformation at scale |
| Orchestration | Apache Airflow | Pipeline automation |
| Storage | PostgreSQL | Data warehouse |
| Dashboard | Streamlit | Live visualization |
| Containerization | Docker | Service management |
| Version Control | Git + GitHub | Code versioning |

## 📊 Pipeline Features

- 🔄 Real-time streaming — new trip generated every second
- 🗺️ Casablanca zones — Maarif, Ain Diab, Hay Hassani, Anfa
- 💰 Dynamic pricing — surge pricing during rush hours
- 📈 Live dashboard — metrics updated every 5 seconds
- ⚙️ Automated — Airflow DAG runs hourly

##  Getting Started

### Prerequisites
- Python 3.12+
- Docker
- Java 17
- PostgreSQL

### Installation

```bash
git clone https://github.com/MontasserDs/Uber_pipeline.git
cd Uber_pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Start Kafka and Zookeeper
docker compose up -d

# Start data simulation
python scripts/producer.py

# Start PySpark processing
python scripts/load.py

# Launch dashboard
streamlit run dashboard/app.py

# Start Airflow
airflow standalone
```

##  Project Structure

uber_pipeline/
├── dags/
│ └── uber_dag.py
├── scripts/
│ ├── simulate.py
│ ├── producer.py
│ ├── consumer.py
│ ├── transform.py
│ └── load.py
├── dashboard/
│ └── app.py
├── docker-compose.yml
├── requirements.txt
└── .env


##  Data Schema

```json
{
  "trip_id": "uuid",
  "driver_name": "string",
  "passenger_name": "string",
  "pickup_zone": "string",
  "dropoff_zone": "string",
  "distance_km": "float",
  "duration_min": "integer",
  "price_mad": "float",
  "surge_multiplier": "float",
  "status": "completed | in_progress | cancelled",
  "trip_category": "short | medium | long",
  "timestamp": "datetime"
}
```

## 👨‍💻 Author

**Montasser** — Data Engineering Portfolio
- GitHub: [@MontasserDs](https://github.com/MontasserDs)
- Master's in Big Data & AI — SUPMIR Casablanca