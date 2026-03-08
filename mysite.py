
import streamlit as st
import google.generativeai as genai

# محاولة جلب المفتاح بأكثر من طريقة لضمان التشغيل
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ المفتاح غير مفعّل. تأكد من ضغط زر Save في إعدادات Secrets.")
    st.stop()
