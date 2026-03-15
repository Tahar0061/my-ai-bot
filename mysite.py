
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="مرصد طاهر المالي", layout="wide")

st.title("💰 تطبيق مراقبة الأسواق العالمية")

# قائمة الأصول التي سنراقبها
assets = {
    'الذهب': 'GC=F',
    'البيتكوين': 'BTC-USD',
    'النفط (برنت)': 'BZ=F',
    'الدولار مقابل اليورو': 'EURUSD=X'
}

st.sidebar.header("إعدادات العرض")
selected_asset = st.sidebar.selectbox("اختر ما تريد مراقبته:", list(assets.keys()))

st.subheader(f"📊 تحليل سعر: {selected_asset}")

try:
    # جلب البيانات من ياهو فاينانس
    data = yf.download(assets[selected_asset], period="1mo", interval="1d")
    
    if not data.empty:
        # عرض السعر الحالي
        current_price = data['Close'].iloc[-1]
        st.metric(label=f"السعر الحالي لـ {selected_asset}", value=f"{current_price:,.2f}")
        
        # رسم بياني لحركة السعر في آخر شهر
        st.line_chart(data['Close'])
        
        # عرض جدول البيانات
        with st.expander("عرض سجل البيانات التاريخي"):
            st.dataframe(data.tail(10))
    else:
        st.error("لم نتمكن من جلب البيانات، تأكد من اتصال السيرفر بالإنترنت.")

except Exception as e:
    st.error(f"حدث خطأ فني: {e}")

st.info("💡 هذا التطبيق يسحب بيانات حية من الأسواق العالمية لاختبار كفاءة تطبيقك.")
