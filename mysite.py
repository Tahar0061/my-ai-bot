# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# 1. إعداد الصفحة الفاخرة الفائقة
st.set_page_config(
    page_title="Taher | Galaxy S26 Ultra Weather", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. نظام اللغات العالمي
LANGS = {
    "ar": {
        "search": "🔍 بحث كوني:", 
        "temp": "🌡️ الحرارة", 
        "hum": "💧 الرطوبة الكونية", 
        "wind": "🌪️ الرياح", 
        "uv": "☢️ مؤشر UV", 
        "feels": "💫 يشعر كـ", 
        "updated": "🔄 آخر تحديث مجري:", 
        "forecast": "📅 توقعات الأيام الكونية"
    },
    "en": {
        "search": "🔍 Cosmic Search:", 
        "temp": "🌡️ Temperature", 
        "hum": "💧 Cosmic Humidity", 
        "wind": "🌪️ Wind", 
        "uv": "☢️ UV Index", 
        "feels": "💫 Feels like", 
        "updated": "🔄 Galaxy Update:", 
        "forecast": "📅 Cosmic Forecast"
    }
}

# 3. تأثيرات بصرية متطورة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(ellipse at 20% 30%, #0a0f1e, #000000);
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(white 1px, transparent 1px);
        background-size: 50px 50px;
        animation: starsMove 200s linear infinite;
        opacity: 0.3;
        pointer-events: none;
    }
    
    @keyframes starsMove {
        from { transform: translateY(0); }
        to { transform: translateY(-500px); }
    }
    
    .dynamic-island {
        background: rgba(20, 30, 50, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 60px;
        padding: 1rem 2rem;
        margin: 1rem auto;
        max-width: 90%;
        color: white;
    }
    
    .s26-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 40px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: 0.4s;
        color: white;
    }
    
    .s26-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 0 30px #4a90e2;
    }
    
    .glow-value {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #a0b0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .galaxy-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #a0d0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .cosmic-time {
        background: rgba(255,255,255,0.03);
        border-radius: 100px;
        padding: 0.8rem 1.5rem;
        color: rgba(255,255,255,0.8);
        display: inline-block;
    }
    
    .galaxy-sphere {
        width: 150px;
        height: 150px;
        margin: 0 auto;
        background: radial-gradient(circle at 30% 30%, #4a90e2, #9b59b6);
        border-radius: 50%;
        animation: floatSphere 3s ease-in-out infinite;
        box-shadow: 0 0 50px #4a90e2;
    }
    
    @keyframes floatSphere {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    </style>
""", unsafe_allow_html=True)

# 4. دوال مساعدة
def get_cosmic_time():
    return datetime.now().strftime("%H:%M • %d %B %Y")

def ai_recommendations(temp, humidity, uv):
    recs = []
    if temp > 30:
        recs.append("🩳 ملابس صيفية")
        recs.append("🧴 واقي شمس")
    elif temp < 15:
        recs.append("🧥 جاكيت دافئ")
    
    if uv > 6:
        recs.append("🕶️ نظارة شمسية")
    
    return recs if recs else ["✨ طقس مثالي"]

# 5. الشريط الجانبي
with st.sidebar:
    st.markdown("<h1 style='text-align:center;color:white;'>🌌 S26 Ultra</h1>", unsafe_allow_html=True)
    
    lang = st.selectbox("🌐", ["ar", "en"], format_func=lambda x: "🇸🇦 عربي" if x=="ar" else "🇬🇧 English")
    st.session_state.l = lang
    _ = LANGS[lang]
    
    city = st.text_input(_["search"], "دبي")
    
    st.markdown("""
        <div style="text-align: center;">
            <div class="galaxy-sphere"></div>
            <p style="color:white;">✨ Galaxy AI Live ✨</p>
        </div>
    """, unsafe_allow_html=True)

# 6. دالة جلب البيانات
@st.cache_data(ttl=300)
def get_weather(city_name):
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1").json()
        if 'results' not in geo:
            return None
        
        loc = geo['results'][0]
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                'latitude': loc['latitude'],
                'longitude': loc['longitude'],
                'current': ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'wind_speed_10m', 'uv_index'],
                'daily': ['temperature_2m_max', 'temperature_2m_min'],
                'timezone': 'auto'
            }
        ).json()
        
        return {
            'city': loc['name'],
            'country': loc.get('country', ''),
            'current': weather['current'],
            'daily': weather['daily']
        }
    except:
        return None

# 7. الواجهة الرئيسية
if 'l' not in st.session_state:
    st.session_state.l = 'ar'

_ = LANGS[st.session_state.l]
data = get_weather(city)

if data:
    current = data['current']
    
    st.markdown(f"""
        <div class="dynamic-island">
            <div style="display: flex; justify-content: space-between;">
                <span>🌍 {data['city']}, {data['country']}</span>
                <span class="cosmic-time">{get_cosmic_time()}</span>
            </div>
        </div>
        <div style="text-align: center; margin: 2rem 0;">
            <div class="galaxy-title">{current['temperature_2m']}°</div>
            <div style="color:white;">{_['feels']} {current['apparent_temperature']}°</div>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    metrics = [
        (_['temp'], f"{current['temperature_2m']}°", "🌡️"),
        (_['hum'], f"{current['relative_humidity_2m']}%", "💧"),
        (_['wind'], f"{current['wind_speed_10m']} km/h", "🌪️"),
        (_['uv'], f"{current['uv_index']}", "☢️")
    ]
    
    for idx, (label, value, icon) in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
                <div class="s26-card">
                    <div>{icon}</div>
                    <div>{label}</div>
                    <div class="glow-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 " + _['forecast'], "🤖 AI"])
    
    with tab1:
        cols = st.columns(7)
        for i, col in enumerate(cols):
            if i < len(data['daily']['time']):
                with col:
                    st.markdown(f"""
                        <div class="s26-card" style="padding:1rem;">
                            <div>Day {i+1}</div>
                            <div style="color:#4a90e2;">{data['daily']['temperature_2m_max'][i]}°</div>
                            <div>{data['daily']['temperature_2m_min'][i]}°</div>
                        </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        recs = ai_recommendations(current['temperature_2m'], current['relative_humidity_2m'], current['uv_index'])
        for rec in recs:
            st.markdown(f'<div class="s26-card">{rec}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
        <div style="text-align: center; padding: 5rem;">
            <h1 class="galaxy-title">🌌 Galaxy S26 Ultra</h1>
            <p style="color:white;">أدخل اسم المدينة في الشريط الجانبي</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div style="text-align:center; color:gray; padding:2rem;">
        {_['updated']} Galaxy AI • 2026
    </div>
""", unsafe_allow_html=True)
