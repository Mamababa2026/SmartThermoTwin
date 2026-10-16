import streamlit as st
import random
import json
from datetime import datetime
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# CHEMINS ABSOLUS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

MESSAGES_FILE = os.path.join(DATA_DIR, "messages.jsonl")
RESULTS_FILE = os.path.join(DATA_DIR, "results.jsonl")

# -----------------------------
# CONFIG GLOBALE
# -----------------------------
st.set_page_config(
    page_title="SmartThermoTwin – Usine Thermofluide",
    page_icon="🏭",
    layout="wide"
)

# -----------------------------
# CSS GLOBAL
# -----------------------------
st.markdown("""
<style>
body { background-color: #0E1117; }
.big-title { font-size: 45px; font-weight: 900; color: #4A90E2; margin-bottom: 10px; }
.sub-title { font-size: 22px; color: #BBBBBB; margin-bottom: 20px; }
.section-title { font-size: 26px; font-weight: 700; color: #4A90E2; margin-top: 20px; margin-bottom: 10px; }
.card { padding: 18px; background: #1E1E26; border-radius: 14px; margin-bottom: 18px; border: 1px solid #2E2E3A; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FONCTIONS JSONL
# -----------------------------
def save_jsonl(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data["timestamp"] = datetime.utcnow().isoformat() + "Z"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def load_jsonl(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        return pd.read_json(path, lines=True)
    except:
        return pd.DataFrame()

# -----------------------------
# MENU LATERAL
# -----------------------------
st.sidebar.title("🏭 SmartThermoTwin")
st.sidebar.write("👤 Réalisé par : **Hamdi Ilhem**")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🌡️ Capteurs utilisés",
        "🛠️ Salle de contrôle",
        "🌊 Circuit d’eau chaude HVAC",
        "♨️ Échangeurs de chaleur",
        "🔧 Pompe principale",
        "🏭 Four industriel",
        "🛢️ Conduites de gaz",
        "💧 Conduites d’eau",
        "🧠 IA & Jumeau numérique",
        "📁 Historique messages.jsonl",
        "📁 Historique results.jsonl"
    ]
)

# -----------------------------
# PAGE ACCUEIL ULTRA MODERNE
# -----------------------------
if page == "🏠 Accueil":

    st.markdown("""
    <style>
    .hero {
        padding: 80px 40px;
        text-align: center;
        background: linear-gradient(135deg, #1E1E26 0%, #0E1117 100%);
        border-radius: 25px;
        margin-bottom: 50px;
        border: 1px solid #2E2E3A;
        box-shadow: 0px 0px 25px rgba(0,0,0,0.4);
    }
    .hero-title {
        font-size: 70px;
        font-weight: 900;
        color: #4A90E2;
        margin-bottom: 20px;
        letter-spacing: 2px;
        text-shadow: 0px 0px 15px #4A90E2;
    }
    .hero-sub {
        font-size: 26px;
        color: #CCCCCC;
        margin-bottom: 40px;
    }
    .card-grid {
        display: flex;
        gap: 25px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 40px;
    }
    .card-home {
        background: #1E1E26;
        padding: 30px;
        width: 280px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid #2E2E3A;
        transition: 0.3s;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
    }
    .card-home:hover {
        transform: scale(1.07);
        border-color: #4A90E2;
        box-shadow: 0px 0px 25px rgba(74,144,226,0.4);
    }
    .card-icon {
        font-size: 50px;
        margin-bottom: 15px;
        color: #4A90E2;
    }
    .card-title {
        font-size: 22px;
        color: #FFFFFF;
        font-weight: 700;
    }
    .footer {
        margin-top: 60px;
        text-align: center;
        color: #888888;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-title">SmartThermoTwin</div>
        <div class="hero-sub">Supervision Thermofluide • IoT • IA • Jumeau Numérique</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-grid">', unsafe_allow_html=True)

    cards = [
        ("🔥", "Circuit HVAC"),
        ("♨️", "Échangeurs de chaleur"),
        ("🔧", "Pompe principale"),
        ("🏭", "Four industriel"),
        ("🛢️", "Conduites de gaz"),
        ("💧", "Conduites d’eau"),
        ("🧠", "IA & Jumeau numérique")
    ]

    for icon, title in cards:
        st.markdown(f"""
        <div class="card-home">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Réalisé par <strong>Hamdi Ilhem</strong> — Projet SmartThermoTwin 2026
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PAGE CAPTEURS UTILISÉS
# -----------------------------
elif page == "🌡️ Capteurs utilisés":
    st.markdown('<div class="big-title">🌡️ Capteurs utilisés dans l’usine</div>', unsafe_allow_html=True)

    st.markdown("## 🔥 HVAC – Circuit d’eau chaude")
    st.write("""
- Capteur de température départ  
- Capteur de température retour  
- Capteur de pression  
- Capteur de débit  
- Capteur de température chaudière  
- Capteur de température pompe  
- Capteur de niveau d’eau  
- Capteur de vibration pompe  
- Capteur d’état vanne motorisée  
""")

    st.markdown("## ♨️ Échangeurs de chaleur")
    st.write("""
- Capteur ΔT chaud  
- Capteur ΔT froid  
- Capteur de débit primaire  
- Capteur de débit secondaire  
- Capteur de pression primaire  
- Capteur de pression secondaire  
- Capteur d’efficacité thermique  
- Capteur d’encrassement  
""")

    st.markdown("## 🔧 Pompe principale")
    st.write("""
- Capteur de température moteur  
- Capteur de vibration  
- Capteur d’intensité électrique  
- Capteur de débit  
- Capteur de pression sortie  
""")

    st.markdown("## 🏭 Four industriel")
    st.write("""
- Capteur de température interne  
- Capteur de température parois  
- Capteur de consommation gaz  
- Capteur de consommation électrique  
- Capteur d’état brûleur  
- Capteur de sécurité  
- Capteur de débit d’air chaud  
""")

    st.markdown("## 🛢 Conduites de gaz")
    st.write("""
- Capteur de pression gaz  
- Capteur de débit gaz  
- Capteur de fuite gaz  
- Capteur de température gaz  
- Capteur de qualité combustion  
""")

    st.markdown("## 💧 Conduites d’eau")
    st.write("""
- Capteur de pression eau  
- Capteur de débit eau  
- Capteur de température eau  
- Capteur de niveau réservoir  
- Capteur de fuite eau  
""")

# -----------------------------
# PAGE SALLE DE CONTRÔLE
# -----------------------------
elif page == "🛠️ Salle de contrôle":
    st.markdown('<div class="big-title">🛠️ Salle de contrôle – Usine Thermofluide</div>', unsafe_allow_html=True)

    df_msg = load_jsonl(MESSAGES_FILE)

    if df_msg.empty:
        st.warning("Aucune donnée disponible. Lance une simulation.")
    else:
        st.dataframe(df_msg.tail(20))

    st.markdown("## 🚨 Alertes système")

    alertes = []

    # HVAC
    if "hvac_temp_depart" in df_msg.columns:
        if df_msg["hvac_temp_depart"].iloc[-1] > 85:
            alertes.append("🔥 Température départ HVAC trop élevée (> 85°C)")
        if df_msg["hvac_temp_depart"].iloc[-1] < 70:
            alertes.append("⚠️ Température départ HVAC trop basse (< 70°C)")

    if "hvac_temp_retour" in df_msg.columns and df_msg["hvac_temp_retour"].iloc[-1] > 75:
        alertes.append("🔥 Température retour HVAC trop élevée (> 75°C)")

    if "hvac_press" in df_msg.columns and df_msg["hvac_press"].iloc[-1] < 3.5:
        alertes.append("⚠️ Pression HVAC trop basse (< 3.5 bar)")

    if "hvac_debit" in df_msg.columns and df_msg["hvac_debit"].iloc[-1] < 50:
        alertes.append("⚠️ Débit HVAC faible (< 50 m³/h)")

    if "hvac_vib_pompe" in df_msg.columns and df_msg["hvac_vib_pompe"].iloc[-1] > 3:
        alertes.append("⚠️ Vibration pompe HVAC élevée (> 3 mm/s)")

    if "hvac_vanne_etat" in df_msg.columns and df_msg["hvac_vanne_etat"].iloc[-1] == "OFF":
        alertes.append("⚠️ Vanne motorisée HVAC désactivée")

    # Échangeurs
    if "ech1_encrassement" in df_msg.columns and df_msg["ech1_encrassement"].iloc[-1] > 20:
        alertes.append("⚠️ Encrassement élevé Échangeur 1 (> 20%)")

    if "ech1_efficacite" in df_msg.columns and df_msg["ech1_efficacite"].iloc[-1] < 70:
        alertes.append("⚠️ Efficacité Échangeur 1 faible (< 70%)")

    if "ech2_encrassement" in df_msg.columns and df_msg["ech2_encrassement"].iloc[-1] > 20:
        alertes.append("⚠️ Encrassement élevé Échangeur 2 (> 20%)")

    if "ech2_efficacite" in df_msg.columns and df_msg["ech2_efficacite"].iloc[-1] < 70:
        alertes.append("⚠️ Efficacité Échangeur 2 faible (< 70%)")

    # Pompe
    if "pompe_temp_moteur" in df_msg.columns and df_msg["pompe_temp_moteur"].iloc[-1] > 80:
        alertes.append("🔥 Température moteur pompe élevée (> 80°C)")

    if "pompe_vib" in df_msg.columns and df_msg["pompe_vib"].iloc[-1] > 3:
        alertes.append("⚠️ Vibration pompe principale élevée (> 3 mm/s)")

    # Four
    if "four_temp_interne" in df_msg.columns and df_msg["four_temp_interne"].iloc[-1] > 280:
        alertes.append("🔥 Température interne four dangereuse (> 280°C)")

    if "four_securite" in df_msg.columns and df_msg["four_securite"].iloc[-1] == "ALERTE":
        alertes.append("🚨 Sécurité four déclenchée")

    # Gaz
    if "gaz_fuite" in df_msg.columns and df_msg["gaz_fuite"].iloc[-1] == 1:
        alertes.append("🚨 Fuite gaz détectée")

    if "gaz_press" in df_msg.columns and df_msg["gaz_press"].iloc[-1] < 3.8:
        alertes.append("⚠️ Pression gaz basse (< 3.8 bar)")

    # Eau
    if "eau_fuite" in df_msg.columns and df_msg["eau_fuite"].iloc[-1] == 1:
        alertes.append("🚨 Fuite eau détectée")

    if "eau_press" in df_msg.columns and df_msg["eau_press"].iloc[-1] < 2.8:
        alertes.append("⚠️ Pression eau basse (< 2.8 bar)")

    if len(alertes) == 0:
        st.success("✔️ Aucun problème détecté")
    else:
        for a in alertes:
            st.error(a)

# -----------------------------
# PAGES SIMULATION
# -----------------------------
elif page == "🌊 Circuit d’eau chaude HVAC":
    st.markdown('<div class="big-title">🌊 Circuit d’eau chaude HVAC</div>', unsafe_allow_html=True)

    data = {
        "hvac_temp_depart": random.uniform(70, 90),
        "hvac_temp_retour": random.uniform(50, 70),
        "hvac_press": random.uniform(3, 6),
        "hvac_debit": random.uniform(40, 120),
        "hvac_temp_chaudiere": random.uniform(80, 95),
        "hvac_temp_pompe": random.uniform(65, 80),
        "hvac_niveau_eau": random.uniform(60, 100),
        "hvac_vib_pompe": random.uniform(1.0, 4.0),
        "hvac_vanne_etat": random.choice(["ON", "OFF"])
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures HVAC enregistrées.")
    st.json(data)

elif page == "♨️ Échangeurs de chaleur":
    st.markdown('<div class="big-title">♨️ Échangeurs de chaleur</div>', unsafe_allow_html=True)

    data = {
        "ech1_dt_chaud": random.uniform(15, 25),
        "ech1_dt_froid": random.uniform(20, 30),
        "ech1_debit_primaire": random.uniform(40, 70),
        "ech1_debit_secondaire": random.uniform(35, 65),
        "ech1_press_primaire": random.uniform(3.0, 4.0),
        "ech1_press_secondaire": random.uniform(2.5, 3.5),
        "ech1_efficacite": random.uniform(70, 85),
        "ech1_encrassement": random.uniform(5, 20),

        "ech2_dt_chaud": random.uniform(18, 28),
        "ech2_dt_froid": random.uniform(22, 32),
        "ech2_debit_primaire": random.uniform(45, 75),
        "ech2_debit_secondaire": random.uniform(40, 70),
        "ech2_press_primaire": random.uniform(3.2, 4.2),
        "ech2_press_secondaire": random.uniform(2.7, 3.7),
        "ech2_efficacite": random.uniform(72, 88),
        "ech2_encrassement": random.uniform(8, 22)
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures échangeurs enregistrées.")
    st.json(data)

elif page == "🔧 Pompe principale":
    st.markdown('<div class="big-title">🔧 Pompe principale</div>', unsafe_allow_html=True)

    data = {
        "pompe_temp_moteur": random.uniform(65, 85),
        "pompe_vib": random.uniform(1.0, 4.0),
        "pompe_intensite": random.uniform(10, 20),
        "pompe_debit": random.uniform(70, 110),
        "pompe_press_sortie": random.uniform(3.5, 4.5),
        "pompe_etat": random.choice(["ON", "OFF"])
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures pompe enregistrées.")
    st.json(data)

elif page == "🏭 Four industriel":
    st.markdown('<div class="big-title">🏭 Four industriel</div>', unsafe_allow_html=True)

    data = {
        "four_temp_interne": random.uniform(200, 300),
        "four_temp_parois": random.uniform(150, 220),
        "four_conso_gaz": random.uniform(20, 40),
        "four_conso_elec": random.uniform(8, 18),
        "four_etat_bruleur": random.choice(["ON", "OFF"]),
        "four_securite": random.choice(["OK", "ALERTE"]),
        "four_debit_air_chaud": random.uniform(400, 600)
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures four enregistrées.")
    st.json(data)

elif page == "🛢️ Conduites de gaz":
    st.markdown('<div class="big-title">🛢️ Conduites de gaz</div>', unsafe_allow_html=True)

    data = {
        "gaz_press": random.uniform(3.5, 4.5),
        "gaz_debit": random.uniform(15, 25),
        "gaz_fuite": random.choice([0, 0, 0, 1]),
        "gaz_temp": random.uniform(35, 50),
        "gaz_qualite_combustion": random.uniform(90, 99)
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures gaz enregistrées.")
    st.json(data)

elif page == "💧 Conduites d’eau":
    st.markdown('<div class="big-title">💧 Conduites d’eau</div>', unsafe_allow_html=True)

    data = {
        "eau_press": random.uniform(2.5, 3.5),
        "eau_debit": random.uniform(50, 80),
        "eau_temp": random.uniform(20, 30),
        "eau_niveau_reservoir": random.uniform(60, 100),
        "eau_fuite": random.choice([0, 0, 0, 1])
    }

    save_jsonl(data, MESSAGES_FILE)
    st.success("Mesures eau enregistrées.")
    st.json(data)

# -----------------------------
# PAGE IA & JUMEAU NUMÉRIQUE
# -----------------------------
elif page == "🧠 IA & Jumeau numérique":
    st.markdown('<div class="big-title">🧠 IA & Jumeau numérique</div>', unsafe_allow_html=True)

    df = load_jsonl(RESULTS_FILE)

    if df.empty:
        st.warning("Aucune donnée IA disponible.")
    else:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

        st.markdown("### 📊 Graphique des risques détectés")
        if len(numeric_cols) > 0:
            fig = px.line(df, x="timestamp", y=numeric_cols, title="Évolution des risques IA")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée numérique pour tracer un graphique.")

        st.markdown("### 📈 Diagramme radar (profil thermique)")
        radar_cols = numeric_cols[:6]
        if len(radar_cols) > 0:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=df[radar_cols].iloc[-1].values,
                theta=radar_cols,
                fill='toself'
            ))
            fig2.update_layout(polar=dict(bgcolor="#1E1E26"), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Pas assez de données numériques pour le radar.")

        st.markdown("## 🚨 Alertes IA avancées")
        alertes_ia = []

        if len(df) > 5:
            for col in numeric_cols:
                serie = df[col].dropna()
                if len(serie) > 5:
                    drift = serie.iloc[-1] - serie.iloc[-5]
                    if abs(drift) > (serie.std() * 2):
                        alertes_ia.append(f"⚠️ Dérive détectée sur {col} (variation anormale)")

            for col in numeric_cols:
                serie = df[col].dropna()
                if len(serie) > 5:
                    mean = serie.mean()
                    std = serie.std()
                    last = serie.iloc[-1]
                    if last > mean + 3 * std:
                        alertes_ia.append(f"🔥 Valeur très élevée détectée sur {col} (hors limite 3σ)")
                    if last < mean - 3 * std:
                        alertes_ia.append(f"❄️ Valeur très basse détectée sur {col} (hors limite 3σ)")

            if len(numeric_cols) >= 2:
                corr = df[numeric_cols].corr()
                for col1 in numeric_cols:
                    for col2 in numeric_cols:
                        if col1 != col2:
                            if corr.loc[col1, col2] < -0.8:
                                alertes_ia.append(f"⚠️ Corrélation négative forte entre {col1} et {col2}")
                            if corr.loc[col1, col2] > 0.95:
                                alertes_ia.append(f"⚠️ Corrélation positive excessive entre {col1} et {col2}")

            if "risk_score" in df.columns:
                risk = df["risk_score"].iloc[-1]
                if risk > 0.85:
                    alertes_ia.append("🚨 Risque IA critique (> 0.85)")
                elif risk > 0.65:
                    alertes_ia.append("⚠️ Risque IA élevé (> 0.65)")
                elif risk > 0.45:
                    alertes_ia.append("🔎 Risque IA modéré (> 0.45)")
                else:
                    alertes_ia.append("✔️ Risque IA faible")
        else:
            st.info("Pas assez de données pour les alertes IA avancées.")

        if len(alertes_ia) == 0:
            st.success("✔️ Aucun problème détecté par l’IA")
        else:
            for a in alertes_ia:
                st.error(a)

        st.markdown("## 📊 Heatmap IA – Corrélations entre capteurs")
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()
            fig_hm = px.imshow(
                corr,
                x=numeric_cols,
                y=numeric_cols,
                color_continuous_scale="RdBu",
                zmin=-1,
                zmax=1,
                title="Matrice de corrélation des capteurs (IA)"
            )
            fig_hm.update_layout(
                width=800,
                height=600,
                margin=dict(l=40, r=40, t=60, b=40),
                coloraxis_colorbar=dict(title="Corrélation")
            )
            st.plotly_chart(fig_hm, use_container_width=True)
        else:
            st.info("Pas assez de capteurs numériques pour générer une heatmap de corrélation.")

        st.markdown("## 📉 Heatmap IA – Anomalies dans le temps")
        if len(numeric_cols) > 0 and len(df) > 5:
            df_norm = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
            fig_hm_time = px.imshow(
                df_norm.T,
                x=df["timestamp"],
                y=numeric_cols,
                color_continuous_scale="Viridis",
                title="Heatmap des dérives/anomalies (normalisation Z-score)"
            )
            fig_hm_time.update_layout(
                width=900,
                height=600,
                margin=dict(l=40, r=40, t=60, b=40),
                xaxis_title="Temps",
                yaxis_title="Capteurs"
            )
            st.plotly_chart(fig_hm_time, use_container_width=True)
        else:
            st.info("Pas assez de données pour générer une heatmap temporelle.")

# -----------------------------
# HISTORIQUES
# -----------------------------
elif page == "📁 Historique messages.jsonl":
    st.markdown('<div class="big-title">📁 Historique messages.jsonl</div>', unsafe_allow_html=True)
    df = load_jsonl(MESSAGES_FILE)
    if df.empty:
        st.warning("Aucun fichier messages.jsonl trouvé ou fichier vide.")
    else:
        st.dataframe(df)

elif page == "📁 Historique results.jsonl":
    st.markdown('<div class="big-title">📁 Historique results.jsonl</div>', unsafe_allow_html=True)
    df = load_jsonl(RESULTS_FILE)
    if df.empty:
        st.warning("Aucun fichier results.jsonl trouvé ou fichier vide.")
    else:
        st.dataframe(df)
