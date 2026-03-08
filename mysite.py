
import streamlit as st
import google.generativeai as genai
import io
import speech_recognition as sr
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import tempfile
import os
import librosa
import soundfile as sf
import numpy as np

# إعداد API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ مفتاح API مفقود!")
    st.stop()

st.set_page_config(page_title="طاهر الصوتي", layout="wide")
st.title("🤖 طاهر - مساعدك الصوتي")
st.markdown("🎙️ **تحدث معي الآن - سأرد عليك صوتياً!**")

# الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "audio_players" not in st.session_state:
    st.session_state.audio_players = []

# عرض المحادثة
for i, m in enumerate(st.session_state.messages[-8:]):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        
        # إضافة زر تشغيل صوت للردود السابقة
        if m["role"] == "assistant" and i < len(st.session_state.audio_players):
            if st.button("🔊 استمع", key=f"replay_{i}"):
                st.audio(st.session_state.audio_players[i], format="audio/mp3")

# الفاصل
st.markdown("─" * 70)

# الميكروفون الرئيسي
col1, col2 = st.columns([3, 1])
with col1:
    audio_bytes = audio_recorder(
        text="🎙️ اضغط طويلاً للتحدث (3-5 ثوان)",
        recording_color="#ff4757",
        neutral_color="#2d3436",
        icon_size="4x",
        sample_rate=16000
    )

with col2:
    st.info("💡 نصائح:\n• تحدث بوضوح\n• 3-5 ثوان كافية\n• العربية الفصحى أفض
