
import streamlit as st
import google.generativeai as genai
import io
import speech_recognition as sr
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder

# الربط بالمفتاح السري (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ المفتاح مفقود! تأكد من وضعه في Secrets.")
    st.stop()

st.set_page_config(page_title="مساعد طاهر الذكي", layout="centered")
st.title("🤖 مساعد طاهر الصوتي")
st.info("اضغط على الميكروفون بالأسفل وتحدث")

# تعريف الموديل الحديث
model = genai.GenerativeModel('gemini-1.5-flash')

# أداة تسجيل الصوت
audio_bytes = audio_recorder(text="سجل صوتك هنا", icon_size="3x")

if audio_bytes:
    try:
        # 1. تحويل الصوت المسجل إلى نص
        r = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        user_text = r.recognize_google(audio, language='ar-SA')
        st.write(f"💬 **أنت:** {user_text}")
        
        # 2. إرسال النص لجوجل والحصول على رد
        response = model.generate_content(user_text)
        bot_reply = response.text
        st.write(f"🤖 **المساعد:** {bot_reply}")
        
        # 3. تحويل رد المساعد إلى صوت مسموع
        tts = gTTS(text=bot_reply, lang='ar')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        st.audio(audio_io.getvalue(), format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"⚠️ حدث تنبيه: تأكد من وضوح الصوت. (التفاصيل: {e})")
