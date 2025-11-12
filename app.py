import streamlit as st
import pandas as pd
from faker import Faker
import random

fake = Faker()

st.sidebar.header("Paramètres de génération")
n_rows = st.sidebar.slider("Nombre de lignes", min_value=100, max_value=1000, value=200, step=50)
n_cols = st.sidebar.slider("Nombre de colonnes", min_value=5, max_value=15, value=8, step=1)

# Choix de scénario
scenario = st.sidebar.selectbox("Type de données", ["Profils utilisateurs", "Passages de trains", "Transactions financières", "Capteurs IoT", "Evénements logs"])

def generate_user_profiles(n):
    data = []
    for _ in range(n):
        data.append({
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80),
            "signup_date": fake.date_between(start_date="-5y", end_date="today"),
            "country": fake.country(),
            "job": fake.job()
        })
    return pd.DataFrame(data)

def generate_train_passages(n):
    data = []
    for _ in range(n):
        data.append({
            "train_id": fake.random_int(min=1000, max=9999),
            "station_from": fake.city(),
            "station_to": fake.city(),
            "departure_time": fake.date_time_between(start_date="-30d", end_date="+30d"),
            "arrival_time": fake.date_time_between(start_date="now", end_date="+2h"),
            "delay_minutes": fake.random_int(min=0, max=180),
            "passenger_count": fake.random_int(min=0, max=500)
        })
    return pd.DataFrame(data)

# … tu peux ajouter d’autres fonctions pour les autres scénarios …

if scenario == "Profils utilisateurs":
    df = generate_user_profiles(n_rows)
elif scenario == "Passages de trains":
    df = generate_train_passages(n_rows)
# … etc …

# Si df a moins de n_cols colonnes, on peut en ajouter des colonnes “fictives” ou sélectionner n_cols parmi les existantes
df = df.iloc[:, :n_cols]  # simplifié

st.dataframe(df)

# Export
csv = df.to_csv(index=False).encode('utf‑8')
st.download_button(label="Télécharger en CSV", data=csv, file_name='fake_data.csv', mime='text/csv')

xlsx = df.to_excel(index=False, engine='openpyxl')
# (il faudra gérer le buffer BytesIO pour Excel)
