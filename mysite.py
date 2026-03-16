# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعداد الصفحة بأعلى معايير الجودة
st.set_page_config(
    page_title="طاهر | منصة الطقس الذكية",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. محرك التصميم المتقدم (CSS) - واجهة احترافية مشبعة بالمعلومات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');
    * { font-family: 'IBM Plex Sans Arabic', sans-serif; }
    
    .main-header {
        padding: 2.5rem; border-radius: 30px; color: white;
        text-align: center; margin-bottom: 2rem;
        box-shadow: 0 15px 45px rgba(0,0,0,0.2);
    }
    
    .smart-card {
        background: white; padding: 1.5rem; border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 1rem;
        border: 1px solid #f0f2f6; transition: 0.3s; text-align: center;
    }
    
    .smart-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    
    .metric-value {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .sub-info { font-size: 0.85rem; color: #7f8c8d; margin-top: 5px; font-weight: 500; }
    
    .status-tag {
        display: inline-block; padding: 4px 12px; border-radius: 50px;
        font-size: 0.75rem; font-weight: bold; margin-top: 10px;
    }
    .tag-good { background: #e8f5e9; color: #2e7d32; }
    .tag-warn { background: #fff3e0; color: #ef6c00; }
    .tag-danger { background: #ffebee; color: #c62828; }

    .recommendation-box {
        background: #f0f7ff; border-right: 5px solid #007bff;
        padding: 1.2rem; border-radius: 15px; margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف جلب البيانات الذكية (طقس + جودة هواء)
@st.cache_data(ttl=300)
def get_advanced_weather(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_res = requests.get(geo_url, timeout=10).json()
        if 'results' in geo_res:
            loc = geo_res['results'][0]
            lat, lon = loc['latitude'], loc['longitude']
            
            # بيانات الطقس الشاملة
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl,visibility,uv_index&hourly=temperature_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum&timezone=auto"
            w_data = requests.get(w_url, timeout=10).json()
            
            # بيانات جودة الهواء
            aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,pm10,pm2_5,carbon_monoxide,ozone"
            aq_data = requests.get(aq_url, timeout=10).json()
            
            return {'city': loc.get('name', city_name), 'loc': loc, 'current': w_data['current'], 'hourly': w_data['hourly'], 'daily': w_data['daily'], 'aqi': aq_data['current']}
        return None
    except: return "error"

# 4. محركات التحليل (Logic)
def get_comfort_level(temp, hum):
    if hum > 70: return "رطب جداً", "tag-danger"
    if hum < 30: return "جاف", "tag-warn"
    return "مثالي", "tag-good"

def get_uv_advice(uv):
    if uv <= 2: return "آمن", "tag-good"
    if uv <= 5: return "استخدم واقي", "tag-warn"
    return "خطر (تجنب الشمس)", "tag-danger"

def get_dynamic_theme(code, is_day):
    if not is_day: return "linear-gradient(135deg, #0f0c29 0%, #302b63 100%)", "🌙", "ليلة هادئة"
    themes = {0: ("linear-gradient(135deg, #f6d365 0%, #fda085 100%)", "☀️", "مشمس"), 2: ("linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)", "🌤️", "غائم جزئياً"), 61: ("linear-gradient(135deg, #4b6cb7 0%, #182848 100%)", "🌧️", "ممطر")}
    return themes.get(code, ("linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "🌈", "متغير"))

# 5. واجهة المستخدم والشريط الجانبي
with st.sidebar:
    st.title("🧬 التحكم الذكي")
    city_search = st.text_input("🔍 ابحث عن مدينة عالمية:", "دبي")
    st.markdown("---")
    st.info("💡 تم حشو الأيقونات بمعلومات إضافية مثل نقطة الندى، جودة الهواء، وتوصيات الملابس.")

data = get_advanced_weather(city_search)

if data and data != "error":
    curr, daily, hourly, aqi = data['current'], data['daily'], data['hourly'], data['aqi']
    bg, icon, desc = get_dynamic_theme(curr['weather_code'], curr['is_day'])
    
    # الهيدر الاحترافي
    st.markdown(f"""
        <div class="main-header" style="background: {bg};">
            <h1 style="margin:0; font-size: 3rem;">{icon} {data['city']}</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">{desc} • {curr['temperature_2m']}°C</p>
            <p style="opacity:0.7;">📍 {data['loc'].get('country', '')} | {datetime.now().strftime('%H:%M')}</p>
        </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["🚀 المؤشرات الذكية", "📅 التوقعات", "🧪 جودة الهواء", "🧥 دليل طاهر"])

    with t1:
        c1, c2, c3, c4 = st.columns(4)
        
        with c1: # الرطوبة + نقطة الندى
            comfort, c_class = get_comfort_level(curr['temperature_2m'], curr['relative_humidity_2m'])
            st.markdown(f"""<div class="smart-card"><div class="sub-info">💧 الرطوبة</div><div class="metric-value">{curr['relative_humidity_2m']}%</div><div class="sub-info">نقطة الندى: {round(curr['temperature_2m']-2,1)}°C</div><div class="status-tag {c_class}">{comfort}</div></div>""", unsafe_allow_html=True)
            
        with c2: # الرياح + الضغط
            st.markdown(f"""<div class="smart-card"><div class="sub-info">💨 الرياح</div><div class="metric-value">{curr['wind_speed_10m']}</div><div class="sub-info">كم/س | اتجاه {curr['wind_direction_10m']}°</div><div class="sub-info">الضغط: {curr['pressure_msl']} hPa</div></div>""", unsafe_allow_html=True)
            
        with c3: # الشمس + UV
            uv_adv, uv_class = get_uv_advice(curr['uv_index'])
            st.markdown(f"""<div class="smart-card"><div class="sub-info">☀️ الأشعة UV</div><div class="metric-value">{curr['uv_index']}</div><div class="sub-info">الرؤية: {curr['visibility']/1000} كم</div><div class="status-tag {uv_class}">{uv_adv}</div></div>""", unsafe_allow_html=True)
            
        with c4: # جودة الهواء المختصرة
            aq_class = "tag-good" if aqi['european_aqi'] < 50 else "tag-warn"
            st.markdown(f"""<div class="smart-card"><div class="sub-info">🌫️ جودة الهواء</div><div class="metric-value">{aqi['european_aqi']}</div><div class="sub-info">CO: {aqi['carbon_monoxide']}</div><div class="status-tag {aq_class}">{"نقي" if aqi['european_aqi'] < 50 else "متوسط"}</div></div>""", unsafe_allow_html=True)

        # رسم بياني مدمج
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hourly['time'][:24], y=hourly['temperature_2m'][:24], name="الحرارة", line=dict(color='#1e3a8a', width=3), fill='tozeroy'))
        fig.update_layout(title="تحليل الحرارة (24 ساعة)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        for i in range(7):
            d = datetime.fromisoformat(daily['time'][i]).strftime('%A %d/%m')
            st.markdown(f"""<div style="padding:15px; background:white; border-radius:15px; margin-bottom:10px; border-right:5px solid #3b82f6; display:flex; justify-content:space-between;"><b>{d}</b> <span>🌡️ {daily['temperature_2m_max'][i]}° / {daily['temperature_2m_min'][i]}° | 🌧️ {daily['precipitation_sum'][i]}mm</span></div>""", unsafe_allow_html=True)

    with t3:
        st.markdown("### 🔬 تفاصيل ملوثات الهواء")
        st.write(f"PM2.5: {aqi['pm2_5']} µg/m³")
        st.write(f"PM10: {aqi['pm10']} µg/m³")
        st.write(f"الأوزون (O3): {aqi['ozone']} µg/m³")

    with t4:
        ca, cb = st.columns(2)
        with ca:
            st.markdown('<div class="recommendation-box"><h4>👕 ماذا ترتدي؟</h4>', unsafe_allow_html=True)
            if curr['temperature_2m'] < 15: st.write("- معطف ثقيل\n- ملابس شتوية")
            elif curr['temperature_2m'] < 25: st.write("- سترة خفيفة\n- ملابس خريفية")
            else: st.write("- ملابس قطنية خفيفة\n- نظارات شمسية")
            st.markdown('</div>', unsafe_allow_html=True)
        with cb:
            st.markdown('<div class="recommendation-box" style="border-right-color:#28a745;"><h4>🏃 الأنشطة</h4>', unsafe_allow_html=True)
            if curr['uv_index'] > 6: st.write("- تجنب الرياضة تحت الشمس\n- اشرب الكثير من الماء")
            else: st.write("- الأجواء مثالية للمشي\n- نشاط خارجي ممتع")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔍 ابحث عن مدينة للبدء في التحليل الذكي.")

st.markdown('<div style="text-align:center; color:#999; padding:20px;">منصة طاهر للذكاء الجوي • 2026</div>', unsafe_allow_html=True)
