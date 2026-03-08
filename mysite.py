import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import io
import speech_recognition as sr

# 1. تهيئة المفتاح السري بأمان
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ خطأ: المفتاح السري غير موجود في Secrets!")
    st.stop()

st.set_page_config(page_title="مساعد طاهر 2026", layout="centered")
st.title("🤖 مساعد طاهر - النسخة الجديدة كلياً")

# 2. تعريف الموديل الحديث
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. واجهة التسجيل الصوتي
audio_bytes = audio_recorder(text="🎤 اضغط وسجل طلبك بوضوح", icon_size="3x")

if audio_bytes:
    try:
        # تحويل الصوت لنص
        r = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        user_text = r.recognize_google(audio, language='ar-SA')
        
        st.info(f"💬 أنت: {user_text}")

        # توليد رد الذكاء الاصطناعي
        with st.spinner("⏳ المساعد يفكر الآن..."):
            response = model.generate_content(user_text)
            res_text = response.text
        
        st.success(f"🤖 المساعد: {res_text}")

        # تحويل الرد لصوت (TTS)
        tts = gTTS(text=res_text, lang='ar')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        st.audio(audio_io.getvalue(), format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.warning("⚠️ يرجى إعادة المحاولة والتحدث بوضوح.")


