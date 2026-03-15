import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# إعداد الموديل
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 مبرمج طاهر الذكي")

# التقاط الأمر الصوتي
st.subheader("قل لي ماذا تريد أن أبرمج لك:")
recorded_text = speech_to_text(language='ar-SA', start_prompt="تحدث الآن 🎤", stop_prompt="إرسال الطلب ✅", key='coder_mic')

if recorded_text:
    st.info(f"🚀 جاري معالجة طلبك: {recorded_text}")
    
    # إرسال الطلب لـ Gemini
    with st.spinner("جاري كتابة الكود..."):
        try:
            prompt = f"أنت مبرمج خبير، اكتب لي كود برمجي كامل لـ: {recorded_text}"
            response = model.generate_content(prompt)
            
            st.success("✅ تم إنشاء الكود بنجاح:")
            st.code(response.text, language='python') # سيعرض الكود بشكل منسق
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
model = genai.GenerativeModel('gemini-1.5-flash-latest')
