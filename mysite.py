
import streamlit as st
import requests
from datetime import datetime

# إعداد الصفحة لتكون عريضة واحترافية
st.set_page_config(page_title="مراقب الطقس العالمي", layout="wide")

# دالة لجلب البيانات الشاملة
def get_full_weather(city_name):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar&format=json"
    geo_res = requests.get(geo_url).json()
    if 'results' in geo_res:
        res = geo_res['results'][0]
        lat, lon, timezone = res['latitude'], res['longitude'], res['timezone']
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,uv_index,visibility&daily=sunrise,sunset,uv_index_max&timezone={timezone}"
        return requests.get(weather_url).json(), res['name']
    return None, None

# واجهة المستخدم
st.title("🌍 مركز الأرصاد الجوية الاحترافي")
city_input = st.text_input("أدخل المدينة لاستكشاف طقسها الآن:", "مكة")

data, city_name = get_full_weather(city_input)

if data:
    curr = data['current']
    daily = data['daily']
    
    # --- قسم الفيديوهات التوضيحية (بناءً على حالة الطقس) ---
    st.subheader("📺 نظرة حية على الأجواء")
    code = curr['weather_code']
    # فيديوهات عينات (روابط مباشرة لمقاطع فيديو قصيرة)
    if code == 0: # صافي
        st.video("https://www.shutterstock.com/shutterstock/videos/1069352158/preview/stock-footage-clear-blue-sky-with-white-clouds-time-lapse-sky-background.mp4")
    elif code in [1, 2, 3]: # غيوم جزئية
        st.video("https://www.shutterstock.com/shutterstock/videos/1060194382/preview/stock-footage-beautiful-white-clouds-soar-across-the-blue-sky.mp4")
    else: # مطر أو عواصف
        st.video("https://www.shutterstock.com/shutterstock/videos/1058455825/preview/stock-footage-rain-drops-falling-on-the-glass-window-rainy-day.mp4")

    st.divider()

    # --- القسم الأول: الحرارة والرطوبة (كما في 776.jpg) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("الحرارة الفعلية", f"{curr['temperature_2m']}°C")
    with col2:
        st.metric("الإحساس الحقيقي", f"{curr['apparent_temperature']}°C")
    with col3:
        st.metric("الرطوبة", f"{curr['relative_humidity_2m']}%")
    with col4:
        st.metric("الرؤية", f"{curr['visibility'] / 1000} كم")

    # --- القسم الثاني: الشمس والرياح (كما في 780.jpg و 782.jpg) ---
    st
