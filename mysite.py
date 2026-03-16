# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
from PIL import Image
import base64
from io import BytesIO

# ==================== إعدادات الصفحة الفاخرة ====================
st.set_page_config(
    page_title="SAMSUNG GALAXY S26 ULTRA | Weather Galaxy AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.samsung.com/galaxy-ai',
        'Report a bug': 'https://www.samsung.com/support',
        'About': '# Galaxy S26 Ultra\n### Weather AI Edition\nPowered by Galaxy AI'
    }
)

# ==================== نظام الألوان الكوني ====================
COLORS = {
    'galaxy_black': '#0A0F1E',
    'cosmic_blue': '#1E3A8A',
    'nebula_purple': '#6B21A8',
    'star_white': '#FFFFFF',
    'aurora_green': '#10B981',
    'sunset_orange': '#F97316',
    'deep_space': '#030712',
    'glass_white': 'rgba(255, 255, 255, 0.1)',
    'glass_dark': 'rgba(10, 15, 30, 0.7)'
}

# ==================== CSS Galaxy Ultra الفاخر ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
    
    /* الأساسيات الكونية */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* خلفية المجرة الحية */
    .stApp {
        background: linear-gradient(145deg, #030712 0%, #0A0F1E 50%, #1E1B4B 100%);
        position: relative;
        overflow-x: hidden;
    }
    
    /* تأثير النجوم المتساقطة */
    .stars, .twinkling, .clouds {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        height: 100%;
        display: block;
        pointer-events: none;
        z-index: 0;
    }
    
    .stars {
        background: #000 url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48Y2lyY2xlIGN4PSI2IiBjeT0iMTQiIHI9IjEiIGZpbGw9IndoaXRlIiAvPjxjaXJjbGUgY3g9IjE2MCIgY3k9IjYwIiByPSIxIiBmaWxsPSJ3aGl0ZSIgLz48Y2lyY2xlIGN4PSI0MCIgY3k9IjEwMCIgcj0iMSIgZmlsbD0id2hpdGUiIC8+PC9zdmc+');
        background-size: 200px 200px;
        animation: starsAnimation 200s linear infinite;
        opacity: 0.5;
    }
    
    .twinkling {
        background: transparent url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSIyIiBmaWxsPSJ3aGl0ZSIgLz48Y2lyY2xlIGN4PSIxNTAiIGN5PSIxMDAiIHI9IjIiIGZpbGw9IndoaXRlIiAvPjwvc3ZnPg==');
        background-size: 300px 300px;
        animation: twinklingAnimation 4s linear infinite;
        opacity: 0.3;
    }
    
    @keyframes starsAnimation {
        from { transform: translateY(0); }
        to { transform: translateY(-2000px); }
    }
    
    @keyframes twinklingAnimation {
        0% { opacity: 0.3; }
        50% { opacity: 0.6; }
        100% { opacity: 0.3; }
    }
    
    /* Dynamic Island - مستوحى من iPhone 15 Pro */
    .dynamic-island {
        background: rgba(20, 30, 50, 0.7);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 40px;
        padding: 12px 24px;
        margin: 20px auto;
        max-width: 90%;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
        animation: slideDown 0.5s ease-out;
        z-index: 1000;
    }
    
    @keyframes slideDown {
        0% { transform: translateY(-100px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    /* بطاقات One UI 6.1 */
    .oneui-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 32px;
        padding: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        z-index: 10;
    }
    
    .oneui-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4A90E2, #9B59B6, transparent);
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    
    .oneui-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(74, 144, 226, 0.5);
        box-shadow: 0 20px 40px rgba(74, 144, 226, 0.2);
    }
    
    .oneui-card:hover::before {
        transform: translateX(100%);
    }
    
    /* درجة الحرارة الرئيسية - تأثير Galaxy AI */
    .galaxy-temperature {
        font-size: 8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF, #A0D0FF, #9B59B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(74, 144, 226, 0.5);
        line-height: 1;
        margin: 0;
        animation: glowPulse 3s ease-in-out infinite;
        text-align: center;
    }
    
    @keyframes glowPulse {
        0%, 100% { filter: brightness(1); text-shadow: 0 0 40px rgba(74, 144, 226, 0.5); }
        50% { filter: brightness(1.2); text-shadow: 0 0 60px rgba(74, 144, 226, 0.8); }
    }
    
    /* القيم المتوهجة */
    .glow-text {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF, #E0E0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    /* أيقونات الطقس المتحركة */
    .weather-icon {
        font-size: 3rem;
        animation: float 3s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 0 20px rgba(74, 144, 226, 0.5));
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* شريط التقدم الدائري */
    .progress-ring {
        transform: rotate(-90deg);
    }
    
    .progress-ring-circle {
        stroke: rgba(255, 255, 255, 0.1);
        stroke-width: 4;
        fill: transparent;
    }
    
    .progress-ring-fill {
        stroke: url(#gradient);
        stroke-width: 4;
        fill: transparent;
        stroke-linecap: round;
        transition: stroke-dashoffset 0.5s;
    }
    
    /* تأثير الزجاج المزدوج */
    .glass-deep {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 48px;
        padding: 32px;
    }
    
    /* عناوين المجرة */
    .galaxy-heading {
        font-size: 1.5rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        letter-spacing: 0.5px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* توقعات الأيام */
    .day-forecast {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .day-forecast:last-child {
        border-bottom: none;
    }
    
    /* تخصيص scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4A90E2, #9B59B6);
        border-radius: 10px;
    }
    
    /* الشريط الجانبي */
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(10, 15, 30, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* تأثيرات hover متقدمة */
    .hover-lift {
        transition: transform 0.2s;
    }
    
    .hover-lift:hover {
        transform: translateY(-4px);
    }
    
    /* شارة AI */
    .ai-badge {
        background: linear-gradient(135deg, #4A90E2, #9B59B6);
        color: white;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
    }
    
    /* التذييل الكوني */
    .cosmic-footer {
        text-align: center;
        padding: 40px;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 60px;
    }
    </style>
    
    <!-- خلفية النجوم المتحركة -->
    <div class="stars"></div>
    <div class="twinkling"></div>
""", unsafe_allow_html=True)

# ==================== نظام اللغات المتطور ====================
LANGUAGES = {
    'ar': {
        'name': 'العربية',
        'flag': '🇸🇦',
        'search': '🔍 ابحث عن مدينة أو منطقة',
        'feels_like': 'يشعر كـ',
        'humidity': 'الرطوبة',
        'wind': 'الرياح',
        'uv': 'مؤشر الأشعة',
        'pressure': 'الضغط الجوي',
        'visibility': 'الرؤية',
        'dew_point': 'نقطة الندى',
        'sunrise': 'الشروق',
        'sunset': 'الغروب',
        'forecast_7days': 'توقعات 7 أيام',
        'hourly_forecast': 'التوقعات الساعية',
        'ai_insights': 'تحليلات Galaxy AI',
        'recommendations': 'توصيات ذكية',
        'air_quality': 'جودة الهواء',
        'good': 'جيد',
        'moderate': 'متوسط',
        'poor': 'سيء',
        'wear_suggestions': 'اقتراحات الملابس',
        'activity_suggestions': 'الأنشطة المناسبة',
        'updated': 'آخر تحديث',
        'powered_by': 'مدعوم من Galaxy AI'
    },
    'en': {
        'name': 'English',
        'flag': '🇬🇧',
        'search': '🔍 Search city or region',
        'feels_like': 'Feels like',
        'humidity': 'Humidity',
        'wind': 'Wind',
        'uv': 'UV Index',
        'pressure': 'Pressure',
        'visibility': 'Visibility',
        'dew_point': 'Dew point',
        'sunrise': 'Sunrise',
        'sunset': 'Sunset',
        'forecast_7days': '7 Days Forecast',
        'hourly_forecast': 'Hourly Forecast',
        'ai_insights': 'Galaxy AI Insights',
        'recommendations': 'Smart Recommendations',
        'air_quality': 'Air Quality',
        'good': 'Good',
        'moderate': 'Moderate',
        'poor': 'Poor',
        'wear_suggestions': 'Wear Suggestions',
        'activity_suggestions': 'Activities',
        'updated': 'Last updated',
        'powered_by': 'Powered by Galaxy AI'
    },
    'de': {
        'name': 'Deutsch',
        'flag': '🇩🇪',
        'search': '🔍 Stadt oder Region suchen',
        'feels_like': 'Gefühlt',
        'humidity': 'Luftfeuchtigkeit',
        'wind': 'Wind',
        'uv': 'UV-Index',
        'pressure': 'Luftdruck',
        'visibility': 'Sichtweite',
        'dew_point': 'Taupunkt',
        'sunrise': 'Sonnenaufgang',
        'sunset': 'Sonnenuntergang',
        'forecast_7days': '7-Tage-Vorhersage',
        'hourly_forecast': 'Stündliche Vorhersage',
        'ai_insights': 'Galaxy AI Einblicke',
        'recommendations': 'Smarte Empfehlungen',
        'air_quality': 'Luftqualität',
        'good': 'Gut',
        'moderate': 'Mäßig',
        'poor': 'Schlecht',
        'wear_suggestions': 'Kleidungsvorschläge',
        'activity_suggestions': 'Aktivitäten',
        'updated': 'Letztes Update',
        'powered_by': 'Powered by Galaxy AI'
    },
    'fr': {
        'name': 'Français',
        'flag': '🇫🇷',
        'search': '🔍 Rechercher une ville',
        'feels_like': 'Ressenti',
        'humidity': 'Humidité',
        'wind': 'Vent',
        'uv': 'Indice UV',
        'pressure': 'Pression',
        'visibility': 'Visibilité',
        'dew_point': 'Point de rosée',
        'sunrise': 'Lever',
        'sunset': 'Coucher',
        'forecast_7days': 'Prévisions 7 jours',
        'hourly_forecast': 'Prévisions horaires',
        'ai_insights': 'Analyses Galaxy AI',
        'recommendations': 'Recommandations',
        'air_quality': "Qualité de l'air",
        'good': 'Bon',
        'moderate': 'Modéré',
        'poor': 'Mauvais',
        'wear_suggestions': 'Suggestions tenue',
        'activity_suggestions': 'Activités',
        'updated': 'Dernière mise à jour',
        'powered_by': 'Propulsé par Galaxy AI'
    }
}

# ==================== تهيئة الجلسة ====================
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'city' not in st.session_state:
    st.session_state.city = 'Dubai'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'units' not in st.session_state:
    st.session_state.units = 'metric'

# ==================== الشريط الجانبي Galaxy AI ====================
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.samsung.com/is/image/samsung/assets/uk/2208/brand/BN68-06576A-01_L-PC.jpg?$ORIGIN_JPG$", 
                 use_column_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # اختيار اللغة
    lang_cols = st.columns(4)
    flags = {'ar': '🇸🇦', 'en': '🇬🇧', 'de': '🇩🇪', 'fr': '🇫🇷'}
    for i, (code, flag) in enumerate(flags.items()):
        with lang_cols[i]:
            if st.button(flag, key=f"lang_{code}", use_container_width=True):
                st.session_state.language = code
                st.rerun()
    
    st.markdown("---")
    
    # بحث المدينة
    _ = LANGUAGES[st.session_state.language]
    city = st.text_input(
        _['search'],
        value=st.session_state.city,
        placeholder="Dubai, London, Paris...",
        label_visibility="collapsed"
    )
    if city:
        st.session_state.city = city
    
    st.markdown("---")
    
    # إعدادات Galaxy AI
    with st.expander("⚙️ Galaxy AI Settings", expanded=False):
        st.session_state.units = st.radio(
            "Units",
            ["metric", "imperial"],
            format_func=lambda x: "°C" if x == "metric" else "°F",
            horizontal=True
        )
        
        st.toggle("🤖 Smart Recommendations", value=True)
        st.toggle("🌙 Night Mode", value=True)
        st.toggle("📊 Detailed Analytics", value=False)
    
    st.markdown("---")
    
    # Galaxy AI Status
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="width: 100px; height: 100px; margin: 0 auto; 
                      background: conic-gradient(from 0deg, #4A90E2, #9B59B6, #4A90E2);
                      border-radius: 50%; animation: rotate 3s linear infinite;
                      box-shadow: 0 0 50px #4A90E2;">
            </div>
            <p style="color: white; margin-top: 15px; font-size: 0.9rem;">
                ⚡ Galaxy AI Active<br>
                <span style="color: #4A90E2;">{datetime.now().strftime('%H:%M')}</span>
            </p>
        </div>
        <style>
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
    """, unsafe_allow_html=True)

# ==================== دوال جلب البيانات المتطورة ====================
@st.cache_data(ttl=600, show_spinner="🔄 Galaxy AI is analyzing cosmic data...")
def get_galaxy_weather(city_name):
    """جلب بيانات الطقس بتقنية Galaxy AI"""
    try:
        # البحث عن المدينة
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=5&language=en"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if 'results' not in geo_data or len(geo_data['results']) == 0:
            return None
        
        # اختيار أفضل نتيجة
        location = geo_data['results'][0]
        
        # جلب جميع بيانات الطقس
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'current': ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 
                       'weather_code', 'wind_speed_10m', 'wind_direction_10m', 
                       'pressure_msl', 'surface_pressure', 'uv_index', 'is_day'],
            'hourly': ['temperature_2m', 'relative_humidity_2m', 'weather_code', 
                      'wind_speed_10m', 'uv_index'],
            'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 
                     'sunrise', 'sunset', 'precipitation_probability_max',
                     'wind_speed_10m_max'],
            'timezone': 'auto'
        }
        
        weather_response = requests.get(weather_url, params=params)
        weather_data = weather_response.json()
        
        # جلب بيانات جودة الهواء
        aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        aqi_params = {
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'current': ['european_aqi', 'pm10', 'pm2_5', 'nitrogen_dioxide', 'ozone']
        }
        
        try:
            aqi_response = requests.get(aqi_url, params=aqi_params)
            aqi_data = aqi_response.json()
        except:
            aqi_data = {'current': {'european_aqi': 50}}
        
        return {
            'location': {
                'name': location.get('name', city_name),
                'country': location.get('country', ''),
                'admin1': location.get('admin1', ''),
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'timezone': location.get('timezone', 'auto')
            },
            'current': weather_data.get('current', {}),
            'hourly': weather_data.get('hourly', {}),
            'daily': weather_data.get('daily', {}),
            'air_quality': aqi_data.get('current', {})
        }
        
    except Exception as e:
        st.error(f"Galaxy AI Error: {str(e)}")
        return None

def get_weather_icon(weather_code, is_day=1):
    """الحصول على أيقونة الطقس المناسبة"""
    icons = {
        0: ('☀️' if is_day else '🌙', 'Clear'),
        1: ('🌤️' if is_day else '🌙⛅', 'Mainly Clear'),
        2: ('⛅' if is_day else '☁️🌙', 'Partly Cloudy'),
        3: ('☁️', 'Overcast'),
        45: ('🌫️', 'Fog'),
        48: ('🌫️❄️', 'Rime Fog'),
        51: ('🌧️💧', 'Light Drizzle'),
        53: ('🌧️', 'Drizzle'),
        55: ('🌧️💦', 'Heavy Drizzle'),
        61: ('🌦️', 'Light Rain'),
        63: ('🌧️', 'Rain'),
        65: ('🌧️🌊', 'Heavy Rain'),
        71: ('🌨️', 'Light Snow'),
        73: ('❄️', 'Snow'),
        75: ('❄️❄️', 'Heavy Snow'),
        77: ('🌨️💨', 'Snow Grains'),
        80: ('🌧️☔', 'Light Showers'),
        81: ('☔', 'Showers'),
        82: ('☔🌊', 'Heavy Showers'),
        95: ('⛈️', 'Thunderstorm'),
        96: ('⛈️🌨️', 'Thunderstorm with Hail'),
        99: ('⛈️❄️', 'Heavy Thunderstorm')
    }
    return icons.get(weather_code, ('🌡️', 'Unknown'))

def get_air_quality_label(aqi):
    """تحديد جودة الهواء"""
    if aqi <= 25:
        return 'Good', '#10B981'
    elif aqi <= 50:
        return 'Moderate', '#FBBF24'
    elif aqi <= 75:
        return 'Poor', '#F97316'
    else:
        return 'Very Poor', '#EF4444'

def get_ai_recommendations(temp, humidity, wind, uv, aqi, weather_code):
    """توصيات Galaxy AI الذكية"""
    recommendations = []
    
    # توصيات حسب درجة الحرارة
    if temp > 35:
        recommendations.append(("🌡️ Heat Alert", "Stay hydrated, avoid sun exposure", "🔴"))
    elif temp > 30:
        recommendations.append(("☀️ Hot", "Light clothes, sunscreen needed", "🟠"))
    elif temp < 5:
        recommendations.append(("❄️ Cold", "Heavy jacket, gloves recommended", "🔵"))
    elif temp < 0:
        recommendations.append(("⛄ Freezing", "Multiple layers, stay warm", "⚪"))
    
    # توصيات حسب الرطوبة
    if humidity > 80:
        recommendations.append(("💧 High Humidity", "Hair may frizz, use anti-frizz", "💧"))
    elif humidity < 20:
        recommendations.append(("🔥 Low Humidity", "Moisturizer recommended", "💨"))
    
    # توصيات حسب الرياح
    if wind > 40:
        recommendations.append(("🌪️ Strong Wind", "Secure loose items", "💨"))
    elif wind > 60:
        recommendations.append(("🌀 Wind Alert", "Stay indoors if possible", "⚠️"))
    
    # توصيات حسب UV
    if uv > 8:
        recommendations.append(("☢️ Extreme UV", "SPF 50+, avoid midday sun", "🛡️"))
    elif uv > 5:
        recommendations.append(("🕶️ High UV", "Sunglasses, hat recommended", "😎"))
    
    # توصيات حسب جودة الهواء
    if aqi > 75:
        recommendations.append(("😷 Poor Air", "Mask recommended outdoors", "😷"))
    
    # توصيات حسب نوع الطقس
    if weather_code in [61, 63, 65, 80, 81, 82]:
        recommendations.append(("☔ Rain", "Umbrella needed", "🌂"))
    elif weather_code in [71, 73, 75, 77]:
        recommendations.append(("❄️ Snow", "Snow boots recommended", "👢"))
    elif weather_code in [95, 96, 99]:
        recommendations.append(("⛈️ Storm", "Stay indoors", "🏠"))
    
    return recommendations if recommendations else [("✨ Perfect", "Ideal weather conditions", "✅")]

# ==================== جلب البيانات ====================
weather_data = get_galaxy_weather(st.session_state.city)
_ = LANGUAGES[st.session_state.language]

# ==================== الواجهة الرئيسية الفاخرة ====================
if weather_data:
    # Dynamic Island Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="dynamic-island">
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">🌍</span>
                    <div style="text-align: center;">
                        <span style="color: white; font-weight: 600; font-size: 1.2rem;">
                            {weather_data['location']['name']}, {weather_data['location']['country']}
                        </span><br>
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                            {weather_data['location'].get('admin1', '')}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # درجة الحرارة الرئيسية
    current = weather_data['current']
    weather_icon, weather_desc = get_weather_icon(
        current.get('weather_code', 0), 
        current.get('is_day', 1)
    )
    
    st.markdown(f"""
        <div style="text-align: center; margin: 40px 0 20px;">
            <div style="font-size: 8rem; animation: float 3s ease-in-out infinite;">
                {weather_icon}
            </div>
            <div class="galaxy-temperature">
                {current['temperature_2m']}°{st.session_state.units == 'metric' and 'C' or 'F'}
            </div>
            <div style="color: rgba(255,255,255,0.7); font-size: 1.5rem; margin: 10px 0;">
                {weather_desc}
            </div>
            <div style="color: rgba(255,255,255,0.5); font-size: 1.2rem;">
                {_['feels_like']} {current['apparent_temperature']}°
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # البطاقات الرئيسية
    st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0;">
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    metrics = [
        ('💧', _['humidity'], f"{current['relative_humidity_2m']}%"),
        ('🌪️', _['wind'], f"{current['wind_speed_10m']} km/h"),
        ('☢️', _['uv'], f"{current['uv_index']}"),
        ('📊', _['pressure'], f"{current.get('pressure_msl', 1013)} hPa")
    ]
    
    for idx, (icon, label, value) in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
                <div class="oneui-card" style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{label}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: white;">{value}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # جودة الهواء
    aqi = weather_data['air_quality'].get('european_aqi', 50)
    aqi_label, aqi_color = get_air_quality_label(aqi)
    
    st.markdown(f"""
        <div class="oneui-card" style="margin: 20px 0;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="font-size: 3rem;">✨</div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: white;">{_['air_quality']}</span>
                        <span style="color: {aqi_color};">{aqi_label}</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                        <div style="width: {aqi}%; height: 100%; background: {aqi_color}; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                        <span style="color: rgba(255,255,255,0.5);">AQI: {aqi}</span>
                        <span style="color: rgba(255,255,255,0.5);">PM2.5: {weather_data['air_quality'].get('pm2_5', 'N/A')}</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # شروق وغروب الشمس
    if 'daily' in weather_data and 'sunrise' in weather_data['daily']:
        sunrise = datetime.fromisoformat(weather_data['daily']['sunrise'][0]).strftime('%H:%M')
        sunset = datetime.fromisoformat(weather_data['daily']['sunset'][0]).strftime('%H:%M')
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"""
                <div class="oneui-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🌅</div>
                    <div style="color: rgba(255,255,255,0.7);">{_['sunrise']}</div>
                    <div style="font-size: 2rem; color: white;">{sunrise}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
                <div class="oneui-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🌇</div>
                    <div style="color: rgba(255,255,255,0.7);">{_['sunset']}</div>
                    <div style="font-size: 2rem; color: white;">{sunset}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # تبويبات Galaxy AI
    tab1, tab2, tab3 = st.tabs([
        f"📅 {_['forecast_7days']}",
        f"🤖 {_['ai_insights']}",
        f"📊 {_['hourly_forecast']}"
    ])
    
    with tab1:
        if 'daily' in weather_data and 'time' in weather_data['daily']:
            days = weather_data['daily']['time'][:7]
            max_temps = weather_data['daily']['temperature_2m_max'][:7]
            min_temps = weather_data['daily']['temperature_2m_min'][:7]
            weather_codes = weather_data['daily']['weather_code'][:7]
            precip_probs = weather_data['daily'].get('precipitation_probability_max', [0]*7)[:7]
            
            for i in range(7):
                day_name = datetime.fromisoformat(days[i]).strftime('%A')
                icon, _ = get_weather_icon(weather_codes[i], 1)
                
                st.markdown(f"""
                    <div class="day-forecast">
                        <div style="display: flex; align-items: center; gap: 20px;">
                            <div style="width: 100px;">
                                <div style="color: white; font-weight: 600;">{day_name[:3]}</div>
                                <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">{days[i][5:]}</div>
                            </div>
                            <div style="font-size: 2rem; width: 60px;">{icon}</div>
                            <div style="flex: 1;">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <span style="color: white; font-size: 1.5rem;">{max_temps[i]}°</span>
                                    <span style="color: rgba(255,255,255,0.5);">/ {min_temps[i]}°</span>
                                </div>
                            </div>
                            <div style="color: #4A90E2;">
                                {precip_probs[i]}% 🌧️
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # توصيات Galaxy AI
        recommendations = get_ai_recommendations(
            current['temperature_2m'],
            current['relative_humidity_2m'],
            current['wind_speed_10m'],
            current['uv_index'],
            aqi,
            current.get('weather_code', 0)
        )
        
        st.markdown(f"""
            <div class="galaxy-heading">
                <span>🤖 {_['recommendations']}</span>
                <span class="ai-badge">AI</span>
            </div>
        """, unsafe_allow_html=True)
        
        for title, desc, emoji in recommendations:
            st.markdown(f"""
                <div class="oneui-card" style="margin: 10px 0; padding: 15px;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 2rem;">{emoji}</div>
                        <div>
                            <div style="color: white; font-weight: 600;">{title}</div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{desc}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # اقتراحات الملابس
        st.markdown(f"""
            <div class="galaxy-heading">
                <span>👕 {_['wear_suggestions']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if current['temperature_2m'] > 25:
            clothes = ["🩳 شورت", "👕 تي شيرت", "🧢 كاب", "🕶️ نظارة شمسية"]
        elif current['temperature_2m'] > 15:
            clothes = ["👖 بنطلون", "👕 قميص", "🧥 جاكيت خفيف"]
        else:
            clothes = ["🧥 معطف ثقيل", "🧣 وشاح", "🧤 قفازات", "👢 boots"]
        
        cols = st.columns(len(clothes))
        for i, (col, cloth) in enumerate(zip(cols, clothes)):
            with col:
                st.markdown(f"""
                    <div class="oneui-card" style="padding: 10px; text-align: center;">
                        <div style="font-size: 1.5rem;">{cloth.split()[0]}</div>
                        <div style="color: white; font-size: 0.8rem;">{' '.join(cloth.split()[1:])}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        if 'hourly' in weather_data and 'time' in weather_data['hourly']:
            hours = pd.to_datetime(weather_data['hourly']['time'][:24])
            temps = weather_data['hourly']['temperature_2m'][:24]
            
            # رسم بياني متطور
            fig = go.Figure()
            
            # إضافة خط درجة الحرارة
            fig.add_trace(go.Scatter(
                x=hours,
                y=temps,
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#4A90E2', width=3),
                marker=dict(size=8, color='white', line=dict(width=2, color='#4A90E2')),
                fill='tozeroy',
                fillcolor='rgba(74, 144, 226, 0.1)'
            ))
            
            # تنسيق الرسم
            fig.update_layout(
                title=dict(
                    text="🌡️ 24-Hour Temperature Trend",
                    font=dict(color='white', size=20)
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title="Time",
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title=f"Temperature (°{st.session_state.units == 'metric' and 'C' or 'F'})",
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                ),
                font=dict(color='white'),
                hovermode='x',
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # جدول سريع للـ 6 ساعات القادمة
            st.markdown("""
                <div style="margin-top: 30px;">
                    <div class="galaxy-heading">⏰ Next 6 Hours</div>
                </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(6)
            for i in range(6):
                with cols[i]:
                    hour_time = datetime.fromisoformat(weather_data['hourly']['time'][i]).strftime('%H:%M')
                    hour_temp = weather_data['hourly']['temperature_2m'][i]
                    hour_icon, _ = get_weather_icon(weather_data['hourly']['weather_code'][i], 1)
                    
                    st.markdown(f"""
                        <div class="oneui-card" style="padding: 10px; text-align: center;">
                            <div style="color: rgba(255,255,255,0.7);">{hour_time}</div>
                            <div style="font-size: 2rem;">{hour_icon}</div>
                            <div style="color: white; font-size: 1.5rem;">{hour_temp}°</div>
                        </div>
                    """, unsafe_allow_html=True)

else:
    # رسالة ترحيب فاخرة عند عدم وجود بيانات
    st.markdown("""
        <div style="text-align: center; padding: 100px 20px;">
            <div style="font-size: 8rem; animation: float 3s ease-in-out infinite;">🌌</div>
            <h1 class="galaxy-title">Galaxy S26 Ultra</h1>
            <p style="color: rgba(255,255,255,0.7); font-size: 1.5rem; margin: 40px 0;">
                Enter a city in the sidebar to experience<br>Galaxy AI Weather Intelligence
            </p>
            <div style="display: flex; justify-content: center; gap: 20px;">
                <div class="ai-badge" style="padding: 10px 20px;">✨ Galaxy AI Ready</div>
                <div class="ai-badge" style="padding: 10px 20px;">🚀 One UI 6.1</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== التذييل الكوني ====================
st.markdown(f"""
    <div class="cosmic-footer">
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
            <span>🌡️ {_['powered_by']}</span>
            <span>⚡ Galaxy AI {datetime.now().strftime('%Y')}</span>
            <span>📱 S26 Ultra Edition</span>
        </div>
        <div style="font-size: 0.8rem;">
            {_['updated']}: {datetime.now().strftime('%H:%M • %d %B %Y')}
        </div>
    </div>
""", unsafe_allow_html=True)
