# -*- coding: utf-8 -*-
import streamlit as st
import requests
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="طاهر | الطقس الذكي", page_icon="🌤️", layout="wide")

# 2. وظيفة جلب البيانات مع معالجة الأخطاء المتقدمة
@st.cache_data(ttl=300)
def get_weather_data(city_name):
    try:
        # البحث عن المدينة
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_response = requests.get(geo_url, timeout=5)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if 'results' in geo_data and len(geo_data['results']) > 0:
            loc = geo_data['results'][0]
            lat, lon = loc['latitude'], loc['longitude']
            
            # جلب الطقس
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,is_day,weather_code,wind_speed_10m,relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone=auto"
            w_res = requests.get(weather_url, timeout=5)
            w_res.raise_for_status()
            w_data = w_res.json()
            
            return {'city': loc.get('name', city_name), 'current': w_data['current'], 'daily': w_data['daily']}
        return "not_found"
    except (requests.exceptions.RequestException, Exception):
        return "error"

# 3. تحديد الثيم الديناميكي بناءً على حالة الطقس
def get_dynamic_theme(code):
    # مشمس
    if code <= 1: return "linear-gradient(135deg, #f6d365 0%, #fda085 100%)", "#ffffff"
    # غائم / ضباب
    elif code <= 48: return "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)", "#ffffff"
    # مطر
    elif code <= 67 or (code >= 80 and code <= 82): return "linear-gradient(135deg, #4b6cb7 0%, #182848 100%)", "#ffffff"
    # عواصف
    else: return "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)", "#ffffff"

# 4. واجهة المستخدم
with st.sidebar:
    st.title("⚙️ الإعدادات")
    city_input = st.text_input("🔍 ابحث عن مدينة:", "الرياض")
    st.info("💡 نصيحة: التطبيق يحدث البيانات تلقائياً كل 5 دقائق.")

data = get_weather_data(city_input)

if data == "error":
    st.error("⚠️ عذراً، نواجه مشكلة في الاتصال بخدمة الطقس.")
    st.info("يرجى التأكد من اتصال الإنترنت أو المحاولة مرة أخرى بعد قليل.")
elif data == "not_found":
    st.warning(f"🔍 لم نتمكن من العثور على '{city_input}'. يرجى التأكد من الاسم.")
else:
    # استخراج البيانات والثيم
    curr = data['current']
    header_bg, text_color = get_dynamic_theme(curr['weather_code'])
    
    # CSS الديناميكي
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
        * {{ font-family: 'IBM Plex Sans Arabic', sans-serif; }}
        .main-header {{
            background: {header_bg};
            padding: 3rem; border-radius: 25px; color: {text_color};
            text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .weather-card {{
            background: white; padding: 1.5rem; border-radius: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05); text-align: center;
        }}
        </style>
        <div class="main-header">
            <h1 style="margin:0;">🌤️ طاهر | الطقس الذكي</h1>
            <p style="opacity:0.9;">أنت تشاهد الآن طقس مدينة {data['city']}</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض البطاقات الرئيسية
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="weather-card"><h3>🌡️ الحرارة</h3><h1 style="color:#1e3a8a;">{curr["temperature_2m"]}°C</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="weather-card"><h3>💧 الرطوبة</h3><h1 style="color:#1e3a8a;">{curr["relative_humidity_2m"]}%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="weather-card"><h3>💨 الرياح</h3><h1 style="color:#1e3a8a;">{curr["wind_speed_10m"]} <small>كم/س</small></h1></div>', unsafe_allow_html=True)

    st.success(f"✅ تم تحديث البيانات بنجاح في {datetime.now().strftime('%H:%M')}")

st.markdown('<div style="text-align:center; color:#888; margin-top:50px;">تطبيق الطقس العالمي | تصميم طاهر</div>', unsafe_allow_html=True)
