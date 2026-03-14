import streamlit as st
import io
import speech_recognition as sr
import numpy as np
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf
import time
import os
import tempfile
from openai import OpenAI

# OpenAI API Configuration مع حقل إدخال
api_key = st.sidebar.text_input("🔑 أدخل OpenAI API Key:", type="password", 
                               help="احصل على المفتاح من https://platform.openai.com/api-keys")

if api_key:
    client = OpenAI(api_key=api_key)
    st.sidebar.success("✅ تم الاتصال بنجاح!")
else:
    st.sidebar.warning("⚠️ يرجى إدخال OpenAI API Key")
    st.stop()

st.set_page_config(page_title="Taher Voice Assistant", page_icon="🤖")

st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# باقي الكود يبقى كما هو...
if "messages" not in st.session_state:
    st.session_state.messages = []
if "listening" not in st.session_state:
    st.session_state.listening = False

# Display Chat History (Last 5 messages)
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")

# Progress bar for visual feedback
progress_bar = st.progress(0)
status_text = st.empty()

# Audio Recorder Component
audio_bytes = audio_recorder(
    text="🎤 اضغط وسجل صوتك",
    icon_name="microphone",
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
            # Convert audio to correct format (16kHz mono WAV)
            audio_io = io.BytesIO(audio_bytes)
            audio_array, sample_rate = librosa.load(audio_io, sr=16000, mono=True)
            
            # Temporary file for speech recognition
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, audio_array, 16000)
                temp_file_path = temp_file.name
            
            progress_bar.progress(50)
            status_text.text("🧠 تحويل الصوت إلى نص...")
            
            # Speech Recognition
            r = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio_data = r.record(source)
            
            # Try Arabic first, then English
            try:
                user_text = r.recognize_google(audio_data, language='ar-SA')
            except Exception:
                try:
                    user_text = r.recognize_google(audio_data, language='en-US')
                except Exception:
                    user_text = "لم أفهم الصوت، حاول مرة أخرى بصوت أوضح 🔄"
            
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            progress_bar.progress(70)
            
            # Append user message
            st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
            with st.chat_message("user"):
                st.markdown(f"**أنت:** {user_text}")
            
            status_text.text("🤖 جاري التفكير في الرد...")
            progress_bar.progress(90)
            
            # Get response from OpenAI GPT-4 (تم تصحيح اسم الموديل)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # تم تصحيح اسم الموديل
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي متعدد اللغات. تتحدث باللغة العربية والإنجليزية. كن مفيداً وودياً وإيجابياً في ردودك."},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=500
            )
            res_text = response.choices[0].message.content
            
            # Convert response to speech
            status_text.text("🔊 تحويل الرد إلى صوت...")
            tts = gTTS(text=res_text[:500], lang='ar', slow=False)
            audio_response_io = io.BytesIO()
            tts.write_to_fp(audio_response_io)
            audio_response_io.seek(0)
            
            progress_bar.progress(100)
            
            # Display Assistant Response
            with st.chat_message("assistant"):
                st.markdown(f"**المساعد:** {res_text}")
                st.audio(audio_response_io.getvalue(), format="audio/mp3")
                st.balloons()
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
            # Reset UI
            status_text.text("✅ جاهز للاستماع!")
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")
            status_text.text("❌ حدث خطأ، حاول مرة أخرى")
            progress_bar.progress(0)

# Text Input Field
if prompt := st.chat_input("💬 اكتب رسالتك هنا أو استخدم الصوت..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # تم تصحيح اسم الموديل
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي متعدد اللغات. تتحدث باللغة العربية والإنجليزية. كن مفيداً وودياً وإيجابياً في ردودك."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        res_text = response.choices[0].message.content
        st.markdown(res_text)
        
        # Text-to-Speech for text response
        tts = gTTS(text=res_text[:500], lang='ar')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        st.audio(audio_io.getvalue(), format="audio/mp3")
        
        st.session_state.messages.append({"role": "assistant", "content": res_text})

# Control Buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🗑️ مسح المحادثة", type="secondary"):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("🔄 إعادة تشغيل", type="primary"):
        st.rerun()
