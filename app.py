import streamlit as st
import datetime
import pandas as pd

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX - Terminal Institucional",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS avanzados para replicar el diseño institucional exacto (Glassmorphism y Dark Theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F17;
        color: #F3F4F6;
        font-family: system-ui, -apple-system, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    div[data-testid="stMetric"] label {
        color: #9CA3AF !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    .stButton button {
        background-color: #111827 !important;
        color: #E5E7EB !important;
        border: 1px solid #1F2937 !important;
        border-radius: 12px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #1F2937 !important;
        border-color: #374151 !important;
        color: #10B981 !important;
    }

    table {
        color: #E5E7EB !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICACIÓN CON CONTRASEÑA FIJA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(17, 24, 39, 0.8); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
                <h2 style="color: white; margin-bottom: 5px;">⚡ MACRO EDGE FX</h2>
                <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 25px;">Terminal Institucional de Macro Trading - Acceso Privado</p>
            </div>
        """, unsafe_allow_html=True)
        
        email_input = st.text_input("Correo Electrónico", value="yanezdepablos6@gmail.com")
        pass_input = st.text_input("Contraseña", type="password", placeholder="Introduce la contraseña...")
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input == "32157532Ca.$":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Inténtalo de nuevo.")
    st.stop()

# --- TERMINAL PRINCIPAL DE MACRO TRADING ---

header_html = f"""
    <div style="background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid #1F2937; padding: 12px 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; background: linear-gradient(to bottom right, #34D399, #0D9488); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #0B0F17; font-weight: 900;">M</div>
            <div>
                <span style="font-size: 13px; font-weight: bold; color: white; display: block;">MACRO EDGE FX</span>
                <span style="font-size: 10px; color: #34D399; font-family: monospace;">LIVE FEED CONNECTED</span>
            </div>
        </div>
        <div style="font-family: monospace; font-size: 12px; color: #9CA3AF; background: #0B0F17; padding: 6px 12px; border-radius: 8px; border: 1px solid #1F2937;">
            🕒 <b>{datetime.datetime.utcnow().strftime('%H:%M:%S')} UTC</b>
        </div>
        <div style="font-family: monospace; font-size: 11px; color: #9CA3AF;">
            yanezdepablos6@gmail.com
        </div>
    </div>
"""
st.markdown(header_html, unsafe_allow_html=True)

if 'currencies' not in st.session_state:
    st.session_state.currencies = {
        'USD': {'score': 7.8, 'status': 'Fuerte'},
        'EUR': {'score': 3.2, 'status': 'Débil'},
        'GBP': {'score': 6.1, 'status': 'Neutral'},
        'JPY': {'score': 2.4, 'status': 'Muy Débil'},
        'AUD': {'score': 5.5, 'status': 'Neutral'},
        'CAD': {'score': 6.8, 'status': 'Fuerte'},
        'CHF': {'score': 4.1, 'status': 'Débil'},
        'NZD': {'score': 4.8, 'status': 'Neutral'}
    }

# 1. MATRIZ DE FUERZA DE DIVISAS
st.markdown("<p style='font-size: 11px; font-weight: bold; color: #9CA3AF; letter-spacing: 0.05em; margin-bottom: 8px;'>📊 MATRIZ DE FUERZA DE DIVISAS (CURRENCY STRENGTH METER)</p>", unsafe_allow_html=True)
cols = st.columns(8)
for i, (curr, data) in enumerate(st.session_state.currencies.items()):
    with cols[i]:
        st.metric(label=curr, value=f"{data['score']:.1f}", delta=data['status'])

st.markdown("<br>", unsafe_allow_html=True)

# 2. SIMULADOR SANDBOX DE FOREX FACTORY
st.markdown("<p style='font-size: 11px; font-weight: bold; color: #9CA3AF; letter-spacing: 0.05em; margin-bottom: 8px;'>🎛️ SIMULADOR DE ESCENARIOS FOREX FACTORY (SANDBOX)</p>", unsafe_allow_html=True)
scen_col1, scen_col2, scen_col3, scen_col4 = st.columns(4)

with scen_col1:
    if st.button("🇺🇸 USD NFP Supera Expectativas", use_container_width=True):
        st.session_state.currencies['USD']['score'] = 9.2
        st.session_state.currencies['USD']['status'] = 'Muy Fuerte'
        st.rerun()

with scen_col2:
    if st.button("🇪🇺 EUR CPI Caída Fuerte", use_container_width=True):
        st.session_state.currencies['EUR']['score'] = 1.8
        st.session_state.currencies['EUR']['status'] = 'Muy Débil'
        st.rerun()

with scen_col3:
    if st.button("🇯🇵 BoJ Subida de Tipos", use_container_width=True):
        st.session_state.currencies['JPY']['score'] = 8.0
        st.session_state.currencies['JPY']['status'] = 'Fuerte'
        st.rerun()

with scen_col4:
    if st.button("🔄 Restablecer Escenarios", use_container_width=True):
        st.session_state.currencies = {
            'USD': {'score': 7.8, 'status': 'Fuerte'},
            'EUR': {'score': 3.2, 'status': 'Débil'},
            'GBP': {'score': 6.1, 'status': 'Neutral'},
            'JPY': {'score': 2.4, 'status': 'Muy Débil'},
            'AUD': {'score': 5.5, 'status': 'Neutral'},
            'CAD': {'score': 6.8, 'status': 'Fuerte'},
            'CHF': {'score': 4.1, 'status': 'Débil'},
            'NZD': {'score': 4.8, 'status': 'Neutral'}
        }
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 3. RANKING DE PARES MACRO (DELTA DIVERGENCIA)
st.markdown("<p style='font-size: 11px; font-weight: bold; color: #9CA3AF; letter-spacing: 0.05em; margin-bottom: 8px;'>🏆 RANKING DE PARES MACRO (DELTA DIVERGENCIA)</p>", unsafe_allow_html=True)

pairs_raw = [
    ("USD/JPY", "Fuerte divergencia de política monetaria entre la Reserva Federal (Hawkish) y el Banco de Japón (Dovish)."),
    ("EUR/USD", "Debilitamiento macroeconómico persistente en la Eurozona con registros de CPI a la baja."),
    ("GBP/USD", "Consolidación lateral en la libra esterlina. El Banco de Inglaterra mantiene tipos moderados."),
    ("USD/CAD", "Precios del petróleo estables apoyan la fortaleza estructural del USD frente al CAD."),
    ("AUD/USD", "Exposición directa al ciclo de materias primas de China en rango neutral."),
    ("EUR/GBP", "Cruce estructural reflejando divergencia entre el bloque europeo y la resiliencia británica.")
]

table_data = []
for pair, thesis in pairs_raw:
    base, quote = pair.split('/')
    b_score = st.session_state.currencies[base]['score']
    q_score = st.session_state.currencies[quote]['score']
    delta = b_score - q_score
    
    direction = "BUY" if delta > 0.5 else ("SELL" if delta < -0.5 else "NEUTRAL")
    prob = int(min(95, max(55, 50 + abs(delta) * 8)))
    risk = "Bajo" if prob > 75 else ("Medio" if prob > 60 else "Alto")
    
    table_data.append({
        "Par": pair,
        "Dirección": direction,
        "Delta Macro": round(delta, 1),
        "Probabilidad": f"{prob}%",
        "Riesgo": risk,
        "Tesis": thesis
    })

df_pairs = pd.DataFrame(table_data)
df_pairs = df_pairs.sort_values(by="Delta Macro", key=abs, ascending=False)

st.dataframe(df_pairs[["Par", "Dirección", "Delta Macro", "Probabilidad", "Riesgo"]], use_container_width=True, hide_index=True)

selected_pair = st.selectbox("Selecciona un par para ver su Tesis Fundamental Algorítmica:", df_pairs["Par"].tolist())
selected_thesis = df_pairs[df_pairs["Par"] == selected_pair]["Tesis"].values[0]
st.info(f"*Tesis para {selected_pair}:* {selected_thesis}")

# 4. FEED DE NOTICIAS MACRO
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 11px; font-weight: bold; color: #9CA3AF; letter-spacing: 0.05em; margin-bottom: 8px;'>📰 FEED DE NOTICIAS MACRO Y DESVIACIÓN ESTÁNDAR (SD)</p>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.6); padding: 14px; border-radius: 12px; border: 1px solid #1F2937;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 6px;">
                <span>USD • NFP Employment</span>
                <span style="color: #34D399; font-weight: bold;">+2.4 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0;">Creación de empleo por encima del consenso. Mantiene presión restrictiva en la Fed.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.6); padding: 14px; border-radius: 12px; border: 1px solid #1F2937;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 6px;">
                <span>EUR • CPI Flash YoY</span>
                <span style="color: #EF4444; font-weight: bold;">-1.8 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0;">Desaceleración inflacionaria mayor a la prevista. Incrementa presión sobre el BCE.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.6); padding: 14px; border-radius: 12px; border: 1px solid #1F2937;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 6px;">
                <span>JPY • BoJ Rate Decision</span>
                <span style="color: #34D399; font-weight: bold;">+2.1 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0;">Giro hacia la normalización monetaria, reduciendo atractivo del carry trade.</p>
        </div>
    """, unsafe_allow_html=True)
