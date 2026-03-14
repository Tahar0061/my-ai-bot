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

# إعداد الصفحة
st.set_page_config(page_title="Taher Voice Assistant", page_icon="🤖")

# شريط جانبي لإدخال API Key
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.markdown("---")
    
    # خياران: إما استخدام متغير البيئة أو إدخال يدوي
    api_key_source = st.radio(
        "اختر طريقة إدخال مفتاح OpenAI:",
        ["متغير البيئة", "إدخال يدوي"]
    )
    
    if api_key_source == "إدخال يدوي":
        api_key = st.text_input(
            "🔑 أدخل OpenAI API Key:",
            type="password",
            help="احصل على المفتاح من https://platform.openai.com/api-keys"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ تم حفظ المفتاح!")
    else:
        # استخدام متغير البيئة الموجود
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ تم العثور على مفتاح في متغيرات البيئة")
        else:
            st.warning("⚠️ لم يتم العثور على مفتاح في متغيرات البيئة")
    
    st.markdown("---")
    st.markdown("### 📝 التعليمات:")
    st.markdown("""
    1. احصل على API Key من [OpenAI](https://platform.openai.com/api-keys)
    2. أدخل المفتاح في الحقل أعلاه
    3. ابدأ المحادثة بالصوت أو النص
    """)

# التحقق من وجود API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("""
    ⚠️ **لم يتم إدخال مفتاح OpenAI API**
    
    يرجى إدخال المفتاح في الشريط الجانبي أو إضافته كمتغير بيئة.
    
    **للحصول على مفتاح:**
    1. اذهب إلى [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    2. سجل الدخول أو أنشئ حساب
    3. اضغط على **Create new secret key**
    4. انسخ المفتاح وأدخله في الشريط الجانبي
    """)
    st.stop()

# تهيئة عميل OpenAI
try:
    client = OpenAI(api_key=api_key)
    # اختبار الاتصال بمحاولة بسيطة
    test_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "hello"}],
        max_tokens=1
    )
    st.sidebar.success("✅ تم الاتصال بـ OpenAI بنجاح!")
except Exception as e:
    st.sidebar.error(f"❌ خطأ في الاتصال: {str(e)}")
    st.stop()

# الواجهة الرئيسية
st.title("🤖 مساعد طاهر الصوتي")
st.markdown("---")

# تهيئة حالة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "listening" not in st.session_state:
    st.session_state.listening = False

# عرض سجل المحادثة (آخر 5 رسائل)
st.subheader("📜 سجل المحادثة")
for m in st.session_state.messages[-5:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")

# شريط التقدم للتغذية الراجعة البصرية
progress_bar = st.progress(0)
status_text = st.empty()

# مكون تسجيل الصوت
st.subheader("🎤 التسجيل الصوتي")
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
            # تحويل الصوت إلى التنسيق الصحيح (WAV 16kHz أحادي)
            audio_io = io.BytesIO(audio_bytes)
            audio_array, sample_rate = librosa.load(audio_io, sr=16000, mono=True)
            
            # ملف مؤقت للتعرف على الكلام
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, audio_array, 16000)
                temp_file_path = temp_file.name
            
            progress_bar.progress(50)
            status_text.text("🧠 تحويل الصوت إلى نص...")
            
            # التعرف على الكلام
            r = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio_data = r.record(source)
            
            # المحاولة بالعربية أولاً، ثم الإنجليزية
            try:
                user_text = r.recognize_google(audio_data, language='ar-SA')
            except Exception:
                try:
                    user_text = r.recognize_google(audio_data, language='en-US')
                except Exception:
                    user_text = "لم أفهم الصوت، حاول مرة أخرى بصوت أوضح 🔄"
            
            # تنظيف الملف المؤقت
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            progress_bar.progress(70)
            
            # إضافة رسالة المستخدم
            st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
            with st.chat_message("user"):
                st.markdown(f"**أنت:** {user_text}")
            
            status_text.text("🤖 جاري التفكير في الرد...")
            progress_bar.progress(90)
            
            # الحصول على رد من OpenAI
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
            
            # تحويل الرد إلى صوت
            status_text.text("🔊 تحويل الرد إلى صوت...")
            tts = gTTS(text=res_text[:500], lang='ar', slow=False)
            audio_response_io = io.BytesIO()
            tts.write_to_fp(audio_response_io)
            audio_response_io.seek(0)
            
            progress_bar.progress(100)
            
            # عرض رد المساعد
            with st.chat_message("assistant"):
                st.markdown(f"**المساعد:** {res_text}")
                st.audio(audio_response_io.getvalue(), format="audio/mp3")
                st.balloons()
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
            # إعادة تعيين واجهة المستخدم
            status_text.text("✅ جاهز للاستماع!")
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")
            status_text.text("❌ حدث خطأ، حاول مرة أخرى")
            progress_bar.progress(0)

# حقل إدخال النص
