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
    page_title="Macro Edge FX — Terminal Institucional",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS limpios, minimalistas y optimizados para móvil (con parche para el badge flotante)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    .stApp {
        background-color: #07090E;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 100% !important;
    }

    .neon-glow {
        color: #34D399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.5);
    }
    
    .asset-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .section-header {
        font-size: 11px;
        font-weight: 800;
        color: #9CA3AF;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 24px;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }

    .stButton button {
        background: #111827 !important;
        color: #E5E7EB !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO PARA ESTABILIDAD ---
if 'asset_scores_history' not in st.session_state:
    st.session_state.asset_scores_history = {
        'USD': 5.5, 'EUR': 4.8, 'GBP': 5.0, 'JPY': 4.2, 'AUD': 5.1, 'CAD': 5.0, 
        'CHF': 5.3, 'NZD': 4.9, 'SEK': 5.0, 'NOK': 5.0, 'SGD': 5.2, 'ZAR': 4.7,
        'XAU': 6.8, 'XAG': 6.2, 'OIL': 5.4, 'BTC': 7.2, 'ETH': 6.5, 'US500': 6.1, 'VIX': 4.5
    }

# --- MOTOR MULTIACTIVO (FILTRO 72H + SENSIBILIDAD EQUILIBRADA) ---
def fetch_real_macro_news():
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
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for source_label, url in rss_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                for item in root.findall('.//item')[:15]:
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
                            if (now_utc - parsed_date).total_days() <= max_age_days:
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
                            score_delta += 0.6
                    for w in bearish_words:
                        if w in title_lower:
                            score_delta -= 0.6
                            
                    score_delta = round(max(-2.0, min(2.0, score_delta)), 1)
                    real_source = source_el.text if (source_el is not None and source_el.text) else source_label
                    
                    live_news.append({
                        "currency": detected_asset,
                        "source": f"{real_source} ({pub_time_str})",
                        "title": title_text,
                        "impact": score_delta,
                        "summary": f"Impacto analizado (< 3 días) para {detected_asset}."
                    })
        except Exception:
            continue

    if not live_news:
        live_news = [{"currency": "USD", "source": "Filtro 72h", "title": "Sincronizando flujo de mercado en vivo...", "impact": 0.0, "summary": "Esperando eventos recientes."}]

    target_scores = st.session_state.asset_scores_history.copy()
    for item in live_news:
        asset = item['currency']
        if asset in target_scores:
            target_scores[asset] += (item['impact'] * 0.35)
            target_scores[asset] = max(1.0, min(9.9, target_scores[asset]))

    alpha = 0.15
    processed_assets = {}
    region_map = {
        'USD': 'USA', 'EUR': 'EUR', 'GBP': 'GBR', 'JPY': 'JPN', 'AUD': 'AUS', 'CAD': 'CAN', 
        'CHF': 'CHE', 'NZD': 'NZL', 'SEK': 'SWE', 'NOK': 'NOR', 'SGD': 'SGP', 'ZAR': 'ZAF',
        'XAU': 'GOLD', 'XAG': 'SILVER', 'OIL': 'ENERGY', 'BTC': 'CRYPTO', 'ETH': 'CRYPTO', 'US500': 'INDEX', 'VIX': 'VOL'
    }
    
    for asset, old_score in st.session_state.asset_scores_history.items():
        new_target = target_scores.get(asset, old_score)
        smoothed_score = round(old_score * (1 - alpha) + new_target * alpha, 1)
        st.session_state.asset_scores_history[asset] = smoothed_score
        
        if smoothed_score >= 5.6:
            status, color, bg = "Fuerte", "#34D399", "rgba(52, 211, 153, 0.12)"
        elif smoothed_score <= 4.4:
            status, color, bg = "Débil", "#EF4444", "rgba(239, 68, 68, 0.12)"
        else:
            status, color, bg = "Neutral", "#FBBF24", "rgba(251, 191, 36, 0.12)"
            
        processed_assets[asset] = {
            'score': smoothed_score,
            'status': status,
            'region': region_map.get(asset, 'GLOBAL'),
            'color': color,
            'bg': bg
        }

    return processed_assets, live_news

# --- AUTENTICACIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(13, 17, 23, 0.95); padding: 35px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
                <div style="font-size: 28px; margin-bottom: 10px;">⚡</div>
                <h3 style="color: white; font-weight: 800; margin-bottom: 5px;">MACRO EDGE FX</h3>
                <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 20px;">Terminal Multiactivo Profesional</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("Usuario", value="yanezdepablos", disabled=True)
        pass_input = st.text_input("Contraseña", type="password", placeholder="Introduce la contraseña...")
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            if pass_input == "32157532Ca.$":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    st.stop()

assets_data, live_news_feed = fetch_real_macro_news()

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🧮 Gestión de Riesgo")
    account_balance = st.number_input("Balance ($)", value=10000.0, step=500.0)
    risk_pct = st.slider("Riesgo (%)", 0.1, 3.0, 1.0, 0.1)
    sl_pips = st.number_input("Stop Loss (Pips)", value=25.0, step=5.0)
    
    risk_amount = account_balance * (risk_pct / 100.0)
    recommended_lots = risk_amount / (sl_pips * 10.0)
    
    st.markdown(f"""
        <div style="background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.2); padding: 10px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; font-size: 11px; color: #34D399; font-weight: bold;">MÉTRICA:</p>
            <p style="margin: 2px 0; font-size: 12px; color: #FFF;">Riesgo: <b>${risk_amount:.2f}</b></p>
            <p style="margin: 2px 0; font-size: 12px; color: #34D399;">Lotes: <b>{recommended_lots:.2f}</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🕒 Killzones")
    utc_h = datetime.datetime.utcnow().hour
    session_text = "🟢 LONDRES / NY" if 7 <= utc_h < 20 else "🟡 ASIA / RANGO"
    st.markdown(f"<div style='font-size: 11px; color: #E5E7EB; background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;'>{session_text}</div>", unsafe_allow_html=True)

# --- CABECERA PRINCIPAL ---
st.markdown("""
    <div style="background: rgba(13, 17, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); padding: 14px 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <span style="font-size: 13px; font-weight: 800; color: white;">⚡ MACRO EDGE FX</span>
            <span style="font-size: 10px; color: #34D399; display: block; font-family: monospace;">● EN VIVO (72H FILTRADO)</span>
        </div>
        <div style="font-family: monospace; font-size: 11px; color: #34D399; background: rgba(255,255,255,0.04); padding: 4px 10px; border-radius: 6px;">
            👤 yanezdepablos
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MATRICES POR CATEGORÍA ---
def render_group(title, keys):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(keys), 6))
    for idx, k in enumerate(keys):
        if k in assets_data:
            d = assets_data[k]
            with cols[idx % 6]:
                st.markdown(f"""
                    <div class="asset-card">
                        <div style="font-size: 8px; color: #9CA3AF; font-family: monospace; margin-bottom: 2px;">{d['region']}</div>
                        <div style="font-size: 11px; font-weight: 800; color: #E5E7EB; margin-bottom: 2px;">{k}</div>
                        <div style="font-size: 18px; font-weight: 900; color: #FFF; font-family: monospace; margin-bottom: 4px;">{d['score']:.1f}</div>
                        <div style="font-size: 8px; font-weight: 700; color: {d['color']}; background: {d['bg']}; padding: 2px 4px; border-radius: 4px; display: inline-block;">{d['status']}</div>
                    </div>
                """, unsafe_allow_html=True)

render_group("💱 Divisas Principales y Cruzadas", ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD', 'SEK', 'NOK', 'SGD', 'ZAR'])
render_group("🥇 Metales y Energía", ['XAU', 'XAG', 'OIL'])
render_group("🪙 Criptomonedas", ['BTC', 'ETH'])
render_group("📈 Futuros e Índices", ['US500', 'VIX'])

st.markdown("<br>", unsafe_allow_html=True)

# --- RANKING DE PARES ---
st.markdown('<div class="section-header">🏆 Ranking Direccional de Activos (Probabilidad Descendente)</div>', unsafe_allow_html=True)

pairs_raw = [
    ("XAU/USD", "GOLD/USA", "Oro vs Dólar: Refugio institucional y tasas reales."),
    ("BTC/USD", "CRYPTO/USA", "Bitcoin vs Dólar: Apetito al riesgo y flujos ETF."),
    ("ETH/USD", "CRYPTO/USA", "Ethereum vs Dólar: Liquidez de criptoactivos."),
    ("XAG/USD", "SILVER/USA", "Plata vs Dólar: Demanda industrial y metales preciosos."),
    ("OIL/USD", "ENERGY/USA", "Petróleo vs Dólar: Geopolítica y oferta global."),
    ("EUR/USD", "EUR/USA", "Euro vs Dólar: Divergencia macroeconómica BCE vs Fed."),
    ("GBP/USD", "GBR/USA", "Libra vs Dólar: Empleo e inflación británica."),
    ("USD/JPY", "USA/JPN", "Dólar vs Yen: Divergencia de tipos Fed vs BoJ."),
    ("AUD/USD", "AUS/USA", "Australiano vs Dólar: Materias primas y demanda asiática."),
    ("USD/CAD", "USA/CAN", "Dólar vs Canadiense: Correlación petrolera."),
    ("US500/USD", "INDEX/USA", "S&P 500 vs Dólar: Sentimiento bursátil global."),
    ("EUR/GBP", "EUR/GBR", "Cruce estructural europeo.")
]

table_data = []
for pair, region, thesis in pairs_raw:
    b, q = pair.split('/')
    b_score = assets_data.get(b, {'score': 5.0})['score']
    q_score = assets_data.get(q, {'score': 5.0})['score']
    delta = b_score - q_score
    
    if delta > 0.25:
        direction = "COMPRAR"
        dir_color = "#34D399"
    elif delta < -0.25:
        direction = "VENDER"
        dir_color = "#EF4444"
    else:
        direction = "NEUTRAL"
        dir_color = "#FBBF24"
        
    prob = int(min(95, max(51, 50 + abs(delta) * 12)))
    risk = "Alto" if abs(delta) > 3.0 else ("Bajo" if prob > 70 else "Medio")
    risk_color = "#EF4444" if abs(delta) > 3.0 else ("#34D399" if prob > 70 else "#FBBF24")
    
    table_data.append({
        "Pair": pair, "Region": region, "Dir": direction, "Color": dir_color,
        "Delta": round(delta, 1), "ProbVal": prob, "Prob": f"{prob}%",
        "Risk": risk, "RiskColor": risk_color, "Thesis": thesis
    })

table_data = sorted(table_data, key=lambda x: x['ProbVal'], reverse=True)

for r in table_data:
    st.markdown(f"""
        <div style="background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div style="width: 140px;">
                <span style="font-size: 8px; color: #9CA3AF; font-family: monospace; display: block;">{r['Region']}</span>
                <span style="font-weight: 800; color: #FFF; font-family: monospace; font-size: 13px;">{r['Pair']}</span>
            </div>
            <div>
                <span style="color: {r['Color']}; font-weight: 800; background: {r['Color']}15; padding: 4px 10px; border-radius: 6px; border: 1px solid {r['Color']}33; font-size: 11px;">{r['Dir']}</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #E5E7EB;">
                Δ: <span class="neon-glow">{r['Delta']:+.1f}</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #34D399; font-weight: bold;">
                {r['Prob']}
            </div>
            <div>
                <span style="color: {r['RiskColor']}; font-weight: 700; font-size: 10px;">{r['Risk']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
sel_pair = st.selectbox("🔍 Selecciona un activo para ver su Tesis Fundamental:", [x['Pair'] for x in table_data])
sel_thesis = next(x['Thesis'] for x in table_data if x['Pair'] == sel_pair)
st.info(f"**Tesis Institucional ({sel_pair}):** {sel_thesis}")

# --- FEED DE NOTICIAS ---
st.markdown('<div class="section-header">📰 Feed de Inteligencia Macro (< 72 Horas)</div>', unsafe_allow_html=True)
f_cols = st.columns(3)
for idx, item in enumerate(live_news_feed[:3]):
    c_val = "#34D399" if item['impact'] > 0 else "#EF4444"
    with f_cols[idx]:
        st.markdown(f"""
            <div class="asset-card" style="text-align: left; min-height: 130px;">
                <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 9px; color: #9CA3AF; margin-bottom: 4px;">
                    <span><b>{item['currency']}</b></span>
                    <span style="color: {c_val};">{item['impact']:+.1f} SD</span>
                </div>
                <div style="font-size: 11px; font-weight: 700; color: #F3F4F6; margin-bottom: 4px;">{item['title']}</div>
                <p style="font-size: 10px; color: #9CA3AF; margin: 0; line-height: 1.3;">{item['summary']}</p>
            </div>
        """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
