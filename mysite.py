import streamlit as st
import pandas as pd
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="مشروع طاهر الجديد", page_icon="📊")

st.title("🚀 مشروع تحليل البيانات واختبار الصوت")

# قسم اختبار الميكروفون
st.header("1. اختبار الميكروفون")
text = speech_to_text(language='ar-SA', start_prompt="تحدث الآن لنجرب الصوت 🎤", stop_prompt="إيقاف ✅", key='mic')

if text:
    st.success(f"✅ الميكروفون يعمل! النص الملتقط: {text}")

# قسم رفع الملفات
st.header("2. مركز رفع الملفات")
uploaded_file = st.file_uploader("اختر ملفاً من جهازك (صورة أو CSV)")

if uploaded_file is not None:
    st.write(f"📁 اسم الملف: {uploaded_file.name}")
    st.write(f"⚖️ حجم الملف: {uploaded_file.size} بايت")
    
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.write("📊 بيانات الملف:")
        st.dataframe(df)
    else:
        st.image(uploaded_file, caption="المعاينة")
