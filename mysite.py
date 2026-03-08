import streamlit as st
import google.generativeai as genai

# إعداد مفتاح API من إعدادات Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("لم يتم العثور على مفتاح GOOGLE_API_KEY في الإعدادات!")

# العنوان
st.title("مساعد طاهر الذكي 🤖")

# التأكد من اسم الموديل الصحيح لتجنب خطأ 404
model = genai.GenerativeModel('gemini-1.5-flash')

# تهيئة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق الإدخال
if prompt := st.chat_input("اسألني أي شيء..."):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # جلب الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                # إضافة رد الذكاء الاصطناعي للذاكرة
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
