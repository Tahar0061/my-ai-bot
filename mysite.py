import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="مرصد طاهر العالمي للطقس", page_icon="🌤️")

st.title("🌤️ تطبيق طاهر للأرصاد الجوية العالمية")

# إدخال اسم المدينة
city = st.text_input("اكتب اسم أي مدينة بالعربي أو الإنجليزي (مثلاً: مكة، Berlin، Cairo):", "مكة")

# استخدام واجهة برمجة تطبيقات مفتوحة للطقس (Open-Meteo) لا تحتاج لمفتاح API
def get_weather(city_name):
    # أولاً: نحصل على إحداثيات المدينة
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ar&format=json"
    geo_res = requests.get(geo_url).json()
    
    if 'results' in geo_res:
        lat = geo_res['results'][0]['latitude']
        lon = geo_res['results'][0]['longitude']
        timezone = geo_res['results'][0]['timezone']
        
        # ثانياً: جلب بيانات الطقس التفصيلية
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m&daily=sunrise,sunset&timezone={timezone}"
        return requests.get(weather_url).json()
    return None

data = get_weather(city)

if data:
    current = data['current']
    daily = data['daily']
    
    # 1. عرض درجة الحرارة والحالة العامة
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("درجة الحرارة الآن", f"{current['temperature_2m']}°C")
    with col2:
        st.metric("الرياح", f"{current['wind_speed_10m']} كم/س")
    with col3:
        st.metric("الرطوبة", f"{current['relative_humidity_2m']}%")

    st.divider()

    # 2. أوقات الشروق والغروب (كما في صورتك)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("🌅 **شروق الشمس:**")
        st.info(daily['sunrise'][0].split("T")[1])
    with col_s2:
        st.write("🌇 **غروب الشمس:**")
        st.info(daily['sunset'][0].split("T")[1])

    st.divider()

    # 3. تحليل حالة المشي (تحليل مبرمج)
    st.subheader("🏃 حالة المشي والرياضة اليوم:")
    temp = current['temperature_2m']
    wind = current['wind_speed_10m']
    
    if 15 <= temp <= 30 and wind < 20:
        st.success("✅ الأجواء ممتازة للمشي الآن!")
    elif temp > 30:
        st.warning("⚠️ الجو حار، يفضل المشي في المساء.")
    else:
        st.error("🥶 الجو بارد جداً أو الرياح قوية، انتبه!")

else:
    st.error("لم يتم العثور على المدينة، تأكد من كتابة الاسم بشكل صحيح.")

st.caption("تمت البرمجة بواسطة طاهر - بيانات حية من القمر الصناعي")
