import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import io
import speech_recognition as sr

# 1. ربط المفتاح السري (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ المفتاح مفقود في إعدادات Secrets!")
    st.stop()

st.set_page_config(page_title="مساعد طاهر الجديد", page_icon="🤖")
st.title("🤖 مساعد طاهر الصوتي (نسخة نظيفة)")

# 2. تعريف الموديل الحديث المتوافق مع مفتاحك
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. أداة تسجيل الصوت
audio_bytes = audio_recorder(text="🎤 اضغط وسجل صوتك الآن", icon_size="3x")

if audio_bytes:
    try:
        # تحويل الصوت لنص
        r = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        user_text = r.recognize_google(audio, language='ar-SA')
        st.info(f"💬 أنت: {user_text}")

        # الحصول على الرد من جوجل
        response = model.generate_content(user_text)
        res_text = response.text
        st.success(f"🤖 المساعد: {res_text}")

        # تحويل الرد لصوت مسموع
        tts = gTTS(text=res_text, lang='ar')
        audio_out = io.BytesIO()
        tts.write_to_fp(audio_out)
        st.audio(audio_out.getvalue(), format="audio/mp3", autoplay=True)

    except Exception as e:
        st.warning("يرجى التحدث بوضوح أو التأكد من اتصال الإنترنت.")
