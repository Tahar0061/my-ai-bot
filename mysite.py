import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="مرصد طاهر المالي", layout="wide")
st.title("💰 تطبيق مراقبة الأسواق العالمية")

assets = {
    'الذهب': 'GC=F',
    'البيتكوين': 'BTC-USD',
    'النفط (برنت)': 'BZ=F',
    'الدولار مقابل اليورو': 'EURUSD=X'
}

st.sidebar.header("إعدادات العرض")
selected_asset = st.sidebar.selectbox("اختر ما تريد مراقبته:", list(assets.keys()))

try:
    # جلب البيانات
    data = yf.download(assets[selected_asset], period="1mo", interval="1d")
    
    if not data.empty:
        # الإصلاح هنا: تحويل السعر إلى رقم عشري بسيط قبل التنسيق
        last_price = float(data['Close'].iloc[-1]) 
        
        st.metric(label=f"السعر الحالي لـ {selected_asset}", value=f"{last_price:,.2f}")
        
        # رسم بياني
        st.line_chart(data['Close'])
        
    else:
        st.error("لم نتمكن من جلب البيانات حالياً.")

except Exception as e:
    st.error(f"حدث خطأ فني: {e}")
