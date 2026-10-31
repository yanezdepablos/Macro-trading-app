import streamlit as st
import datetime
import pandas as pd

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX - Terminal Institucional",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS avanzados: Replicando fielmente el prototipo original de alta gama
st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #07090E;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Contenedor tipo Terminal / Glassmorphism Avanzado */
    .terminal-container {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }

    /* Tarjetas de Divisas */
    .currency-card {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(13, 17, 23, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .currency-card:hover {
        border-color: rgba(52, 211, 153, 0.4);
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.15);
    }
    
    /* Botones de acción estilizados */
    .stButton button {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%) !important;
        color: #E5E7EB !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #374151 0%, #1F2937 100%) !important;
        border-color: #34D399 !important;
        color: #34D399 !important;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICACIÓN BLINDADO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(13, 17, 23, 0.9); padding: 35px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px rgba(0,0,0,0.8); text-align: center;">
                <div style="font-size: 28px; margin-bottom: 10px;">⚡</div>
                <h2 style="color: white; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 5px;">MACRO EDGE FX</h2>
                <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 25px;">Terminal Institucional de Macro Trading — Acceso Privado</p>
            </div>
        """, unsafe_allow_html=True)
        
        email_input = st.text_input("Correo Electrónico", value="yanezdepablos6@gmail.com")
        pass_input = st.text_input("Contraseña de Acceso", type="password", placeholder="Introduce la contraseña...")
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input == "32157532Ca.$":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Verifícalo.")
    st.stop()

# --- TERMINAL PRINCIPAL DE MACRO TRADING (ESTÉTICA PROTOTIPO ORIGINAL) ---

# Header Institucional Superior
header_html = f"""
    <div style="background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); padding: 16px 24px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 38px; height: 38px; background: linear-gradient(135deg, #34D399 0%, #059669 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #07090E; font-weight: 900; font-size: 18px; box-shadow: 0 0 15px rgba(52,211,153,0.3);">M</div>
            <div>
                <span style="font-size: 14px; font-weight: 800; color: white; letter-spacing: 0.05em; display: block;">MACRO EDGE FX</span>
                <span style="font-size: 10px; color: #34D399; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 4px;">
                    <span style="width: 6px; height: 6px; background-color: #34D399; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #34D399;"></span> LIVE FEED CONNECTED
                </span>
            </div>
        </div>
        <div style="font-family: monospace; font-size: 12px; color: #D1D5DB; background: rgba(0,0,0,0.4); padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
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
        'USD': {'score': 7.8, 'status': 'Fuerte', 'color': '#34D399'},
        'EUR': {'score': 3.2, 'status': 'Débil', 'color': '#EF4444'},
        'GBP': {'score': 6.1, 'status': 'Neutral', 'color': '#FBBF24'},
        'JPY': {'score': 2.4, 'status': 'Muy Débil', 'color': '#EF4444'},
        'AUD': {'score': 5.5, 'status': 'Neutral', 'color': '#FBBF24'},
        'CAD': {'score': 6.8, 'status': 'Fuerte', 'color': '#34D399'},
        'CHF': {'score': 4.1, 'status': 'Débil', 'color': '#EF4444'},
        'NZD': {'score': 4.8, 'status': 'Neutral', 'color': '#FBBF24'}
    }

# 1. MATRIZ DE FUERZA DE DIVISAS
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>📊 Matriz de Fuerza de Divisas (Currency Strength Meter)</p>", unsafe_allow_html=True)
cols = st.columns(8)
for i, (curr, data) in enumerate(st.session_state.currencies.items()):
    with cols[i]:
        st.markdown(f"""
            <div class="currency-card">
                <div style="font-size: 12px; font-weight: 800; color: #9CA3AF; margin-bottom: 4px;">{curr}</div>
                <div style="font-size: 22px; font-weight: 900; color: #FFFFFF; margin-bottom: 6px;">{data['score']:.1f}</div>
                <div style="font-size: 10px; font-weight: 700; color: {data['color']}; background: rgba(0,0,0,0.3); padding: 3px 6px; border-radius: 6px; display: inline-block;">{data['status']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. SIMULADOR SANDBOX DE FOREX FACTORY
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>🎛️ Simulador de Escenarios Forex Factory (Sandbox)</p>", unsafe_allow_html=True)
scen_col1, scen_col2, scen_col3, scen_col4 = st.columns(4)

with scen_col1:
    if st.button("🇺🇸 USD NFP Supera Expectativas", use_container_width=True):
        st.session_state.currencies['USD']['score'] = 9.2
        st.session_state.currencies['USD']['status'] = 'Muy Fuerte'
        st.session_state.currencies['USD']['color'] = '#34D399'
        st.rerun()

with scen_col2:
    if st.button("🇪🇺 EUR CPI Caída Fuerte", use_container_width=True):
        st.session_state.currencies['EUR']['score'] = 1.8
        st.session_state.currencies['EUR']['status'] = 'Muy Débil'
        st.session_state.currencies['EUR']['color'] = '#EF4444'
        st.rerun()

with scen_col3:
    if st.button("🇯🇵 BoJ Subida de Tipos", use_container_width=True):
        st.session_state.currencies['JPY']['score'] = 8.0
        st.session_state.currencies['JPY']['status'] = 'Fuerte'
        st.session_state.currencies['JPY']['color'] = '#34D399'
        st.rerun()

with scen_col4:
    if st.button("🔄 Restablecer Escenarios", use_container_width=True):
        st.session_state.currencies = {
            'USD': {'score': 7.8, 'status': 'Fuerte', 'color': '#34D399'},
            'EUR': {'score': 3.2, 'status': 'Débil', 'color': '#EF4444'},
            'GBP': {'score': 6.1, 'status': 'Neutral', 'color': '#FBBF24'},
            'JPY': {'score': 2.4, 'status': 'Muy Débil', 'color': '#EF4444'},
            'AUD': {'score': 5.5, 'status': 'Neutral', 'color': '#FBBF24'},
            'CAD': {'score': 6.8, 'status': 'Fuerte', 'color': '#34D399'},
            'CHF': {'score': 4.1, 'status': 'Débil', 'color': '#EF4444'},
            'NZD': {'score': 4.8, 'status': 'Neutral', 'color': '#FBBF24'}
        }
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 3. RANKING DE PARES MACRO (DELTA DIVERGENCIA)
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>🏆 Ranking de Pares Macro (Delta Divergencia)</p>", unsafe_allow_html=True)

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
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>📰 Feed de Noticias Macro y Desviación Estándar (SD)</p>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
        <div style="background: rgba(13, 17, 23, 0.8); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>USD • NFP Employment</span>
                <span style="color: #34D399; font-weight: bold;">+2.4 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Creación de empleo por encima del consenso. Mantiene presión restrictiva en la Fed.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
        <div style="background: rgba(13, 17, 23, 0.8); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>EUR • CPI Flash YoY</span>
                <span style="color: #EF4444; font-weight: bold;">-1.8 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Desaceleración inflacionaria mayor a la prevista. Incrementa presión sobre el BCE.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
        <div style="background: rgba(13, 17, 23, 0.8); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>JPY • BoJ Rate Decision</span>
                <span style="color: #34D399; font-weight: bold;">+2.1 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Giro hacia la normalización monetaria, reduciendo atractivo del carry trade.</p>
        </div>
    """, unsafe_allow_html=True)
