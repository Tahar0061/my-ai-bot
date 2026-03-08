


import streamlit as st
import google.generativeai as genai
import io
import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf

# 1. إعداد المفتاح السري من Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ مفتاح API غير موجود في إعدادات Secrets!")
    st.stop()

st.set_page_config(page_title="مساعد طاهر الصوتي", page_icon="🤖")
st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 2. أداة تسجيل الصوت
audio_bytes = audio_recorder(
    text="🎤 اضغط وسجل صوتك",
    icon_size="3x",
    recording_color="#ff4b4b",
    neutral_color="#6c757d"
)

if audio_bytes:
    with st.spinner("🔄 جاري المعالجة..."):
        try:
            # معالجة الصوت وتحويل التردد لضمان دقة التعرف
            audio_array, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, audio_array, 16000)
                temp_file_path = temp_file.name
            
            # تحويل الصوت لنص
            r = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio = r.record(source)
            
            # التعرف على الكلام باللغة العربية
            user_text = r.recognize_google(audio, language='ar-SA')
            os.unlink(temp_file_path)
            
            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(user_text)
            
            # 3. استخدام الموديل الصحيح مع علامة اليساوي (تم التصحيح هنا)
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            response = model.generate_content(user_text)
            res_text = response.text
            
            # 4. تحويل الرد لصوت
            tts = gTTS(text=res_text[:300], lang='ar')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            
            with st.chat_message("assistant"):
                st.markdown(res_text)
                st.audio(audio_io.getvalue(), format="audio/mp3", autoplay=True)
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            st.rerun()

        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")

# خانة الكتابة النصية البديلة
if prompt := st.chat_input("💬 أو اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    # تصحيح السطر هنا أيضاً
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    res = model.generate_content(prompt)
    st.session_state.messages.append({"role": "assistant", "content": res.text})
    with st.chat_message("assistant"): st.markdown(res.text)

# زر مسح المحادثة
if st.button("🗑️ مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()
