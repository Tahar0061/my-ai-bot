# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_lottie import st_lottie
import numpy as np

# 1. إعداد الصفحة الفاخرة الفائقة (S26 Ultra Dynamic Island Style)
st.set_page_config(
    page_title="Taher | Galaxy S26 Ultra Weather", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. نظام اللغات العالمي مع تأثيرات بصرية
LANGS = {
    "ar": {
        "search": "🔍 بحث كوني:", 
        "settings": "⚙️ إعدادات المجرة", 
        "temp": "🌡️ الحرارة", 
        "hum": "💧 الرطوبة الكونية", 
        "wind": "🌪️ الرياح", 
        "uv": "☢️ مؤشر UV", 
        "feels": "💫 يشعر كـ", 
        "aqi": "✨ نقاء الهواء", 
        "wear": "👕 ملابس اليوم", 
        "act": "🚀 أنشطة", 
        "updated": "🔄 آخر تحديث مجري:", 
        "forecast": "📅 توقعات الأيام الكونية",
        "sunrise": "🌅 شروق",
        "sunset": "🌇 غروب",
        "pressure": "📊 ضغط جوي",
        "visibility": "👁️ رؤية",
        "precip": "🌧️ فرصة أمطار"
    },
    "en": {
        "search": "🔍 Cosmic Search:", 
        "settings": "⚙️ Galaxy Settings", 
        "temp": "🌡️ Temperature", 
        "hum": "💧 Cosmic Humidity", 
        "wind": "🌪️ Wind", 
        "uv": "☢️ UV Index", 
        "feels": "💫 Feels like", 
        "aqi": "✨ Air Quality", 
        "wear": "👕 Today's Wear", 
        "act": "🚀 Activities", 
        "updated": "🔄 Galaxy Update:", 
        "forecast": "📅 Cosmic Forecast",
        "sunrise": "🌅 Sunrise",
        "sunset": "🌇 Sunset",
        "pressure": "📊 Pressure",
        "visibility": "👁️ Visibility",
        "precip": "🌧️ Precipitation"
    }
}

# 3. تأثيرات بصرية متطورة (Dynamic Island Effects)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* خلفية ديناميكية متحركة */
    .stApp {
        background: radial-gradient(ellipse at 20% 30%, #0a0f1e, #000000);
        position: relative;
        overflow: hidden;
    }
    
    /* تأثير النجوم المتحركة */
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
    
    /* Dynamic Island Header */
    .dynamic-island {
        background: rgba(20, 30, 50, 0.3);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 60px;
        padding: 1rem 2rem;
        margin: 1rem auto;
        max-width: 90%;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(255, 255, 255, 0.05);
        animation: floatIn 1s ease-out;
    }
    
    @keyframes floatIn {
        0% { transform: translateY(-100px) scale(0.8); opacity: 0; }
        100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    
    /* بطاقات زجاجية فائقة مع تأثير ثلاثي الأبعاد */
    .s26-card {
        background: linear-gradient(145deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5),
                   0 0 0 1px rgba(255, 255, 255, 0.05) inset;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .s26-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s;
        pointer-events: none;
    }
    
    .s26-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 40px 60px -15px rgba(0, 0, 0, 0.6),
                   0 0 0 2px rgba(255, 255, 255, 0.2) inset;
    }
    
    .s26-card:hover::before {
        opacity: 1;
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* قيم رقمية متوهجة */
    .glow-value {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #a0b0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(100, 150, 255, 0.5);
        line-height: 1.2;
    }
    
    /* عناوين متألقة */
    .galaxy-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a0d0ff 50%, #fff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(70, 130, 255, 0.7);
        margin-bottom: 0.5rem;
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    /* توقيت كوني */
    .cosmic-time {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 100px;
        padding: 0.8rem 1.5rem;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: inline-block;
        backdrop-filter: blur(10px);
    }
    
    /* شريط تقدم دائري */
    .circular-progress {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#4a90e2 0deg 180deg, #2c3e50 180deg 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    /* تذييل متطور */
    .cosmic-footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.9rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 3rem;
    }
    
    /* أيقونات متحركة */
    .pulse-icon {
        animation: pulse 2s ease-in-out infinite;
        display: inline-block;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    /* شريط جانبي زجاجي */
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(10, 15, 25, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* تخصيص الـ scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4a90e2, #9b59b6);
        border-radius: 10px;
    }
    
    /* تأثير الظل النيون */
    .neon-glow {
        text-shadow: 0 0 10px rgba(74, 144, 226, 0.5),
                     0 0 20px rgba(74, 144, 226, 0.3),
                     0 0 30px rgba(74, 144, 226, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 4. دوال مساعدة متطورة
def load_lottie_url(url):
    """تحميل رسوم متحركة Lottio مع تأثيرات"""
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

def get_cosmic_time():
    """الحصول على الوقت الكوني المنسق"""
    now = datetime.now()
    return now.strftime("%H:%M • %d %B %Y")

def create_gauge_chart(value, max_value, title):
    """إنشاء مقياس دائري متطور"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'color': 'white', 'size': 14}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#4a90e2"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, max_value/2], 'color': 'rgba(74, 144, 226, 0.2)'},
                {'range': [max_value/2, max_value], 'color': 'rgba(155, 89, 182, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Space Grotesk"},
        height=200,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# 5. تحميل الرسوم المتحركة
lottie_galaxy = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_p8bfn5tk.json")
lottie_weather = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_t0x0v9.json")

# 6. الشريط الجانبي الفاخر
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 2rem; background: linear-gradient(135deg, #fff, #a0b0ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🌌 S26 Ultra
            </h1>
            <div class="cosmic-time">✨ Galaxy AI ✨</div>
        </div>
    """, unsafe_allow_html=True)
    
    # اختيار اللغة مع تأثير
    lang = st.selectbox(
        "🌐",
        ["ar", "en"],
        format_func=lambda x: {"ar": "🇸🇦 العربية", "en": "🇬🇧 English"}[x],
        label_visibility="collapsed"
    )
    st.session_state.l = lang
    _ = LANGS[lang]
    
    # شريط بحث كوني
    city = st.text_input(
        _["search"], 
        "دبي",
        placeholder="مثال: دبي، لندن، نيويورك..."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # رسوم متحركة
    if lottie_galaxy:
        st_lottie(lottie_galaxy, height=150, key="galaxy_anim")
    
    st.markdown("---")
    
    # إعدادات سريعة
    with st.expander("⚡ AI Settings", expanded=False):
        st.slider("🎚️ AI Sensitivity", 0, 100, 50)
        st.toggle("🤖 Smart Recommendations", value=True)
        st.toggle("🌙 Night Mode", value=True)

# 7. دالة جلب بيانات متطورة
@st.cache_data(ttl=300, show_spinner="🔄 جاري الاتصال بالمجرّة...")
def get_galaxy_weather(city_name):
    """جلب بيانات الطقس بتقنية Galaxy AI"""
    try:
        # البحث عن الموقع
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        ).json()
        
        if 'results' not in geo:
            return None
            
        loc = geo['results'][0]
        
        # جلب جميع البيانات في وقت واحد
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast",
            params={
                'latitude': loc['latitude'],
                'longitude': loc['longitude'],
                'current': ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 
                           'weather_code', 'wind_speed_10m', 'wind_direction_10m', 
                           'pressure_msl', 'surface_pressure', 'uv_index'],
                'hourly': ['temperature_2m', 'relative_humidity_2m', 'weather_code'],
                'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 
                         'sunrise', 'sunset', 'precipitation_probability_max'],
                'timezone': 'auto'
            }
        ).json()
        
        # معالجة البيانات
        return {
            'city': loc['name'],
            'country': loc.get('country', ''),
            'lat': loc['latitude'],
            'lon': loc['longitude'],
            'current': weather['current'],
            'hourly': weather['hourly'],
            'daily': weather['daily']
        }
    except Exception as e:
        st.error(f"⚠️ خطأ في الاتصال: {str(e)}")
        return None

# 8. دالة تحليل AI
def ai_recommendations(temp, humidity, uv):
    """توصيات ذكية من Galaxy AI"""
    recommendations = []
    if temp > 30:
        recommendations.append("🩳 ملابس صيفية خفيفة")
        recommendations.append("🧴 استخدم واقي الشمس")
    elif temp < 15:
        recommendations.append("🧥 جاكيت دافئ")
        recommendations.append("☕ مشروب ساخن")
    
    if uv > 6:
        recommendations.append("🕶️ نظارة شمسية")
    
    if humidity > 70:
        recommendations.append("💧 جفف شعرك جيداً")
    
    return recommendations if recommendations else ["✨ طقس مثالي لأي نشاط"]

# 9. الواجهة الرئيسية
if 'l' not in st.session_state:
    st.session_state.l = 'ar'

_ = LANGS[st.session_state.l]

# عرض البيانات
data = get_galaxy_weather(city)

if data:
    current = data['current']
    
    # Dynamic Island Header
    st.markdown(f"""
        <div class="dynamic-island">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="pulse-icon">🌍</span>
                    <span style="color: white; font-size: 1.2rem; margin-left: 10px;">{data['city']}, {data['country']}</span>
                </div>
                <div class="cosmic-time">
                    {get_cosmic_time()}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # العنوان الرئيسي
    st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <div class="galaxy-title">{current['temperature_2m']}°</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 1.5rem;">
                {_['feels']} {current['apparent_temperature']}°
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # بطاقات القياسات الرئيسية
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
                    <div style="font-size: 2rem; margin-bottom: 1rem;">{icon}</div>
                    <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; letter-spacing: 1px;">{label}</div>
                    <div class="glow-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # التبويبات المتطورة
    tab1, tab2, tab3 = st.tabs([
        "📅 " + _['forecast'], 
        "🤖 AI Insights", 
        "📊 Cosmic Analysis"
    ])
    
    with tab1:
        # توقعات 7 أيام
        cols = st.columns(7)
        for i, col in enumerate(cols):
            with col:
                day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i % 7]
                max_temp = data['daily']['temperature_2m_max'][i] if i < len(data['daily']['temperature_2m_max']) else "--"
                min_temp = data['daily']['temperature_2m_min'][i] if i < len(data['daily']['temperature_2m_min']) else "--"
                
                st.markdown(f"""
                    <div class="s26-card" style="padding: 1rem;">
                        <div style="font-size: 1.2rem; color: white;">{day_name}</div>
                        <div style="font-size: 2rem; color: #4a90e2;">{max_temp}°</div>
                        <div style="color: rgba(255,255,255,0.5);">{min_temp}°</div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # توصيات AI
        recs = ai_recommendations(
            current['temperature_2m'],
            current['relative_humidity_2m'],
            current['uv_index']
        )
        
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: white; font-size: 2rem;">🤖 Galaxy AI Recommendations</h2>
            </div>
        """, unsafe_allow_html=True)
        
        for rec in recs:
            st.markdown(f"""
                <div class="s26-card" style="margin: 0.5rem 0; padding: 1.5rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 2rem;">{rec.split()[0]}</span>
                        <span style="color: white; font-size: 1.2rem;">{' '.join(rec.split()[1:])}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # رسم بياني متطور
        if data['hourly']:
            hours = pd.to_datetime(data['hourly']['time'][:24])
            temps = data['hourly']['temperature_2m'][:24]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hours,
                y=temps,
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#4a90e2', width=4),
                marker=dict(size=8, color='white', line=dict(width=2, color='#4a90e2')),
                fill='tozeroy',
                fillcolor='rgba(74, 144, 226, 0.2)'
            ))
            
            fig.update_layout(
                title=dict(text="📈 24-Hour Temperature Trend", font=dict(color='white', size=20)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Time", title_font=dict(color='white')),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Temperature (°C)", title_font=dict(color='white')),
                font=dict(color='white'),
                hovermode='x'
            )
            
            st.plotly_chart(fig, use_container_width=True)

else:
    # رسالة ترحيب متطورة
    st.markdown("""
        <div style="text-align: center; padding: 5rem;">
            <h1 class="galaxy-title">🌌 Galaxy S26 Ultra</h1>
            <p style="color: rgba(255,255,255,0.7); font-size: 1.5rem; margin: 2rem;">
                أدخل اسم المدينة في الشريط الجانبي لاستكشاف الطقس بتقنية AI
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if lottie_weather:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_weather, height=300)

# تذييل كوني
st.markdown(f"""
    <div class="cosmic-footer">
        {_['updated']} Galaxy AI • {datetime.now().strftime('%Y')}
    </div>
""", unsafe_allow_html=True)
