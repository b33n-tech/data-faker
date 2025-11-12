import streamlit as st
import pandas as pd
from faker import Faker
import random
from io import BytesIO

fake = Faker()

st.set_page_config(page_title="Générateur de données fictives", layout="wide")
st.title("🎲 Générateur de données fictives")

# --- Paramètres utilisateur ---
st.sidebar.header("Paramètres de génération")
n_rows = st.sidebar.slider("Nombre de lignes", min_value=100, max_value=1000, value=200, step=50)
n_cols = st.sidebar.slider("Nombre de colonnes", min_value=5, max_value=15, value=8, step=1)

# Choix du thème
theme = st.sidebar.selectbox("Thème des données", [
    "Profils utilisateurs",
    "Passages de trains",
    "Transactions financières",
    "Capteurs IoT",
    "Événements logs",
    "Produits e-commerce",
    "Commandes / ventes",
    "Réseaux sociaux / posts",
    "Santé / patients",
    "Écoles / étudiants",
    "Tickets de support / incidents",
    "Logements / immobilier",
    "Événements sportifs",
    "Livres / bibliothèque",
    "Météo / climat"
])

# --- Fonctions de génération ---
def generate_user_profiles(n):
    return pd.DataFrame([{
        "user_id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "signup_date": fake.date_between(start_date="-5y", end_date="today"),
        "country": fake.country(),
        "job": fake.job()
    } for _ in range(n)])

def generate_train_passages(n):
    return pd.DataFrame([{
        "train_id": fake.random_int(min=1000, max=9999),
        "station_from": fake.city(),
        "station_to": fake.city(),
        "departure_time": fake.date_time_between(start_date="-30d", end_date="+30d"),
        "arrival_time": fake.date_time_between(start_date="now", end_date="+2h"),
        "delay_minutes": fake.random_int(min=0, max=180),
        "passenger_count": fake.random_int(min=0, max=500)
    } for _ in range(n)])

def generate_financial_transactions(n):
    return pd.DataFrame([{
        "transaction_id": fake.uuid4(),
        "account_id": fake.random_int(1000, 9999),
        "date": fake.date_between(start_date="-2y", end_date="today"),
        "amount": round(random.uniform(-1000, 5000), 2),
        "currency": random.choice(["EUR","USD","GBP","JPY"]),
        "merchant": fake.company(),
        "category": random.choice(["Alimentation","Transport","Loisirs","Santé","Tech","Services"])
    } for _ in range(n)])

def generate_iot_sensors(n):
    return pd.DataFrame([{
        "sensor_id": fake.uuid4(),
        "timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
        "temperature": round(random.uniform(-10,40),1),
        "humidity": round(random.uniform(0,100),1),
        "pressure": round(random.uniform(950,1050),1),
        "status": random.choice(["OK","WARN","ERROR"])
    } for _ in range(n)])

def generate_logs(n):
    return pd.DataFrame([{
        "log_id": fake.uuid4(),
        "timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
        "user_id": fake.uuid4(),
        "event_type": random.choice(["login","logout","error","transaction","update"]),
        "message": fake.sentence()
    } for _ in range(n)])

def generate_ecommerce_products(n):
    return pd.DataFrame([{
        "product_id": fake.uuid4(),
        "name": fake.word().capitalize(),
        "category": random.choice(["Electronics","Clothing","Food","Books","Sports"]),
        "price": round(random.uniform(5,1000),2),
        "stock": random.randint(0,500)
    } for _ in range(n)])

# --- Mapping thèmes → fonctions ---
theme_funcs = {
    "Profils utilisateurs": generate_user_profiles,
    "Passages de trains": generate_train_passages,
    "Transactions financières": generate_financial_transactions,
    "Capteurs IoT": generate_iot_sensors,
    "Événements logs": generate_logs,
    "Produits e-commerce": generate_ecommerce_products,
    # tu peux ajouter les autres thèmes ici
}

# Génération
if theme in theme_funcs:
    df = theme_funcs[theme](n_rows)
else:
    st.error("Thème non implémenté pour l'instant.")
    st.stop()

# --- Ajuster le nombre de colonnes ---
while df.shape[1] < n_cols:
    df[f"extra_col_{df.shape[1]+1}"] = [fake.word() for _ in range(len(df))]

df = df.iloc[:, :n_cols]

st.dataframe(df)

# --- Export CSV ---
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Télécharger CSV", csv, file_name="fake_data.csv", mime="text/csv")

# --- Export XLSX ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="Sheet1")
output.seek(0)
st.download_button("📥 Télécharger XLSX", output, file_name="fake_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
