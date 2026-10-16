import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# ---------------------------------------------------------
#  SIMULATION MQTT (THÉORIQUE, SANS BROKER RÉEL)
# ---------------------------------------------------------

def mqtt_simulation():
    """Simule des données comme si elles venaient d'un broker MQTT."""
    data = {
        "temperature": 20 + random.uniform(-0.5, 0.5),
        "humidite": 40 + random.uniform(-2, 2),
        "gaz": random.randint(100, 350),   # ppm
        "eau": random.uniform(0, 5),       # L/min
    }
    return data


# ---------------------------------------------------------
#  FONCTIONS JUMEAU NUMÉRIQUE (MODÈLE RC + ALERTE)
# ---------------------------------------------------------

def simuler(df, R, C, T0, dt=60.0):
    t_ext = df["t_ext"].to_numpy()
    p = df["puissance"].to_numpy()
    T = np.empty(len(df))
    T[0] = T0
    for k in range(1, len(df)):
        T[k] = T[k - 1] + dt * ((t_ext[k - 1] - T[k - 1]) / R + p[k - 1]) / C
    return pd.Series(T, index=df.index, name="modele")

def alerte(ecart, seuil=0.5, duree=15):
    return (ecart.abs() > seuil).rolling(duree).sum() >= duree


# ---------------------------------------------------------
#  CONFIGURATION DE L'APPLICATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SmartThermo Twin : IoT, IA et Jumeau Numérique RC pour Bâtiments Intelligents",
    layout="wide"
)

