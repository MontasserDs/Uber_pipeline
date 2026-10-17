from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuration du DAG
default_args = {
    'owner': 'montasser',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='uber_pipeline',
    default_args=default_args,
    description='Pipeline Uber Casablanca end-to-end',
    schedule='@hourly',
    start_date=datetime(2026, 10, 1),
    catchup=False
) as dag:

    # Tâche 1 — Lancer le Producer
    producer = BashOperator(
        task_id='producer',
        bash_command='cd /home/montasser/uber_pipeline && source venv/bin/activate && timeout 30 python scripts/producer.py'
    )

    # Tâche 2 — Lancer PySpark Load
    load = BashOperator(
        task_id='load',
        bash_command='cd /home/montasser/uber_pipeline && source venv/bin/activate && timeout 30 python scripts/load.py'
    )

    # Ordre d'exécution
    producer >> load