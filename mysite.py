

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
