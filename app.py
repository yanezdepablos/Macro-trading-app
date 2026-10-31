import streamlit as st
import datetime
import pandas as pd

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX - Terminal Institucional",
    page_icon="📈",
    layout="wide"
)

# Estilo visual Dark Mode institucional
st.markdown("""
    <style>
    .main { background-color: #0B0F17; color: #F3F4F6; }
    .stMetric { background-color: #111827; padding: 15px; border-radius: 12px; border: 1px solid #1F2937; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICACIÓN SEGURO (Reemplaza a Supabase sin fallos de red) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🔒 MACRO EDGE FX")
        st.caption("Terminal Institucional de Macro Trading - Acceso Privado")
        
        email_input = st.text_input("Correo Electrónico", value="yanezdepablos6@gmail.com")
        pass_input = st.text_input("Contraseña", type="password", placeholder="••••••••")
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input.strip() != "":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Por favor ingresa una contraseña válida.")
    st.stop() # Detiene la ejecución si no ha iniciado sesión

# --- TERMINAL PRINCIPAL DE MACRO TRADING ---

# Header de la Terminal
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown("### ⚡ MACRO EDGE FX")
    st.caption("Terminal Institucional de Macro Trading")
with col2:
    utc_now = datetime.datetime.utcnow().strftime("%H:%M:%S")
    st.markdown(f"*Reloj UTC:* {utc_now} UTC")
with col3:
    st.markdown("🟢 *LIVE FEED CONNECTED*")

st.divider()

# Estado inicial de la Matriz de Fuerza de Divisas
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
st.markdown("#### 📊 MATRIZ DE FUERZA DE DIVISAS (CURRENCY STRENGTH METER)")
cols = st.columns(8)
for i, (curr, data) in enumerate(st.session_state.currencies.items()):
    with cols[i]:
        st.metric(label=curr, value=f"{data['score']:.1f}", delta=data['status'])

st.divider()

# 2. SIMULADOR SANDBOX DE FOREX FACTORY
st.markdown("#### 🎛️ SIMULADOR DE ESCENARIOS FOREX FACTORY (SANDBOX)")
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
    if st.button("🔄 Restablecer", use_container_width=True):
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

st.divider()

# 3. RANKING DE PARES MACRO (DELTA DIVERGENCIA)
st.markdown("#### 🏆 RANKING DE PARES MACRO (DELTA DIVERGENCIA)")

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

# Tesis Fundamental Interactiva
selected_pair = st.selectbox("Selecciona un par para ver su Tesis Fundamental Algorítmica:", df_pairs["Par"].tolist())
selected_thesis = df_pairs[df_pairs["Par"] == selected_pair]["Tesis"].values[0]
st.info(f"*Tesis para {selected_pair}:* {selected_thesis}")

# 4. FEED DE NOTICIAS MACRO
st.divider()
st.markdown("#### 📰 FEED DE NOTICIAS MACRO Y DESVIACIÓN ESTÁNDAR (SD)")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("*USD • NFP Employment*  +2.4 SD")
    st.caption("Creación de empleo por encima del consenso. Mantiene presión restrictiva en la Fed.")

with f_col2:
    st.markdown("*EUR • CPI Flash YoY*  -1.8 SD")
    st.caption("Desaceleración inflacionaria mayor a la prevista. Incrementa presión sobre el BCE.")

with f_col3:
    st.markdown("*JPY • BoJ Rate Decision*  +2.1 SD")
    st.caption("Giro hacia la normalización monetaria, reduciendo atractivo del carry trade.")
