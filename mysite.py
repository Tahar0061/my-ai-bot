# -*- coding: utf-8 -*-
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
    "ar": {
        "search": "🔍 ابحث عن مدينة:", 
        "settings": "⚙️ الإعدادات", 
        "temp": "الحرارة", 
        "hum": "الرطوبة", 
        "wind": "الرياح", 
        "uv": "مؤشر UV", 
        "feels": "يشعر كـ", 
        "aqi": "جودة الهواء", 
        "wear": "ماذا ترتدي؟", 
        "act": "الأنشطة", 
        "updated": "تحديث ذكي:", 
        "forecast": "📅 التوقعات",
        "not_found": "⚠️ المدينة غير موجودة. يرجى المحاولة مرة أخرى.",
        "good": "جيد",
        "moderate": "متوسط",
        "poor": "سيء",
        "day": "يوم"
    },
    "en": {
        "search": "🔍 Search City:", 
        "settings": "⚙️ Settings", 
        "temp": "Temperature", 
        "hum": "Humidity", 
        "wind": "Wind", 
        "uv": "UV Index", 
        "feels": "Feels like", 
        "aqi": "Air Quality", 
        "wear": "What to wear?", 
        "act": "Activities", 
        "updated": "Smart Update:", 
        "forecast": "📅 Forecast",
        "not_found": "⚠️ City not found. Please try again.",
        "good": "Good",
        "moderate": "Moderate",
        "poor": "Poor",
        "day": "Day"
    },
    "de": {
        "search": "🔍 Stadt suchen:", 
        "settings": "⚙️ Einstellungen", 
        "temp": "Temperatur", 
        "hum": "Feuchtigkeit", 
        "wind": "Wind", 
        "uv": "UV-Index", 
        "feels": "Gefühlt", 
        "aqi": "Luftqualität", 
        "wear": "Was anziehen?", 
        "act": "Aktivitäten", 
        "updated": "Update:", 
        "forecast": "📅 Vorhersage",
        "not_found": "⚠️ Stadt nicht gefunden. Bitte versuchen Sie es erneut.",
        "good": "Gut",
        "moderate": "Mäßig",
        "poor": "Schlecht",
        "day": "Tag"
    },
    "fr": {
        "search": "🔍 Chercher ville:", 
        "settings": "⚙️ Paramètres", 
        "temp": "Température", 
        "hum": "Humidité", 
        "wind": "Vent", 
        "uv": "Indice UV", 
        "feels": "Ressenti", 
        "aqi": "Qualité d'air", 
        "wear": "Que porter ?", 
        "act": "Activités", 
        "updated": "Mise à jour:", 
        "forecast": "📅 Prévisions",
        "not_found": "⚠️ Ville non trouvée. Veuillez réessayer.",
        "good": "Bon",
        "moderate": "Modéré",
        "poor": "Mauvais",
        "day": "Jour"
    }
}

