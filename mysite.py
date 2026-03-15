import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# إعداد الصفحة والمفتاح
st.set_page_config(page_title="مبرمج طاهر الذكي", layout="centered")
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح السري مفقود في إعدادات Secrets!")
    st.stop()

st.title("🤖 مبرمج طاهر الذكي")

# محاولة تحميل الموديل بأكثر من اسم لضمان العمل
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

# واجهة التحدث
st.subheader("قل لي ماذا تريد أن أبرمج لك:")
recorded_text = speech_to_text(language='ar-SA', start_prompt="تحدث الآن 🎤", stop_prompt="إرسال الطلب ✅", key='final_mic')

if recorded_text:
    st.info(f"🚀 جاري معالجة طلبك: {recorded_text}")
    with st.spinner("جاري كتابة الكود..."):
        try:
            # استخدام generate_content بطريقة آمنة
            response = model.generate_content(f"اكتب كود برمجي لـ: {recorded_text}")
            st.success("✅ تم إنشاء الكود:")
            st.code(response.text)
        except Exception as e:
            st.error(f"حدث خطأ في النظام: {e}")
