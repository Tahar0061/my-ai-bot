import streamlit as st
import google.generativeai as genai
import os
import io
import base64
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import tempfile
import time

# --- Configuration --- #
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
elif os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    st.error("GOOGLE_API_KEY not found. Please add it to Streamlit secrets or set it as an environment variable.")
    st.stop()

st.title("🤖 Taher's Voice Assistant - صوتي ومتحدث")

# --- Session State Initialization --- #
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_voice_mode" not in st.session_state:
    st.session_state.is_voice_mode = False
if "tts_language" not in st.session_state:
    st.session_state.tts_language = "ar"

# --- Helper Functions --- #
@st.cache_data(ttl=3600)
def get_available_models():
    try:
        all_models = genai.list_models()
        supported_models = []
        for m in all_models:
            if "generateContent" in m.supported_generation_methods:
                supported_models.append(m.name.split('/')[-1])
        return supported_models
    except Exception as e:
        st.error(f"Error listing models: {e}")
        return []

def select_model():
    available_models = get_available_models()
    if not available_models:
        st.error("No suitable Gemini models found.")
        return None
    preferred_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    for model_name in preferred_models:
        if model_name in available_models:
            return model_name
    return available_models[0]

def speech_to_text(audio_bytes):
    """Convert speech to text using Google's Speech Recognition"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ar-SA')  # Arabic language
        return text
    except sr.UnknownValueError:
        return "لم أفهم الصوت، حاول مرة أخرى"
    except sr.RequestError:
        return "خطأ في التعرف على الصوت"
    except Exception as e:
        return f"خطأ: {str(e)}"

def text_to_speech(text, lang="ar"):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        st.error(f"TTS Error: {e}")
        return None

# --- Sidebar Controls --- #
with st.sidebar:
    st.header("⚙️ الإعدادات")
    voice_mode = st.toggle("وضع الصوت", value=st.session_state.is_voice_mode)
    st.session_state.is_voice_mode = voice_mode
    
    language = st.selectbox("لغة الرد الصوتي", ["ar", "en"], 
                           index=0 if st.session_state.tts_language == "ar" else 1)
    st.session_state.tts_language = language

# --- Main Application Logic --- #
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### الرسائل السابقة")
    for message in st.session_state.messages[-5:]:  # Show last 5 messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with col2:
    # Voice Mode Interface
    if st.session_state.is_voice_mode:
        st.markdown("### 🎤 وضع الصوت النشط")
        
        # Audio Recorder
        audio_bytes = audio_recorder(
            text="اضغط وسجل صوتك...",
            recording_color="#e8b923",
            neutral_color="#6c757d",
            wave_dark_color="#e8b923",
            progress_back_color="#e8b923"
        )
        
        if audio_bytes:
            # Convert speech to text
            with st.spinner("جاري الاستماع..."):
                prompt = speech_to_text(audio_bytes)
                st.session_state.messages.append({"role": "user", "content": f"🎤 {prompt}"})
                
                with st.chat_message("user"):
                    st.markdown(f"🎤 **أنت:** {prompt}")
                
                # Get AI response
                selected_model_name = select_model()
                if selected_model_name:
                    model = genai.GenerativeModel(selected_model_name)
                    response = model.generate_content(prompt)
                    
                    response_text = response.text
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    with st.chat_message("assistant"):
                        st.markdown(f"🤖 **المساعد:** {response_text}")
                        
                        # Text to Speech
                        audio_data = text_to_speech(response_text, st.session_state.tts_language)
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3")
                            st.balloons()
    
    else:
        # Text Chat Interface
        st.markdown("### 💬 الدردشة النصية")
        if prompt := st.chat_input("اكتب رسالتك هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            selected_model_name = select_model()
            if selected_model_name:
                try:
                    model = genai.GenerativeModel(selected_model_name)
                    response = model.generate_content(prompt)
                    
                    response_text = response.text
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    with st.chat_message("assistant"):
                        st.markdown(response_text)
                        
                        # Optional: TTS even in text mode
                        if st.button("🔊 الاستماع للرد", key=f"tts_{len(st.session_state.messages)}"):
                            audio_data = text_to_speech(response_text, st.session_state.tts_language)
                            if audio_data:
                                st.audio(audio_data, format="audio/mp3")

# --- Clear Chat Button --- #
if st.button("🗑️ مسح المحادثة", type="secondary"):
    st.session_state.messages = []
    st.rerun()

# --- Instructions --- #
with st.expander("📋 كيفية الاستخدام"):
    st.markdown("""
    ### في وضع الصوت:
    1. فعّل **وضع الصوت** من الشريط الجانبي
    2. اضغط على الزر الأحمر وسجل صوتك
    3. المساعد سيسمعك ويرد عليك صوتياً
    
    ### في وضع النص:
    1. اكتب رسالتك في المربع السفلي
    2. اضغط **🔊 الاستماع للرد** لسماع الرد صوتياً
    
    **اللغة**: العربية والإنجليزية مدعومة
    """)
