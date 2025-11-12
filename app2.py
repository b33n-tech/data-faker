import streamlit as st
import pandas as pd
from faker import Faker
import random
from io import BytesIO

fake = Faker()
st.set_page_config(page_title="Générateur de tables chaotiques", layout="wide")
st.title("🎲 Générateur de tables chaotiques")

# --- Paramètres ---
st.sidebar.header("Paramètres")
n_rows = st.sidebar.slider("Nombre de profils", 10, 500, 50, step=10)
max_cols = st.sidebar.slider("Nombre max de colonnes", 5, 15, 8)

# --- Génération des profils de base ---
profiles = []
for _ in range(n_rows):
    profiles.append({
        "full_name": fake.name(),
        "email": fake.email(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "signup_date": fake.date_between(start_date="-5y", end_date="today"),
        "country": fake.country(),
        "job": fake.job()
    })

df_base = pd.DataFrame(profiles)

# --- Fonction pour générer une version chaotique ---
def chaotic_version(df, max_cols):
    df_copy = df.copy()

    # 1️⃣ Mélanger l’ordre des colonnes
    cols = list(df_copy.columns)
    random.shuffle(cols)
    df_copy = df_copy[cols]

    # 2️⃣ Supprimer ou renommer certaines colonnes aléatoirement
    for col in list(df_copy.columns):
        if random.random() < 0.3:  # 30% de chance de renommer
            df_copy = df_copy.rename(columns={col: f"{col}_{fake.word()}"})
        if random.random() < 0.2:  # 20% de chance de supprimer
            df_copy.drop(columns=[col], inplace=True)

    # 3️⃣ Ajouter des colonnes aléatoires pour atteindre max_cols
    while df_copy.shape[1] < max_cols:
        df_copy[f"extra_{fake.word()}"] = [fake.word() for _ in range(len(df_copy))]

    # 4️⃣ Mélanger les lignes
    df_copy = df_copy.sample(frac=1).reset_index(drop=True)
    return df_copy

# --- Générer deux versions chaotiques ---
df_v1 = chaotic_version(df_base, max_cols)
df_v2 = chaotic_version(df_base, max_cols)

st.subheader("🟢 Table version 1")
st.dataframe(df_v1)

st.subheader("🔴 Table version 2")
st.dataframe(df_v2)

# --- Export CSV/XLSX ---
def export_excel(dfs, names):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for df, name in zip(dfs, names):
            df.to_excel(writer, sheet_name=name, index=False)
    output.seek(0)
    return output

csv_v1 = df_v1.to_csv(index=False).encode('utf-8')
csv_v2 = df_v2.to_csv(index=False).encode('utf-8')

st.download_button("📥 Télécharger version 1 CSV", csv_v1, "table_v1.csv", "text/csv")
st.download_button("📥 Télécharger version 2 CSV", csv_v2, "table_v2.csv", "text/csv")

xlsx_all = export_excel([df_v1, df_v2], ["Version 1", "Version 2"])
st.download_button("📥 Télécharger les deux versions XLSX", xlsx_all, "tables_chaotiques.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
