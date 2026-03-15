
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="طاهر | الطقس الذكي", page_icon="🌤️", layout="wide")

# التصميم الذي أعجبك (CSS)
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
        box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center;
    }
    .metric-value { font-size: 2.5rem; font-weight: 700; color: #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌤️ مركز طاهر للأرصاد الجوية</h1></div>', unsafe_allow_html=True)

# دالة جلب البيانات (المصححة)
@st.cache_data(ttl=300)
def get_weather_data(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_res = requests.get(geo_url).json()
        if 'results' in geo_res:
            loc = geo_res['results'][0]
            lat, lon = loc['latitude'], loc['longitude']
            # طلب البيانات الحالية واليومية معاً
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl&daily=sunrise,sunset,uv_index_max&timezone=auto"
            w_res = requests.get(w_url).json()
            return w_res, loc['name']
    except: return None, None
    return None, None

city = st.sidebar.text_input("🔍 ابحث عن مدينة:", "Witten")
data, city_full_name = get_weather_data(city)

if data and 'current' in data:
    curr = data['current']
    daily = data['daily']

    # 1. عرض الفيديو (نظرة حية) -
    st.subheader(f"📺 نظرة حية على الأجواء في {city_full_name}")
    if curr['weather_code'] == 0:
        st.video("https://www.w3schools.com/html/mov_bbb.mp4") # فيديو سماء صافية
    else:
        st.video("https://v.ftcdn.net/02/10/33/21/700_F_210332152_m6p6oT7fU6AAYkP7XWvXvB9B0A3JjV5m_ST.mp4") # فيديو غيوم/مطر

    # 2. بطاقات البيانات الأساسية -
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="weather-card"><div>🌡️ الحرارة</div><div class="metric-value">{curr["temperature_2m"]}°C</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="weather-card"><div>💧 الرطوبة</div><div class="metric-value">{curr["relative_humidity_2m"]}%</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="weather-card"><div>🌬️ الرياح</div><div class="metric-value">{curr["wind_speed_10m"]} كم/س</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="weather-card"><div>⏲️ الضغط</div><div class="metric-value">{int(curr["pressure_msl"])} hPa</div></div>', unsafe_allow_html=True)

    # 3. تفاصيل الشمس والأشعة -
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); padding: 20px; border-radius: 20px; color: white; text-align: center;">
                <h3>🌅 دورة الشمس اليوم</h3>
                <p>الشروق: {daily['sunrise'][0].split('T')[1]}</p>
                <p>الغروب: {daily['sunset'][0].split('T')[1]}</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%); padding: 20px; border-radius: 20px; color: white; text-align: center;">
                <h3>🔆 مؤشر الأشعة UV</h3>
                <div style="font-size: 2.5rem; font-weight: bold;">{daily['uv_index_max'][0]}</div>
                <p>{"منخفض" if daily['uv_index_max'][0] < 3 else "مرتفع، احذر!"}</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.warning("يرجى التأكد من اسم المدينة أو الانتظار قليلاً لتحديث البيانات.")

st.markdown("---")
st.info("تطبيق احترافي مطور بواسطة طاهر الذكي")
