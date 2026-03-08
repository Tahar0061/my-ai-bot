import streamlit as st
import google.generativeai as genai
import io
import os
import tempfile
import speech_recognition as sr
import numpy as np
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf

# إعداد المفتاح السري (تأكد من وجوده في Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ مفقود مفتاح API!")
    st.stop()

st.set_page_config(page_title="مساعد طاهر الصوتي", page_icon="🤖")
st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض آخر 5 رسائل
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")

# أداة تسجيل الصوت
audio_bytes = audio_recorder(
    text="🎤 اضغط وسجل صوتك",
    icon_size="3x",
    recording_color="#ff4b4b",
    neutral_color="#6c757d"
)

if audio_bytes:
    with st.spinner("🔄 جاري المعالجة..."):
        try:
            # تحويل الصوت للصيغة الصحيحة
            audio_array, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, audio_array, 16000)
                temp_file_path = temp_file.name
            
            # التعرف على الكلام
            r = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio = r.record(source)
            
            try:
                user_text = r.recognize_google(audio, language='ar-SA')
            except:
                user_text = r.recognize_google(audio, language='en-US')
            
            os.unlink(temp_file_path) # مسح الملف المؤقت
            
            # إضافة رسالة المستخدم
            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(user_text)
            
            # الحصول على رد من Gemini (تم استخدام الإصدار الأحدث لضمان الرد)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(user_text)
            res_text = response.text
            
            # تحويل الرد لصوت
            tts = gTTS(text=res_text[:300], lang='ar')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            
            with st.chat_message("assistant"):
                st.markdown(res_text)
                st.audio(audio_io.getvalue(), format="audio/mp3", autoplay=True)
                st.balloons()
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")

# خانة الكتابة النصية
if prompt := st.chat_input("💬 اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    res = model.generate_content(prompt)
    st.session_state.messages.append({"role": "assistant", "content": res.text})
    with st.chat_message("assistant"): st.markdown(res.text)

# أزرار التحكم
if st.button("🗑️ مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()
