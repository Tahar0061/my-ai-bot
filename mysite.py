import streamlit as st
import requests

# محاولة استيراد المكتبة بذكاء لتجنب الشاشة الحمراء
try:
    from streamlit_lottie import st_lottie
    LOTTIE_OK = True
except ImportError:
    LOTTIE_OK = False

# ... باقي الكود الخاص بك ...

# عند عرض الأيقونة المتحركة
if LOTTIE_OK:
    # هنا تضع كود st_lottie
    pass
else:
    st.info("جاري تحميل الأيقونات المتحركة... يرجى الانتظار")# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_lottie import st_lottie

# 1. إعداد الصفحة الفاخرة (S26 Ultra Style)
st.set_page_config(page_title="Taher | Weather Galaxy S26", page_icon="📱", layout="wide")

# 2. نظام اللغات العالمي (AR, EN, DE, FR)
LANGS = {
    "ar": {"search": "🔍 ابحث عن مدينة:", "settings": "⚙️ الإعدادات", "temp": "الحرارة", "hum": "الرطوبة", "wind": "الرياح", "uv": "مؤشر UV", "feels": "يشعر كـ", "aqi": "جودة الهواء", "wear": "ماذا ترتدي؟", "act": "الأنشطة", "updated": "تحديث ذكي:", "forecast": "📅 التوقعات"},
    "en": {"search": "🔍 Search City:", "settings": "⚙️ Settings", "temp": "Temperature", "hum": "Humidity", "wind": "Wind", "uv": "UV Index", "feels": "Feels like", "aqi": "Air Quality", "wear": "What to wear?", "act": "Activities", "updated": "Smart Update:", "forecast": "📅 Forecast"},
    "de": {"search": "🔍 Stadt suchen:", "settings": "⚙️ Einstellungen", "temp": "Temperatur", "hum": "Feuchtigkeit", "wind": "Wind", "uv": "UV-Index", "feels": "Gefühlt", "aqi": "Luftqualität", "wear": "Was anziehen?", "act": "Aktivitäten", "updated": "Update:", "forecast": "📅 Vorhersage"},
    "fr": {"search": "🔍 Chercher ville:", "settings": "⚙️ Paramètres", "temp": "Température", "hum": "Humidité", "wind": "Vent", "uv": "Indice UV", "feels": "Ressenti", "aqi": "Qualité d'air", "wear": "Que porter ?", "act": "Activités", "updated": "Mise à jour:", "forecast": "📅 Prévisions"}
}

if 'l' not in st.session_state: st.session_state.l = "ar"

# 3. واجهة الزجاج الفائقة (Ultra Glassmorphism CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif; }}
    body {{ background: #f4f7f9; }}
    .main-header {{
        background: linear-gradient(135deg, rgba(30,58,138,0.85), rgba(59,130,246,0.85));
        padding: 3rem; border-radius: 40px; color: white; text-align: center;
        backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15); margin-bottom: 2rem;
    }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.75); padding: 2rem; border-radius: 30px;
        backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4);
        text-align: center; transition: 0.4s ease-in-out; margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(31, 38, 135, 0.1);
    }}
    .glass-card:hover {{ transform: scale(1.05); background: rgba(255,255,255,0.95); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
    .m-val {{ font-size: 3rem; font-weight: 800; background: linear-gradient(45deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .m-lbl {{ font-size: 1rem; color: #444; font-weight: 700; letter-spacing: 1px; }}
    </style>
""", unsafe_allow_html=True)

# 4. محرك الأيقونات المتحركة (Lottie)
def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

lottie_weather = load_lottie("https://assets9.lottiefiles.com/packages/lf20_t0x0v9.json")

# 5. الشريط الجانبي
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>📱 Galaxy S26</h1>", unsafe_allow_html=True)
    st.session_state.l = st.selectbox("🌐 Language", ["ar", "en", "de", "fr"])
    _ = LANGS[st.session_state.l]
    city = st.text_input(_["search"], "دبي")
    st.markdown("---")
    st_lottie(lottie_weather, height=150)

# 6. جلب البيانات
@st.cache_data(ttl=300)
def get_data(name, lang):
    try:
        g = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language={lang}").json()
        if 'results' in g:
            l = g['results'][0]
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={l['latitude']}&longitude={l['longitude']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto").json()
            aq = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={l['latitude']}&longitude={l['longitude']}&current=european_aqi").json()
            return {'city': l['name'], 'country': l.get('country',''), 'curr': w['current'], 'daily': w['daily'], 'hourly': w['hourly'], 'aqi': aq['current']['european_aqi']}
    except: return None

data = get_data(city, st.session_state.l)

if data:
    c = data['curr']
    st.markdown(f"""<div class="main-header"><h1 style="font-size: 4rem; margin:0;">🌤️ {data['city']}</h1><p style="font-size: 1.5rem; opacity: 0.9;">{data['country']} | {c['temperature_2m']}°C</p></div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    items = [(_['temp'], f"{c['temperature_2m']}°", f"{_['feels']}: {c['apparent_temperature']}°"), (_['hum'], f"{c['relative_humidity_2m']}%", "Ideal"), (_['wind'], f"{c['wind_speed_10m']}", "km/h"), (_['aqi'], f"{data['aqi']}", "Good")]
    
    for i, (lbl, val, sub) in enumerate(items):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'<div class="glass-card"><div class="m-lbl">{lbl}</div><div class="m-val">{val}</div><div style="color:#777;">{sub}</div></div>', unsafe_allow_html=True)

    t1, t2 = st.tabs([_["forecast"], "📊 Analysis"])
    with t1:
        for i in range(7):
            st.markdown(f'<div class="glass-card" style="text-align:left; padding:15px;"><b>Day {i+1}</b>: {data["daily"]["temperature_2m_max"][i]}° / {data["daily"]["temperature_2m_min"][i]}°</div>', unsafe_allow_html=True)
    with t2:
        fig = go.Figure(go.Scatter(x=data['hourly']['time'][:24], y=data['hourly']['temperature_2m'][:24], fill='tozeroy', line=dict(color='#1e3a8a', width=5)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

st.markdown(f'<div style="text-align:center; color:#aaa; padding:30px;">{_["updated"]} Taher Weather Galaxy S26 • 2026</div>', unsafe_allow_html=True)
