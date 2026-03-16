import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="طاهر | الطقس الذكي", page_icon="🌤️", layout="wide")

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * { font-family: 'IBM Plex Sans Arabic', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem;
    }
    .weather-card {
        background: white; padding: 1.5rem; border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center; margin-bottom: 1rem;
    }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; }
    .sun-card {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: white; padding: 1.5rem; border-radius: 20px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌤️ مركز طاهر للأرصاد الجوية</h1></div>', unsafe_allow_html=True)

# 3. دالة جلب البيانات
@st.cache_data(ttl=300)
def get_weather(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_res = requests.get(geo_url).json()
        if 'results' in geo_res:
            loc = geo_res['results'][0]
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}&longitude={loc['longitude']}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&timezone=auto"
            return requests.get(w_url).json(), loc['name']
    except: return None, None
    return None, None

city = st.sidebar.text_input("🔍 ابحث عن مدينة:", "Witten")
data, city_full_name = get_weather(city)

# 4. عرض البيانات (مع معالجة أخطاء KeyError و Indentation)
if data and 'current' in data:
    curr = data['current']
    daily = data['daily']

    tab1, tab2, tab3 = st.tabs(["📊 اليوم", "🗓️ الأسبوع", "💡 نصائح"])

    with tab1:
        # قسم الفيديو
        st.subheader(f"📺 الأجواء في {city_full_name}")
        v_url = "https://www.w3schools.com/html/mov_bbb.mp4" if curr['weather_code'] == 0 else "https://v.ftcdn.net/02/10/33/21/700_F_210332152_m6p6oT7fU6AAYkP7XWvXvB9B0A3JjV5m_ST.mp4"
        st.video(v_url)

        # بطاقات البيانات
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="weather-card">🌡️ حرارة<br><div class="metric-value">{curr["temperature_2m"]}°C</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="weather-card">💧 رطوبة<br><div class="metric-value">{curr["relative_humidity_2m"]}%</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="weather-card">🌬️ رياح<br><div class="metric-value">{curr["wind_speed_10m"]}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="weather-card">⏲️ ضغط<br><div class="metric-value">{int(curr["pressure_msl"])}</div></div>', unsafe_allow_html=True)

        # تصحيح سطر الشروق والغروب (السطر 421 سابقاً)
        st.divider()
        sc1, sc2 = st.columns(
