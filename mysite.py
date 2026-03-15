import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="طاهر | الطقس الذكي", page_icon="🌤️", layout="wide")

# تصميم CSS احترافي متكامل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * { font-family: 'IBM Plex Sans Arabic', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;
    }
    .weather-card {
        background: #f8f9fa; padding: 15px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌤️ مركز طاهر للأرصاد الجوية</h1></div>', unsafe_allow_html=True)

# دالة جلب البيانات
@st.cache_data(ttl=300)
def get_weather(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        res = requests.get(geo_url).json()
        if 'results' in res:
            loc = res['results'][0]
            lat, lon = loc['latitude'], loc['longitude']
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl&daily=sunrise,sunset,uv_index_max&timezone=auto"
            return requests.get(w_url).json(), loc['name']
    except: return None, None
    return None, None

city = st.sidebar.text_input("🔍 ابحث عن مدينة:", "Witten")
data, city_name = get_weather(city)

if data:
    curr = data['current']
    daily = data['daily']

    # --- 1. قسم الفيديوهات (نظرة حية) ---
    st.subheader("📺 محاكاة حالة الطقس")
    code = curr['weather_code']
    if code == 0: # صافي
        st.video("https://www.w3schools.com/html/mov_bbb.mp4") 
    elif code in [1, 2, 3]: # غيوم
        st.video("https://www.shutterstock.com/shutterstock/videos/1060194382/preview/stock-footage-beautiful-white-clouds-soar-across-the-blue-sky.mp4")
    else: # مطر
        st.video("https://www.w3schools.com/html/rain.mp4")

    st.divider()

    # --- 2. أيقونات البيانات الأساسية (مثل صورك 776 و 780) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="weather-card"><div>🌡️ الحرارة</div><div class="metric-value">{curr["temperature_2m"]}°C</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="weather-card"><div>💧 الرطوبة</div><div class="metric-value">{curr["relative_humidity_2m"]}%</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="weather-card"><div>🌬️ الرياح</div><div class="metric-value">{curr["wind_speed_10m"]} كم/س</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="weather-card"><div>⏲️ الضغط</div><div class="metric-value">{int(curr["pressure_msl"])} hPa</div></div>', unsafe_allow_html=True)

    st.divider()

    # --- 3. الشمس والأنشطة (مثل 782) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("☀️ دورة الشمس")
        st.write(f"🌅 الشروق: {daily['sunrise'][0].split('T')[1]}")
        st.write(f"🌇 الغروب: {daily['sunset'][0].split('T')[1]}")
    with c2:
        st.subheader("🔆 الأشعة والجو")
        st.write(f"مؤشر UV: {daily['uv_index_max'][0]}")
        st.progress(min(daily['uv_index_max'][0] / 12, 1.0))
    with c3:
        st.subheader("🏃 نصيحة طاهر")
        if curr['temperature_2m'] < 30 and code < 3:
            st.success("الجو مثالي للمشي الآن! 🏃")
        else:
            st.warning("يفضل البقاء في الداخل 🏠")

else:
    st.error("تأكد من كتابة اسم المدينة بشكل صحيح.")
