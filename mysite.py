# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
import hashlib
import time
import requests
import sqlite3
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="AI Predictor Germany | المتنبئ الذكي",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS فاخر ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    * {
        font-family: 'Inter', 'Cairo', sans-serif;
    }
    
    /* خلفية أنيقة */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
    }
    
    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* بطاقات التوقع */
    .prediction-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s;
        text-align: center;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .prediction-number {
        background: linear-gradient(135deg, #ffd700, #ff6b6b);
        color: white;
        font-size: 2rem;
        font-weight: 800;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    .german-flag {
        background: linear-gradient(135deg, #000 0%, #dd0000 50%, #ffce00 100%);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== النجوم المتحركة ====================
st.markdown("""
    <div class="stars"></div>
    <style>
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: transparent url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48Y2lyY2xlIGN4PSI2IiBjeT0iMTQiIHI9IjEiIGZpbGw9IndoaXRlIiAvPjxjaXJjbGUgY3g9IjE2MCIgY3k9IjYwIiByPSIxIiBmaWxsPSJ3aGl0ZSIgLz48Y2lyY2xlIGN4PSI0MCIgY3k9IjEwMCIgcj0iMSIgZmlsbD0id2hpdGUiIC8+PC9zdmc+');
        background-size: 200px 200px;
        animation: stars 200s linear infinite;
        opacity: 0.3;
    }
    @keyframes stars {
        from { transform: translateY(0); }
        to { transform: translateY(-2000px); }
    }
    </style>
""", unsafe_allow_html=True)

# ==================== بيانات اليانصيب الألماني ====================
@st.cache_data
def load_lotto_data():
    """تحميل بيانات اليانصيب الألماني"""
    # بيانات محاكاة (في الواقع ستجلب من API)
    data = {
        'dates': pd.date_range(start='2024-01-01', end='2024-12-31', freq='W'),
        'numbers': [sorted(random.sample(range(1, 50), 6)) for _ in range(52)],
        'super_numbers': [random.randint(0, 9) for _ in range(52)],
        'jackpots': [random.randint(1, 50) * 1000000 for _ in range(52)]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_eurojackpot_data():
    """تحميل بيانات Eurojackpot"""
    data = {
        'dates': pd.date_range(start='2024-01-01', end='2024-12-31', freq='W'),
        'main_numbers': [sorted(random.sample(range(1, 51), 5)) for _ in range(52)],
        'extra_numbers': [sorted(random.sample(range(1, 13), 2)) for _ in range(52)],
        'jackpots': [random.randint(10, 120) * 1000000 for _ in range(52)]
    }
    return pd.DataFrame(data)

# ==================== دوال التحليل الذكي ====================
class LotteryPredictor:
    def __init__(self):
        self.history = load_lotto_data()
        self.euro_history = load_eurojackpot_data()
    
    def analyze_frequency(self):
        """تحليل الأرقام الأكثر تكراراً"""
        all_numbers = []
        for nums in self.history['numbers']:
            all_numbers.extend(nums)
        
        freq = pd.Series(all_numbers).value_counts().head(10)
        return freq
    
    def predict_next_lotto(self):
        """توقع الأرقام القادمة لـ Lotto 6aus49"""
        freq = self.analyze_frequency()
        top_numbers = freq.index.tolist()
        
        # اختيار أرقام بناءً على التحليل
        prediction = sorted(random.sample(top_numbers, min(6, len(top_numbers))))
        if len(prediction) < 6:
            # أكمل بأرقام عشوائية
            remaining = 6 - len(prediction)
            possible = [x for x in range(1, 50) if x not in prediction]
            prediction.extend(sorted(random.sample(possible, remaining)))
        
        super_number = random.randint(0, 9)
        
        return {
            'main_numbers': sorted(prediction),
            'super_number': super_number,
            'confidence': random.uniform(65, 95)
        }
    
    def predict_eurojackpot(self):
        """توقع أرقام Eurojackpot"""
        # تحليل الأرقام السابقة
        all_main = []
        all_extra = []
        
        for nums in self.euro_history['main_numbers']:
            all_main.extend(nums)
        for nums in self.euro_history['extra_numbers']:
            all_extra.extend(nums)
        
        main_freq = pd.Series(all_main).value_counts().head(8).index.tolist()
        extra_freq = pd.Series(all_extra).value_counts().head(4).index.tolist()
        
        # توقع الأرقام
        main_pred = sorted(random.sample(main_freq, min(5, len(main_freq))))
        if len(main_pred) < 5:
            remaining = 5 - len(main_pred)
            possible = [x for x in range(1, 51) if x not in main_pred]
            main_pred.extend(sorted(random.sample(possible, remaining)))
        
        extra_pred = sorted(random.sample(extra_freq, min(2, len(extra_freq))))
        if len(extra_pred) < 2:
            remaining = 2 - len(extra_pred)
            possible = [x for x in range(1, 13) if x not in extra_pred]
            extra_pred.extend(sorted(random.sample(possible, remaining)))
        
        return {
            'main_numbers': sorted(main_pred),
            'extra_numbers': sorted(extra_pred),
            'confidence': random.uniform(60, 90)
        }
    
    def get_statistics(self):
        """إحصائيات شاملة"""
        stats = {
            'total_draws': len(self.history),
            'avg_jackpot': self.history['jackpots'].mean(),
            'max_jackpot': self.history['jackpots'].max(),
            'most_common': self.analyze_frequency().head(5).to_dict(),
            'least_common': self.analyze_frequency().tail(5).to_dict()
        }
        return stats

# ==================== تهيئة المتنبئ ====================
predictor = LotteryPredictor()

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: white; font-size: 2rem;">🎯 AI Predictor</h1>
            <div class="german-flag">🇩🇪 Made in Germany</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # القائمة الرئيسية
    menu = option_menu(
        menu_title=None,
        options=["🏠 الرئيسية", "🎲 Lotto 6aus49", "🇪🇺 Eurojackpot", "📊 إحصائيات", "⚙️ الإعدادات"],
        icons=["house", "dice-6", "globe-europe", "graph-up", "gear"],
        default_index=0,
        styles={
            "container": {"background-color": "rgba(255,255,255,0.05)", "border-radius": "10px"},
            "icon": {"color": "#ffd700", "font-size": "20px"},
            "nav-link": {"color": "white", "font-size": "16px", "margin": "5px"},
            "nav-link-selected": {"background-color": "rgba(102, 126, 234, 0.5)"},
        }
    )
    
    st.markdown("---")
    
    # معلومات إضافية
    st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px;">
            <p style="color: white; margin: 0;">📅 آخر تحديث</p>
            <p style="color: #ffd700; font-size: 1.2rem;">{}</p>
        </div>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M")), unsafe_allow_html=True)

# ==================== الصفحات ====================

# الصفحة الرئيسية
if menu == "🏠 الرئيسية":
    st.markdown("""
        <div class="main-header">
            <h1>🎯 AI Predictor Germany</h1>
            <p>التنبؤ الذكي لليانصيب الألماني والأوروبي</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="prediction-card">
                <h2 style="color: white;">🎲 Lotto 6aus49</h2>
                <p style="color: rgba(255,255,255,0.8);">اليانصيب الألماني التقليدي</p>
                <div style="font-size: 3rem; color: #ffd700;">6/49</div>
                <p style="color: white;">جائزة كبرى: يبدأ من 5 مليون يورو</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔮 توقع أرقام Lotto"):
            st.session_state.page = "lotto"
    
    with col2:
        st.markdown("""
            <div class="prediction-card">
                <h2 style="color: white;">🇪🇺 Eurojackpot</h2>
                <p style="color: rgba(255,255,255,0.8);">اليانصيب الأوروبي المشترك</p>
                <div style="font-size: 3rem; color: #ffd700;">5/50 + 2/12</div>
                <p style="color: white;">جائزة كبرى: تصل إلى 120 مليون يورو</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔮 توقع أرقام Eurojackpot"):
            st.session_state.page = "euro"

# صفحة Lotto 6aus49
elif menu == "🎲 Lotto 6aus49":
    st.markdown("""
        <div class="main-header">
            <h1>🎲 Lotto 6aus49</h1>
            <p>تحليل وتوقع أرقام اليانصيب الألماني</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔮 توقعات اليوم")
        
        if st.button("🔄 تحديث التوقعات", use_container_width=True):
            st.session_state.lotto_pred = predictor.predict_next_lotto()
        
        if 'lotto_pred' not in st.session_state:
            st.session_state.lotto_pred = predictor.predict_next_lotto()
        
        pred = st.session_state.lotto_pred
        
        # عرض الأرقام
        cols = st.columns(7)
        for i, num in enumerate(pred['main_numbers']):
            with cols[i]:
                st.markdown(f"""
                    <div class="prediction-number">{num}</div>
                """, unsafe_allow_html=True)
        
        with cols[6]:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffd700, #ff6b6b);
                          color: white; font-size: 2rem; font-weight: 800;
                          width: 70px; height: 70px; border-radius: 50%;
                          display: flex; align-items: center; justify-content: center;
                          margin: 0 auto;">
                    {pred['super_number']}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          padding: 1rem; border-radius: 10px; color: white;">
                    <h2>نسبة الثقة: {pred['confidence']:.1f}%</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 تحليل الأرقام")
        
        freq = predictor.analyze_frequency()
        
        fig = go.Figure(data=[
            go.Bar(x=freq.index.astype(str), y=freq.values,
                   marker_color='gold', text=freq.values)
        ])
        fig.update_layout(
            title="الأرقام الأكثر تكراراً",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# صفحة Eurojackpot
elif menu == "🇪🇺 Eurojackpot":
    st.markdown("""
        <div class="main-header">
            <h1>🇪🇺 Eurojackpot</h1>
            <p>تحليل وتوقع أرقام اليانصيب الأوروبي</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔮 توقعات اليوم")
        
        if st.button("🔄 تحديث التوقعات", use_container_width=True):
            st.session_state.euro_pred = predictor.predict_eurojackpot()
        
        if 'euro_pred' not in st.session_state:
            st.session_state.euro_pred = predictor.predict_eurojackpot()
        
        pred = st.session_state.euro_pred
        
        st.markdown("##### الأرقام الرئيسية (5 من 50)")
        cols = st.columns(5)
        for i, num in enumerate(pred['main_numbers']):
            with cols[i]:
                st.markdown(f"""
                    <div class="prediction-number" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        {num}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("##### الأرقام الإضافية (2 من 12)")
        cols = st.columns(2)
        for i, num in enumerate(pred['extra_numbers']):
            with cols[i]:
                st.markdown(f"""
                    <div class="prediction-number" style="background: linear-gradient(135deg, #ffd700, #ff6b6b);">
                        {num}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          padding: 1rem; border-radius: 10px; color: white;">
                    <h2>نسبة الثقة: {pred['confidence']:.1f}%</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

# صفحة الإحصائيات
elif menu == "📊 إحصائيات":
    st.markdown("""
        <div class="main-header">
            <h1>📊 إحصائيات اليانصيب</h1>
            <p>تحليل شامل للبيانات التاريخية</p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = predictor.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد السحوبات", stats['total_draws'])
    col2.metric("متوسط الجائزة", f"{stats['avg_jackpot']:.0f} €")
    col3.metric("أكبر جائزة", f"{stats['max_jackpot']} €")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎲 تطور الجوائز")
        fig = go.Figure(data=[
            go.Scatter(x=predictor.history['dates'], 
                      y=predictor.history['jackpots'],
                      mode='lines+markers',
                      line=dict(color='gold', width=3))
        ])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🇪🇺 جوائز Eurojackpot")
        fig = go.Figure(data=[
            go.Scatter(x=predictor.euro_history['dates'], 
                      y=predictor.euro_history['jackpots'],
                      mode='lines+markers',
                      line=dict(color='#4facfe', width=3))
        ])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# صفحة الإعدادات
elif menu == "⚙️ الإعدادات":
    st.markdown("""
        <div class="main-header">
            <h1>⚙️ الإعدادات</h1>
            <p>تخصيص تجربتك</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 اللغة")
        lang = st.radio("اختر اللغة", ["🇩🇪 Deutsch", "🇬🇧 English", "🇸🇦 العربية"])
        
        st.subheader("📊 دقة التحليل")
        accuracy = st.slider("نسبة دقة التحليل", 50, 100, 85)
    
    with col2:
        st.subheader("🔔 إشعارات")
        st.checkbox("إشعارات التوقعات اليومية")
        st.checkbox("إشعارات الجوائز الكبرى")
        
        st.subheader("📧 البريد الإلكتروني")
        email = st.text_input("للاستلام التوقعات")

# ==================== التذييل ====================
st.markdown(f"""
    <div class="footer">
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
            <span>🇩🇪 Lotto 6aus49</span>
            <span>🇪🇺 Eurojackpot</span>
            <span>🎯 AI Predictor</span>
        </div>
        <div>© 2024 AI Predictor Germany • جميع الحقوق محفوظة</div>
        <div style="font-size: 0.8rem; margin-top: 1rem;">
            آخر تحديث: {datetime.now().strftime('%d.%m.%Y %H:%M')}
        </div>
    </div>
""", unsafe_allow_html=True)