st.markdown("""
    <div style="background-color:#1E3A8A;padding:20px;border-radius:15px;margin-bottom:25px;
                box-shadow:0px 4px 10px rgba(0,0,0,0.3);">
        <h1 style="color:white;text-align:center;">SmartThermo Twin</h1>
        <h3 style="color:#cbd5e1;text-align:center;">IoT • IA • Jumeau Numérique RC • Sécurité Gaz & Eau (Simulation)</h3>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📌 Menu",
    ["🏠 Accueil", "📡 Capteurs IoT", "🚨 Fuites Gaz & Eau", "🤖 IA Anomalies", "🏢 Bâtiment", "🔥 Jumeau Numérique"]
)


# ---------------------------------------------------------
#  PAGE ACCUEIL
# ---------------------------------------------------------

if menu == "🏠 Accueil":
    st.markdown("""
        <h2 style="color:#1E3A8A;">🎯 SmartThermo Twin</h2>
        <p style="font-size:18px;">
            Plateforme théorique combinant IoT simulé, IA, jumeau numérique RC et sécurité gaz/eau
            pour la supervision thermique et sécuritaire des bâtiments intelligents.
        </p>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
#  PAGE CAPTEURS IOT (AVEC MQTT SIMULÉ)
# ---------------------------------------------------------

if menu == "📡 Capteurs IoT":

    st.markdown("## 📡 Capteurs IoT — Données simulées (MQTT théorique)")

    mqtt_data = mqtt_simulation()

    temperature = mqtt_data["temperature"]
    humidite = mqtt_data["humidite"]
    energie = 277  # valeur fixe d'exemple
    fumee = "Non"
    presence = "Détectée"

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Température", f"{temperature:.1f} °C")
    col2.metric("💧 Humidité", f"{humidite:.0f} %")
    col3.metric("⚡ Énergie", f"{energie} W")

    col4, col5 = st.columns(2)
    col4.metric("🔥 Fumée", fumee)
    col5.metric("🚶 Présence", presence)


# ---------------------------------------------------------
#  PAGE FUITES GAZ & EAU (AVEC MQTT SIMULÉ)
# ---------------------------------------------------------

if menu == "🚨 Fuites Gaz & Eau":

    st.markdown("## 🚨 Détection de Fuites Gaz & Eau (Simulation)")

    mqtt_data = mqtt_simulation()

    gaz_concentration = mqtt_data["gaz"]
    eau_debit = mqtt_data["eau"]

    gaz_detecte = gaz_concentration > 200   # seuil exemple
    eau_detectee = eau_debit > 2.0         # seuil exemple

    col1, col2 = st.columns(2)

    col1.markdown("### 🔥 Fuite de gaz")
    col1.metric("État", "Fuite détectée" if gaz_detecte else "Aucune fuite")
    col1.metric("Concentration gaz", f"{gaz_concentration} ppm")

    col2.markdown("### 💧 Fuite d'eau")
    col2.metric("État", "Fuite détectée" if eau_detectee else "Aucune fuite")
    col2.metric("Débit d'eau", f"{eau_debit:.2f} L/min")

    st.markdown("---")

    st.markdown("### 📈 Graphique — Débit d'eau (simulé)")
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(np.random.rand(20)*5, color="blue")
    ax.set_ylabel("Débit (L/min)")
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("### 📈 Graphique — Gaz (ppm, simulé)")
    fig2, ax2 = plt.subplots(figsize=(10,4))
    ax2.plot(np.random.rand(20)*300, color="red")
    ax2.set_ylabel("Gaz (ppm)")
    ax2.grid(True)
    st.pyplot(fig2)


# ---------------------------------------------------------
#  PAGE IA ANOMALIES
# ---------------------------------------------------------

if menu == "🤖 IA Anomalies":

    st.markdown("## 🤖 Détection IA des anomalies (scénarios simulés)")

    anomalies = [
        "Fenêtre ouverte",
        "Fuite thermique",
        "Chauffage insuffisant",
        "Surconsommation énergétique",
        "Fuite de gaz",
        "Fuite d'eau"
    ]

    for a in anomalies:
        st.markdown(f"- 🚨 **{a} (scénario simulé)**")


# ---------------------------------------------------------
#  PAGE BÂTIMENT
# ---------------------------------------------------------

if menu == "🏢 Bâtiment":

    st.markdown("## 🏢 Bâtiment — Zones supervisées (modèle théorique)")

    zones = {
        "🏛️ Hall d'entrée": "Température, Présence",
        "🟥 Rez-de-chaussée": "Température, Humidité, Énergie",
        "🟦 1er étage": "Température, Fumée",
        "🟩 Salle de réunion": "Température, CO₂, Présence",
        "🟪 Bureau IA": "Température, Énergie, IA prédictions"
    }

    for zone, info in zones.items():
        st.markdown(f"### {zone}")
        st.write(info)
        st.markdown("---")


# ---------------------------------------------------------
#  PAGE JUMEAU NUMÉRIQUE THERMIQUE (RC)
# ---------------------------------------------------------

if menu == "🔥 Jumeau Numérique":

    st.markdown("## 🔥 Jumeau Numérique Thermique — Modèle RC (Simulation)")

    R = st.slider("Résistance thermique R", 0.5, 5.0, 2.0)
    C = st.slider("Capacité thermique C", 10.0, 200.0, 50.0)
    seuil = st.slider("Seuil d'anomalie (°C)", 0.1, 2.0, 0.5)
    duree = st.slider("Durée min. d'anomalie (min)", 5, 60, 15)

    timestamps = pd.date_range("2024-01-01", periods=120, freq="min")
    t_ext = 15 + np.random.normal(0, 0.3, 120)
    puissance = [0]*20 + [500]*50 + [0]*50
    mesure = 20 + np.random.normal(0, 0.2, 120)

    df = pd.DataFrame({
        "t_ext": t_ext,
        "puissance": puissance,
        "mesure": mesure
    }, index=timestamps)

    df["modele"] = simuler(df, R, C, df["mesure"].iloc[0])
    df["ecart"] = df["mesure"] - df["modele"]
    df["alerte"] = alerte(df["ecart"], seuil, duree)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Mesure", f"{df['mesure'].iloc[-1]:.1f} °C")
    col2.metric("📘 Modèle RC", f"{df['modele'].iloc[-1]:.1f} °C")
    col3.metric("📉 Écart", f"{df['ecart'].iloc[-1]:.2f} °C")
    col4.metric("🚨 Alerte", "OUI" if df["alerte"].iloc[-1] else "NON")

    st.markdown("---")

    fig1, ax1 = plt.subplots(figsize=(10,4))
    ax1.plot(df.index, df["mesure"], label="Mesure", color="#2563eb")
    ax1.plot(df.index, df["modele"], label="Modèle RC", color="#f97316")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(10,4))
    ax2.plot(df.index, df["ecart"], label="Écart", color="#7e22ce")
    ax2.axhline(seuil, color="red", linestyle="--")
    ax2.axhline(-seuil, color="red", linestyle="--")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(10,3))
    ax3.plot(df.index, df["alerte"].astype(int), color="red")
    ax3.set_yticks([0,1])
    ax3.set_yticklabels(["False","True"])
    ax3.grid(True)
    st.pyplot(fig3)

    anomalies = df[df["alerte"]]
    st.markdown("### 🛑 Anomalies détectées")
    if anomalies.empty:
        st.info("Aucune anomalie détectée (simulation).")
    else:
        st.dataframe(anomalies)
