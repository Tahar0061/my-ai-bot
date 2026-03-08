

import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. إعداد الصفحة (لتظهر باسمك)
st.set_page_config(page_title="مساعد طاهر الذكي", page_icon="🎙️")

# 2. ربط مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح السري ناقص في الإعدادات!")
    st.stop()

st.title("🎙️ مساعد طاهر الذكي")

# 3. نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 4. الميكروفون (الاستبدال الصحيح)
audio = mic_recorder(start_prompt="🎤 ابدأ التحدث الآن", stop_prompt="✅ إرسال وفهم الصوت", key='recorder')

if audio:
    with st.spinner("جاري سماعك وفهم كلامك..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # إرسال الصوت لـ Gemini ليقوم بالرد عليه مباشرة
            response = model.generate_content([
                "أجب على هذا التسجيل الصوتي باللغة العربية بذكاء:",
                {"mime_type": "audio/wav", "data": audio['bytes']}
            ])
            
            # عرض الرد في الصفحة
            st.session_state.messages.append({"role": "user", "content": "🎤 (رسالة صوتية)"})
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"خطأ: {e}")

# خانة الكتابة العادية
if prompt := st.chat_input("أو اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content(prompt)
    with st.chat_message("assistant"): st.markdown(res.text)
    st.session_state.messages.append({"role": "assistant", "content": res.text})
