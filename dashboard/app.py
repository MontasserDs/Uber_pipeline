import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Connexion PostgreSQL
def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

def load_data():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM trips ORDER BY timestamp DESC LIMIT 1000", engine)

# Interface
st.set_page_config(page_title="Uber Pipeline Dashboard", layout="wide")
st.title("🚗 Uber Casablanca — Live Dashboard")

# Métriques
df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trajets", len(df))
col2.metric("Prix Moyen", f"{df['price_mad'].mean():.2f} MAD")
col3.metric("Distance Moyenne", f"{df['distance_km'].mean():.2f} km")
col4.metric("Trajets en cours", len(df[df['status'] == 'in_progress']))

st.divider()

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("Trajets par Zone de Départ")
    zone_counts = df['pickup_zone'].value_counts()
    st.bar_chart(zone_counts)

with col2:
    st.subheader("Catégories de Trajets")
    cat_counts = df['trip_category'].value_counts()
    st.bar_chart(cat_counts)

st.divider()

# Trajets récents
st.subheader("Trajets Récents")
st.dataframe(
    df[['trip_id', 'pickup_zone', 'dropoff_zone', 'distance_km', 'price_mad', 'status', 'trip_category']].head(20),
    use_container_width=True
)

# Auto-refresh toutes les 5 secondes
time.sleep(5)
st.rerun()