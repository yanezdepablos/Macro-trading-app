import streamlit as st
import datetime
import pandas as pd
import time
import urllib.request
import xml.etree.ElementTree as ET
import streamlit.components.v1 as components
import email.utils
import sqlite3

# Configuración de la página institucional
st.set_page_config(
    page_title="Macro Edge FX — Terminal SaaS",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS limpios y optimizados para PC y móvil
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
        padding-bottom: 4rem !important;
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
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .section-header {
        font-size: 12px;
        font-weight: 800;
        color: #34D399;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 28px;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(52, 211, 153, 0.3);
        padding-bottom: 6px;
    }

    .ranking-card {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    .card-row-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .card-row-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE BASE DE DATOS DE LICENCIAS (SQLITE) ---
def init_db():
    conn = sqlite3.connect('macro_licenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        INSERT OR REPLACE INTO users (username, password, expiry_date, is_admin)
        VALUES ('yanezdepablos', '32157532Ca', '2099-12-31', 1)
    ''')
    conn.commit()
    conn.close()

init_db()

# --- GESTIÓN DE SESIÓN Y LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'show_admin_panel' not in st.session_state:
    st.session_state.show_admin_panel = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(7, 9, 14, 0.98)); 
                        padding: 40px 30px; border-radius: 18px; border: 1px solid rgba(52, 211, 153, 0.2); 
                        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="font-size: 32px; margin-bottom: 8px;">⚡</div>
                <h2 style="color: white; font-weight: 900; letter-spacing: 0.05em; margin-bottom: 2px;">MACRO EDGE FX</h2>
                <p style="color: #34D399; font-size: 11px; font-family: monospace; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 25px;">Terminal Multiactivo Profesional</p>
                <div style="border-top: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;"></div>
        """, unsafe_allow_html=True)
        
        login_user = st.text_input("Usuario de Acceso", placeholder="Introduce tu usuario...")
        login_pass = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña...")
        
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        
        if st.button("ACCEDER A LA TERMINAL", use_container_width=True):
            conn = sqlite3.connect('macro_licenses.db')
            cursor = conn.cursor()
            cursor.execute("SELECT password, expiry_date, is_admin FROM users WHERE username = ?", (login_user,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                db_pass, db_expiry, db_admin = row
                if login_pass == db_pass:
                    today_str = datetime.date.today().strftime("%Y-%m-%d")
                    if db_expiry >= today_str:
                        st.session_state.logged_in = True
                        st.session_state.username = login_user
                        st.session_state.is_admin = bool(db_admin)
                        st.rerun()
                    else:
                        st.error("⚠️ Su licencia mensual ha expirado. Contacte al administrador.")
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no registrado o inactivo.")
        
        st.markdown("""
                <div style="margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 15px;">
                    <span style="color: #6B7280; font-size: 10px; font-family: monospace; letter-spacing: 0.05em;">ENGINEERED & MANAGED BY</span>
                    <div style="color: #34D399; font-size: 12px; font-weight: 700; margin-top: 2px; letter-spacing: 0.08em;">YANEZDEPABLOS</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- INICIALIZACIÓN DE ESTADO ESTABLE PARA PRECIOS ---
if 'asset_scores_history' not in st.session_state:
    st.session_state.asset_scores_history = {
        'USD': 5.5, 'EUR': 4.8, 'GBP': 5.0, 'JPY': 4.2, 'AUD': 5.1, 'CAD': 5.0, 
        'CHF': 5.3, 'NZD': 4.9, 'SEK': 5.0, 'NOK': 5.0, 'SGD': 5.2, 'ZAR': 4.7,
        'XAU': 6.8, 'XAG': 6.2, 'WTI': 5.4, 'BTC': 7.2, 'ETH': 6.5, 'US500': 6.1, 'VIX': 4.5
    }

# --- MOTOR MULTIACTIVO AISLADO ---
@st.cache_data(ttl=300)
def fetch_real_macro_news_cached():
    url = "https://news.google.com/rss/search?q=forex+OR+gold+OR+bitcoin+OR+wti+oil+OR+fed+inflation+when:3d&hl=en-US&gl=US&ceid=US:en"
    
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
        'WTI': ['wti', 'crude', 'oil', 'brent', 'energy', 'opec'],
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
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:15]:
                title_el = item.find('title')
                pub_el = item.find('pubDate')
                source_el = item.find('source')
                
                if title_el is None or not title_el.text: continue
                title_text = title_el.text.strip()
                
                norm_title = title_text.lower().strip()
                if norm_title in seen_titles: continue
                    
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
                        
                if not is_recent: continue
                seen_titles.add(norm_title)
                title_lower = title_text.lower()
                
                detected_asset = 'USD'
                for asset, kws in asset_keywords.items():
                    if any(kw in title_lower for kw in kws):
                        detected_asset = asset
                        break
                        
                score_delta = 0.0
                for w in bullish_words:
                    if w in title_lower: score_delta += 0.6
                for w in bearish_words:
                    if w in title_lower: score_delta -= 0.6
                        
                score_delta = round(max(-2.0, min(2.0, score_delta)), 1)
                real_source = source_el.text if (source_el is not None and source_el.text) else "Google News"
                
                live_news.append({
                    "currency": detected_asset,
                    "source": f"{real_source} ({pub_time_str})",
                    "title": title_text,
                    "impact": score_delta,
                    "summary": f"Impacto analizado (< 3 días) para {detected_asset}."
                })
    except Exception:
        pass

    if not live_news:
        live_news = [{"currency": "USD", "source": "Filtro 72h", "title": "Sincronizando flujo de mercado en vivo...", "impact": 0.0, "summary": "Esperando eventos recientes."}]

    return live_news

live_news_feed = fetch_real_macro_news_cached()

if 'last_news_processed' not in st.session_state:
    st.session_state.last_news_processed = len(live_news_feed)
    target_scores = st.session_state.asset_scores_history.copy()
    for item in live_news_feed:
        asset = item['currency']
        if asset in target_scores:
            target_scores[asset] += (item['impact'] * 0.35)
            target_scores[asset] = max(1.0, min(9.9, target_scores[asset]))

    alpha = 0.15
    for asset, old_score in st.session_state.asset_scores_history.items():
        new_target = target_scores.get(asset, old_score)
        smoothed_score = round(old_score * (1 - alpha) + new_target * alpha, 1)
        st.session_state.asset_scores_history[asset] = smoothed_score

assets_data = {}
region_map = {
    'USD': 'USA', 'EUR': 'EUR', 'GBP': 'GBR', 'JPY': 'JPN', 'AUD': 'AUS', 'CAD': 'CAN', 
    'CHF': 'CHE', 'NZD': 'NZL', 'SEK': 'SWE', 'NOK': 'NOR', 'SGD': 'SGP', 'ZAR': 'ZAF',
    'XAU': 'GOLD', 'XAG': 'SILVER', 'WTI': 'ENERGY', 'BTC': 'CRYPTO', 'ETH': 'CRYPTO', 'US500': 'INDEX', 'VIX': 'VOL'
}

for asset, smoothed_score in st.session_state.asset_scores_history.items():
    if smoothed_score >= 5.6:
        status, color, bg = "Fuerte", "#34D399", "rgba(52, 211, 153, 0.12)"
    elif smoothed_score <= 4.4:
        status, color, bg = "Débil", "#EF4444", "rgba(239, 68, 68, 0.12)"
    else:
        status, color, bg = "Neutral", "#FBBF24", "rgba(251, 191, 36, 0.12)"
        
    assets_data[asset] = {
        'score': smoothed_score,
        'status': status,
        'region': region_map.get(asset, 'GLOBAL'),
        'color': color,
        'bg': bg
    }

# --- BARRA LATERAL (GESTIÓN DE RIESGO) ---
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

# --- CABECERA PRINCIPAL Y BOTÓN ADMIN ---
user_badge = f"👑 {st.session_state.username}" if st.session_state.is_admin else f"🛡️ {st.session_state.username}"

st.markdown(f"""
    <div style="background: rgba(13, 17, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); padding: 14px 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div>
            <span style="font-size: 13px; font-weight: 800; color: white;">⚡ MACRO EDGE FX</span>
            <span style="font-size: 10px; color: #34D399; display: block; font-family: monospace;">● EN VIVO (72H FILTRADO)</span>
        </div>
        <div style="font-family: monospace; font-size: 11px; color: #34D399; background: rgba(52,211,153,0.04); padding: 4px 12px; border-radius: 6px; border: 1px solid rgba(52,211,153,0.15);">
            {user_badge}
        </div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.username == "yanezdepablos":
    st.session_state.is_admin = True
    btn_text = "🔒 Cerrar Panel Admin SaaS" if st.session_state.show_admin_panel else "🔐 Abrir Panel Admin SaaS"
    if st.button(btn_text, use_container_width=True):
        st.session_state.show_admin_panel = not st.session_state.show_admin_panel
        st.rerun()

# --- PANEL DE ADMINISTRACIÓN SAAS ---
if st.session_state.is_admin and st.session_state.show_admin_panel:
    with st.container():
        st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.98); border: 1px solid rgba(52, 211, 153, 0.4); padding: 25px; border-radius: 14px; margin-top: 10px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
                <h3 style="color: #34D399; margin-top: 0; font-size: 16px; font-weight: 800; letter-spacing: 0.05em;">🔐 PANEL DE ADMINISTRACIÓN SAAS</h3>
        """, unsafe_allow_html=True)
        
        col_adm1, col_adm2 = st.columns(2, gap="large")
        with col_adm1:
            new_client = st.text_input("Usuario del Cliente", key="admin_new_client")
            new_pass = st.text_input("Contraseña del Cliente", type="password", key="admin_new_pass")
            days_valid = st.number_input("Días de Suscripción", value=30, step=1, key="admin_days")
            
            if st.button("Crear / Renovar Licencia", use_container_width=True):
                if new_client and new_pass:
                    expiry = (datetime.date.today() + datetime.timedelta(days=int(days_valid))).strftime("%Y-%m-%d")
                    conn = sqlite3.connect('macro_licenses.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO users (username, password, expiry_date, is_admin)
                        VALUES (?, ?, ?, 0)
                        ON CONFLICT(username) DO UPDATE SET password=excluded.password, expiry_date=excluded.expiry_date
                    ''', (new_client, new_pass, expiry))
                    conn.commit()
                    conn.close()
                    st.success(f"¡Licencia creada con éxito para {new_client} hasta el {expiry}!")
                else:
                    st.warning("Por favor completa el usuario y la contraseña.")
                    
        with col_adm2:
            st.markdown("<p style='font-size: 13px; font-weight: bold; color: #E5E7EB; margin-bottom: 8px;'>Clientes Registrados:</p>", unsafe_allow_html=True)
            conn = sqlite3.connect('macro_licenses.db')
            df_users = pd.read_sql_query("SELECT username, expiry_date FROM users WHERE is_admin = 0", conn)
            conn.close()
            if not df_users.empty:
                st.dataframe(df_users, use_container_width=True, height=180)
            else:
                st.info("No hay clientes registrados aún.")
                
        st.markdown("</div>", unsafe_allow_html=True)

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
render_group("🥇 Metales y Energía (WTI Spot)", ['XAU', 'XAG', 'WTI'])
render_group("🪙 Criptomonedas", ['BTC', 'ETH'])
render_group("📈 Futuros e Índices", ['US500', 'VIX'])

st.markdown("<br>", unsafe_allow_html=True)

# --- TABLAS DE RANKING ---
def render_single_asset_ranking(category_title, assets_list):
    st.markdown(f'<div class="section-header">🏆 Ranking: {category_title} (Probabilidad Descendente)</div>', unsafe_allow_html=True)
    
    table_data = []
    for asset_key, region, thesis in assets_list:
        score = assets_data.get(asset_key, {'score': 5.0})['score']
        if score >= 5.6:
            direction, dir_color = "COMPRAR", "#34D399"
        elif score <= 4.4:
            direction, dir_color = "VENDER", "#EF4444"
        else:
            direction, dir_color = "NEUTRAL", "#FBBF24"
            
        prob = int(min(95, max(51, 50 + abs(score - 5.0) * 15)))
        risk = "Alto" if abs(score - 5.0) > 2.5 else ("Bajo" if prob > 70 else "Medio")
        risk_color = "#EF4444" if abs(score - 5.0) > 2.5 else ("#34D399" if prob > 70 else "#FBBF24")
        
        table_data.append({
            "Asset": asset_key, "Region": region, "Dir": direction, "Color": dir_color,
            "Score": score, "ProbVal": prob, "Prob": f"{prob}%",
            "Risk": risk, "RiskColor": risk_color, "Thesis": thesis
        })
    
    table_data = sorted(table_data, key=lambda x: x['ProbVal'], reverse=True)
    
    for r in table_data:
        st.markdown(f"""
            <div class="ranking-card">
                <div class="card-row-top">
                    <div>
                        <span style="font-size: 8px; color: #9CA3AF; font-family: monospace; display: block;">{r['Region']}</span>
                        <span style="font-weight: 900; color: #FFF; font-family: monospace; font-size: 15px;">{r['Asset']}</span>
                    </div>
                    <div>
                        <span style="color: {r['Color']}; font-weight: 800; background: {r['Color']}15; padding: 4px 12px; border-radius: 6px; border: 1px solid {r['Color']}33; font-size: 11px;">{r['Dir']}</span>
                    </div>
                    <div style="font-family: monospace; font-size: 15px; color: #34D399; font-weight: 900;">
                        {r['Prob']}
                    </div>
                </div>
                <div class="card-row-bottom">
                    <div style="font-family: monospace; font-size: 11px; color: #9CA3AF;">
                        Score: <span class="neon-glow" style="font-weight: bold;">{r['Score']:.1f}</span>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {r['RiskColor']};">
                        Riesgo: {r['Risk']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def render_category_ranking(category_title, pairs_list):
    st.markdown(f'<div class="section-header">🏆 Ranking: {category_title} (Probabilidad Descendente)</div>', unsafe_allow_html=True)
    
    table_data = []
    for pair, region, thesis in pairs_list:
        b, q = pair.split('/')
        b_score = assets_data.get(b, {'score': 5.0})['score']
        q_score = assets_data.get(q, {'score': 5.0})['score']
        delta = b_score - q_score
        
        if delta > 0.25:
            direction, dir_color = "COMPRAR", "#34D399"
        elif delta < -0.25:
            direction, dir_color = "VENDER", "#EF4444"
        else:
            direction, dir_color = "NEUTRAL", "#FBBF24"
            
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
            <div class="ranking-card">
                <div class="card-row-top">
                    <div>
                        <span style="font-size: 8px; color: #9CA3AF; font-family: monospace; display: block;">{r['Region']}</span>
                        <span style="font-weight: 900; color: #FFF; font-family: monospace; font-size: 15px;">{r['Pair']}</span>
                    </div>
                    <div>
                        <span style="color: {r['Color']}; font-weight: 800; background: {r['Color']}15; padding: 4px 12px; border-radius: 6px; border: 1px solid {r['Color']}33; font-size: 11px;">{r['Dir']}</span>
                    </div>
                    <div style="font-family: monospace; font-size: 15px; color: #34D399; font-weight: 900;">
                        {r['Prob']}
                    </div>
                </div>
                <div class="card-row-bottom">
                    <div style="font-family: monospace; font-size: 11px; color: #9CA3AF;">
                        Delta: <span class="neon-glow" style="font-weight: bold;">{r['Delta']:+.1f}</span>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {r['RiskColor']};">
                        Riesgo: {r['Risk']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# 1. Divisas (Lista Ampliada y Completa)
forex_pairs = [
    ("EUR/USD", "EUR/USA", "Euro vs Dólar: Divergencia macroeconómica BCE vs Fed."),
    ("GBP/USD", "GBR/USA", "Libra vs Dólar: Empleo e inflación británica."),
    ("USD/JPY", "USA/JPN", "Dólar vs Yen: Divergencia de tipos Fed vs BoJ."),
    ("AUD/USD", "AUS/USA", "Australiano vs Dólar: Materias primas y demanda asiática."),
    ("USD/CAD", "USA/CAN", "Dólar vs Canadiense: Correlación petrolera y balanza comercial."),
    ("NZD/USD", "NZL/USA", "Neozelandés vs Dólar: Dairy auction y flujos oceanía."),
    ("USD/CHF", "USA/CHE", "Dólar vs Franco Suizo: Refugio seguro vs tasa de interés."),
    ("EUR/GBP", "EUR/GBR", "Cruce estructural europeo: Comercio bilateral Reino Unido-UE."),
    ("EUR/JPY", "EUR/JPY", "Euro vs Yen: Cruce de alta volatilidad y apetito al riesgo."),
    ("GBP/JPY", "GBR/JPN", "Libra vs Yen ('The Beast'): Máxima volatilidad y carry trade."),
    ("AUD/JPY", "AUS/JPN", "Australiano vs Yen: Indicador clave del sentimiento de riesgo global.")
]
render_category_ranking("Divisas", forex_pairs)

# 2. Metales y Energía (WTI Spot)
metals_energy_assets = [
    ("XAU", "GOLD", "Oro Spot: Activo de refugio institucional y tasas reales."),
    ("XAG", "SILVER", "Plata Spot: Demanda industrial y metales preciosos."),
    ("WTI", "ENERGY", "WTI Spot Oil: Petróleo crudo, inventarios y geopolítica en tiempo real.")
]
render_single_asset_ranking("Metales y Energía (WTI Spot)", metals_energy_assets)

# 3. Criptomonedas
crypto_assets = [
    ("BTC", "CRYPTO", "Bitcoin: Apetito al riesgo global y flujos de mercado institucional."),
    ("ETH", "CRYPTO", "Ethereum: Liquidez y adopción en ecosistema de criptoactivos.")
]
render_single_asset_ranking("Criptomonedas", crypto_assets)

# 4. Futuros e Índices
futures_assets = [
    ("US500", "INDEX", "S&P 500: Sentimiento bursátil y liquidez de renta variable global."),
    ("VIX", "VOLATILITY", "Índice de Volatilidad: Miedo y aversión al riesgo en mercados globales.")
]
render_single_asset_ranking("Futuros, Índices y Volatilidad", futures_assets)

# --- SELECTOR DE TESIS ---
all_selectors = [x[0] for x in forex_pairs] + [x[0] for x in metals_energy_assets] + [x[0] for x in crypto_assets] + [x[0] for x in futures_assets]
sel_asset = st.selectbox("🔍 Selecciona un activo para ver su Tesis Fundamental:", all_selectors)

def get_thesis(asset):
    for p, r, t in forex_pairs:
        if p == asset: return t
    for a, r, t in metals_energy_assets:
        if a == asset: return t
    for a, r, t in crypto_assets:
        if a == asset: return t
    for a, r, t in futures_assets:
        if a == asset: return t
    return "Análisis macroeconómico institucional en curso."

st.info(f"**Tesis Institucional ({sel_asset}):** {get_thesis(sel_asset)}")

# --- FEED DE NOTICIAS (FORZADO A MÁXIMO 3 ÚNICAS) ---
st.markdown('<div class="section-header">📰 Feed de Inteligencia Macro (< 72 Horas)</div>', unsafe_allow_html=True)

raw_news = fetch_real_macro_news_cached()
unique_news = []
seen_titles_final = set()

for item in raw_news:
    t_clean = item['title'].lower().strip()
    if t_clean not in seen_titles_final:
        seen_titles_final.add(t_clean)
        unique_news.append(item)
    if len(unique_news) == 3:  # Forzamos exactamente 3
        break

# Renderizado vertical limpio y blindado
for item in unique_news:
    c_val = "#34D399" if item['impact'] > 0 else "#EF4444"
    st.markdown(f"""
        <div class="asset-card">
            <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 9px; color: #9CA3AF; margin-bottom: 4px;">
                <span><b>{item['currency']}</b></span>
                <span style="color: {c_val};">{item['impact']:+.1f} SD</span>
            </div>
            <div style="font-size: 12px; font-weight: 700; color: #F3F4F6; margin-bottom: 4px;">{item['title']}</div>
            <p style="font-size: 10px; color: #9CA3AF; margin: 0; line-height: 1.3;">{item['summary']}</p>
        </div>
    """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
