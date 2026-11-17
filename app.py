import streamlit as st
import datetime
import pandas as pd
import time
import urllib.request
import xml.etree.ElementTree as ET
import streamlit.components.v1 as components
import email.utils

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX - Terminal Multiactivo Separado",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS avanzados con Neón brillante y Glassmorphism
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
        padding-bottom: 1.5rem !important;
        max-width: 100% !important;
    }

    .neon-glow {
        color: #34D399;
        text-shadow: 0 0 12px rgba(52, 211, 153, 0.7);
    }
    
    .neon-card {
        background: rgba(13, 17, 23, 0.9);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        transition: all 0.2s ease;
    }
    .neon-card:hover {
        border-color: rgba(52, 211, 153, 0.4);
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.2);
    }

    .section-title {
        font-size: 12px;
        font-weight: 800;
        color: #34D399;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(52, 211, 153, 0.2);
        padding-bottom: 4px;
    }

    .stButton button {
        background: linear-gradient(135deg, #111827 0%, #0D1117 100%) !important;
        color: #E5E7EB !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        border-color: #34D399 !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- MOTOR MULTIACTIVO CON FILTRO DE 3 DÍAS ---
def fetch_real_macro_news():
    """Descarga feeds RSS, descarta noticias > 3 días y evalúa fuerza para todas las categorías."""
    
    rss_urls = [
        ("Google News Multiactivo", "https://news.google.com/rss/search?q=forex+OR+gold+OR+bitcoin+OR+oil+OR+fed+inflation+when:3d&hl=en-US&gl=US&ceid=US:en"),
        ("Google News Mercados", "https://news.google.com/rss/search?q=USD+OR+EUR+OR+XAU+OR+BTC+OR+WTI+markets+when:3d&hl=en-US&gl=US&ceid=US:en")
    ]
    
    asset_keywords = {
        'USD': ['usd', 'dollar', 'fed', 'federal reserve', 'powell', 'us ', 'u.s.', 'nfp', 'fomc'],
        'EUR': ['eur', 'euro', 'ecb', 'lagarde', 'eurozone', 'germany'],
        'GBP': ['gbp', 'pound', 'sterling', 'boe', 'uk ', 'britain'],
        'JPY': ['jpy', 'yen', 'boj', 'bank of japan', 'ueda'],
        'AUD': ['aud', 'aussie', 'rba', 'australia'],
        'CAD': ['cad', 'loonie', 'boc', 'canada'],
        'CHF': ['chf', 'swiss', 'franc', 'snb'],
        'NZD': ['nzd', 'kiwi', 'rbnz'],
        'SEK': ['sek', 'sweden', 'krona'],
        'NOK': ['nok', 'norway', 'krone'],
        'SGD': ['sgd', 'singapore'],
        'ZAR': ['zar', 'south africa', 'rand'],
        'XAU': ['gold', 'xau', 'bullion', 'precious metals'],
        'XAG': ['silver', 'xag'],
        'OIL': ['oil', 'crude', 'brent', 'wti', 'energy', 'opec'],
        'BTC': ['bitcoin', 'btc', 'crypto', 'cryptocurrency'],
        'ETH': ['ethereum', 'eth', 'altcoin'],
        'US500': ['s&p 500', 'wall street', 'stocks', 'nasdaq', 'spx', 'equity'],
        'VIX': ['vix', 'volatility', 'fear index']
    }
    
    bullish_words = ['surge', 'jump', 'rise', 'higher', 'hawkish', 'hike', 'beat', 'strong', 'gain', 'rally', 'boost', 'hot', 'growth', 'soar', 'up', 'bull']
    bearish_words = ['drop', 'fall', 'plunge', 'lower', 'dovish', 'cut', 'miss', 'weak', 'loss', 'slump', 'cool', 'slow', 'decline', 'down', 'tumble', 'bear']
    
    live_news = []
    seen_titles = set()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    max_age_days = 3
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for source_label, url in rss_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                for item in root.findall('.//item')[:18]:
                    title_el = item.find('title')
                    pub_el = item.find('pubDate')
                    source_el = item.find('source')
                    
                    if title_el is None or not title_el.text:
                        continue
                        
                    title_text = title_el.text.strip()
                    if title_text in seen_titles:
                        continue
                        
                    is_recent = False
                    pub_time_str = "Reciente"
                    if pub_el is not None and pub_el.text:
                        try:
                            parsed_date = email.utils.parsedate_to_datetime(pub_el.text)
                            if parsed_date.tzinfo is None:
                                parsed_date = parsed_date.replace(tzinfo=datetime.timezone.utc)
                            
                            age_delta = now_utc - parsed_date
                            if age_delta.total_days() <= max_age_days:
                                is_recent = True
                                pub_time_str = parsed_date.strftime("%d/%m %H:%M UTC")
                        except Exception:
                            is_recent = True
                            
                    if not is_recent:
                        continue
                        
                    seen_titles.add(title_text)
                    title_lower = title_text.lower()
                    
                    detected_asset = 'USD'
                    for asset, kws in asset_keywords.items():
                        if any(kw in title_lower for kw in kws):
                            detected_asset = asset
                            break
                            
                    score_delta = 0.0
                    for w in bullish_words:
                        if w in title_lower:
                            score_delta += 0.5
                    for w in bearish_words:
                        if w in title_lower:
                            score_delta -= 0.5
                            
                    score_delta = round(max(-2.0, min(2.0, score_delta)), 1)
                    real_source = source_el.text if (source_el is not None and source_el.text) else source_label
                    
                    live_news.append({
                        "currency": detected_asset,
                        "source": f"{real_source} ({pub_time_str})",
                        "title": title_text,
                        "impact": score_delta,
                        "summary": f"Impacto filtrado (< 3 días) para {detected_asset}."
                    })
        except Exception:
            continue

    if not live_news:
        live_news = [
            {"currency": "USD", "source": "Filtro 72h Activo", "title": "Sincronizando flujo institucional limpio...", "impact": 0.0, "summary": "Esperando eventos recientes."}
        ]

    base_scores = {
        'USD': 5.0, 'EUR': 5.0, 'GBP': 5.0, 'JPY': 5.0, 'AUD': 5.0, 'CAD': 5.0, 
        'CHF': 5.0, 'NZD': 5.0, 'SEK': 5.0, 'NOK': 5.0, 'SGD': 5.0, 'ZAR': 5.0,
        'XAU': 5.2, 'XAG': 5.0, 'OIL': 5.0, 'BTC': 5.5, 'ETH': 5.3, 'US500': 5.4, 'VIX': 4.8
    }

    for item in live_news:
        asset = item['currency']
        if asset in base_scores:
            base_scores[asset] += (item['impact'] * 0.4)
            base_scores[asset] = max(1.0, min(9.9, base_scores[asset]))

    processed_assets = {}
    region_map = {
        'USD': 'USA', 'EUR': 'EUR', 'GBP': 'GBR', 'JPY': 'JPN', 'AUD': 'AUS', 'CAD': 'CAN', 
        'CHF': 'CHE', 'NZD': 'NZL', 'SEK': 'SWE', 'NOK': 'NOR', 'SGD': 'SGP', 'ZAR': 'ZAF',
        'XAU': 'GOLD', 'XAG': 'SILVER', 'OIL': 'ENERGY', 'BTC': 'CRYPTO', 'ETH': 'CRYPTO', 'US500': 'INDEX', 'VIX': 'VOL'
    }
    
    for asset, score in base_scores.items():
        if score >= 6.0:
            status, color, bg = "Fuerte", "#34D399", "rgba(52, 211, 153, 0.1)"
        elif score <= 4.0:
            status, color, bg = "Débil", "#EF4444", "rgba(239, 68, 68, 0.1)"
        else:
            status, color, bg = "Neutral", "#FBBF24", "rgba(251, 191, 36, 0.1)"
            
        processed_assets[asset] = {
            'score': round(score, 1),
            'status': status,
            'region': region_map.get(asset, 'GLOBAL'),
            'color': color,
            'bg': bg
        }

    return processed_assets, live_news

# --- SISTEMA DE AUTENTICACIÓN (Usuario: yanezdepablos) ---
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
                <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 30px;">Terminal Multiactivo Institucional</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Usuario", value="yanezdepablos", disabled=True)
        pass_input = st.text_input("Contraseña de Acceso", type="password", placeholder="Introduce la contraseña...")
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input == "32157532Ca.$":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Inténtalo de nuevo.")
    st.stop()

assets_data, live_news_feed = fetch_real_macro_news()

# --- BARRA LATERAL: GESTIÓN DE RIESGO ---
with st.sidebar:
    st.markdown("### 🧮 Gestión de Riesgo")
    account_balance = st.number_input("Balance de Cuenta ($)", value=10000.0, step=500.0)
    risk_pct = st.slider("Riesgo por Operación (%)", 0.1, 3.0, 1.0, 0.1)
    sl_pips = st.number_input("Stop Loss Estimado (Pips)", value=25.0, step=5.0)
    
    risk_amount = account_balance * (risk_pct / 100.0)
    recommended_lots = risk_amount / (sl_pips * 10.0)
    
    st.markdown(f"""
        <div style="background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.2); padding: 12px; border-radius: 10px; margin-top: 15px;">
            <p style="margin: 0; font-size: 11px; color: #34D399; font-weight: bold;">MÉTRICA DE RIESGO:</p>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #FFFFFF;">Riesgo Monetario: <b>${risk_amount:.2f}</b></p>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #34D399; font-weight: bold;">Lote Sugerido: {recommended_lots:.2f} Lotes</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🕒 Sesión Activa (Killzones)")
    
    current_utc_hour = datetime.datetime.utcnow().hour
    if 7 <= current_utc_hour < 15:
        session_name = "🟢 LONDRES (Alta Liquidez)"
    elif 12 <= current_utc_hour < 20:
        session_name = "🟢 NUEVA YORK (Solapamiento Principal)"
    elif 0 <= current_utc_hour < 8:
        session_name = "🟡 TOKIO / ASIÁTICA"
    else:
        session_name = "⚪ RANGO / BAJA LIQUIDEZ"
        
    st.markdown(f"<div style='font-size: 12px; color: #E5E7EB; background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;'>{session_name}</div>", unsafe_allow_html=True)

# --- TERMINAL PRINCIPAL ---
header_top_html = """
    <div style="background: rgba(13, 17, 23, 0.9); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); padding: 18px 24px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #34D399 0%, #059669 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #05070B; font-weight: 900; font-size: 18px; box-shadow: 0 0 20px rgba(52,211,153,0.4);">M</div>
            <div>
                <span style="font-size: 14px; font-weight: 800; color: white; letter-spacing: 0.05em; display: block;">MACRO EDGE FX — MULTIACTIVO</span>
                <span style="font-size: 10px; color: #34D399; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                    <span style="width: 7px; height: 7px; background-color: #34D399; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #34D399;"></span> VISTA SEPARADA POR CATEGORÍAS
                </span>
            </div>
        </div>
        <div style="font-family: monospace; font-size: 11px; color: #34D399; background: rgba(255,255,255,0.03); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            👤 yanezdepablos
        </div>
    </div>
"""
st.markdown(header_top_html, unsafe_allow_html=True)

# Reloj UTC dinámico
clock_component_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: transparent; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; }
        .clock-box {
            font-family: monospace; font-size: 14px; color: #34D399;
            background: rgba(52,211,153,0.08); padding: 10px 20px; border-radius: 8px;
            border: 1px solid rgba(52,211,153,0.2); text-shadow: 0 0 8px rgba(52,211,153,0.5);
            letter-spacing: 0.05em; font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="clock-box" id="utc-clock">🕒 Sincronizando UTC...</div>
    <script>
        function updateUTC() {
            const now = new Date();
            const utcString = now.toUTCString().split(' ')[4];
            document.getElementById('utc-clock').innerText = "🕒 " + utcString + " UTC";
        }
        setInterval(updateUTC, 1000);
        updateUTC();
    </script>
</body>
</html>
"""
components.html(clock_component_html, height=50)

st.markdown("<br>", unsafe_allow_html=True)

# --- MATRICES SEPARADAS POR SECCIÓN ---

def render_asset_group(title_text, asset_keys):
    st.markdown(f'<div class="section-title">{title_text}</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(asset_keys), 6))
    for idx, asset in enumerate(asset_keys):
        if asset in assets_data:
            data = assets_data[asset]
            with cols[idx % 6]:
                st.markdown(f"""
                    <div class="neon-card" style="margin-bottom: 10px;">
                        <div style="font-size: 9px; font-weight: 700; color: #6B7280; background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; display: inline-block; margin-bottom: 4px; font-family: monospace;">{data['region']}</div>
                        <div style="font-size: 12px; font-weight: 800; color: #9CA3AF; margin-bottom: 4px; letter-spacing: 0.05em;">{asset}</div>
                        <div style="font-size: 20px; font-weight: 900; color: #FFFFFF; margin-bottom: 6px; font-family: monospace;">{data['score']:.1f}</div>
                        <div style="font-size: 8px; font-weight: 700; color: {data['color']}; background: {data['bg']}; padding: 2px 5px; border-radius: 6px; display: inline-block; border: 1px solid {data['color']}33;">{data['status']}</div>
                    </div>
                """, unsafe_allow_html=True)

# 1. Divisas
render_asset_group("💱 Divisas Principales y Cruzadas", ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD', 'SEK', 'NOK', 'SGD', 'ZAR'])

# 2. Metales y Energía
render_asset_group("🥇 Metales y Materias Primas (Energía)", ['XAU', 'XAG', 'OIL'])

# 3. Criptomonedas
render_asset_group("🪙 Criptomonedas", ['BTC', 'ETH'])

# 4. Futuros e Índices
render_asset_group("📈 Futuros, Índices y Volatilidad", ['US500', 'VIX'])

st.markdown("<br>", unsafe_allow_html=True)

# --- RANKING DE PARES Y ACTIVOS (ORDENADO STRICTAMENTE DE MAYOR A MENOR PROBABILIDAD) ---
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>🏆 Ranking Multiactivo (Ordenado de Mayor a Menor Probabilidad)</p>", unsafe_allow_html=True)

pairs_raw = [
    ("XAU/USD", "GOLD/USA", "Oro vs Dólar: Flujos de refugio institucional y tasas reales de la Fed."),
    ("BTC/USD", "CRYPTO/USA", "Bitcoin vs Dólar: Apetito al riesgo global y flujos institucionales ETF."),
    ("XAG/USD", "SILVER/USA", "Plata vs Dólar: Demanda industrial y correlación con metales preciosos."),
    ("OIL/USD", "ENERGY/USA", "Petróleo Crudo vs Dólar: Geopolítica, inventarios y oferta global."),
    ("ETH/USD", "CRYPTO/USA", "Ethereum vs Dólar: Dinámica de adopción tecnológica y liquidez de criptoactivos."),
    ("EUR/USD", "EUR/USA", "Euro vs Dólar: Divergencia macroeconómica BCE vs Fed."),
    ("GBP/USD", "GBR/USA", "Libra vs Dólar: Datos de empleo e inflación británica."),
    ("USD/JPY", "USA/JPN", "Dólar vs Yen: Divergencia de tipos de interés Fed vs Banco de Japón."),
    ("AUD/USD", "AUS/USA", "Australiano vs Dólar: Materias primas y ciclo de demanda asiática."),
    ("USD/CAD", "USA/CAN", "Dólar vs Canadiense: Correlación directa con flujos petroleros."),
    ("US500/USD", "INDEX/USA", "S&P 500 vs Dólar: Sentimiento de riesgo bursátil global."),
    ("EUR/GBP", "EUR/GBR", "Cruce estructural europeo de baja volatilidad relative.")
]

table_data = []
for pair, region, thesis in pairs_raw:
    base, quote = pair.split('/')
    b_score = assets_data.get(base, {'score': 5.0})['score']
    q_score = assets_data.get(quote, {'score': 5.0})['score']
    delta = b_score - q_score
    
    direction = "BUY" if delta > 0.3 else ("SELL" if delta < -0.3 else "NEUTRAL")
    dir_color = "#34D399" if direction == "BUY" else ("#EF4444" if direction == "SELL" else "#FBBF24")
    
    prob = int(min(96, max(52, 50 + abs(delta) * 11)))
    
    is_high_volatility = abs(delta) > 3.2
    risk = "Alto (Kill-Switch)" if is_high_volatility else ("Bajo" if prob > 72 else "Medio")
    risk_color = "#EF4444" if is_high_volatility else ("#34D399" if prob > 72 else "#FBBF24")
    
    table_data.append({
        "Pair": pair,
        "Region": region,
        "Dir": direction,
        "DirColor": dir_color,
        "Delta": round(delta, 1),
        "ProbVal": prob,
        "Prob": f"{prob}%",
        "Risk": risk,
        "RiskColor": risk_color,
        "Thesis": thesis
    })

# ORDENAMIENTO ESTRICTO: De mayor probabilidad a menor probabilidad
table_data = sorted(table_data, key=lambda x: x['ProbVal'], reverse=True)

for row in table_data:
    st.markdown(f"""
        <div style="background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px 20px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 6px 18px rgba(0,0,0,0.4);">
            <div style="display: flex; align-items: center; gap: 12px; width: 170px;">
                <span style="font-size: 9px; font-weight: 700; color: #9CA3AF; background: rgba(255,255,255,0.06); padding: 3px 6px; border-radius: 4px; font-family: monospace;">{row['Region']}</span>
                <span style="font-weight: 800; color: #FFFFFF; font-family: monospace; font-size: 14px;">{row['Pair']}</span>
            </div>
            <div><span style="color: {row['DirColor']}; font-weight: 800; background: {row['DirColor']}15; padding: 5px 12px; border-radius: 6px; border: 1px solid {row['DirColor']}33; font-size: 11px; text-shadow: 0 0 8px {row['DirColor']}66;">{row['Dir']}</span></div>
            <div style="font-family: monospace; font-weight: 700; color: #E5E7EB; font-size: 13px;">Delta: <span class="neon-glow">{row['Delta']:+.1f}</span></div>
            <div style="font-family: monospace; color: #34D399; font-weight: 800; font-size: 13px;">Prob: {row['Prob']}</div>
            <div><span style="color: {row['RiskColor']}; font-weight: 700; font-size: 11px;">{row['Risk']}</span></div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
selected_pair = st.selectbox("🔍 Selecciona un activo para ver su Tesis Fundamental Algorítmica:", [r['Pair'] for r in table_data])
selected_thesis = next(r['Thesis'] for r in table_data if r['Pair'] == selected_pair)
st.info(f"**Tesis Institucional para {selected_pair}:** {selected_thesis}")

# --- FEED DE NOTICIAS & LOG 72H ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;'>📰 Titulares Multiactivos en Vivo (Filtro Estricto Máximo 3 Días)</p>", unsafe_allow_html=True)

f_cols = st.columns(3)
for idx, item in enumerate(live_news_feed[:3]):
    sd_text = f"+{item['impact']} SD" if item['impact'] > 0 else f"{item['impact']} SD"
    color_val = "#34D399" if item['impact'] > 0 else "#EF4444"
    with f_cols[idx]:
        st.markdown(f"""
            <div class="neon-card" style="text-align: left; min-height: 155px;">
                <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 10px; color: #9CA3AF; margin-bottom: 6px;">
                    <span style="color: #6B7280; font-weight: bold;">{item['currency']} | {item['source'][:22]}</span>
                    <span style="color: {color_val}; font-weight: bold; text-shadow: 0 0 8px {color_val}66;">{sd_text}</span>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #F3F4F6; margin-bottom: 6px;">{item['title']}</div>
                <p style="font-size: 11px; color: #9CA3AF; margin: 0; line-height: 1.4;">{item['summary']}</p>
            </div>
        """, unsafe_allow_html=True)

with st.expander("📂 Ver Registro Histórico Multiactivo Procesado (< 72 Horas)"):
    history_df = pd.DataFrame(live_news_feed)
    st.dataframe(history_df, use_container_width=True)

# Refresco autónomo cada 30 segundos
time.sleep(30)
st.rerun()
