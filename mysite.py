import streamlit as st
import google.generativeai as genai

# 1. الربط مع المفتاح السري (تأكد من وجوده في إعدادات الموقع)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("لم يتم العثور على المفتاح السري GOOGLE_API_KEY")

st.title("🤖 مساعد طاهر الذكي")

# 2. إنشاء مخزن للمحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال طلب المستخدم (هنا كان النقص)
if prompt := st.chat_input("اسألني أي شيء..."):
    # إضافة رسالة المستخدم للموقع
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. طلب الرد من الذكاء الاصطناعي (هذا هو الجزء المفقود)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # عرض رد المساعد وحفظه في الذاكرة
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ في الرد: {e}")
