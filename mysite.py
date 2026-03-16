# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعداد الصفحة الفاخرة
st.set_page_config(page_title="Taher | Weather OS", page_icon="📱", layout="wide")

# 2. نظام اللغات المتكامل (AR, EN, DE, FR)
LANGS = {
    "ar": {"search": "🔍 ابحث عن مدينة:", "temp": "الحرارة", "hum": "الرطوبة", "wind": "الرياح", "uv": "مؤشر UV", "feels": "يشعر كـ", "aqi": "جودة الهواء", "wear": "ماذا ترتدي؟", "act": "الأنشطة", "updated": "تحديث ذكي:"},
    "en": {"search": "🔍 Search City:", "temp": "Temperature", "hum": "Humidity", "wind": "Wind", "uv": "UV Index", "feels": "Feels like", "aqi": "Air Quality", "wear": "What to wear?", "act": "Activities", "updated": "Smart Update:"},
    "de": {"search": "🔍 Stadt suchen:", "temp": "Temperatur", "hum": "Feuchtigkeit", "wind": "Wind", "uv": "UV-Index", "feels": "Gefühlt", "aqi": "Luftqualität", "wear": "Was anziehen?", "act": "Aktivitäten", "updated": "Update:"},
    "fr": {"search": "🔍 Chercher ville:", "temp": "Température", "hum": "Humidité", "wind": "Vent", "uv": "Indice UV", "feels": "Ressenti", "aqi": "Qualité d'air", "wear": "Que porter ?", "act": "Activités", "updated": "Mise à jour:"}
}

if 'l' not in st.session_state: st.session_state.l = "ar"

# 3. واجهة الزجاج (Glassmorphism CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif; }}
    .main-header {{
        background: linear-gradient(135deg, rgba(102,126,234,0.8), rgba(118,75,162,0.8));
        padding: 2.5rem; border-radius: 30px; color: white; text-align: center;
        backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 2rem;
    }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.7); padding: 1.5rem; border-radius: 25px;
        backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);
        text-align: center; transition: 0.3s; margin-bottom: 1rem;
    }}
    .glass-card:hover {{ transform: translateY(-10px); background: rgba(255,255,255,0.9); }}
    .m-val {{ font-size: 2.8rem; font-weight: 800; color: #1e3a8a; margin: 5px 0; }}
    .m-lbl {{ font-size: 0.9rem; color: #555; font-weight: 700; text-transform: uppercase; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 1rem; }}
    .stTabs [data-baseweb="tab"] {{ background: rgba(255,255,255,0.5); border-radius: 12px; padding: 8px 20px; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 4. الشريط الجانبي والتحكم
with st.sidebar:
    st.title("⚙️ Weather OS")
    st.session_state.l = st.selectbox("🌐 Language / اللغة", ["ar", "en", "de", "fr"])
    _ = LANGS[st.session_state.l]
    city = st.text_input(_["search"], "دبي")
    st.markdown("---")
    st.info("💡 نظام الزجاج (Glassmorphism) مفعل الآن.")

# 5. جلب البيانات الذكية
@st.cache_data(ttl=300)
def get_data(name, lang):
    try:
        g = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language={lang}").json()
        if 'results' in g:
            l = g['results'][0]
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={l['latitude']}&longitude={l['longitude']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,uv_index&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto").json()
            aq = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={l['latitude']}&longitude={l['longitude']}&current=european_aqi").json()
            return {'city': l['name'], 'country': l.get('country',''), 'curr': w['current'], 'daily': w['daily'], 'hourly': w['hourly'], 'aqi': aq['current']['european_aqi']}
    except: return None

data = get_data(city, st.session_state.l)

if data:
    c = data['curr']
    # الهيدر الفاخر
    st.markdown(f"""
        <div class="main-header">
            <h1 style="font-size: 3.5rem; margin:0;">🌤️ {data['city']}</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">{data['country']} | {c['temperature_2m']}°C</p>
            <p style="opacity:0.7;">{_['updated']} {datetime.now().strftime('%H:%M')}</p>
        </div>
    """, unsafe_allow_html=True)

    # مكعبات المعلومات (Widgets)
    col1, col2, col3, col4 = st.columns(4)
    widgets = [
        (_['temp'], f"{c['temperature_2m']}°", f"{_['feels']}: {c['apparent_temperature']}°"),
        (_['hum'], f"{c['relative_humidity_2m']}%", "نقطة الندى: "+str(round(c['temperature_2m']-2,1))+"°"),
        (_['wind'], f"{c['wind_speed_10m']}", "كم/س | اتجاه ذكي"),
        (_['aqi'], f"{data['aqi']}", "نقي" if data['aqi'] < 50 else "متوسط")
    ]
    
    for i, (lbl, val, sub) in enumerate(widgets):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'<div class="glass-card"><div class="m-lbl">{lbl}</div><div class="m-val">{val}</div><div style="color:#666; font-size:0.8rem;">{sub}</div></div>', unsafe_allow_html=True)

    # التبويبات والرسوم
    t1, t2 = st.tabs(["📈 التحليل", "📅 الأسبوع"])
    with t1:
        fig = go.Figure(go.Scatter(x=data['hourly']['time'][:24], y=data['hourly']['temperature_2m'][:24], fill='tozeroy', line=dict(color='#1e3a8a', width=4)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        for i in range(7):
            st.markdown(f'<div class="glass-card" style="text-align:left; padding:10px 20px;"><b>اليوم {i+1}</b>: {data["daily"]["temperature_2m_max"][i]}° / {data["daily"]["temperature_2m_min"][i]}°</div>', unsafe_allow_html=True)

else:
    st.info("🔍 ابحث عن مدينة للبدء.")

st.markdown(f'<div style="text-align:center; color:#888; padding:20px;">{_["updated"]} Taher Weather OS 2026</div>', unsafe_allow_html=True)
