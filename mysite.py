
import streamlit as st
import google.generativeai as genai
import os
from streamlit_mic_recorder import mic_recorder # تأكد من إضافة streamlit-mic-recorder في ملف requirements.txt

# --- الإعدادات العامة --- #
# تم تغيير اسم الصفحة والأيقونة هنا لتظهر بشكل مستقل
st.set_page_config(page_title="مساعد طاهر الذكي", page_icon="🎙️")

# التحقق من وجود المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
elif os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    st.error("المفتاح السري GOOGLE_API_KEY غير موجود.")
    st.stop()

st.title("🎙️ مساعد طاهر الذكي")

# --- تهيئة ذاكرة المحادثة --- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- الوظائف المساعدة --- #
@st.cache_data(ttl=3600)
def get_available_models():
    try:
        all_models = genai.list_models()
        supported_models = [m.name.split('/')[-1] for m in all_models if "generateContent" in m.supported_generation_methods]
        return supported_models
    except Exception as e:
        st.error(f"Error listing models: {e}")
        return []

def select_model():
    available_models = get_available_models()
    if not available_models:
        st.error("لم يتم العثور على نماذج متاحة.")
        return None
    preferred_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    for model_name in preferred_models:
        if model_name in available_models:
            return model_name
    return available_models[0]

# --- منطق التطبيق الرئيسي --- #

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- قسم الأوامر الصوتية --- #
st.write("اضغط للتحدث:")
# إضافة الميكروفون
audio = mic_recorder(start_prompt="🎤 ابدأ التحدث", stop_prompt="🛑 إيقاف وإرسال", key='recorder')

# استقبال النص من الكتابة
prompt = st.chat_input("اسألني أي شيء...")

# إذا تم استخدام الصوت، نقوم بوضع نص بديل (لأن تحويل الصوت لنص يتطلب خدمة إضافية)
# ولكن الهاتف سيتعرف على الصوت إذا استخدمت ميكروفون لوحة المفاتيح في خانة الكتابة
if audio:
    prompt = "لقد استلمت رسالتك الصوتية بنجاح!" 

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    selected_model_name = select_model()
    if selected_model_name:
        try:
            model = genai.GenerativeModel(selected_model_name)
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
