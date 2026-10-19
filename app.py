import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="ThermoTwin AI – IA & Jumeau numérique",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1b1b2f, #0f0f1a);
    color: #ffffff;
}
.big-title {
    font-size: 40px;
    font-weight: 900;
    color: #a18cd1;
    text-shadow: 0px 0px 10px rgba(161,140,209,0.5);
    margin-bottom: 20px;
}
.alert-card {
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    color: white;
    font-weight: 700;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
}
.alert-normal {
    background: linear-gradient(135deg, #6a5acd, #7b68ee);
}
.alert-warning {
    background: linear-gradient(135deg, #ffb347, #ffcc33);
}
.alert-danger {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
}
.card {
    padding: 14px;
    border-radius: 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DONNÉES SIMULÉES (12h)
# ---------------------------------------------------------
HVAC_DATA = [
    {"heure": "00h", "temp_depart": 72, "temp_retour": 55, "pression": 4.8, "debit": 110},
    {"heure": "01h", "temp_depart": 73, "temp_retour": 56, "pression": 4.7, "debit": 108},
    {"heure": "02h", "temp_depart": 74, "temp_retour": 56, "pression": 4.6, "debit": 107},
    {"heure": "03h", "temp_depart": 75, "temp_retour": 57, "pression": 4.5, "debit": 105},
    {"heure": "04h", "temp_depart": 76, "temp_retour": 58, "pression": 4.4, "debit": 103},
    {"heure": "05h", "temp_depart": 78, "temp_retour": 59, "pression": 4.3, "debit": 100},
    {"heure": "06h", "temp_depart": 80, "temp_retour": 60, "pression": 4.2, "debit": 98},
    {"heure": "07h", "temp_depart": 82, "temp_retour": 61, "pression": 4.1, "debit": 95},
    {"heure": "08h", "temp_depart": 84, "temp_retour": 62, "pression": 4.0, "debit": 92},
    {"heure": "09h", "temp_depart": 86, "temp_retour": 63, "pression": 3.8, "debit": 90},
    {"heure": "10h", "temp_depart": 88, "temp_retour": 64, "pression": 3.6, "debit": 88},
    {"heure": "11h", "temp_depart": 90, "temp_retour": 65, "pression": 3.4, "debit": 85},
]

FOUR_DATA = [
    {"heure": "00h", "temp": 210, "debit_gaz": 32, "pression_gaz": 4.8, "combustion": 98},
    {"heure": "01h", "temp": 215, "debit_gaz": 31, "pression_gaz": 4.7, "combustion": 97},
    {"heure": "02h", "temp": 220, "debit_gaz": 30, "pression_gaz": 4.6, "combustion": 97},
    {"heure": "03h", "temp": 225, "debit_gaz": 29, "pression_gaz": 4.5, "combustion": 96},
    {"heure": "04h", "temp": 230, "debit_gaz": 28, "pression_gaz": 4.4, "combustion": 96},
    {"heure": "05h", "temp": 235, "debit_gaz": 27, "pression_gaz": 4.3, "combustion": 95},
    {"heure": "06h", "temp": 240, "debit_gaz": 26, "pression_gaz": 4.2, "combustion": 95},
    {"heure": "07h", "temp": 250, "debit_gaz": 25, "pression_gaz": 4.1, "combustion": 94},
    {"heure": "08h", "temp": 260, "debit_gaz": 24, "pression_gaz": 4.0, "combustion": 93},
    {"heure": "09h", "temp": 275, "debit_gaz": 22, "pression_gaz": 3.7, "combustion": 92},
    {"heure": "10h", "temp": 290, "debit_gaz": 20, "pression_gaz": 3.4, "combustion": 90},
    {"heure": "11h", "temp": 305, "debit_gaz": 18, "pression_gaz": 3.1, "combustion": 88},
]

TURBINE_DATA = [
    {"heure": "00h", "rpm": 1800, "vib": 1.2, "temp": 55, "amp": 14},
    {"heure": "01h", "rpm": 1850, "vib": 1.3, "temp": 56, "amp": 15},
    {"heure": "02h", "rpm": 1900, "vib": 1.4, "temp": 57, "amp": 15},
    {"heure": "03h", "rpm": 1950, "vib": 1.5, "temp": 58, "amp": 16},
    {"heure": "04h", "rpm": 2000, "vib": 1.6, "temp": 60, "amp": 17},
    {"heure": "05h", "rpm": 2100, "vib": 1.8, "temp": 62, "amp": 18},
    {"heure": "06h", "rpm": 2200, "vib": 2.0, "temp": 65, "amp": 19},
    {"heure": "07h", "rpm": 2300, "vib": 2.2, "temp": 68, "amp": 20},
    {"heure": "08h", "rpm": 2400, "vib": 2.5, "temp": 70, "amp": 21},
    {"heure": "09h", "rpm": 2600, "vib": 3.0, "temp": 75, "amp": 22},
    {"heure": "10h", "rpm": 2800, "vib": 3.6, "temp": 80, "amp": 23},
    {"heure": "11h", "rpm": 3100, "vib": 4.2, "temp": 88, "amp": 26},
]

EAU_DATA = [
    {"heure": "00h", "pression": 3.5, "debit": 60, "niveau": 90, "fuite": 0},
    {"heure": "01h", "pression": 3.4, "debit": 62, "niveau": 89, "fuite": 0},
    {"heure": "02h", "pression": 3.3, "debit": 63, "niveau": 88, "fuite": 0},
    {"heure": "03h", "pression": 3.2, "debit": 65, "niveau": 87, "fuite": 0},
    {"heure": "04h", "pression": 3.1, "debit": 67, "niveau": 86, "fuite": 0},
    {"heure": "05h", "pression": 3.0, "debit": 70, "niveau": 85, "fuite": 0},
    {"heure": "06h", "pression": 2.9, "debit": 75, "niveau": 84, "fuite": 0},
    {"heure": "07h", "pression": 2.8, "debit": 80, "niveau": 83, "fuite": 0},
    {"heure": "08h", "pression": 2.6, "debit": 90, "niveau": 82, "fuite": 0},
    {"heure": "09h", "pression": 2.4, "debit": 110, "niveau": 80, "fuite": 1},
    {"heure": "10h", "pression": 2.2, "debit": 130, "niveau": 78, "fuite": 1},
    {"heure": "11h", "pression": 2.0, "debit": 150, "niveau": 75, "fuite": 1},
]

GAZ_DATA = [
    {"heure": "00h", "pression": 4.8, "debit": 28, "temp": 40, "fuite": 0},
    {"heure": "01h", "pression": 4.7, "debit": 27, "temp": 41, "fuite": 0},
    {"heure": "02h", "pression": 4.6, "debit": 26, "temp": 42, "fuite": 0},
    {"heure": "03h", "pression": 4.5, "debit": 25, "temp": 43, "fuite": 0},
    {"heure": "04h", "pression": 4.4, "debit": 24, "temp": 44, "fuite": 0},
    {"heure": "05h", "pression": 4.3, "debit": 23, "temp": 45, "fuite": 0},
    {"heure": "06h", "pression": 4.2, "debit": 22, "temp": 46, "fuite": 0},
    {"heure": "07h", "pression": 4.0, "debit": 20, "temp": 47, "fuite": 0},
    {"heure": "08h", "pression": 3.8, "debit": 18, "temp": 48, "fuite": 0},
    {"heure": "09h", "pression": 3.5, "debit": 15, "temp": 50, "fuite": 1},
    {"heure": "10h", "pression": 3.2, "debit": 12, "temp": 55, "fuite": 1},
    {"heure": "11h", "pression": 3.0, "debit": 10, "temp": 60, "fuite": 1},
]

EXCHANGER_DATA = [
    {"heure": "00h", "temp_chaud_in": 180, "temp_chaud_out": 150, "temp_froid_in": 40, "temp_froid_out": 70, "delta_T": 60},
    {"heure": "01h", "temp_chaud_in": 185, "temp_chaud_out": 152, "temp_froid_in": 40, "temp_froid_out": 72, "delta_T": 60},
    {"heure": "02h", "temp_chaud_in": 190, "temp_chaud_out": 155, "temp_froid_in": 41, "temp_froid_out": 74, "delta_T": 59},
    {"heure": "03h", "temp_chaud_in": 195, "temp_chaud_out": 158, "temp_froid_in": 42, "temp_froid_out": 76, "delta_T": 59},
    {"heure": "04h", "temp_chaud_in": 200, "temp_chaud_out": 160, "temp_froid_in": 43, "temp_froid_out": 78, "delta_T": 58},
    {"heure": "05h", "temp_chaud_in": 205, "temp_chaud_out": 162, "temp_froid_in": 44, "temp_froid_out": 80, "delta_T": 57},
    {"heure": "06h", "temp_chaud_in": 210, "temp_chaud_out": 165, "temp_froid_in": 45, "temp_froid_out": 82, "delta_T": 56},
    {"heure": "07h", "temp_chaud_in": 215, "temp_chaud_out": 168, "temp_froid_in": 46, "temp_froid_out": 84, "delta_T": 55},
    {"heure": "08h", "temp_chaud_in": 220, "temp_chaud_out": 170, "temp_froid_in": 47, "temp_froid_out": 86, "delta_T": 54},
    {"heure": "09h", "temp_chaud_in": 225, "temp_chaud_out": 172, "temp_froid_in": 48, "temp_froid_out": 88, "delta_T": 53},
    {"heure": "10h", "temp_chaud_in": 230, "temp_chaud_out": 175, "temp_froid_in": 49, "temp_froid_out": 90, "delta_T": 52},
    {"heure": "11h", "temp_chaud_in": 235, "temp_chaud_out": 178, "temp_froid_in": 50, "temp_froid_out": 92, "delta_T": 51},
]

# ---------------------------------------------------------
# SEUILS
# ---------------------------------------------------------
SEUILS = {
    "hvac": {"temp_depart_alerte": 85, "temp_depart_panne": 90, "pression_alerte": 3.8, "pression_panne": 3.4},
    "four": {"temp_alerte": 290, "temp_panne": 305, "combustion_alerte": 90, "combustion_panne": 88},
    "turbine": {"vib_alerte": 3.0, "vib_panne": 3.5, "temp_alerte": 80, "temp_panne": 88},
    "eau": {"pression_alerte": 2.6, "pression_panne": 2.2, "debit_alerte": 110, "debit_panne": 130},
    "gaz": {"pression_alerte": 3.5, "pression_panne": 3.2, "debit_alerte": 15, "debit_panne": 12},
    "exchanger": {"delta_T_min_alerte": 55, "delta_T_min_panne": 50}
}

# ---------------------------------------------------------
# CAPTEURS / EMPLACEMENTS
# ---------------------------------------------------------
CAPTEURS = {
    "HVAC": [
        "Sonde température départ (canalisation départ HVAC – chaufferie)",
        "Sonde température retour (canalisation retour HVAC – chaufferie)",
        "Capteur pression circuit eau chaude (collecteur principal)",
        "Débitmètre eau chaude (ligne départ vers échangeurs)"
    ],
    "Four": [
        "Thermocouple four (zone de combustion)",
        "Capteur pression gaz (collecteur gaz brûleur)",
        "Débitmètre gaz (ligne alimentation brûleur)",
        "Capteur O2 / combustion (cheminée / fumées)"
    ],
    "Turbine": [
        "Capteur vibration palier (palier avant turbine)",
        "Capteur température palier (palier arrière)",
        "Capteur RPM (arbre turbine)",
        "Capteur intensité moteur (armoire électrique)"
    ],
    "Échangeur": [
        "Sonde température fluide chaud entrée",
        "Sonde température fluide chaud sortie",
        "Sonde température fluide froid entrée",
        "Sonde température fluide froid sortie"
    ],
    "Eau": [
        "Capteur pression réseau eau (collecteur principal)",
        "Débitmètre eau (ligne distribution)",
        "Capteur niveau réservoir (cuve principale)",
        "Détecteur fuite (zone critique tuyauterie)"
    ],
    "Gaz": [
        "Capteur pression gaz (collecteur principal)",
        "Débitmètre gaz (ligne alimentation)",
        "Capteur température gaz (ligne principale)",
        "Détecteur fuite gaz (zone brûleur / collecteur)"
    ]
}

# ---------------------------------------------------------
# UTILITAIRES
# ---------------------------------------------------------
def alert_card(status, message):
    if status == "panne":
        css = "alert-danger"
    elif status == "alerte":
        css = "alert-warning"
    else:
        css = "alert-normal"
    st.markdown(f'<div class="alert-card {css}">{message}</div>', unsafe_allow_html=True)

def gauge(title, value, min_val, max_val, unit="", threshold=None, mode="high"):
    color = "#7b68ee"
    if threshold is not None:
        if mode == "high":
            if value >= threshold:
                color = "#ff4b2b"
        else:
            if value <= threshold:
                color = "#ff4b2b"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{title}</b>", 'font': {'color': 'white'}},
        number={'suffix': f" {unit}", 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [{'range': [min_val, max_val], 'color': 'rgba(255,255,255,0.05)'}],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
    return fig

# ---------------------------------------------------------
# DIAGNOSTICS
# ---------------------------------------------------------
def eval_hvac(last):
    s = SEUILS["hvac"]
    if last["temp_depart"] >= s["temp_depart_panne"] or last["pression"] <= s["pression_panne"]:
        diag = "Surchauffe circuit HVAC et chute de pression. Vérifier pompe, vanne mélange et purge d’air."
        return "panne", f"🔥 Panne HVAC : surchauffe + pression trop basse.\n🔧 {diag}"
    if last["temp_depart"] >= s["temp_depart_alerte"] or last["pression"] <= s["pression_alerte"]:
        diag = "Dérive thermique ou hydraulique. Contrôler consigne régulation, filtre et circulation."
        return "alerte", f"⚠️ Alerte HVAC : dérive thermique / pression.\n🔧 {diag}"
    return "normal", "🌿 HVAC normal.\n🔧 Paramètres dans la plage normale."

def eval_four(last):
    s = SEUILS["four"]
    if last["temp"] >= s["temp_panne"] or last["combustion"] <= s["combustion_panne"]:
        diag = "Surchauffe four et combustion dégradée. Vérifier brûleur, réglage air/gaz, encrassement échangeur."
        return "panne", f"🔥 Panne Four : surchauffe + combustion mauvaise.\n🔧 {diag}"
    if last["temp"] >= s["temp_alerte"] or last["combustion"] <= s["combustion_alerte"]:
        diag = "Risque de dérive de combustion. Ajuster ratio air/gaz, contrôler sonde O2."
        return "alerte", f"⚠️ Alerte Four : dérive thermique.\n🔧 {diag}"
    return "normal", "🌿 Four normal.\n🔧 Combustion stable, température maîtrisée."

def eval_turbine(last):
    s = SEUILS["turbine"]
    if last["vib"] >= s["vib_panne"] or last["temp"] >= s["temp_panne"]:
        diag = "Vibration élevée et température palier haute. Risque de défaillance mécanique. Vérifier roulements, alignement."
        return "panne", f"🔥 Panne Turbine : vibration + température palier.\n🔧 {diag}"
    if last["vib"] >= s["vib_alerte"] or last["temp"] >= s["temp_alerte"]:
        diag = "Dérive vibratoire ou thermique. Planifier analyse vibratoire et contrôle lubrification."
        return "alerte", f"⚠️ Alerte Turbine : dérive mécanique.\n🔧 {diag}"
    return "normal", "🌿 Turbine normale.\n🔧 Comportement mécanique stable."

def eval_eau(last):
    s = SEUILS["eau"]
    if last["pression"] <= s["pression_panne"] or last["debit"] >= s["debit_panne"] or last["fuite"] == 1:
        diag = "Suspicion de fuite eau ou chute de pression. Vérifier tuyauteries, joints, purge et niveau cuve."
        return "panne", f"💧 Panne Eau : fuite détectée / dérive forte.\n🔧 {diag}"
    if last["pression"] <= s["pression_alerte"] or last["debit"] >= s["debit_alerte"]:
        diag = "Dérive hydraulique. Contrôler pompe, vanne de régulation et éventuelles fuites."
        return "alerte", f"⚠️ Alerte Eau : dérive hydraulique.\n🔧 {diag}"
    return "normal", "🌿 Eau normale.\n🔧 Circuit eau stable."

def eval_gaz(last):
    s = SEUILS["gaz"]
    if last["pression"] <= s["pression_panne"] or last["debit"] <= s["debit_panne"] or last["fuite"] == 1:
        diag = "Risque de fuite gaz ou manque de pression. Vérifier étanchéité, vanne gaz, détecteurs."
        return "panne", f"🛢️ Panne Gaz : fuite détectée / dérive forte.\n🔧 {diag}"
    if last["pression"] <= s["pression_alerte"] or last["debit"] <= s["debit_alerte"]:
        diag = "Dérive alimentation gaz. Contrôler pression amont, filtre et régulateur."
        return "alerte", f"⚠️ Alerte Gaz : dérive gaz.\n🔧 {diag}"
    return "normal", "🌿 Gaz normal.\n🔧 Alimentation gaz correcte."

def eval_exchanger(last):
    s = SEUILS["exchanger"]
    if last["delta_T"] <= s["delta_T_min_panne"]:
        diag = "Perte de performance échangeur. Risque d’encrassement ou défaut de circulation. Nettoyage recommandé."
        return "panne", f"🔥 Panne Échangeur : delta T trop faible.\n🔧 {diag}"
    if last["delta_T"] <= s["delta_T_min_alerte"]:
        diag = "Dérive de performance. Surveiller encrassement et débit des deux circuits."
        return "alerte", f"⚠️ Alerte Échangeur : performance en baisse.\n🔧 {diag}"
    return "normal", "🌿 Échangeur normal.\n🔧 Transfert thermique correct."

# ---------------------------------------------------------
# IA PRÉDICTIVE – RISQUE INSTANTANÉ
# ---------------------------------------------------------
def compute_risks():
    hvac = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    risks = {}
    risks["HVAC"] = (
        (hvac["temp_depart"] / SEUILS["hvac"]["temp_depart_panne"]) * 0.5 +
        (SEUILS["hvac"]["pression_panne"] / hvac["pression"]) * 0.5
    )
    risks["Four"] = (
        (four["temp"] / SEUILS["four"]["temp_panne"]) * 0.6 +
        ((100 - four["combustion"]) / (100 - SEUILS["four"]["combustion_panne"])) * 0.4
    )
    risks["Turbine"] = (
        (turb["vib"] / SEUILS["turbine"]["vib_panne"]) * 0.6 +
        (turb["temp"] / SEUILS["turbine"]["temp_panne"]) * 0.4
    )
    risks["Eau"] = (
        (SEUILS["eau"]["pression_panne"] / eau["pression"]) * 0.5 +
        (eau["debit"] / SEUILS["eau"]["debit_panne"]) * 0.5
    )
    risks["Gaz"] = (
        (SEUILS["gaz"]["pression_panne"] / gaz["pression"]) * 0.5 +
        ((SEUILS["gaz"]["debit_alerte"] / max(gaz["debit"], 1)) * 0.5)
    )
    risks["Échangeur"] = (
        (SEUILS["exchanger"]["delta_T_min_panne"] / max(exch["delta_T"], 1)) * 0.8
    )

    for k in risks:
        risks[k] = max(0.0, min(1.0, risks[k]))
    return risks

def train_random_forest():
    data = []
    labels = []
    for row in HVAC_DATA:
        x = [row["temp_depart"], row["pression"], row["debit"]]
        y = int(row["temp_depart"] >= SEUILS["hvac"]["temp_depart_panne"] or row["pression"] <= SEUILS["hvac"]["pression_panne"])
        data.append(x)
        labels.append(y)
    X = np.array(data)
    y = np.array(labels)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

def predict_hvac_failure_probability(model):
    last = pd.DataFrame(HVAC_DATA).iloc[-1]
    x = np.array([[last["temp_depart"], last["pression"], last["debit"]]])
    proba = model.predict_proba(x)[0][1]
    return proba

# ---------------------------------------------------------
# JUMEAU NUMÉRIQUE – INDICATEURS
# ---------------------------------------------------------
def compute_digital_twin_indicators():
    hvac_last = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four_last = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb_last = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau_last = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz_last = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch_last = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    perf = (
        (hvac_last["debit"] / 150) * 0.3 +
        (four_last["temp"] / 305) * 0.3 +
        (turb_last["rpm"] / 3100) * 0.4
    )

    stab = (
        (1 - min(turb_last["vib"] / SEUILS["turbine"]["vib_panne"], 1)) * 0.4 +
        (1 - min(abs(hvac_last["pression"] - 4.0) / 2.0, 1)) * 0.3 +
        (1 - min(abs(four_last["combustion"] - 95) / 15, 1)) * 0.3
    )

    eff = (
        min(exch_last["delta_T"] / 60, 1) * 0.5 +
        min(four_last["combustion"] / 100, 1) * 0.5
    )

    stress = (
        min(turb_last["temp"] / 88, 1) * 0.4 +
        min(gaz_last["pression"] / 4.8, 1) * 0.3 +
        min(eau_last["debit"] / 150, 1) * 0.3
    )

    perf = max(0.0, min(1.0, perf))
    stab = max(0.0, min(1.0, stab))
    eff = max(0.0, min(1.0, eff))
    stress = max(0.0, min(1.0, stress))

    return {
        "Performance": perf,
        "Stabilité": stab,
        "Efficacité": eff,
        "Stress": stress
    }

def compute_digital_twin_timeseries():
    hvac_df = pd.DataFrame(HVAC_DATA)
    four_df = pd.DataFrame(FOUR_DATA)
    turb_df = pd.DataFrame(TURBINE_DATA)
    eau_df = pd.DataFrame(EAU_DATA)
    gaz_df = pd.DataFrame(GAZ_DATA)
    exch_df = pd.DataFrame(EXCHANGER_DATA)

    heures = hvac_df["heure"].tolist()
    perf_list, stab_list, eff_list, stress_list = [], [], [], []

    for i in range(len(heures)):
        hvac = hvac_df.iloc[i].to_dict()
        four = four_df.iloc[i].to_dict()
        turb = turb_df.iloc[i].to_dict()
        eau = eau_df.iloc[i].to_dict()
        gaz = gaz_df.iloc[i].to_dict()
        exch = exch_df.iloc[i].to_dict()

        perf = (
            (hvac["debit"] / 150) * 0.3 +
            (four["temp"] / 305) * 0.3 +
            (turb["rpm"] / 3100) * 0.4
        )
        stab = (
            (1 - min(turb["vib"] / SEUILS["turbine"]["vib_panne"], 1)) * 0.4 +
            (1 - min(abs(hvac["pression"] - 4.0) / 2.0, 1)) * 0.3 +
            (1 - min(abs(four["combustion"] - 95) / 15, 1)) * 0.3
        )
        eff = (
            min(exch["delta_T"] / 60, 1) * 0.5 +
            min(four["combustion"] / 100, 1) * 0.5
        )
        stress = (
            min(turb["temp"] / 88, 1) * 0.4 +
            min(gaz["pression"] / 4.8, 1) * 0.3 +
            min(eau["debit"] / 150, 1) * 0.3
        )

        perf_list.append(max(0.0, min(1.0, perf)))
        stab_list.append(max(0.0, min(1.0, stab)))
        eff_list.append(max(0.0, min(1.0, eff)))
        stress_list.append(max(0.0, min(1.0, stress)))

    return pd.DataFrame({
        "heure": heures,
        "Performance": perf_list,
        "Stabilité": stab_list,
        "Efficacité": eff_list,
        "Stress": stress_list
    })

# ---------------------------------------------------------
# SIDEBAR / NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("🏭 ThermoTwin AI")
st.sidebar.write("👤 Développé par Hamdi Ilhem")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "📊 Supervision globale – Pannes, solutions & capteurs",
        "🧬 Jumeau numérique – Vue complète",
        "🌬️ HVAC",
        "🔥 Four industriel",
        "🌀 Turbine à gaz",
        "💧 Circuit d’eau",
        "🛢️ Circuit de gaz",
        "🔥 Échangeur de chaleur",
        "🤖 IA – Risques globaux",
        "📍 Capteurs et emplacements",
    ]
)

# ---------------------------------------------------------
# PAGES
# ---------------------------------------------------------
if page == "🏠 Accueil":
    st.markdown('<div class="big-title">ThermoTwin AI – IA & Jumeau numérique</div>', unsafe_allow_html=True)
    st.write("Supervision HVAC, four, turbine, échangeur, eau, gaz avec IA prédictive et jumeau numérique avancé.")

    risks = compute_risks()

    def status_icon(score):
        if score >= 0.80:
            return "🔴", "Panne probable"
        elif score >= 0.50:
            return "🟠", "Début de problème"
        else:
            return "🟢", "Fonctionnement normal"

    st.subheader("📌 Statut rapide des équipements")

    equip_list = {
        "HVAC": risks["HVAC"],
        "Four": risks["Four"],
        "Turbine": risks["Turbine"],
        "Échangeur": risks["Échangeur"],
        "Eau": risks["Eau"],
        "Gaz": risks["Gaz"],
    }

    cols = st.columns(3)
    items = list(equip_list.items())
    for i, (name, score) in enumerate(items):
        icon, txt = status_icon(score)
        with cols[i % 3]:
            st.markdown(
                f'<div class="card"><b>{icon} {name}</b><br/>Score risque : {score:.2f}<br/>{txt}</div>',
                unsafe_allow_html=True
            )

elif page == "📊 Supervision globale – Pannes, solutions & capteurs":
    st.markdown('<div class="big-title">📊 Supervision globale – Pannes, solutions & capteurs</div>', unsafe_allow_html=True)

    hvac_last = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four_last = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb_last = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau_last = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz_last = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch_last = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    diag_hvac = eval_hvac(hvac_last)
    diag_four = eval_four(four_last)
    diag_turb = eval_turbine(turb_last)
    diag_eau = eval_eau(eau_last)
    diag_gaz = eval_gaz(gaz_last)
    diag_exch = eval_exchanger(exch_last)

    diagnostics = {
        "HVAC": (diag_hvac, hvac_last),
        "Four": (diag_four, four_last),
        "Turbine": (diag_turb, turb_last),
        "Eau": (diag_eau, eau_last),
        "Gaz": (diag_gaz, gaz_last),
        "Échangeur": (diag_exch, exch_last)
    }

    for equip, (diag, last_vals) in diagnostics.items():
        status, message = diag
        alert_card(status, f"<b>{equip}</b><br>{message}")

        st.markdown(f"**Capteurs {equip} :**", unsafe_allow_html=True)
        for c in CAPTEURS.get(equip, []):
            st.write(f"- {c}")

        st.markdown("### 🎛️ Dernières valeurs (gauges)")
        colA, colB, colC, colD = st.columns(4)

        with colA:
            st.plotly_chart(
                gauge("Temp départ", last_vals.get("temp_depart", 0), 0, 120, "°C",
                      SEUILS["hvac"]["temp_depart_alerte"], "high"),
                use_container_width=True,
                key=f"{equip}_temp_depart"
            )

        with colB:
            st.plotly_chart(
                gauge("Temp retour", last_vals.get("temp_retour", 0), 0, 100, "°C"),
                use_container_width=True,
                key=f"{equip}_temp_retour"
            )

        with colC:
            st.plotly_chart(
                gauge("Pression", last_vals.get("pression", 0), 0, 6, "bar",
                      SEUILS["hvac"]["pression_alerte"], "low"),
                use_container_width=True,
                key=f"{equip}_pression"
            )

        with colD:
            st.plotly_chart(
                gauge("Débit", last_vals.get("debit", 0), 0, 150, "m³/h",
                      SEUILS["eau"]["debit_alerte"], "high"),
                use_container_width=True,
                key=f"{equip}_debit"
            )

        st.markdown("---")

    st.subheader("📋 Tableau récapitulatif")
    table = []
    for equip, (diag, last_vals) in diagnostics.items():
        status, message = diag
        diag_txt = message.split("🔧")[0].strip()
        sol_txt = "🔧 " + message.split("🔧")[1].strip() if "🔧" in message else "N/A"
        table.append({
            "Équipement": equip,
            "Statut": status,
            "Diagnostic": diag_txt,
            "Solution": sol_txt
        })

    st.dataframe(pd.DataFrame(table), use_container_width=True)

elif page == "🧬 Jumeau numérique – Vue complète":
    st.markdown('<div class="big-title">🧬 Jumeau numérique – Vue complète</div>', unsafe_allow_html=True)

    indicators = compute_digital_twin_indicators()
    ts = compute_digital_twin_timeseries()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Performance", f"{indicators['Performance']:.2f}")
    with col2:
        st.metric("Stabilité", f"{indicators['Stabilité']:.2f}")
    with col3:
        st.metric("Efficacité", f"{indicators['Efficacité']:.2f}")
    with col4:
        st.metric("Stress", f"{indicators['Stress']:.2f}")

    st.subheader("📈 Courbes du jumeau numérique (12h)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Performance"], name="Performance"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Stabilité"], name="Stabilité"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Efficacité"], name="Efficacité"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Stress"], name="Stress"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font=dict(color="white"),
        xaxis_title="Heure",
        yaxis_title="Score (0–1)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Données du jumeau numérique")
    st.dataframe(ts, use_container_width=True)

