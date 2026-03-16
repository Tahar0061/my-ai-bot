# تطبيق طقس متطور مع واجهة مستخدم حديثة

```python
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
from PIL import Image
import io
import base64

# إعداد الصفحة
st.set_page_config(
    page_title="طاهر | الطقس الذكي",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تثبيت التصميم الحديث
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
    }
    
    .weather-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
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
    }
    
    .wind-card {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
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
    
    .city-badge {
        display: inline-block;
        background: #e0f7fa;
        color: #006064;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        margin: 0.25rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .city-badge:hover {
        background: #006064;
        color: white;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1.5rem;
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
    
    .hourly-forecast {
        display: flex;
        overflow-x: auto;
        gap: 1rem;
        padding: 1rem 0;
    }
    
    .hour-item {
        min-width: 100px;
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
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

# الواجهة الرئيسية
st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5rem;">🌤️ طاهر | الطقس الذكي</h1>
        <p style="margin:0; opacity: 0.9; font-size: 1.1rem;">تطبيق الطقس المتطور مع واجهة مستوحاة من تطبيقات الهواتف الذكية</p>
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.ssidebar:
    st.markdown("### ⚙️ الإعدادات")
    
    # البحث عن المدينة
    city = st.text_input("🔍 ابحث عن مدينة:", "Witten")
    
    # المدن المفضلة
    st.markdown("### ⭐ المدن المفضلة")
    favorite_cities = ["الرياض", "جدة", "دبي", "القاهرة", "الدوحة"]
    
    cols = st.columns(2)
    for i, fav_city in enumerate(favorite_cities):
        with cols[i % 2]:
            if st.button(f"📍 {fav_city}", key=f"fav_{fav_city}"):
                city = fav_city
                st.rerun()
    
    # إعدادات الوحدة
    st.markdown("### 📏 الوحدات")
    unit_system = st.radio("نظام الوحدات:", ["متري (°C, km/h)", "إمبراطوري (°F, mph)"])
    
    # تحديث البيانات
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.rerun()

# وظيفة جلب بيانات الطقس
@st.cache_data(ttl=300)
def get_weather_data(city_name):
    try:
        # البحث عن الإحداثيات
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar"
        geo_response = requests.get(geo_url, timeout=10)
        geo_data = geo_response.json()
        
        if 'results' in geo_data and len(geo_data['results']) > 0:
            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            city_name_ar = location.get('name', city_name)
            
            # جلب بيانات الطقس الحالية والمستقبلية
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl,visibility&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=7"
            
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()
            
            # جلب بيانات جودة الهواء (API وهمي للتوضيح)
            aqi_data = {
                'aqi': 45,  # مؤشر جودة الهواء
                'pm25': 12.5,
                'pm10': 25.0,
                'no2': 18.3,
                'o3': 42.1
            }
            
            return {
                'city': city_name_ar,
                'location': location,
                'current': weather_data['current'],
                'hourly': weather_data['hourly'],
                'daily': weather_data['daily'],
                'aqi': aqi_data
            }
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {str(e)}")
        return None
    
    return None

# تحويل رمز الطقس إلى أيقونة
def get_weather_icon(code, is_day=True):
    icons = {
        0: "☀️" if is_day else "🌙",  # صافي
        1: "🌤️",  # قليل السحب
        2: "⛅",  # غائم جزئياً
        3: "☁️",  # غائم
        45: "🌫️", # ضباب
        48: "🌫️", # ضباب متجمد
        51: "🌦️", # رذاذ خفيف
        53: "🌦️", # رذاذ متوسط
        55: "🌦️", # رذاذ كثيف
        56: "🌧️", # رذاذ متجمد خفيف
        57: "🌧️", # رذاذ متجمد كثيف
        61: "🌧️", # مطر خفيف
        63: "🌧️", # مطر متوسط
        65: "🌧️", # مطر شديد
        66: "🌨️", # مطر متجمد خفيف
        67: "🌨️", # مطر متجمد شديد
        71: "❄️", # ثلج خفيف
        73: "❄️", # ثلج متوسط
        75: "❄️", # ثلج شديد
        77: "🌨️", # حبيبات ثلجية
        80: "🌧️", # زخات مطر خفيفة
        81: "🌧️", # زخات مطر متوسطة
        82: "⛈️", # زخات مطر شديدة
        85: "🌨️", # زخات ثلج خفيفة
        86: "🌨️", # زخات ثلج شديدة
        95: "⛈️", # عواصف رعدية
        96: "⛈️", # عواصف رعدية مع برد خفيف
        99: "⛈️", # عواصف رعدية مع برد شديد
    }
    return icons.get(code, "🌈")

# تحويل رمز الطقس إلى وصف
def get_weather_description(code):
    descriptions = {
        0: "سماء صافية",
        1: "قليل السحب",
        2: "غائم جزئياً",
        3: "غائم",
        45: "ضباب",
        48: "ضباب متجمد",
        51: "رذاذ خفيف",
        53: "رذاذ",
        55: "رذاذ كثيف",
        61: "مطر خفيف",
        63: "مطر",
        65: "مطر شديد",
        71: "ثلج خفيف",
        73: "ثلج",
        75: "ثلج شديد",
        77: "حبيبات ثلجية",
        80: "زخات مطر خفيفة",
        81: "زخات مطر",
        82: "زخات مطر غزيرة",
        85: "زخات ثلج خفيفة",
        86: "زخات ثلج غزيرة",
        95: "عواصف رعدية",
        96: "عواصف رعدية مع برد",
        99: "عواصف رعدية شديدة مع برد",
    }
    return descriptions.get(code, "حالة جوية غير معروفة")

# جلب بيانات الطقس
data = get_weather_data(city)

if data:
    current = data['current']
    daily = data['daily']
    hourly = data['hourly']
    aqi = data['aqi']
    
    # رأس الصفحة مع معلومات المدينة
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### 🌍 {data['city']}")
        st.markdown(f"📍 {data['location'].get('admin1', '')}, {data['location'].get('country', '')}")
        st.markdown(f"🕐 {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    
    with col2:
        weather_icon = get_weather_icon(current['weather_code'], current['is_day'])
        st.markdown(f'<div class="weather-icon-large">{weather_icon}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="metric-value">{current["temperature_2m"]}°C</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">يشعر كـ {current["apparent_temperature"]}°C</div>', unsafe_allow_html=True)
    
    # علامات التبويب
    tab1, tab2, tab3, tab4 = st.tabs(["📊 اليوم", "📈 7 أيام", "🌡️ تفاصيل", "🎯 التوصيات"])
    
    with tab1:
        # بطاقات الطقس الرئيسية
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="weather-card">
                    <div class="metric-label">💧 الرطوبة</div>
                    <div class="metric-value">{humidity}%</div>
                </div>
            """.format(humidity=current['relative_humidity_2m']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="wind-card">
                    <div class="metric-label">🌬️ سرعة الرياح</div>
                    <div class="metric-value">{wind} كم/س</div>
                    <div class="metric-label">اتجاه: {direction}°</div>
                </div>
            """.format(wind=current['wind_speed_10m'], direction=current['wind_direction_10m']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="weather-card">
                    <div class="metric-label">📊 الضغط الجوي</div>
                    <div class="metric-value">{pressure} hPa</div>
                </div>
            """.format(pressure=current['pressure_msl']), unsafe_allow_html=True)
        
        with col4:
            # جودة الهواء
            aqi_value = aqi['aqi']
            aqi_class = "aqi-good" if aqi_value <= 50 else "aqi-moderate" if aqi_value <= 100 else "aqi-unhealthy"
            st.markdown(f"""
                <div class="air-quality {aqi_class}">
                    <div>🌫️ جودة الهواء</div>
                    <div style="font-size: 1.5rem;">{aqi_value}</div>
                    <div>{"جيد" if aqi_value <= 50 else "معتدل" if aqi_value <= 100 else "غير صحي"}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # توقعات ساعية
        st.markdown("### 📅 التوقعات للساعات القادمة")
        
        # إنشاء عرض التوقعات الساعية
        hourly_data = []
        for i in range(0, min(12, len(hourly['time']))):
            time_str = hourly['time'][i]
            temp = hourly['temperature_2m'][i]
            icon = get_weather_icon(hourly['weather_code'][i], True)
            
            hourly_data.append({
                "time": datetime.fromisoformat(time_str).strftime("%I %p"),
                "temp": f"{temp}°C",
                "icon": icon
            })
        
        # عرض التوقعات الساعية
        cols = st.columns(len(hourly_data))
        for idx, hour_data in enumerate(hourly_data):
            with cols[idx]:
                st.markdown(f"""
                    <div class="hour-item">
                        <div style="font-weight: bold;">{hour_data['time']}</div>
                        <div style="font-size: 1.5rem;">{hour_data['icon']}</div>
                        <div style="font-size: 1.2rem; font-weight: bold;">{hour_data['temp']}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # شروق وغروب الشمس
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="sun
        # تكملة شروق وغروب الشمس
        with col1:
            st.markdown(f"""
                <div class="sun-card">
                   st.markdown("<div>\u2600\ufe0f شروق الشمس</div>", unsafe_allow_html=True)
                    <div class="metric-value" style="color: white;">{datetime.fromisoformat(daily['sunrise'][0]).strftime('%I:%M %p')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="sun-card" style="background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);">
                    <div class="metric-label" style="color: white; opacity: 0.9;">🌇 غروب الشمس</div>
                    <div class="metric-value" style="color: white;">{datetime.fromisoformat(daily['sunset'][0]).strftime('%I:%M %p')}</div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🗓️ توقعات الأيام السبعة القادمة")
        # تحويل البيانات لجدول أنيق
        df_daily = pd.DataFrame({
            "التاريخ": [datetime.fromisoformat(t).strftime('%Y-%m-%d') for t in daily['time']],
            "الحرارة القصوى (°C)": daily['temperature_2m_max'],
            "الحرارة الدنيا (°C)": daily['temperature_2m_min'],
            "الأمطار (مم)": daily['precipitation_sum'],
            "مؤشر UV": daily['uv_index_max']
        })
        
        # رسم بياني احترافي
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_daily["التاريخ"], y=df_daily["الحرارة القصوى (°C)"], name="العظمى", line=dict(color='#ff4b4b', width=4)))
        fig.add_trace(go.Scatter(x=df_daily["التاريخ"], y=df_daily["الحرارة الدنيا (°C)"], name="الصغرى", line=dict(color='#1c83e1', width=4)))
        fig.update_layout(title="تذبذب درجات الحرارة خلال الأسبوع", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.table(df_daily)

    with tab3:
        st.markdown("### 🌡️ تفاصيل تقنية إضافية")
        c1, c2, c3 = st.columns(3)
        c1.metric("الرؤية", f"{current['visibility'] / 1000} كم")
        c2.metric("مؤشر UV اليوم", daily['uv_index_max'][0])
        c3.metric("كمية الأمطار المتوقعة", f"{daily['precipitation_sum'][0]} مم")

    with tab4:
        st.markdown("### 🎯 توصيات طاهر الذكية")
        temp = current['temperature_2m']
        if temp > 30:
            st.warning("⚠️ الجو حار! ننصح بشرب الكثير من الماء وتجنب الشمس المباشرة.")
        elif temp < 15:
            st.info("🧥 الجو بارد نوعاً ما، لا تنسَ ارتداء ملابس دافئة.")
        else:
            st.success("🌤️ الجو مثالي لممارسة الرياضة أو المشي في الخارج.")

else:
    st.info("💡 أدخل اسم مدينة في الشريط الجانبي لبدء عرض بيانات الطقس.")

st.markdown("---")
st.markdown("<center style='color: #666;'>تم التطوير بكل حب بواسطة <b>طاهر</b> | 2026</center>", unsafe_allow_html=True)