# تهيئة اللغة في الجلسة
if 'l' not in st.session_state: 
    st.session_state.l = "ar"

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
    .error-message {{
        background: rgba(255, 100, 100, 0.2);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        margin: 2rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. محرك الأيقونات المتحركة (Lottie)
def load_lottie(url):
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except: 
        return None

lottie_weather = load_lottie("https://assets9.lottiefiles.com/packages/lf20_t0x0v9.json")

# 5. دالة جلب البيانات المحسنة
@st.cache_data(ttl=300)
def get_weather_data(city_name, lang):
    try:
        # البحث عن المدينة
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language={lang}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if 'results' not in geo_data or len(geo_data['results']) == 0:
            return None
            
        location = geo_data['results'][0]
        
        # جلب بيانات الطقس
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={location['latitude']}&longitude={location['longitude']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        # جلب بيانات جودة الهواء مع التحقق من الأخطاء
        aqi_value = "N/A"
        try:
            aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={location['latitude']}&longitude={location['longitude']}&current=european_aqi"
            aqi_response = requests.get(aqi_url)
            aqi_data = aqi_response.json()
            
            if 'current' in aqi_data and 'european_aqi' in aqi_data['current']:
                aqi_value = aqi_data['current']['european_aqi']
        except Exception as e:
            print(f"Error fetching AQI: {e}")
        
        # تجهيز البيانات للعرض
        return {
            'city': location.get('name', city_name),
            'country': location.get('country', ''),
            'current': weather_data['current'],
            'daily': weather_data['daily'],
            'hourly': weather_data['hourly'],
            'aqi': aqi_value
        }
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# 6. دالة تحديد حالة جودة الهواء
def get_aqi_status(aqi_value, lang):
    _ = LANGS[lang]
    if isinstance(aqi_value, (int, float)):
        if aqi_value < 50:
            return _["good"]
        elif aqi_value < 100:
            return _["moderate"]
        else:
            return _["poor"]
    return ""

# 7. الشريط الجانبي
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>📱 Galaxy S26</h1>", unsafe_allow_html=True)
    
    # اختيار اللغة
    selected_lang = st.selectbox("🌐 Language", ["ar", "en", "de", "fr"], index=["ar", "en", "de", "fr"].index(st.session_state.l))
    st.session_state.l = selected_lang
    _ = LANGS[st.session_state.l]
    
    # إدخال المدينة
    city = st.text_input(_["search"], "دبي")
    
    st.markdown("---")
    
    # عرض الأيقونة المتحركة
    if lottie_weather:
        st_lottie(lottie_weather, height=150)
    else:
        st.markdown("☁️ Weather Animation")

# 8. جلب وعرض البيانات
weather_data = get_weather_data(city, st.session_state.l)

if weather_data:
    # عرض رأس الصفحة
    current = weather_data['current']
    st.markdown(f"""
        <div class="main-header">
            <h1 style="font-size: 4rem; margin:0;">🌤️ {weather_data['city']}</h1>
            <p style="font-size: 1.5rem; opacity: 0.9;">{weather_data['country']} | {current['temperature_2m']}°C</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض البطاقات الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    # تجهيز عناصر البطاقات
    items = [
        (_['temp'], f"{current['temperature_2m']}°", f"{_['feels']}: {current['apparent_temperature']}°"),
        (_['hum'], f"{current['relative_humidity_2m']}%", "💧"),
        (_['wind'], f"{current['wind_speed_10m']} km/h", "🌪️"),
        (_['aqi'], f"{weather_data['aqi']}", get_aqi_status(weather_data['aqi'], st.session_state.l))
    ]
    
    # عرض البطاقات
    for i, (lbl, val, sub) in enumerate(items):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'''
                <div class="glass-card">
                    <div class="m-lbl">{lbl}</div>
                    <div class="m-val">{val}</div>
                    <div style="color:#777;">{sub}</div>
                </div>
            ''', unsafe_allow_html=True)

    # إنشاء التبويبات
    tab1, tab2 = st.tabs([_["forecast"], "📊 Analysis"])
    
    # تبويب التوقعات
    with tab1:
        for i in range(min(7, len(weather_data['daily']['time']))):
            st.markdown(f'''
                <div class="glass-card" style="text-align:right; padding:15px;">
                    <b>{_['day']} {i+1}</b>: {weather_data['daily']['temperature_2m_max'][i]}° / {weather_data['daily']['temperature_2m_min'][i]}°
                </div>
            ''', unsafe_allow_html=True)
    
    # تبويب التحليل والرسوم البيانية
    with tab2:
        if weather_data['hourly'] and 'time' in weather_data['hourly']:
            # تجهيز بيانات الرسم البياني
            hourly_data = pd.DataFrame({
                'time': pd.to_datetime(weather_data['hourly']['time'][:24]),
                'temperature': weather_data['hourly']['temperature_2m'][:24]
            })
            
            # إنشاء الرسم البياني
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hourly_data['time'],
                y=hourly_data['temperature'],
                mode='lines',
                name='Temperature',
                line=dict(color='#1e3a8a', width=4),
                fill='tozeroy',
                fillcolor='rgba(30, 58, 138, 0.2)'
            ))
            
            # تنسيق الرسم البياني
            fig.update_layout(
                title='Temperature Forecast - Next 24 Hours',
                xaxis_title='Time',
                yaxis_title='Temperature (°C)',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=40, b=40),
                hovermode='x unified'
            )
            
            fig.update_xaxes(gridcolor='lightgray', gridwidth=1)
            fig.update_yaxes(gridcolor='lightgray', gridwidth=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # إحصائيات سريعة
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Max Today", f"{max(weather_data['hourly']['temperature_2m'][:24])}°")
            with col2:
                st.metric("Min Today", f"{min(weather_data['hourly']['temperature_2m'][:24])}°")
            with col3:
                st.metric("Average", f"{sum(weather_data['hourly']['temperature_2m'][:24])/24:.1f}°")
        else:
            st.info("No hourly data available")

else:
    # عرض رسالة خطأ عند عدم العثور على المدينة
    st.markdown(f'''
        <div class="error-message">
            <h2 style="color: #ff4444;">{_["not_found"]}</h2>
            <p style="color: #666;">🔍 {city}</p>
        </div>
    ''', unsafe_allow_html=True)

# 9. التذييل
st.markdown(f'''
    <div style="text-align:center; color:#aaa; padding:30px; margin-top: 50px;">
        {_["updated"]} Taher Weather Galaxy S26 • 2026
    </div>
''', unsafe_allow_html=True)
