# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# محاولة استيراد المكتبة بذكاء (لأنها قد تأخذ ثواني للتثبيت على السيرفر)
try:
    from streamlit_lottie import st_lottie
    LOTTIE_OK = True
except:
    LOTTIE_OK = False

# 1. إعداد الصفحة
st.set_page_config(page_title="طاهر | Galaxy S26 Ultra", page_icon="📱", layout="wide")

# 2. تصميم الواجهة الزجاجية السحابية (Ultra Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * { font-family: 'IBM Plex Sans Arabic', sans-serif; }
    
    .stApp {
        background: url('https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    h1, h2, h3, p, span { color: white !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); }
    .m-val { font-size: 3rem; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def get_data(city_name):
    try:
        g = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar").json()
        if 'results' in g:
            res = g['results'][0]
            lat, lon = res['latitude'], res['longitude']
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto").json()
            return w, res['name']
    except: return None, None
    return None, None

# 4. الواجهة الجانبية
city = st.sidebar.text_input("🔍 ابحث عن مدينة:", "Witten")
data, city_name = get_data(city)

# 5. عرض المحتوى
if data:
    curr = data['current']
    daily = data['daily']

    # الهيدر الزجاجي
    st.markdown(f"""
        <div class="glass-card">
            <h1 style="margin:0;">🌤️ {city_name}</h1>
            <div class="m-val">{curr['temperature_2m']}°C</div>
            <p>الرطوبة: {curr['relative_humidity_2m']}% | الأجواء الآن</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض الأيقونة المتحركة إذا كانت المكتبة جاهزة
    if LOTTIE_OK:
        # رابط أيقونة شمس (Lottie)
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_t0x0v9.json"
        lottie_json = requests.get(lottie_url).json()
        with st.sidebar:
            st_lottie(lottie_json, height=150)
    else:
        st.sidebar.info("جاري تجهيز الأيقونات المتحركة...")

    # البطاقات السفلية
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='glass-card'>🌅 الشروق<br><b>{daily['sunrise'][0].split('T')[1]}</b></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='glass-card'>🌇 الغروب<br><b>{daily['sunset'][0].split('T')[1]}</b></div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='glass-card'>🔍 بانتظار إدخال اسم المدينة...</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity:0.6;'>Taher Weather Galaxy S26 • 2026</p>", unsafe_allow_html=True)