elif page == "🌬️ HVAC":
    st.markdown('<div class="big-title">🌬️ Système HVAC</div>', unsafe_allow_html=True)
    df = pd.DataFrame(HVAC_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_hvac(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Temp départ", last["temp_depart"], 70, 95, "°C",
                  SEUILS["hvac"]["temp_depart_alerte"], "high"),
            use_container_width=True,
            key="hvac_page_temp_depart"
        )
    with col2:
        st.plotly_chart(
            gauge("Temp retour", last["temp_retour"], 50, 70, "°C"),
            use_container_width=True,
            key="hvac_page_temp_retour"
        )
    with col3:
        st.plotly_chart(
            gauge("Pression", last["pression"], 3.0, 5.0, "bar",
                  SEUILS["hvac"]["pression_alerte"], "low"),
            use_container_width=True,
            key="hvac_page_pression"
        )

    st.subheader("Courbes 12h – HVAC")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_depart"], name="Temp départ"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_retour"], name="Temp retour"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🔥 Four industriel":
    st.markdown('<div class="big-title">🔥 Four industriel (gaz)</div>', unsafe_allow_html=True)
    df = pd.DataFrame(FOUR_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_four(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Temp four", last["temp"], 200, 320, "°C",
                  SEUILS["four"]["temp_alerte"], "high"),
            use_container_width=True,
            key="four_page_temp"
        )
    with col2:
        st.plotly_chart(
            gauge("Pression gaz", last["pression_gaz"], 3.0, 5.0, "bar",
                  SEUILS["gaz"]["pression_alerte"], "low"),
            use_container_width=True,
            key="four_page_pression_gaz"
        )
    with col3:
        st.plotly_chart(
            gauge("Combustion", last["combustion"], 80, 100, "%",
                  SEUILS["four"]["combustion_alerte"], "low"),
            use_container_width=True,
            key="four_page_combustion"
        )

    st.subheader("Courbes 12h – Four")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp four"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["combustion"], name="Combustion"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit_gaz"], name="Débit gaz"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🌀 Turbine à gaz":
    st.markdown('<div class="big-title">🌀 Turbine à gaz</div>', unsafe_allow_html=True)
    df = pd.DataFrame(TURBINE_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_turbine(last)
    alert_card(status, msg)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(
            gauge("RPM", last["rpm"], 1800, 3200, "rpm"),
            use_container_width=True,
            key="turbine_page_rpm"
        )
    with col2:
        st.plotly_chart(
            gauge("Vibration", last["vib"], 1.0, 4.5, "mm/s",
                  SEUILS["turbine"]["vib_alerte"], "high"),
            use_container_width=True,
            key="turbine_page_vib"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp palier", last["temp"], 50, 95, "°C",
                  SEUILS["turbine"]["temp_alerte"], "high"),
            use_container_width=True,
            key="turbine_page_temp"
        )
    with col4:
        st.plotly_chart(
            gauge("Intensité", last["amp"], 10, 30, "A"),
            use_container_width=True,
            key="turbine_page_amp"
        )

    st.subheader("Courbes 12h – Turbine")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["rpm"], name="RPM"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["vib"], name="Vibration"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp palier"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "💧 Circuit d’eau":
    st.markdown('<div class="big-title">💧 Circuit d’eau</div>', unsafe_allow_html=True)
    df = pd.DataFrame(EAU_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_eau(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Pression eau", last["pression"], 2.0, 4.0, "bar",
                  SEUILS["eau"]["pression_alerte"], "low"),
            use_container_width=True,
            key="eau_page_pression"
        )
    with col2:
        st.plotly_chart(
            gauge("Débit eau", last["debit"], 50, 160, "m³/h",
                  SEUILS["eau"]["debit_alerte"], "high"),
            use_container_width=True,
            key="eau_page_debit"
        )
    with col3:
        st.plotly_chart(
            gauge("Niveau cuve", last["niveau"], 70, 100, "%"),
            use_container_width=True,
            key="eau_page_niveau"
        )

    st.subheader("Courbes 12h – Eau")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit"], name="Débit"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["niveau"], name="Niveau"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🛢️ Circuit de gaz":
    st.markdown('<div class="big-title">🛢️ Circuit de gaz</div>', unsafe_allow_html=True)
    df = pd.DataFrame(GAZ_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_gaz(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Pression gaz", last["pression"], 3.0, 5.0, "bar",
                  SEUILS["gaz"]["pression_alerte"], "low"),
            use_container_width=True,
            key="gaz_page_pression"
        )
    with col2:
        st.plotly_chart(
            gauge("Débit gaz", last["debit"], 10, 35, "m³/h",
                  SEUILS["gaz"]["debit_alerte"], "low"),
            use_container_width=True,
            key="gaz_page_debit"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp gaz", last["temp"], 40, 70, "°C"),
            use_container_width=True,
            key="gaz_page_temp"
        )

    st.subheader("Courbes 12h – Gaz")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit"], name="Débit"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🔥 Échangeur de chaleur":
    st.markdown('<div class="big-title">🔥 Échangeur de chaleur</div>', unsafe_allow_html=True)
    df = pd.DataFrame(EXCHANGER_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_exchanger(last)
    alert_card(status, msg)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(
            gauge("Temp chaud in", last["temp_chaud_in"], 180, 240, "°C"),
            use_container_width=True,
            key="exch_page_temp_chaud_in"
        )
    with col2:
        st.plotly_chart(
            gauge("Temp chaud out", last["temp_chaud_out"], 150, 200, "°C"),
            use_container_width=True,
            key="exch_page_temp_chaud_out"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp froid in", last["temp_froid_in"], 40, 55, "°C"),
            use_container_width=True,
            key="exch_page_temp_froid_in"
        )
    with col4:
        st.plotly_chart(
            gauge("Temp froid out", last["temp_froid_out"], 70, 95, "°C"),
            use_container_width=True,
            key="exch_page_temp_froid_out"
        )

    st.subheader("Courbes 12h – Échangeur")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_chaud_in"], name="Temp chaud in"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_chaud_out"], name="Temp chaud out"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_froid_in"], name="Temp froid in"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_froid_out"], name="Temp froid out"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["delta_T"], name="ΔT", line=dict(width=4)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🤖 IA – Risques globaux":
    st.markdown('<div class="big-title">🤖 IA – Risques globaux</div>', unsafe_allow_html=True)
    risks = compute_risks()

    st.subheader("Diagramme radar – comparaison des risques instantanés")
    categories = ["HVAC", "Four", "Turbine", "Échangeur", "Eau", "Gaz"]
    values = [risks[c] for c in categories]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Risques'
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.05)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.2)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="radar_risques")

    st.subheader("RandomForest – Probabilité de panne HVAC")
    rf_model = train_random_forest()
    proba = predict_hvac_failure_probability(rf_model)
    st.write(f"Probabilité prédite de panne HVAC (RandomForest) : **{proba:.2f}**")

    st.write("Scores de risques (0 = aucun, 1 = très élevé) :")
    st.json(risks)

