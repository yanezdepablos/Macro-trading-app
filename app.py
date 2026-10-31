import streamlit as st
import datetime
import pandas as pd

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX - Terminal Institucional",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS avanzados con Neón y Glassmorphism de alta gama
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #05070B;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }

    /* Efectos de Neón */
    .neon-text {
        color: #34D399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.6);
    }
    
    .neon-card {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        transition: all 0.2s ease;
    }
    .neon-card:hover {
        border-color: rgba(52, 211, 153, 0.4);
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.2);
    }

    /* Botones estilizados */
    .stButton button {
        background: linear-gradient(135deg, #111827 0%, #0D1117 100%) !important;
        color: #E5E7EB !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        border-color: #34D399 !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.25);
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
            <div style="background: rgba(13, 17, 23, 0.9); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px rgba(0,0,0,0.8); text-align: center;">
                <div style="font-size: 32px; margin-bottom: 12px;">⚡</div>
                <h2 style="color: white; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 6px;">MACRO EDGE FX</h2>
                <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 30px;">Terminal Institucional de Macro Trading — Acceso Privado</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Correo Electrónico", value="yanezdepablos6@gmail.com", disabled=True)
        pass_input = st.text_input("Contraseña de Acceso", type="password", placeholder="Introduce la contraseña...")
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input == "32157532Ca.$":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Inténtalo de nuevo.")
    st.stop()

# --- TERMINAL PRINCIPAL DE MACRO TRADING ---

header_html = f"""
    <div style="background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); padding: 16px 24px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #34D399 0%, #059669 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #05070B; font-weight: 900; font-size: 18px; box-shadow: 0 0 20px rgba(52,211,153,0.4);">M</div>
            <div>
                <span style="font-size: 14px; font-weight: 800; color: white; letter-spacing: 0.05em; display: block;">MACRO EDGE FX</span>
                <span style="font-size: 10px; color: #34D399; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                    <span style="width: 7px; height: 7px; background-color: #34D399; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #34D399;"></span> LIVE FEED CONNECTED
                </span>
            </div>
        </div>
        <div style="font-family: monospace; font-size: 12px; color: #34D399; background: rgba(52,211,153,0.08); padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(52,211,153,0.2); text-shadow: 0 0 8px rgba(52,211,153,0.5);">
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
        'USD': {'score': 7.8, 'status': 'Fuerte', 'flag': '🇺🇸', 'color': '#34D399', 'bg': 'rgba(52, 211, 153, 0.1)'},
        'EUR': {'score': 3.2, 'status': 'Débil', 'flag': '🇪🇺', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
        'GBP': {'score': 6.1, 'status': 'Neutral', 'flag': '🇬🇧', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'},
        'JPY': {'score': 2.4, 'status': 'Muy Débil', 'flag': '🇯🇵', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
        'AUD': {'score': 5.5, 'status': 'Neutral', 'flag': '🇦🇺', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'},
        'CAD': {'score': 6.8, 'status': 'Fuerte', 'flag': '🇨🇦', 'color': '#34D399', 'bg': 'rgba(52, 211, 153, 0.1)'},
        'CHF': {'score': 4.1, 'status': 'Débil', 'flag': '🇨🇭', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
        'NZD': {'score': 4.8, 'status': 'Neutral', 'flag': '🇳🇿', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'}
    }

# 1. MATRIZ DE FUERZA DE DIVISAS CON BANDERAS
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>📊 Matriz de Fuerza de Divisas (Currency Strength Meter)</p>", unsafe_allow_html=True)
cols = st.columns(8)
for i, (curr, data) in enumerate(st.session_state.currencies.items()):
    with cols[i]:
        st.markdown(f"""
            <div class="neon-card">
                <div style="font-size: 14px; margin-bottom: 2px;">{data['flag']}</div>
                <div style="font-size: 11px; font-weight: 800; color: #9CA3AF; margin-bottom: 4px; letter-spacing: 0.05em;">{curr}</div>
                <div style="font-size: 20px; font-weight: 900; color: #FFFFFF; margin-bottom: 6px; font-family: monospace;">{data['score']:.1f}</div>
                <div style="font-size: 9px; font-weight: 700; color: {data['color']}; background: {data['bg']}; padding: 3px 6px; border-radius: 6px; display: inline-block; border: 1px solid {data['color']}33;">{data['status']}</div>
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
        st.session_state.currencies['USD']['bg'] = 'rgba(52, 211, 153, 0.1)'
        st.rerun()

with scen_col2:
    if st.button("🇪🇺 EUR CPI Caída Fuerte", use_container_width=True):
        st.session_state.currencies['EUR']['score'] = 1.8
        st.session_state.currencies['EUR']['status'] = 'Muy Débil'
        st.session_state.currencies['EUR']['color'] = '#EF4444'
        st.session_state.currencies['EUR']['bg'] = 'rgba(239, 68, 68, 0.1)'
        st.rerun()

with scen_col3:
    if st.button("🇯🇵 BoJ Subida de Tipos", use_container_width=True):
        st.session_state.currencies['JPY']['score'] = 8.0
        st.session_state.currencies['JPY']['status'] = 'Fuerte'
        st.session_state.currencies['JPY']['color'] = '#34D399'
        st.session_state.currencies['JPY']['bg'] = 'rgba(52, 211, 153, 0.1)'
        st.rerun()

with scen_col4:
    if st.button("🔄 Restablecer Escenarios", use_container_width=True):
        st.session_state.currencies = {
            'USD': {'score': 7.8, 'status': 'Fuerte', 'flag': '🇺🇸', 'color': '#34D399', 'bg': 'rgba(52, 211, 153, 0.1)'},
            'EUR': {'score': 3.2, 'status': 'Débil', 'flag': '🇪🇺', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
            'GBP': {'score': 6.1, 'status': 'Neutral', 'flag': '🇬🇧', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'},
            'JPY': {'score': 2.4, 'status': 'Muy Débil', 'flag': '🇯🇵', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
            'AUD': {'score': 5.5, 'status': 'Neutral', 'flag': '🇦🇺', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'},
            'CAD': {'score': 6.8, 'status': 'Fuerte', 'flag': '🇨🇦', 'color': '#34D399', 'bg': 'rgba(52, 211, 153, 0.1)'},
            'CHF': {'score': 4.1, 'status': 'Débil', 'flag': '🇨🇭', 'color': '#EF4444', 'bg': 'rgba(239, 68, 68, 0.1)'},
            'NZD': {'score': 4.8, 'status': 'Neutral', 'flag': '🇳🇿', 'color': '#FBBF24', 'bg': 'rgba(251, 191, 36, 0.1)'}
        }
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 3. RANKING DE PARES MACRO (TODOS LOS CRUCES PRINCIPALES Y CRUZADOS)
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>🏆 Ranking Completo de Pares Macro (Delta Divergencia)</p>", unsafe_allow_html=True)

pairs_raw = [
    ("USD/JPY", "🇺🇸/🇯🇵", "Fuerte divergencia de política monetaria entre la Reserva Federal (Hawkish) y el Banco de Japón (Dovish)."),
    ("EUR/USD", "🇪🇺/🇺🇸", "Debilitamiento macroeconómico persistente en la Eurozona con registros de CPI a la baja frente al dólar."),
    ("GBP/USD", "🇬🇧/🇺🇸", "Consolidación lateral en la libra esterlina. El Banco de Inglaterra mantiene tipos moderados."),
    ("USD/CAD", "🇺🇸/🇨🇦", "Precios del petróleo estables apoyan la fortaleza estructural del USD frente al CAD."),
    ("AUD/USD", "🇦🇺/🇺🇸", "Exposición directa al ciclo de materias primas de China en rango neutral frente al billete verde."),
    ("EUR/GBP", "🇪🇺/🇬🇧", "Cruce estructural reflejando divergencia entre el bloque europeo y la resiliencia británica."),
    ("NZD/USD", "🇳🇿/🇺🇸", "Crecimiento moderado en Nueva Zelanda con flujos de leche en niveles estacionales."),
    ("USD/CHF", "🇺🇸/🇨🇭", "Busqueda de refugio seguro equilibrada con los diferenciales de tipos de la SNB y la Fed."),
    ("EUR/JPY", "🇪🇺/🇯🇵", "Divergencia entre los estímulos europeos y la salida de tipos negativos en Japón."),
    ("GBP/JPY", "🇬🇧/🇯🇵", "Alta volatilidad en el carry trade por expectativas de intervención en el par cruzado.")
]

table_data = []
for pair, flags, thesis in pairs_raw:
    base, quote = pair.split('/')
    b_score = st.session_state.currencies[base]['score']
    q_score = st.session_state.currencies[quote]['score']
    delta = b_score - q_score
    
    direction = "BUY" if delta > 0.5 else ("SELL" if delta < -0.5 else "NEUTRAL")
    dir_color = "#34D399" if direction == "BUY" else ("#EF4444" if direction == "SELL" else "#FBBF24")
    prob = int(min(95, max(55, 50 + abs(delta) * 8)))
    risk = "Bajo" if prob > 75 else ("Medio" if prob > 60 else "Alto")
    risk_color = "#34D399" if risk == "Bajo" else ("#FBBF24" if risk == "Medio" else "#EF4444")
    
    table_data.append({
        "Pair": pair,
        "Flags": flags,
        "Dir": direction,
        "DirColor": dir_color,
        "Delta": round(delta, 1),
        "Prob": f"{prob}%",
        "Risk": risk,
        "RiskColor": risk_color,
        "Thesis": thesis
    })

table_data = sorted(table_data, key=lambda x: abs(x['Delta']), reverse=True)

# Renderizar cada par como tarjeta interactiva con banderas y neón
for row in table_data:
    st.markdown(f"""
        <div style="background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px 20px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="display: flex; align-items: center; gap: 10px; width: 140px;">
                <span style="font-size: 16px;">{row['Flags']}</span>
                <span style="font-weight: 800; color: #FFFFFF; font-family: monospace; font-size: 14px;">{row['Pair']}</span>
            </div>
            <div><span style="color: {row['DirColor']}; font-weight: 800; background: {row['DirColor']}15; padding: 4px 10px; border-radius: 6px; border: 1px solid {row['DirColor']}33; font-size: 11px; text-shadow: 0 0 8px {row['DirColor']}66;">{row['Dir']}</span></div>
            <div style="font-family: monospace; font-weight: 700; color: #E5E7EB; font-size: 13px;">Delta: <span class="neon-text">{row['Delta']:+.1f}</span></div>
            <div style="font-family: monospace; color: #9CA3AF; font-size: 13px;">Prob: {row['Prob']}</div>
            <div><span style="color: {row['RiskColor']}; font-weight: 700; font-size: 12px;">Riesgo: {row['Risk']}</span></div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
selected_pair = st.selectbox("🔍 Selecciona un par para ver su Tesis Fundamental Algorítmica detallada:", [r['Pair'] for r in table_data])
selected_thesis = next(r['Thesis'] for r in table_data if r['Pair'] == selected_pair)
st.info(f"*Tesis Institucional para {selected_pair}:* {selected_thesis}")

# 4. FEED DE NOTICIAS MACRO
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>📰 Feed de Noticias Macro y Desviación Estándar (SD)</p>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
        <div class="neon-card" style="text-align: left;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>🇺🇸 USD • NFP Employment</span>
                <span class="neon-text" style="font-weight: bold;">+2.4 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Creación de empleo por encima del consenso. Mantiene presión restrictiva en la Fed.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
        <div class="neon-card" style="text-align: left;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>🇪🇺 EUR • CPI Flash YoY</span>
                <span style="color: #EF4444; font-weight: bold; text-shadow: 0 0 8px rgba(239,68,68,0.6);">-1.8 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Desaceleración inflacionaria mayor a la prevista. Incrementa presión sobre el BCE.</p>
        </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
        <div class="neon-card" style="text-align: left;">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 11px; color: #9CA3AF; margin-bottom: 8px;">
                <span>🇯🇵 JPY • BoJ Rate Decision</span>
                <span class="neon-text" style="font-weight: bold;">+2.1 SD</span>
            </div>
            <p style="font-size: 12px; color: #D1D5DB; margin: 0; line-height: 1.4;">Giro hacia la normalización monetaria, reduciendo atractivo del carry trade.</p>
        </div>
    """, unsafe_allow_html=True)
