import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG GLOBALE
# -----------------------------
st.set_page_config(
    page_title="SmartThermo Twin",
    page_icon="🔥",
    layout="wide"
)

# -----------------------------
# CSS DESIGN
# -----------------------------
st.markdown("""
<style>
.big-title {
    font-size: 36px;
    font-weight: bold;
    color: #4A90E2;
}
.card {
    padding: 20px;
    background: #1E1E1E;
    border-radius: 12px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #4A90E2;
    margin-top: 10px;
    margin-bottom: 10px;
}
button {
    font-size: 20px !important;
    padding: 12px 20px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# MENU LATERAL
# -----------------------------
st.sidebar.title("📡 SmartThermo Twin")
st.sidebar.write("👤 Développé par **Hamdi Ilhem**")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🧭 Capteurs IoT",
        "💧 Fuites Gaz & Eau",
        "⚙️ IA Anomalies",
        "🏢 Bâtiment",
        "🔥 Jumeau Numérique"
    ]
)

# -----------------------------
# FONCTIONS UTILITAIRES
# -----------------------------
def detect_anomaly(temp):
    if temp > 28:
        return "🔥 Surchauffe détectée"
    elif temp < 15:
        return "❄️ Température trop basse"
    return "✔️ Température normale"

# -----------------------------
# PAGE ACCUEIL
# -----------------------------
if page == "🏠 Accueil":
    st.markdown('<div class="big-title">SmartThermo Twin</div>', unsafe_allow_html=True)

    # Nom du développeur
    st.markdown("""
    <div class="card" style="text-align:center;">
        <h2 style="color:#4A90E2;">👤 Réalisé par : <span style="color:white;">Hamdi Ilhem</span></h2>
    </div>
    """, unsafe_allow_html=True)

    # Bouton actualiser
    if st.button("🔄 Actualiser l'application"):
        st.experimental_rerun()

    # Carte principale
    st.markdown("""
    <div class="card">
        <h2 style="color:#4A90E2;">🔧 Plateforme IoT • IA • Jumeau Numérique</h2>
        <p>
            SmartThermo Twin combine :
            <br>• 📡 Capteurs IoT simulés
            <br>• 🤖 IA de détection d’anomalies
            <br>• 🔥 Jumeau numérique thermique RC
            <br>• 💧 Sécurité Gaz & Eau
            <br>• 🏢 Supervision du bâtiment
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Icônes modules
    st.markdown('<div class="section-title">📦 Modules disponibles</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">🧭</span>
        <h4>Capteurs IoT</h4>
        <p>Température, humidité, gaz, eau</p>
    </div>
    """, unsafe_allow_html=True)
    col2.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">⚙️</span>
        <h4>IA Anomalies</h4>
        <p>Analyse thermique intelligente</p>
    </div>
    """, unsafe_allow_html=True)
    col3.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">🔥</span>
        <h4>Jumeau Numérique RC</h4>
        <p>Simulation thermique dynamique</p>
    </div>
    """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    col4.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">💧</span>
        <h4>Gaz & Eau</h4>
        <p>Détection de fuites</p>
    </div>
    """, unsafe_allow_html=True)
    col5.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">🏢</span>
        <h4>Bâtiment</h4>
        <p>Zones, étages, supervision</p>
    </div>
    """, unsafe_allow_html=True)
    col6.markdown("""
    <div class="card" style="text-align:center;">
        <span style="font-size:40px;">📊</span>
        <h4>Dashboard</h4>
        <p>Vue globale du système</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PAGE CAPTEURS IoT
# -----------------------------
elif page == "🧭 Capteurs IoT":
    st.markdown('<div class="big-title">Capteurs IoT simulés</div>', unsafe_allow_html=True)

    temp = random.uniform(18, 32)
    hum = random.uniform(30, 70)
    gaz = random.choice([0, 1])
    eau = random.choice([0, 1])

    col1, col2 = st.columns(2)
    col1.metric("🌡️ Température", f"{temp:.1f} °C")
    col2.metric("💧 Humidité", f"{hum:.1f} %")

    col3, col4 = st.columns(2)
    col3.metric("🔥 Gaz", "Détection" if gaz else "OK")
    col4.metric("🚰 Eau", "Fuite" if eau else "OK")

    if st.button("🔄 Actualiser les capteurs"):
        st.experimental_rerun()

# -----------------------------
# PAGE FUITES GAZ & EAU
# -----------------------------
elif page == "💧 Fuites Gaz & Eau":
    st.markdown('<div class="big-title">Sécurité Gaz & Eau</div>', unsafe_allow_html=True)

    gaz = random.choice([0, 1])
    eau = random.choice([0, 1])

    st.markdown('<div class="section-title">🔥 Gaz</div>', unsafe_allow_html=True)
    st.error("🔥 Fuite de gaz détectée !" if gaz else "Gaz : OK")

    st.markdown('<div class="section-title">🚰 Eau</div>', unsafe_allow_html=True)
    st.error("🚰 Fuite d’eau détectée !" if eau else "Eau : OK")

# -----------------------------
# PAGE IA ANOMALIES
# -----------------------------
elif page == "⚙️ IA Anomalies":
    st.markdown('<div class="big-title">IA - Détection d’anomalies</div>', unsafe_allow_html=True)

    temp = random.uniform(15, 35)
    st.metric("Température mesurée", f"{temp:.1f} °C")

    result = detect_anomaly(temp)

    if "✔️" in result:
        st.success(result)
    else:
        st.error(result)

