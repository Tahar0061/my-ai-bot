import streamlit as st
import requests

# إعداد الصفحة لتكون احترافية
st.set_page_config(page_title="مرصد طاهر المتطور", layout="wide")

# تصميم الواجهة بالألوان (CSS)
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e3a8a;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }
    .main-title { color: #3b82f6; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌤️ مركز طاهر العالمي للأرصاد</h1>", unsafe_allow_html=True)

city = st.text_input("📍 أدخل اسم المدينة (مثلاً: Witten أو مكة):", "Witten")

def get_weather(city_name):
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1").json()
        if 'results' in geo:
            res = geo['results'][0]
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={res['latitude']}&longitude={res['longitude']}&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m,pressure_msl,surface_pressure&daily=sunrise,sunset,uv_index_max&timezone=auto"
            return requests.get(w_url).json()
    except: return None
    return None

data = get_weather(city)

if data:
    curr = data['current']
    daily = data['daily']
    
    # --- الواجهة الرئيسية (مثل صورك 776.jpg) ---
    st.markdown(f"### 🌡️ حالة الطقس في {city.upper()}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>🌡️ الحرارة</h3><h2>{curr['temperature_2m']}°C</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>💧 الرطوبة</h3><h2>{curr['relative_humidity_2m']}%</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>🌬️ الرياح</h3><h2>{curr['wind_speed_10m']} كم/س</h2></div>", unsafe_allow_html=True)

    st.divider()

    # --- أيقونات الضغط والشمس (مثل 780.jpg) ---
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"**⏲️ الضغط الجوي:** {curr['pressure_msl']} hPa")
        st.info("أيقونة الضغط الجوي مستقرة ✅")
    with col5:
        st.markdown(f"**☀️ مؤشر الأشعة UV:** {daily['uv_index_max'][0]}")
        st.warning("أيقونة الشمس والحرارة ☀️")
    with col6:
        st.markdown(f"**🏃 حالة المشي:**")
        if curr['temperature_2m'] < 30: st.success("مناسب للمشي 🏃")
        else: st.error("حار جداً للمشي 🥵")

    st.divider()

    # --- شروق وغروب الشمس (مثل 782.jpg) ---
    st.subheader("🌅 دورة الشمس اليوم")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.write(f"☀️ شروق الشمس: **{daily['sunrise'][0].split('T')[1]}**")
    with c_s2:
        st.write(f"🌑 غروب الشمس: **{daily['sunset'][0].split('T')[1]}**")

    # --- الفيديو التوضيحي (بناءً على حالة الجو) ---
    st.subheader("🎬 محاكاة حية للأجواء")
    if curr['weather_code'] == 0:
        st.video("https://www.w3schools.com/html/mov_bbb.mp4") # فيديو توضيحي للسماء الصافية
    else:
        st.video("https://www.w3schools.com/html/rain.mp4") # فيديو للمطر

else:
    st.error("لم نتمكن من العثور على المدينة. تأكد من اتصال الإنترنت.")
