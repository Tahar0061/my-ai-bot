
import streamlit as st

st.set_page_config(page_title="مختبر طاهر", page_icon="✅")

st.title("📝 تطبيق إدارة المهام (إختبار النظام)")

# إنشاء قائمة مهام في ذاكرة المتصفح
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# إدخال مهمة جديدة
new_task = st.text_input("أضف مهمة جديدة لاختبار النظام:", placeholder="مثلاً: تنظيف الملفات...")

if st.button("إضافة"):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.success("تمت الإضافة بنجاح!")
    else:
        st.warning("اكتب شيئاً أولاً")

# عرض المهام
st.subheader("قائمة المهام المضافة:")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        st.write(f"{i+1}. {task}")
else:
    st.info("القائمة فارغة حالياً.")

# زر لمسح كل شيء
if st.button("مسح الكل"):
    st.session_state.tasks = []
    st.rerun()
