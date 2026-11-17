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
        """,