# -----------------------------
# PAGE BÂTIMENT — AVANCÉE + COURBES
# -----------------------------
elif page == "🏢 Bâtiment":
    st.markdown('<div class="big-title">Bâtiment intelligent</div>', unsafe_allow_html=True)

    nb_etages = st.number_input("Nombre d'étages", min_value=1, max_value=10, value=3)
    largeur_plan = st.number_input("Largeur du plan (cases)", min_value=3, max_value=10, value=5)
    hauteur_plan = st.number_input("Hauteur du plan (cases)", min_value=3, max_value=10, value=4)

    if "historique_batiment" not in st.session_state:
        st.session_state["historique_batiment"] = []

    st.markdown('<div class="section-title">📡 Capteurs par étage</div>', unsafe_allow_html=True)

    for etage in range(1, nb_etages + 1):
        st.markdown(f"""
        <div class="card">
            <h3 style="color:#4A90E2;">Étage {etage}</h3>
        """, unsafe_allow_html=True)

        heatmap = np.random.uniform(18, 32, (hauteur_plan, largeur_plan))

        capteurs = [
            ("Température", "🌡️", (0, 0)),
            ("Humidité", "💧", (hauteur_plan - 1, largeur_plan - 1)),
            ("Gaz", "🔥", (0, largeur_plan - 1)),
            ("Eau", "🚰", (hauteur_plan - 1, 0)),
        ]

        temp = random.uniform(18, 32)
        hum = random.uniform(30, 70)
        gaz = random.choice([0, 1])
        eau = random.choice([0, 1])

        col1, col2 = st.columns(2)
        col1.metric("🌡️ Température moyenne étage", f"{temp:.1f} °C")
        col2.metric("💧 Humidité moyenne étage", f"{hum:.1f} %")

        col3, col4 = st.columns(2)
        col3.metric("🔥 Gaz", "Détection" if gaz else "OK")
        col4.metric("🚰 Eau", "Fuite" if eau else "OK")

        if temp > 28 or gaz or eau:
            st.error("🤖 IA étage : Anomalie détectée.")
        else:
            st.success("🤖 IA étage : Normal.")

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(heatmap, cmap="inferno")

        for nom, icone, (y, x) in capteurs:
            ax.text(x, y, icone, ha="center", va="center", color="white", fontsize=14)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Carte thermique - Étage {etage}", color="white")

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        st.pyplot(fig)

        st.session_state["historique_batiment"].append({
            "etage": etage,
            "temp": temp,
            "hum": hum,
            "gaz": gaz,
            "eau": eau
        })

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📜 Historique des mesures</div>', unsafe_allow_html=True)

    historique = st.session_state["historique_batiment"]
    if historique:
        for record in historique[-nb_etages:]:
            st.write(
                f"• Étage {record['etage']} → "
                f"🌡️ {record['temp']:.1f} °C | "
                f"💧 {record['hum']:.1f} % | "
                f"🔥 {'Détection' if record['gaz'] else 'OK'} | "
                f"🚰 {'Fuite' if record['eau'] else 'OK'}"
            )
    else:
        st.write("Aucun historique pour l’instant.")

    if st.button("🧹 Réinitialiser l’historique"):
        st.session_state["historique_batiment"] = []
        st.success("Historique réinitialisé.")

    # -----------------------------
    # COURBES D’INTERPRÉTATION
    # -----------------------------
    st.markdown('<div class="section-title">📈 Courbes d’interprétation</div>', unsafe_allow_html=True)

    historique = st.session_state["historique_batiment"]
    if historique:
        etages = [h["etage"] for h in historique]
        temperatures = [h["temp"] for h in historique]
        humidites = [h["hum"] for h in historique]

        fig1, ax1 = plt.subplots(figsize=(6, 3))
        ax1.plot(etages, temperatures, marker='o', color='orange')
        ax1.set_title("🌡️ Température par étage")
        ax1.set_xlabel("Étage")
        ax1.set_ylabel("Température (°C)")
        ax1.grid(True)
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.plot(etages, humidites, marker='o', color='cyan')
        ax2.set_title("💧 Humidité par étage")
        ax2.set_xlabel("Étage")
        ax2.set_ylabel("Humidité (%)")
        ax2.grid(True)
        st.pyplot(fig2)

        fig3, ax3 = plt.subplots(figsize=(6, 3))
        ax3.plot(etages, temperatures, marker='o', color='orange', label="Température")
        ax3.plot(etages, humidites, marker='o', color='cyan', label="Humidité")
        ax3.set_title("📊 Température & Humidité par étage")
        ax3.set_xlabel("Étage")
        ax3.set_ylabel("Valeurs")
        ax3.legend()
        ax3.grid(True)
        st.pyplot(fig3)
    else:
        st.info("Aucune donnée disponible pour tracer les courbes.")

# -----------------------------
# PAGE JUMEAU NUMÉRIQUE RC
# -----------------------------
elif page == "🔥 Jumeau Numérique":
    st.markdown('<div class="big-title">Jumeau Numérique RC</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        C = st.number_input("Capacité thermique C", min_value=500.0, max_value=5000.0, value=1500.0)
        R = st.number_input("Résistance thermique R", min_value=0.5, max_value=10.0, value=2.5)
    with col2:
        T_ext = st.number_input("Température extérieure (°C)", min_value=-20.0, max_value=40.0, value=10.0)
        T_int = st.number_input("Température intérieure actuelle (°C)", min_value=5.0, max_value=35.0, value=22.0)

    T_new = T_int + (1/(R*C)) * (T_ext - T_int)

    st.metric("Température simulée (RC)", f"{T_new:.2f} °C")
