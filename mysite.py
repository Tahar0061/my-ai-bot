import streamlit as st
import google.generativeai as genai

# إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح مفقود!")
    st.stop()

st.set_page_config(page_title="منفذ الأوامر الذكي", layout="wide")
st.title("🛠️ منفذ أوامر طاهر")

# تهيئة المحرك
model = genai.GenerativeModel('gemini-1.5-flash')

# خانة إدخال الأمر (كتابة أو عبر الميكروفون إذا أردت لاحقاً)
user_input = st.text_area("أدخل أمرك هنا (مثلاً: اكتب كود لعبة دومينو بـ Python):", height=150)

if st.button("تنفيذ الأمر"):
    if user_input:
        with st.spinner("جاري التنفيذ..."):
            try:
                # طلب النتيجة مباشرة
                response = model.generate_content(user_input)
                
                st.subheader("النتيجة:")
                # عرض النتيجة في صندوق نصي احترافي لسهولة النسخ
                st.code(response.text)
                
            except Exception as e:
                st.error(f"فشل التنفيذ: {e}")
    else:
        st.warning("الرجاء كتابة أمر أولاً.")



