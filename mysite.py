# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
from PIL import Image
import io
import base64

# 1. إعداد الصفحة
st.set_page_config(
    page_title="طاهر | الطقس الذكي",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تثبيت التصميم الحديث (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'IBM Plex Sans Arabic', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .weather-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        border: 1px solid #f0f0f0;
        text-align: center;
    }
    
    .weather-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sun-card {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    .weather-icon-large {
        font-size: 4rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .hour-item {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }
    
    .air-quality {
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    
    .aqi-good { background: #00e676; }
    .aqi-moderate { background: #ffeb3b; color: #333; }
    .aqi-unhealthy { background: #ff9800; }
    .aqi-very-unhealthy { background: #f44336; }
    .aqi-hazardous { background: #9c27b0; }
    </style>
""", unsafe_allow_html=True)

# 3. الواجهة الرئيسية
st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5rem;">🌤️ طاهر | الطقس الذكي</h1>
        <p style="margin:0; opacity: 0.9; font-size: 1.1rem;">تطبيق الطقس المتطور مع واجهة حديثة</p>
    </div>
""", unsafe_allow_html=True)

# 4. الشريط الجانبي (تم تصحيح ssidebar إلى sidebar)
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    city = st.text_input("🔍 ابحث عن مدينة:", "Witten")
    
    st.markdown("### ⭐ المدن المفضلة")
    favorite_cities = ["الرياض", "جدة", "دبي", "القاهرة", "الدوحة"]
    cols = st.columns(2)
    for i, fav_city in enumerate(favorite_cities):
        with cols[i % 2]:
            if st.button(f"📍 {fav_city}", key=f"fav_{fav_city}"):
                city = fav_city
                st.rerun()
    
    st.markdown("### 📏 الوحدات")
    unit_system = st.radio("نظام الوحدات:", ["متري (°C, km/h)", "إمبراطوري (°F, mph)"])
    
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.rerun()

# 5. وظائف جلب البيانات
@st.cache_data(ttl=300)
def get_weather_data(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_response = requests.get(geo_url, timeout=10)
        geo_data = geo_response.json()
        
        if 'results' in geo_data and len(geo_data['results']) > 0:
            location = geo_data['results'][0]
            lat, lon = location['latitude'], location['longitude']
            city_name_ar = location.get('name', city_name)
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl,visibility&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=7"
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()
            
            return {
                'city': city_name_ar,
                'location': location,
                'current': weather_data['current'],
                'hourly': weather_data['hourly'],
                'daily': weather_data['daily'],
                'aqi': {'aqi': 45} # قيمة افتراضية
            }
        else:
            st.warning(f"لم يتم العثور على مدينة باسم '{city_name}'")
            return None
    except Exception as e:
        st.error(f"خطأ: {str(e)}")
        return None

def get_weather_icon(code, is_day=True):
    icons = {0: "☀️" if is_day else "🌙", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌦️", 61: "🌧️", 71: "❄️", 80: "🌧️", 95: "⛈️"}
    return icons.get(code, "🌈")

def get_weather_description(code):
    descriptions = {0: "سماء صافية", 1: "قليل السحب", 2: "غائم جزئياً", 3: "غائم", 45: "ضباب", 61: "مطر خفيف", 95: "عواصف رعدية"}
    return descriptions.get(code, "حالة جوية غير معروفة")

# 6. عرض البيانات
data = get_weather_data(city)

if data:
    current, daily, hourly, aqi = data['current'], data['daily'], data['hourly'], data['aqi']
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### 🌍 {data['city']}")
        st.markdown(f"📍 {data['location'].get('admin1', '')}, {data['location'].get('country', '')}")
        st.markdown(f"🕐 {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    with col2:
        st.markdown(f'<div class="weather-icon-large">{get_weather_icon(current["weather_code"], current["is_day"])}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-value">{current["temperature_2m"]}°C</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">يشعر كـ {current["apparent_temperature"]}°C</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 اليوم", "📈 7 أيام", "🌡️ تفاصيل", "🎯 التوصيات"])
    
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="weather-card"><div class="metric-label">💧 الرطوبة</div><div class="metric-value">{current["relative_humidity_2m"]}%</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="weather-card"><div class="metric-label">💨 الرياح</div><div class="metric-value">{current["wind_speed_10m"]} كم/س</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="weather-card"><div class="metric-label">📊 الضغط</div><div class="metric-value">{current["pressure_msl"]}</div></div>', unsafe_allow_html=True)
        
        aqi_val = aqi['aqi']
        aqi_class = "aqi-good" if aqi_val <= 50 else "aqi-moderate"
        c4.markdown(f'<div class="air-quality {aqi_class}">🌫️ جودة الهواء<br><span style="font-size:1.5rem">{aqi_val}</span><br>جيد</div>', unsafe_allow_html=True)
        
        st.markdown("### 📅 التوقعات للساعات القادمة")
        h_cols = st.columns(6)
        for i in range(6):
            with h_cols[i]:
                t = datetime.fromisoformat(hourly['time'][i]).strftime("%H:%M")
                st.markdown(f'<div class="hour-item"><b>{t}</b><br>{get_weather_icon(hourly["weather_code"][i])}<br><b>{hourly["temperature_2m"][i]}°C</b></div>', unsafe_allow_html=True)

        # شروق وغروب الشمس (تم تصحيح الرموز هنا لمنع SyntaxError)
        s1, s2 = st.columns(2)
        sunrise = datetime.fromisoformat(daily['sunrise'][0]).strftime('%H:%M')
        sunset = datetime.fromisoformat(daily['sunset'][0]).strftime('%H:%M')
        s1.markdown(f'<div class="sun-card">🌅 شروق الشمس<br><span style="font-size:1.5rem; font-weight:bold;">{sunrise}</span></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="sun-card">🌇 غروب الشمس<br><span style="font-size:1.5rem; font-weight:bold;">{sunset}</span></div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📈 توقعات 7 أيام")
        for i in range(7):
            day = datetime.fromisoformat(daily['time'][i]).strftime('%A %d/%m')
            st.write(f"**{day}:** عظمى {daily['temperature_2m_max'][i]}°C | صغرى {daily['temperature_2m_min'][i]}°C")

    with tab3:
        st.markdown("### 🌡️ تفاصيل إضافية")
        st.write(f"الرؤية: {current['visibility']} متر")
        st.write(f"مؤشر UV: {daily['uv_index_max'][0]}")
        st.write(f"كمية الأمطار: {daily['precipitation_sum'][0]} مم")

    with tab4:
        st.markdown("### 🎯 التوصيات")
        if current['temperature_2m'] < 15: st.info("الجو بارد، ارتدِ ملابس دافئة.")
        elif current['temperature_2m'] > 30: st.warning("الجو حار، اشرب الكثير من الماء.")
        else: st.success("الجو رائع للخروج!")

st.markdown('<div style="text-align:center; color:#666; padding:20px;">تطبيق الطقس الذكي | تصميم طاهر</div>', unsafe_allow_html=True)
