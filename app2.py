import streamlit as st
import pandas as pd
from faker import Faker
import random
from io import BytesIO

fake = Faker()
st.set_page_config(page_title="Générateur de tables chaotiques", layout="wide")
st.title("🎲 Générateur de tables chaotiques pour tests ETL")

# --- Paramètres ---
st.sidebar.header("Paramètres")
n_rows = st.sidebar.slider("Nombre de profils", 10, 500, 50, step=10)
max_cols = st.sidebar.slider("Nombre max de colonnes", 5, 15, 8)
n_tables = st.sidebar.slider("Nombre de tables à générer", 2, 3, 2)

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
    for col in list(df_copy.columns):  # copier la liste pour éviter KeyError
        if random.random() < 0.3:  # 30% de chance de renommer
            df_copy = df_copy.rename(columns={col: f"{col}_{fake.word()}"})
        if random.random() < 0.2:  # 20% de chance de supprimer
            df_copy.drop(columns=[col], inplace=True, errors='ignore')

    # 3️⃣ Ajouter des colonnes aléatoires pour atteindre max_cols
    while df_copy.shape[1] < max_cols:
        df_copy[f"extra_{fake.word()}"] = [fake.word() for _ in range(len(df_copy))]

    # 4️⃣ Mélanger les lignes
    df_copy = df_copy.sample(frac=1).reset_index(drop=True)

    # 5️⃣ Ajouter des valeurs manquantes aléatoires
    for col in df_copy.columns:
        df_copy.loc[df_copy.sample(frac=0.1).index, col] = None  # 10% NaN

    return df_copy

# --- Générer plusieurs tables ---
dfs = []
for i in range(n_tables):
    dfs.append(chaotic_version(df_base, max_cols))

# --- Affichage ---
for idx, df in enumerate(dfs):
    st.subheader(f"🟢 Table version {idx+1}")
    st.dataframe(df)

# --- Export XLSX ---
def export_excel(dfs, names):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for df, name in zip(dfs, names):
            df.to_excel(writer, sheet_name=name, index=False)
    output.seek(0)
    return output

xlsx_all = export_excel(dfs, [f"Version {i+1}" for i in range(n_tables)])
st.download_button("📥 Télécharger toutes les tables XLSX", xlsx_all, "tables_chaotiques.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- Export CSV séparés ---
for idx, df in enumerate(dfs):
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(f"📥 Télécharger version {idx+1} CSV", csv_data, f"table_v{idx+1}.csv", "text/csv")
