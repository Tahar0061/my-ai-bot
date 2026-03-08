import streamlit as st
import google.generativeai as genai
import io
import speech_recognition as sr
import numpy as np
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf
import time

# إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ مفقود مفتاح API!")
    st.stop()

st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "listening" not in st.session_state:
    st.session_state.listening = False

# عرض آخر 5 رسائل
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")

# شريط التقدم للصوت
progress_bar = st.progress(0)
status_text = st.empty()

# أداة تسجيل الصوت المحسّنة
audio_bytes = audio_recorder(
    text="🎤 اضغط وسجل صوتك",
    icon_name="user",
    icon_size="3x",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    wave_dark_color="#ff4b4b",
    progress_back_color="#ffeaa7"
)

if audio_bytes:
    with st.spinner("🔄 جاري الاستماع والمعالجة..."):
        status_text.text("🎧 تحليل الصوت...")
        progress_bar.progress(20)
        
        try:
            # تحويل الصوت للصيغة الصحيحة (16kHz mono WAV)
            audio_array, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)
            
            # حفظ مؤقت للملف
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, audio_array, 16000)
                temp_file_path = temp_file.name
            
            progress_bar.progress(50)
            status_text.text("🧠 تحويل الصوت إلى نص...")
            
            # التعرف على الكلام
            r = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio = r.record(source)
            
            # محاولة التعرف بالعربية أولاً ثم الإنجليزية
            try:
                user_text = r.recognize_google(audio, language='ar-SA')
            except:
                try:
                    user_text = r.recognize_google(audio, language='en-US')
                except:
                    user_text = "لم أفهم الصوت، حاول مرة أخرى بصوت أوضح 🔄"
            
            # تنظيف الملف المؤقت
            os.unlink(temp_file_path)
            
            progress_bar.progress(70)
            
            # إضافة رسالة المستخدم
            st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
            with st.chat_message("user"):
                st.markdown(f"**أنت:** {user_text}")
            
            status_text.text("🤖 جاري التفكير في الرد...")
            progress_bar.progress(90)
            
            # الحصول على رد من Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_text)
            res_text = response.text
            
            # تحويل الرد لصوت
            status_text.text("🔊 تحويل الرد إلى صوت...")
            tts = gTTS(text=res_text[:500], lang='ar', slow=False)  # تقصير النص للصوت
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            
            progress_bar.progress(100)
            
            # عرض الرد
            with st.chat_message("assistant"):
                st.markdown(f"**المساعد:** {res_text}")
                st.audio(audio_io.getvalue(), format="audio/mp3")
                st.balloons()
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
            # إعادة تعيين
            status_text.text("✅ جاهز للاستماع!")
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")
            status_text.text("❌ حدث خطأ، حاول مرة أخرى")
            progress_bar.empty()

# خانة الكتابة النصية
col1, col2 = st.columns([4, 1])
with col1:
    if prompt := st.chat_input("💬 اكتب رسالتك هنا أو استخدم الصوت..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(prompt)
            res_text = res.text
            st.markdown(res_text)
            
            # زر الاستماع للرد النصي
            if st.button("🔊 الاستماع", key=f"listen_{len(st.session_state.messages)}"):
                tts = gTTS(text=res_text[:500], lang='ar')
                audio_io = io.BytesIO()
                tts.write_to_fp(audio_io)
                st.audio(audio_io.getvalue(), format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})

# أزرار التحكم
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🗑️ مسح المحادثة", type="secondary"):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("🔄 إعادة تشغيل", type="primary"):
        st.rerun()
