import streamlit as st
import google.generativeai as genai
import io
import speech_recognition as sr
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import tempfile
import os
import soundfile as sf
import librosa
import numpy as np

# إعداد API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ مفتاح API مفقود!")
    st.stop()

st.title("🤖 مساعد طاهر الصوتي")
st.caption("🎤 تحدث معي الآن - سأسمعك وأرد صوتياً!")

# الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# عرض آخر 6 رسائل
for m in st.session_state.messages[-6:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("─" * 60)

# ✅ أداة تسجيل الصوت المُصححة
audio_bytes = audio_recorder(
    text="🎙️ اضغط للتحدث",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_size="3x",
    sample_rate=16000  # ✅ إضافة sample_rate هنا تحل المشكلة!
)

if audio_bytes and not st.session_state.processing:
    st.session_state.processing = True
    
    with st.spinner("🔄 جاري سماعك وتحليل الكلام..."):
        try:
            # ✅ 1. تصحيح صيغة الصوت (هذا الحل الرئيسي!)
            # تحويل لـ 16kHz mono WAV
            audio_array, sr_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)
            
            # حفظ مؤقت للصيغة الصحيحة
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                sf.write(tmp_file.name, audio_array, 16000)
                fixed_audio_path = tmp_file.name
            
            # 2. تحويل الصوت لنص (الآن سيعمل 100%)
            r = sr.Recognizer()
            with sr.AudioFile(fixed_audio_path) as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.record(source)
            
            # التعرف على الكلام
            user_text = r.recognize_google(audio, language='ar-SA')
            
            # تنظيف الملف المؤقت
            os.unlink(fixed_audio_path)
            
            # عرض كلامك
            st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
            with st.chat_message("user"):
                st.markdown(f"**أنت:** {user_text}")
                st.balloons()
            
            # 3. رد الذكاء الاصطناعي
            model = genai.GenerativeModel('gemini-1.5-flash')  # الأسرع والأفضل
            response = model.generate_content(user_text)
            res_text = response.text
            
            # 4. تحويل الرد لصوت
            tts = gTTS(text=res_text[:350], lang='ar', slow=False)
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            
            with st.chat_message("assistant"):
                st.markdown(f"**طاهر:** {res_text}")
                st.audio(audio_io.getvalue(), format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except sr.UnknownValueError:
            st.warning("👂 لم أفهم الكلام! تحدث ببطء ووضوح أكثر 😊")
        except sr.RequestError as e:
            st.error(f"❌ مشكلة في Google Speech: {e}")
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)[:100]}")
        
        st.session_state.processing = False
        st.rerun()

# خانة النص
if prompt := st.chat_input("💬 أو اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# أزرار التحكم
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ مسح المحادثة", type="secondary"):
        st.session_state.messages = []
        st.session_state.processing = False
        st.rerun()
with col2:
    st.info("✅ جاهز للاستماع!")

st.markdown("---")
st.caption("👨‍💻 طاهر | صوتي وسريع الاستجابة 🚀")
