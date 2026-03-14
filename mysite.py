import streamlit as st
import io
import speech_recognition as sr
import numpy as np
from gtts import gTTS
import librosa
import soundfile as sf
import time
import os
import tempfile
import base64
from openai import OpenAI

# إعداد الصفحة
st.set_page_config(page_title="Taher Voice Assistant", page_icon="🤖")

# شريط جانبي لإدخال API Key
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("🔑 OpenAI API Key:", type="password")
    
    if not api_key:
        st.warning("⚠️ أدخل مفتاح OpenAI")
        st.stop()
    
    st.success("✅ جاهز!")

# تهيئة OpenAI
client = OpenAI(api_key=api_key)

st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# الحالة
if "messages" not in st.session_state:
    st.session_state.messages = []

# سجل المحادثة
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")

# ✅ الدردشة النصية (تعمل دائماً)
if prompt := st.chat_input("💬 اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "أنت مساعد ذكي يتحدث العربية."},
                     {"role": "user", "content": prompt}],
            temperature=0.7
        )
        res_text = response.choices[0].message.content
        st.markdown(res_text)
        
        # صوت الرد
        tts = gTTS(res_text[:300], lang='ar')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        st.audio(audio_io.getvalue())
    
    st.session_state.messages.append({"role": "assistant", "content": res_text})

# ✅ تسجيل صوت بـ HTML5 (بدون مكتبات خارجية)
st.markdown("---")
st.subheader("🎤 تسجيل صوت")

# مكون تسجيل HTML
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        button { padding: 15px 30px; font-size: 18px; border-radius: 25px; border: none; cursor: pointer; margin: 5px; }
        .record { background: #ff4757; color: white; }
        .stop { background: #57606f; color: white; }
        .status { font-weight: bold; margin: 10px 0; padding: 10px; border-radius: 10px; }
        .recording { background: #ffa502; color: white; }
    </style>
</head>
<body>
    <button id="recordBtn" class="record">🎤 ابدأ التسجيل</button>
    <button id="stopBtn" class="stop" style="display:none;">⏹️ إيقاف</button>
    <div id="status" class="status">اضغط ابدأ التسجيل</div>
    
    <script>
    let recorder, stream;
    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const status = document.getElementById('status');
    
    recordBtn.onclick = async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({audio: true});
            recorder = new MediaRecorder(stream);
            let chunks = [];
            
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = () => {
                const blob = new Blob(chunks, {type: 'audio/webm'});
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onload = () => {
                    parent.document.getElementById('audio-input').value = reader.result;
                    status.innerHTML = '✅ تم التسجيل! اضغط تحويل';
                    status.className = 'status';
                    status.style.background = '#10ac84';
                };
                stream.getTracks().forEach(track => track.stop());
            };
            
            recorder.start();
            recordBtn.style.display = 'none';
            stopBtn.style.display = 'inline';
            status.innerHTML = '🎙️ جاري التسجيل...';
            status.className = 'status recording';
        } catch(e) {
            status.innerHTML = '❌ خطأ في الميكروفون';
        }
    };
    
    stopBtn.onclick = () => {
        recorder.stop();
        recordBtn.style.display = 'inline';
        stopBtn.style.display = 'none';
    };
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=200)

# تحويل الصوت المسجل
audio_input = st.text_area("الصوت المسجل:", key="audio_data", height=0)
col1, col2 = st.columns([3,1])
with col2:
    if st.button("🔄 تحويل الصوت", type="primary") and audio_input:
        with st.spinner("جاري التحويل..."):
            try:
                # معالجة الصوت
                audio_bytes = base64.b64decode(audio_input.split(',')[1])
                audio_io = io.BytesIO(audio_bytes)
                
                # تحويل لـ WAV
                y, sr = librosa.load(audio_io, sr=16000, mono=True)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    sf.write(f.name, y, 16000)
                    wav_path = f.name
                
                # التعرف على الكلام
                r = sr.Recognizer()
                with sr.AudioFile(wav_path) as source:
                    data = r.record(source)
                
                text = r.recognize_google(data, language='ar-SA')
                os.unlink(wav_path)
                
                # معالجة النص
                st.session_state.messages.append({"role": "user", "content": f"🎤 {text}"})
                with st.chat_message("user"):
                    st.markdown(f"**أنت:** {text}")
                
                # رد المساعد
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": "أنت مساعد ذكي يتحدث العربية."},
                             {"role": "user", "content": text}],
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    tts = gTTS(reply[:300], lang='ar')
                    audio_io = io.BytesIO()
                    tts.write_to_fp(audio_io)
                    st.audio(audio_io.getvalue())
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.success("✅ تم!")
                
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# أزرار التحكم
if st.button("🗑️ مسح الدردشة"):
    st.session_state.messages = []
    st.rerun()
