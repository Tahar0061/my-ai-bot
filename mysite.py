

import streamlit as st
import google.generativeai as genai
import io
import speech_recognition as sr
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder

# إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")
    st.stop()

st.title("🤖 مساعد طاهر الصوتي")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# أداة تسجيل الصوت
audio_bytes = audio_recorder(text="اضغط وسجل صوتك", icon_size="2x")

if audio_bytes:
    try:
        # تحويل الصوت لنص
        r = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = r.record(source)
        user_text = r.recognize_google(audio, language='ar-SA')
        
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"): st.markdown(user_text)

        # الحصول على رد من Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_text)
        res_text = response.text

        # تحويل الرد لصوت
        tts = gTTS(text=res_text, lang='ar')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        
        with st.chat_message("assistant"):
            st.markdown(res_text)
            st.audio(audio_io.getvalue(), format="audio/mp3")
        
        st.session_state.messages.append({"role": "assistant", "content": res_text})

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

# خانة الكتابة
if prompt := st.chat_input("اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content(prompt)
    with st.chat_message("assistant"): st.markdown(res.text)
    st.session_state.messages.append({"role": "assistant", "content": res.text})