elif page == "📍 Capteurs et emplacements":
    st.markdown('<div class="big-title">📍 Capteurs et emplacements</div>', unsafe_allow_html=True)
    for equip, caps in CAPTEURS.items():
        st.subheader(equip)
        for c in caps:
            st.write(f"- {c}")
        st.markdown("---")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="ThermoTwin AI – IA & Jumeau numérique",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1b1b2f, #0f0f1a);
    color: #ffffff;
}
.big-title {
    font-size: 40px;
    font-weight: 900;
    color: #a18cd1;
    text-shadow: 0px 0px 10px rgba(161,140,209,0.5);
    margin-bottom: 20px;
}
.alert-card {
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    color: white;
    font-weight: 700;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
}
.alert-normal {
    background: linear-gradient(135deg, #6a5acd, #7b68ee);
}
.alert-warning {
    background: linear-gradient(135deg, #ffb347, #ffcc33);
}
.alert-danger {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
}
.card {
    padding: 14px;
    border-radius: 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DONNÉES SIMULÉES (12h)
# ---------------------------------------------------------
HVAC_DATA = [
    {"heure": "00h", "temp_depart": 72, "temp_retour": 55, "pression": 4.8, "debit": 110},
    {"heure": "01h", "temp_depart": 73, "temp_retour": 56, "pression": 4.7, "debit": 108},
    {"heure": "02h", "temp_depart": 74, "temp_retour": 56, "pression": 4.6, "debit": 107},
    {"heure": "03h", "temp_depart": 75, "temp_retour": 57, "pression": 4.5, "debit": 105},
    {"heure": "04h", "temp_depart": 76, "temp_retour": 58, "pression": 4.4, "debit": 103},
    {"heure": "05h", "temp_depart": 78, "temp_retour": 59, "pression": 4.3, "debit": 100},
    {"heure": "06h", "temp_depart": 80, "temp_retour": 60, "pression": 4.2, "debit": 98},
    {"heure": "07h", "temp_depart": 82, "temp_retour": 61, "pression": 4.1, "debit": 95},
    {"heure": "08h", "temp_depart": 84, "temp_retour": 62, "pression": 4.0, "debit": 92},
    {"heure": "09h", "temp_depart": 86, "temp_retour": 63, "pression": 3.8, "debit": 90},
    {"heure": "10h", "temp_depart": 88, "temp_retour": 64, "pression": 3.6, "debit": 88},
    {"heure": "11h", "temp_depart": 90, "temp_retour": 65, "pression": 3.4, "debit": 85},
]

FOUR_DATA = [
    {"heure": "00h", "temp": 210, "debit_gaz": 32, "pression_gaz": 4.8, "combustion": 98},
    {"heure": "01h", "temp": 215, "debit_gaz": 31, "pression_gaz": 4.7, "combustion": 97},
    {"heure": "02h", "temp": 220, "debit_gaz": 30, "pression_gaz": 4.6, "combustion": 97},
    {"heure": "03h", "temp": 225, "debit_gaz": 29, "pression_gaz": 4.5, "combustion": 96},
    {"heure": "04h", "temp": 230, "debit_gaz": 28, "pression_gaz": 4.4, "combustion": 96},
    {"heure": "05h", "temp": 235, "debit_gaz": 27, "pression_gaz": 4.3, "combustion": 95},
    {"heure": "06h", "temp": 240, "debit_gaz": 26, "pression_gaz": 4.2, "combustion": 95},
    {"heure": "07h", "temp": 250, "debit_gaz": 25, "pression_gaz": 4.1, "combustion": 94},
    {"heure": "08h", "temp": 260, "debit_gaz": 24, "pression_gaz": 4.0, "combustion": 93},
    {"heure": "09h", "temp": 275, "debit_gaz": 22, "pression_gaz": 3.7, "combustion": 92},
    {"heure": "10h", "temp": 290, "debit_gaz": 20, "pression_gaz": 3.4, "combustion": 90},
    {"heure": "11h", "temp": 305, "debit_gaz": 18, "pression_gaz": 3.1, "combustion": 88},
]

TURBINE_DATA = [
    {"heure": "00h", "rpm": 1800, "vib": 1.2, "temp": 55, "amp": 14},
    {"heure": "01h", "rpm": 1850, "vib": 1.3, "temp": 56, "amp": 15},
    {"heure": "02h", "rpm": 1900, "vib": 1.4, "temp": 57, "amp": 15},
    {"heure": "03h", "rpm": 1950, "vib": 1.5, "temp": 58, "amp": 16},
    {"heure": "04h", "rpm": 2000, "vib": 1.6, "temp": 60, "amp": 17},
    {"heure": "05h", "rpm": 2100, "vib": 1.8, "temp": 62, "amp": 18},
    {"heure": "06h", "rpm": 2200, "vib": 2.0, "temp": 65, "amp": 19},
    {"heure": "07h", "rpm": 2300, "vib": 2.2, "temp": 68, "amp": 20},
    {"heure": "08h", "rpm": 2400, "vib": 2.5, "temp": 70, "amp": 21},
    {"heure": "09h", "rpm": 2600, "vib": 3.0, "temp": 75, "amp": 22},
    {"heure": "10h", "rpm": 2800, "vib": 3.6, "temp": 80, "amp": 23},
    {"heure": "11h", "rpm": 3100, "vib": 4.2, "temp": 88, "amp": 26},
]

EAU_DATA = [
    {"heure": "00h", "pression": 3.5, "debit": 60, "niveau": 90, "fuite": 0},
    {"heure": "01h", "pression": 3.4, "debit": 62, "niveau": 89, "fuite": 0},
    {"heure": "02h", "pression": 3.3, "debit": 63, "niveau": 88, "fuite": 0},
    {"heure": "03h", "pression": 3.2, "debit": 65, "niveau": 87, "fuite": 0},
    {"heure": "04h", "pression": 3.1, "debit": 67, "niveau": 86, "fuite": 0},
    {"heure": "05h", "pression": 3.0, "debit": 70, "niveau": 85, "fuite": 0},
    {"heure": "06h", "pression": 2.9, "debit": 75, "niveau": 84, "fuite": 0},
    {"heure": "07h", "pression": 2.8, "debit": 80, "niveau": 83, "fuite": 0},
    {"heure": "08h", "pression": 2.6, "debit": 90, "niveau": 82, "fuite": 0},
    {"heure": "09h", "pression": 2.4, "debit": 110, "niveau": 80, "fuite": 1},
    {"heure": "10h", "pression": 2.2, "debit": 130, "niveau": 78, "fuite": 1},
    {"heure": "11h", "pression": 2.0, "debit": 150, "niveau": 75, "fuite": 1},
]

GAZ_DATA = [
    {"heure": "00h", "pression": 4.8, "debit": 28, "temp": 40, "fuite": 0},
    {"heure": "01h", "pression": 4.7, "debit": 27, "temp": 41, "fuite": 0},
    {"heure": "02h", "pression": 4.6, "debit": 26, "temp": 42, "fuite": 0},
    {"heure": "03h", "pression": 4.5, "debit": 25, "temp": 43, "fuite": 0},
    {"heure": "04h", "pression": 4.4, "debit": 24, "temp": 44, "fuite": 0},
    {"heure": "05h", "pression": 4.3, "debit": 23, "temp": 45, "fuite": 0},
    {"heure": "06h", "pression": 4.2, "debit": 22, "temp": 46, "fuite": 0},
    {"heure": "07h", "pression": 4.0, "debit": 20, "temp": 47, "fuite": 0},
    {"heure": "08h", "pression": 3.8, "debit": 18, "temp": 48, "fuite": 0},
    {"heure": "09h", "pression": 3.5, "debit": 15, "temp": 50, "fuite": 1},
    {"heure": "10h", "pression": 3.2, "debit": 12, "temp": 55, "fuite": 1},
    {"heure": "11h", "pression": 3.0, "debit": 10, "temp": 60, "fuite": 1},
]

EXCHANGER_DATA = [
    {"heure": "00h", "temp_chaud_in": 180, "temp_chaud_out": 150, "temp_froid_in": 40, "temp_froid_out": 70, "delta_T": 60},
    {"heure": "01h", "temp_chaud_in": 185, "temp_chaud_out": 152, "temp_froid_in": 40, "temp_froid_out": 72, "delta_T": 60},
    {"heure": "02h", "temp_chaud_in": 190, "temp_chaud_out": 155, "temp_froid_in": 41, "temp_froid_out": 74, "delta_T": 59},
    {"heure": "03h", "temp_chaud_in": 195, "temp_chaud_out": 158, "temp_froid_in": 42, "temp_froid_out": 76, "delta_T": 59},
    {"heure": "04h", "temp_chaud_in": 200, "temp_chaud_out": 160, "temp_froid_in": 43, "temp_froid_out": 78, "delta_T": 58},
    {"heure": "05h", "temp_chaud_in": 205, "temp_chaud_out": 162, "temp_froid_in": 44, "temp_froid_out": 80, "delta_T": 57},
    {"heure": "06h", "temp_chaud_in": 210, "temp_chaud_out": 165, "temp_froid_in": 45, "temp_froid_out": 82, "delta_T": 56},
    {"heure": "07h", "temp_chaud_in": 215, "temp_chaud_out": 168, "temp_froid_in": 46, "temp_froid_out": 84, "delta_T": 55},
    {"heure": "08h", "temp_chaud_in": 220, "temp_chaud_out": 170, "temp_froid_in": 47, "temp_froid_out": 86, "delta_T": 54},
    {"heure": "09h", "temp_chaud_in": 225, "temp_chaud_out": 172, "temp_froid_in": 48, "temp_froid_out": 88, "delta_T": 53},
    {"heure": "10h", "temp_chaud_in": 230, "temp_chaud_out": 175, "temp_froid_in": 49, "temp_froid_out": 90, "delta_T": 52},
    {"heure": "11h", "temp_chaud_in": 235, "temp_chaud_out": 178, "temp_froid_in": 50, "temp_froid_out": 92, "delta_T": 51},
]

# ---------------------------------------------------------
# SEUILS
# ---------------------------------------------------------
SEUILS = {
    "hvac": {"temp_depart_alerte": 85, "temp_depart_panne": 90, "pression_alerte": 3.8, "pression_panne": 3.4},
    "four": {"temp_alerte": 290, "temp_panne": 305, "combustion_alerte": 90, "combustion_panne": 88},
    "turbine": {"vib_alerte": 3.0, "vib_panne": 3.5, "temp_alerte": 80, "temp_panne": 88},
    "eau": {"pression_alerte": 2.6, "pression_panne": 2.2, "debit_alerte": 110, "debit_panne": 130},
    "gaz": {"pression_alerte": 3.5, "pression_panne": 3.2, "debit_alerte": 15, "debit_panne": 12},
    "exchanger": {"delta_T_min_alerte": 55, "delta_T_min_panne": 50}
}

# ---------------------------------------------------------
# CAPTEURS / EMPLACEMENTS
# ---------------------------------------------------------
CAPTEURS = {
    "HVAC": [
        "Sonde température départ (canalisation départ HVAC – chaufferie)",
        "Sonde température retour (canalisation retour HVAC – chaufferie)",
        "Capteur pression circuit eau chaude (collecteur principal)",
        "Débitmètre eau chaude (ligne départ vers échangeurs)"
    ],
    "Four": [
        "Thermocouple four (zone de combustion)",
        "Capteur pression gaz (collecteur gaz brûleur)",
        "Débitmètre gaz (ligne alimentation brûleur)",
        "Capteur O2 / combustion (cheminée / fumées)"
    ],
    "Turbine": [
        "Capteur vibration palier (palier avant turbine)",
        "Capteur température palier (palier arrière)",
        "Capteur RPM (arbre turbine)",
        "Capteur intensité moteur (armoire électrique)"
    ],
    "Échangeur": [
        "Sonde température fluide chaud entrée",
        "Sonde température fluide chaud sortie",
        "Sonde température fluide froid entrée",
        "Sonde température fluide froid sortie"
    ],
    "Eau": [
        "Capteur pression réseau eau (collecteur principal)",
        "Débitmètre eau (ligne distribution)",
        "Capteur niveau réservoir (cuve principale)",
        "Détecteur fuite (zone critique tuyauterie)"
    ],
    "Gaz": [
        "Capteur pression gaz (collecteur principal)",
        "Débitmètre gaz (ligne alimentation)",
        "Capteur température gaz (ligne principale)",
        "Détecteur fuite gaz (zone brûleur / collecteur)"
    ]
}

# ---------------------------------------------------------
# UTILITAIRES
# ---------------------------------------------------------
def alert_card(status, message):
    if status == "panne":
        css = "alert-danger"
    elif status == "alerte":
        css = "alert-warning"
    else:
        css = "alert-normal"
    st.markdown(f'<div class="alert-card {css}">{message}</div>', unsafe_allow_html=True)

def gauge(title, value, min_val, max_val, unit="", threshold=None, mode="high"):
    color = "#7b68ee"
    if threshold is not None:
        if mode == "high":
            if value >= threshold:
                color = "#ff4b2b"
        else:
            if value <= threshold:
                color = "#ff4b2b"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{title}</b>", 'font': {'color': 'white'}},
        number={'suffix': f" {unit}", 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [{'range': [min_val, max_val], 'color': 'rgba(255,255,255,0.05)'}],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
    return fig

# ---------------------------------------------------------
# DIAGNOSTICS
# ---------------------------------------------------------
def eval_hvac(last):
    s = SEUILS["hvac"]
    if last["temp_depart"] >= s["temp_depart_panne"] or last["pression"] <= s["pression_panne"]:
        diag = "Surchauffe circuit HVAC et chute de pression. Vérifier pompe, vanne mélange et purge d’air."
        return "panne", f"🔥 Panne HVAC : surchauffe + pression trop basse.\n🔧 {diag}"
    if last["temp_depart"] >= s["temp_depart_alerte"] or last["pression"] <= s["pression_alerte"]:
        diag = "Dérive thermique ou hydraulique. Contrôler consigne régulation, filtre et circulation."
        return "alerte", f"⚠️ Alerte HVAC : dérive thermique / pression.\n🔧 {diag}"
    return "normal", "🌿 HVAC normal.\n🔧 Paramètres dans la plage normale."

def eval_four(last):
    s = SEUILS["four"]
    if last["temp"] >= s["temp_panne"] or last["combustion"] <= s["combustion_panne"]:
        diag = "Surchauffe four et combustion dégradée. Vérifier brûleur, réglage air/gaz, encrassement échangeur."
        return "panne", f"🔥 Panne Four : surchauffe + combustion mauvaise.\n🔧 {diag}"
    if last["temp"] >= s["temp_alerte"] or last["combustion"] <= s["combustion_alerte"]:
        diag = "Risque de dérive de combustion. Ajuster ratio air/gaz, contrôler sonde O2."
        return "alerte", f"⚠️ Alerte Four : dérive thermique.\n🔧 {diag}"
    return "normal", "🌿 Four normal.\n🔧 Combustion stable, température maîtrisée."

def eval_turbine(last):
    s = SEUILS["turbine"]
    if last["vib"] >= s["vib_panne"] or last["temp"] >= s["temp_panne"]:
        diag = "Vibration élevée et température palier haute. Risque de défaillance mécanique. Vérifier roulements, alignement."
        return "panne", f"🔥 Panne Turbine : vibration + température palier.\n🔧 {diag}"
    if last["vib"] >= s["vib_alerte"] or last["temp"] >= s["temp_alerte"]:
        diag = "Dérive vibratoire ou thermique. Planifier analyse vibratoire et contrôle lubrification."
        return "alerte", f"⚠️ Alerte Turbine : dérive mécanique.\n🔧 {diag}"
    return "normal", "🌿 Turbine normale.\n🔧 Comportement mécanique stable."

def eval_eau(last):
    s = SEUILS["eau"]
    if last["pression"] <= s["pression_panne"] or last["debit"] >= s["debit_panne"] or last["fuite"] == 1:
        diag = "Suspicion de fuite eau ou chute de pression. Vérifier tuyauteries, joints, purge et niveau cuve."
        return "panne", f"💧 Panne Eau : fuite détectée / dérive forte.\n🔧 {diag}"
    if last["pression"] <= s["pression_alerte"] or last["debit"] >= s["debit_alerte"]:
        diag = "Dérive hydraulique. Contrôler pompe, vanne de régulation et éventuelles fuites."
        return "alerte", f"⚠️ Alerte Eau : dérive hydraulique.\n🔧 {diag}"
    return "normal", "🌿 Eau normale.\n🔧 Circuit eau stable."

def eval_gaz(last):
    s = SEUILS["gaz"]
    if last["pression"] <= s["pression_panne"] or last["debit"] <= s["debit_panne"] or last["fuite"] == 1:
        diag = "Risque de fuite gaz ou manque de pression. Vérifier étanchéité, vanne gaz, détecteurs."
        return "panne", f"🛢️ Panne Gaz : fuite détectée / dérive forte.\n🔧 {diag}"
    if last["pression"] <= s["pression_alerte"] or last["debit"] <= s["debit_alerte"]:
        diag = "Dérive alimentation gaz. Contrôler pression amont, filtre et régulateur."
        return "alerte", f"⚠️ Alerte Gaz : dérive gaz.\n🔧 {diag}"
    return "normal", "🌿 Gaz normal.\n🔧 Alimentation gaz correcte."

def eval_exchanger(last):
    s = SEUILS["exchanger"]
    if last["delta_T"] <= s["delta_T_min_panne"]:
        diag = "Perte de performance échangeur. Risque d’encrassement ou défaut de circulation. Nettoyage recommandé."
        return "panne", f"🔥 Panne Échangeur : delta T trop faible.\n🔧 {diag}"
    if last["delta_T"] <= s["delta_T_min_alerte"]:
        diag = "Dérive de performance. Surveiller encrassement et débit des deux circuits."
        return "alerte", f"⚠️ Alerte Échangeur : performance en baisse.\n🔧 {diag}"
    return "normal", "🌿 Échangeur normal.\n🔧 Transfert thermique correct."

# ---------------------------------------------------------
# IA PRÉDICTIVE – RISQUE INSTANTANÉ
# ---------------------------------------------------------
def compute_risks():
    hvac = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    risks = {}
    risks["HVAC"] = (
        (hvac["temp_depart"] / SEUILS["hvac"]["temp_depart_panne"]) * 0.5 +
        (SEUILS["hvac"]["pression_panne"] / hvac["pression"]) * 0.5
    )
    risks["Four"] = (
        (four["temp"] / SEUILS["four"]["temp_panne"]) * 0.6 +
        ((100 - four["combustion"]) / (100 - SEUILS["four"]["combustion_panne"])) * 0.4
    )
    risks["Turbine"] = (
        (turb["vib"] / SEUILS["turbine"]["vib_panne"]) * 0.6 +
        (turb["temp"] / SEUILS["turbine"]["temp_panne"]) * 0.4
    )
    risks["Eau"] = (
        (SEUILS["eau"]["pression_panne"] / eau["pression"]) * 0.5 +
        (eau["debit"] / SEUILS["eau"]["debit_panne"]) * 0.5
    )
    risks["Gaz"] = (
        (SEUILS["gaz"]["pression_panne"] / gaz["pression"]) * 0.5 +
        ((SEUILS["gaz"]["debit_alerte"] / max(gaz["debit"], 1)) * 0.5)
    )
    risks["Échangeur"] = (
        (SEUILS["exchanger"]["delta_T_min_panne"] / max(exch["delta_T"], 1)) * 0.8
    )

    for k in risks:
        risks[k] = max(0.0, min(1.0, risks[k]))
    return risks

def train_random_forest():
    data = []
    labels = []
    for row in HVAC_DATA:
        x = [row["temp_depart"], row["pression"], row["debit"]]
        y = int(row["temp_depart"] >= SEUILS["hvac"]["temp_depart_panne"] or row["pression"] <= SEUILS["hvac"]["pression_panne"])
        data.append(x)
        labels.append(y)
    X = np.array(data)
    y = np.array(labels)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

def predict_hvac_failure_probability(model):
    last = pd.DataFrame(HVAC_DATA).iloc[-1]
    x = np.array([[last["temp_depart"], last["pression"], last["debit"]]])
    proba = model.predict_proba(x)[0][1]
    return proba

# ---------------------------------------------------------
# JUMEAU NUMÉRIQUE – INDICATEURS
# ---------------------------------------------------------
def compute_digital_twin_indicators():
    hvac_last = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four_last = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb_last = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau_last = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz_last = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch_last = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    perf = (
        (hvac_last["debit"] / 150) * 0.3 +
        (four_last["temp"] / 305) * 0.3 +
        (turb_last["rpm"] / 3100) * 0.4
    )

    stab = (
        (1 - min(turb_last["vib"] / SEUILS["turbine"]["vib_panne"], 1)) * 0.4 +
        (1 - min(abs(hvac_last["pression"] - 4.0) / 2.0, 1)) * 0.3 +
        (1 - min(abs(four_last["combustion"] - 95) / 15, 1)) * 0.3
    )

    eff = (
        min(exch_last["delta_T"] / 60, 1) * 0.5 +
        min(four_last["combustion"] / 100, 1) * 0.5
    )

    stress = (
        min(turb_last["temp"] / 88, 1) * 0.4 +
        min(gaz_last["pression"] / 4.8, 1) * 0.3 +
        min(eau_last["debit"] / 150, 1) * 0.3
    )

    perf = max(0.0, min(1.0, perf))
    stab = max(0.0, min(1.0, stab))
    eff = max(0.0, min(1.0, eff))
    stress = max(0.0, min(1.0, stress))

    return {
        "Performance": perf,
        "Stabilité": stab,
        "Efficacité": eff,
        "Stress": stress
    }

def compute_digital_twin_timeseries():
    hvac_df = pd.DataFrame(HVAC_DATA)
    four_df = pd.DataFrame(FOUR_DATA)
    turb_df = pd.DataFrame(TURBINE_DATA)
    eau_df = pd.DataFrame(EAU_DATA)
    gaz_df = pd.DataFrame(GAZ_DATA)
    exch_df = pd.DataFrame(EXCHANGER_DATA)

    heures = hvac_df["heure"].tolist()
    perf_list, stab_list, eff_list, stress_list = [], [], [], []

    for i in range(len(heures)):
        hvac = hvac_df.iloc[i].to_dict()
        four = four_df.iloc[i].to_dict()
        turb = turb_df.iloc[i].to_dict()
        eau = eau_df.iloc[i].to_dict()
        gaz = gaz_df.iloc[i].to_dict()
        exch = exch_df.iloc[i].to_dict()

        perf = (
            (hvac["debit"] / 150) * 0.3 +
            (four["temp"] / 305) * 0.3 +
            (turb["rpm"] / 3100) * 0.4
        )
        stab = (
            (1 - min(turb["vib"] / SEUILS["turbine"]["vib_panne"], 1)) * 0.4 +
            (1 - min(abs(hvac["pression"] - 4.0) / 2.0, 1)) * 0.3 +
            (1 - min(abs(four["combustion"] - 95) / 15, 1)) * 0.3
        )
        eff = (
            min(exch["delta_T"] / 60, 1) * 0.5 +
            min(four["combustion"] / 100, 1) * 0.5
        )
        stress = (
            min(turb["temp"] / 88, 1) * 0.4 +
            min(gaz["pression"] / 4.8, 1) * 0.3 +
            min(eau["debit"] / 150, 1) * 0.3
        )

        perf_list.append(max(0.0, min(1.0, perf)))
        stab_list.append(max(0.0, min(1.0, stab)))
        eff_list.append(max(0.0, min(1.0, eff)))
        stress_list.append(max(0.0, min(1.0, stress)))

    return pd.DataFrame({
        "heure": heures,
        "Performance": perf_list,
        "Stabilité": stab_list,
        "Efficacité": eff_list,
        "Stress": stress_list
    })

# ---------------------------------------------------------
# SIDEBAR / NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("🏭 ThermoTwin AI")
st.sidebar.write("👤 Développé par Hamdi Ilhem")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "📊 Supervision globale – Pannes, solutions & capteurs",
        "🧬 Jumeau numérique – Vue complète",
        "🌬️ HVAC",
        "🔥 Four industriel",
        "🌀 Turbine à gaz",
        "💧 Circuit d’eau",
        "🛢️ Circuit de gaz",
        "🔥 Échangeur de chaleur",
        "🤖 IA – Risques globaux",
        "📍 Capteurs et emplacements",
    ]
)

# ---------------------------------------------------------
# PAGES
# ---------------------------------------------------------
if page == "🏠 Accueil":
    st.markdown('<div class="big-title">ThermoTwin AI – IA & Jumeau numérique</div>', unsafe_allow_html=True)
    st.write("Supervision HVAC, four, turbine, échangeur, eau, gaz avec IA prédictive et jumeau numérique avancé.")

    risks = compute_risks()

    def status_icon(score):
        if score >= 0.80:
            return "🔴", "Panne probable"
        elif score >= 0.50:
            return "🟠", "Début de problème"
        else:
            return "🟢", "Fonctionnement normal"

    st.subheader("📌 Statut rapide des équipements")

    equip_list = {
        "HVAC": risks["HVAC"],
        "Four": risks["Four"],
        "Turbine": risks["Turbine"],
        "Échangeur": risks["Échangeur"],
        "Eau": risks["Eau"],
        "Gaz": risks["Gaz"],
    }

    cols = st.columns(3)
    items = list(equip_list.items())
    for i, (name, score) in enumerate(items):
        icon, txt = status_icon(score)
        with cols[i % 3]:
            st.markdown(
                f'<div class="card"><b>{icon} {name}</b><br/>Score risque : {score:.2f}<br/>{txt}</div>',
                unsafe_allow_html=True
            )

elif page == "📊 Supervision globale – Pannes, solutions & capteurs":
    st.markdown('<div class="big-title">📊 Supervision globale – Pannes, solutions & capteurs</div>', unsafe_allow_html=True)

    hvac_last = pd.DataFrame(HVAC_DATA).iloc[-1].to_dict()
    four_last = pd.DataFrame(FOUR_DATA).iloc[-1].to_dict()
    turb_last = pd.DataFrame(TURBINE_DATA).iloc[-1].to_dict()
    eau_last = pd.DataFrame(EAU_DATA).iloc[-1].to_dict()
    gaz_last = pd.DataFrame(GAZ_DATA).iloc[-1].to_dict()
    exch_last = pd.DataFrame(EXCHANGER_DATA).iloc[-1].to_dict()

    diag_hvac = eval_hvac(hvac_last)
    diag_four = eval_four(four_last)
    diag_turb = eval_turbine(turb_last)
    diag_eau = eval_eau(eau_last)
    diag_gaz = eval_gaz(gaz_last)
    diag_exch = eval_exchanger(exch_last)

    diagnostics = {
        "HVAC": (diag_hvac, hvac_last),
        "Four": (diag_four, four_last),
        "Turbine": (diag_turb, turb_last),
        "Eau": (diag_eau, eau_last),
        "Gaz": (diag_gaz, gaz_last),
        "Échangeur": (diag_exch, exch_last)
    }

    for equip, (diag, last_vals) in diagnostics.items():
        status, message = diag
        alert_card(status, f"<b>{equip}</b><br>{message}")

        st.markdown(f"**Capteurs {equip} :**", unsafe_allow_html=True)
        for c in CAPTEURS.get(equip, []):
            st.write(f"- {c}")

        st.markdown("### 🎛️ Dernières valeurs (gauges)")
        colA, colB, colC, colD = st.columns(4)

        with colA:
            st.plotly_chart(
                gauge("Temp départ", last_vals.get("temp_depart", 0), 0, 120, "°C",
                      SEUILS["hvac"]["temp_depart_alerte"], "high"),
                use_container_width=True,
                key=f"{equip}_temp_depart"
            )

        with colB:
            st.plotly_chart(
                gauge("Temp retour", last_vals.get("temp_retour", 0), 0, 100, "°C"),
                use_container_width=True,
                key=f"{equip}_temp_retour"
            )

        with colC:
            st.plotly_chart(
                gauge("Pression", last_vals.get("pression", 0), 0, 6, "bar",
                      SEUILS["hvac"]["pression_alerte"], "low"),
                use_container_width=True,
                key=f"{equip}_pression"
            )

        with colD:
            st.plotly_chart(
                gauge("Débit", last_vals.get("debit", 0), 0, 150, "m³/h",
                      SEUILS["eau"]["debit_alerte"], "high"),
                use_container_width=True,
                key=f"{equip}_debit"
            )

        st.markdown("---")

    st.subheader("📋 Tableau récapitulatif")
    table = []
    for equip, (diag, last_vals) in diagnostics.items():
        status, message = diag
        diag_txt = message.split("🔧")[0].strip()
        sol_txt = "🔧 " + message.split("🔧")[1].strip() if "🔧" in message else "N/A"
        table.append({
            "Équipement": equip,
            "Statut": status,
            "Diagnostic": diag_txt,
            "Solution": sol_txt
        })

    st.dataframe(pd.DataFrame(table), use_container_width=True)

elif page == "🧬 Jumeau numérique – Vue complète":
    st.markdown('<div class="big-title">🧬 Jumeau numérique – Vue complète</div>', unsafe_allow_html=True)

    indicators = compute_digital_twin_indicators()
    ts = compute_digital_twin_timeseries()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Performance", f"{indicators['Performance']:.2f}")
    with col2:
        st.metric("Stabilité", f"{indicators['Stabilité']:.2f}")
    with col3:
        st.metric("Efficacité", f"{indicators['Efficacité']:.2f}")
    with col4:
        st.metric("Stress", f"{indicators['Stress']:.2f}")

    st.subheader("📈 Courbes du jumeau numérique (12h)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Performance"], name="Performance"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Stabilité"], name="Stabilité"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Efficacité"], name="Efficacité"))
    fig.add_trace(go.Scatter(x=ts["heure"], y=ts["Stress"], name="Stress"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font=dict(color="white"),
        xaxis_title="Heure",
        yaxis_title="Score (0–1)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Données du jumeau numérique")
    st.dataframe(ts, use_container_width=True)

elif page == "🌬️ HVAC":
    st.markdown('<div class="big-title">🌬️ Système HVAC</div>', unsafe_allow_html=True)
    df = pd.DataFrame(HVAC_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_hvac(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Temp départ", last["temp_depart"], 70, 95, "°C",
                  SEUILS["hvac"]["temp_depart_alerte"], "high"),
            use_container_width=True,
            key="hvac_page_temp_depart"
        )
    with col2:
        st.plotly_chart(
            gauge("Temp retour", last["temp_retour"], 50, 70, "°C"),
            use_container_width=True,
            key="hvac_page_temp_retour"
        )
    with col3:
        st.plotly_chart(
            gauge("Pression", last["pression"], 3.0, 5.0, "bar",
                  SEUILS["hvac"]["pression_alerte"], "low"),
            use_container_width=True,
            key="hvac_page_pression"
        )

    st.subheader("Courbes 12h – HVAC")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_depart"], name="Temp départ"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_retour"], name="Temp retour"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🔥 Four industriel":
    st.markdown('<div class="big-title">🔥 Four industriel (gaz)</div>', unsafe_allow_html=True)
    df = pd.DataFrame(FOUR_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_four(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Temp four", last["temp"], 200, 320, "°C",
                  SEUILS["four"]["temp_alerte"], "high"),
            use_container_width=True,
            key="four_page_temp"
        )
    with col2:
        st.plotly_chart(
            gauge("Pression gaz", last["pression_gaz"], 3.0, 5.0, "bar",
                  SEUILS["gaz"]["pression_alerte"], "low"),
            use_container_width=True,
            key="four_page_pression_gaz"
        )
    with col3:
        st.plotly_chart(
            gauge("Combustion", last["combustion"], 80, 100, "%",
                  SEUILS["four"]["combustion_alerte"], "low"),
            use_container_width=True,
            key="four_page_combustion"
        )

    st.subheader("Courbes 12h – Four")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp four"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["combustion"], name="Combustion"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit_gaz"], name="Débit gaz"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🌀 Turbine à gaz":
    st.markdown('<div class="big-title">🌀 Turbine à gaz</div>', unsafe_allow_html=True)
    df = pd.DataFrame(TURBINE_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_turbine(last)
    alert_card(status, msg)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(
            gauge("RPM", last["rpm"], 1800, 3200, "rpm"),
            use_container_width=True,
            key="turbine_page_rpm"
        )
    with col2:
        st.plotly_chart(
            gauge("Vibration", last["vib"], 1.0, 4.5, "mm/s",
                  SEUILS["turbine"]["vib_alerte"], "high"),
            use_container_width=True,
            key="turbine_page_vib"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp palier", last["temp"], 50, 95, "°C",
                  SEUILS["turbine"]["temp_alerte"], "high"),
            use_container_width=True,
            key="turbine_page_temp"
        )
    with col4:
        st.plotly_chart(
            gauge("Intensité", last["amp"], 10, 30, "A"),
            use_container_width=True,
            key="turbine_page_amp"
        )

    st.subheader("Courbes 12h – Turbine")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["rpm"], name="RPM"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["vib"], name="Vibration"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp palier"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "💧 Circuit d’eau":
    st.markdown('<div class="big-title">💧 Circuit d’eau</div>', unsafe_allow_html=True)
    df = pd.DataFrame(EAU_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_eau(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Pression eau", last["pression"], 2.0, 4.0, "bar",
                  SEUILS["eau"]["pression_alerte"], "low"),
            use_container_width=True,
            key="eau_page_pression"
        )
    with col2:
        st.plotly_chart(
            gauge("Débit eau", last["debit"], 50, 160, "m³/h",
                  SEUILS["eau"]["debit_alerte"], "high"),
            use_container_width=True,
            key="eau_page_debit"
        )
    with col3:
        st.plotly_chart(
            gauge("Niveau cuve", last["niveau"], 70, 100, "%"),
            use_container_width=True,
            key="eau_page_niveau"
        )

    st.subheader("Courbes 12h – Eau")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit"], name="Débit"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["niveau"], name="Niveau"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🛢️ Circuit de gaz":
    st.markdown('<div class="big-title">🛢️ Circuit de gaz</div>', unsafe_allow_html=True)
    df = pd.DataFrame(GAZ_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_gaz(last)
    alert_card(status, msg)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(
            gauge("Pression gaz", last["pression"], 3.0, 5.0, "bar",
                  SEUILS["gaz"]["pression_alerte"], "low"),
            use_container_width=True,
            key="gaz_page_pression"
        )
    with col2:
        st.plotly_chart(
            gauge("Débit gaz", last["debit"], 10, 35, "m³/h",
                  SEUILS["gaz"]["debit_alerte"], "low"),
            use_container_width=True,
            key="gaz_page_debit"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp gaz", last["temp"], 40, 70, "°C"),
            use_container_width=True,
            key="gaz_page_temp"
        )

    st.subheader("Courbes 12h – Gaz")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["pression"], name="Pression"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["debit"], name="Débit"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp"], name="Temp"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🔥 Échangeur de chaleur":
    st.markdown('<div class="big-title">🔥 Échangeur de chaleur</div>', unsafe_allow_html=True)
    df = pd.DataFrame(EXCHANGER_DATA)
    last = df.iloc[-1].to_dict()
    status, msg = eval_exchanger(last)
    alert_card(status, msg)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(
            gauge("Temp chaud in", last["temp_chaud_in"], 180, 240, "°C"),
            use_container_width=True,
            key="exch_page_temp_chaud_in"
        )
    with col2:
        st.plotly_chart(
            gauge("Temp chaud out", last["temp_chaud_out"], 150, 200, "°C"),
            use_container_width=True,
            key="exch_page_temp_chaud_out"
        )
    with col3:
        st.plotly_chart(
            gauge("Temp froid in", last["temp_froid_in"], 40, 55, "°C"),
            use_container_width=True,
            key="exch_page_temp_froid_in"
        )
    with col4:
        st.plotly_chart(
            gauge("Temp froid out", last["temp_froid_out"], 70, 95, "°C"),
            use_container_width=True,
            key="exch_page_temp_froid_out"
        )

    st.subheader("Courbes 12h – Échangeur")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_chaud_in"], name="Temp chaud in"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_chaud_out"], name="Temp chaud out"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_froid_in"], name="Temp froid in"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["temp_froid_out"], name="Temp froid out"))
    fig.add_trace(go.Scatter(x=df["heure"], y=df["delta_T"], name="ΔT", line=dict(width=4)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "🤖 IA – Risques globaux":
    st.markdown('<div class="big-title">🤖 IA – Risques globaux</div>', unsafe_allow_html=True)
    risks = compute_risks()

    st.subheader("Diagramme radar – comparaison des risques instantanés")
    categories = ["HVAC", "Four", "Turbine", "Échangeur", "Eau", "Gaz"]
    values = [risks[c] for c in categories]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Risques'
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.05)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.2)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="radar_risques")

    st.subheader("RandomForest – Probabilité de panne HVAC")
    rf_model = train_random_forest()
    proba = predict_hvac_failure_probability(rf_model)
    st.write(f"Probabilité prédite de panne HVAC (RandomForest) : **{proba:.2f}**")

    st.write("Scores de risques (0 = aucun, 1 = très élevé) :")
    st.json(risks)

elif page == "📍 Capteurs et emplacements":
    st.markdown('<div class="big-title">📍 Capteurs et emplacements</div>', unsafe_allow_html=True)
    for equip, caps in CAPTEURS.items():
        st.subheader(equip)
        for c in caps:
            st.write(f"- {c}")
        st.markdown("---")
