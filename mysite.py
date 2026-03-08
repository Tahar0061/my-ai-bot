
import streamlit as st
import google.generativeai as genai

# محاولة جلب المفتاح بأكثر من طريقة لضمان التشغيل
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    # رسالة خطأ توضيحية أكثر
    st.error("❌ الكود لم يجد المفتاح في Secrets. يرجى التأكد من الحفظ.")
    st.stop()
