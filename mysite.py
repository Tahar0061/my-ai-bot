GOOGLE_API_KEY = "AIzaSyDgpIC105BSADkJphkFzUa_kTrvI6881Zo"
import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import io
import speech_recognition as sr

# ربط المفتاح السري (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح مفقود في Secrets!")
    st.stop()

st.title("🤖 مساعد طاهر - النسخة الكاملة")

# تعريف الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

audio_bytes = audio_recorder(text="🎤 اضغط وتحدث الآن")

if audio_bytes:
    try:
        # الجزء الأول: تحويل الصوت لنص (يعمل عندك حالياً)
        r = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        user_text = r.recognize_google(audio, language='ar-SA')
        st.info(f"💬 أنت قلت: {user_text}")

        # الجزء الثاني: "العقل" (هذا هو الجزء الذي كان ناقصاً)
        with st.spinner("🤖 المساعد يفكر..."):
            response = model.generate_content(user_text)
            bot_reply = response.text
        
        # عرض الرد على الشاشة
        st.success(f"🤖 المساعد: {bot_reply}")

        # الجزء الثالث: "النطق" (تحويل الرد لصوت)
        tts = gTTS(text=bot_reply, lang='ar')
        audio_out = io.BytesIO()
        tts.write_to_fp(audio_out)
        st.audio(audio_out.getvalue(), format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الرد: {e}")

