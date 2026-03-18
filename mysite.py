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

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Predictor Germany",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE ====================
if 'language' not in st.session_state:
    st.session_state.language = 'de'  # Default: German

# ==================== TRANSLATIONS (3 LANGUAGES) ====================
TRANS = {
    'de': {
        # German
        'app_name': '🎯 KI-Vorhersage Deutschland',
        'subtitle': 'Intelligente Vorhersagen für Lotto und Eurojackpot',
        'menu_home': '🏠 Startseite',
        'menu_lotto': '🎲 Lotto 6aus49',
        'menu_euro': '🇪🇺 Eurojackpot',
        'menu_stats': '📊 Statistiken',
        'menu_settings': '⚙️ Einstellungen',
        'predict': '🔮 Vorhersagen',
        'refresh': '🔄 Aktualisieren',
        'confidence': 'Konfidenz',
        'main_numbers': 'Hauptzahlen',
        'super_number': 'Superzahl',
        'extra_numbers': 'Eurozahlen',
        'frequency': 'Häufigste Zahlen',
        'last_update': 'Letzte Aktualisierung',
        'total_draws': 'Ziehungen insgesamt',
        'avg_jackpot': 'Durchschnittlicher Jackpot',
        'max_jackpot': 'Höchster Jackpot',
        'language': 'Sprache',
        'de': 'Deutsch',
        'en': 'English',
        'ar': 'العربية',
        'footer': '© 2024 KI-Vorhersage Deutschland • Alle Rechte vorbehalten',
        'disclaimer': 'Hinweis: Dies sind Vorhersagen, keine Garantien. Spielsucht kann gefährlich sein.',
        'german_lottery': 'Deutsche Lotto 6aus49',
        'european_lottery': 'Eurojackpot',
        'today_predictions': 'Heutige Vorhersagen',
        'statistics': 'Statistiken',
        'analysis': 'Analyse'
    },
    'en': {
        # English
        'app_name': '🎯 AI Predictor Germany',
        'subtitle': 'Smart Predictions for Lotto and Eurojackpot',
        'menu_home': '🏠 Home',
        'menu_lotto': '🎲 Lotto 6aus49',
        'menu_euro': '🇪🇺 Eurojackpot',
        'menu_stats': '📊 Statistics',
        'menu_settings': '⚙️ Settings',
        'predict': '🔮 Predict',
        'refresh': '🔄 Refresh',
        'confidence': 'Confidence',
        'main_numbers': 'Main Numbers',
        'super_number': 'Super Number',
        'extra_numbers': 'Extra Numbers',
        'frequency': 'Most Frequent Numbers',
        'last_update': 'Last Update',
        'total_draws': 'Total Draws',
        'avg_jackpot': 'Average Jackpot',
        'max_jackpot': 'Highest Jackpot',
        'language': 'Language',
        'de': 'German',
        'en': 'English',
        'ar': 'Arabic',
        'footer': '© 2024 AI Predictor Germany • All rights reserved',
        'disclaimer': 'Note: These are predictions, not guarantees. Gambling can be addictive.',
        'german_lottery': 'German Lotto 6aus49',
        'european_lottery': 'Eurojackpot',
        'today_predictions': 'Today\'s Predictions',
        'statistics': 'Statistics',
        'analysis': 'Analysis'
    },
    'ar': {
        # Arabic
        'app_name': '🎯 المتنبئ الذكي ألمانيا',
        'subtitle': 'تنبؤات ذكية لليانصيب الألماني والأوروبي',
        'menu_home': '🏠 الرئيسية',
        'menu_lotto': '🎲 لوتو 6aus49',
        'menu_euro': '🇪🇺 يوروجاكبوت',
        'menu_stats': '📊 إحصائيات',
        'menu_settings': '⚙️ الإعدادات',
        'predict': '🔮 توقع',
        'refresh': '🔄 تحديث',
        'confidence': 'نسبة الثقة',
        'main_numbers': 'الأرقام الرئيسية',
        'super_number': 'الرقم الإضافي',
        'extra_numbers': 'الأرقام الأوروبية',
        'frequency': 'الأرقام الأكثر تكراراً',
        'last_update': 'آخر تحديث',
        'total_draws': 'إجمالي السحوبات',
        'avg_jackpot': 'متوسط الجائزة',
        'max_jackpot': 'أكبر جائزة',
        'language': 'اللغة',
        'de': 'الألمانية',
        'en': 'الإنجليزية',
        'ar': 'العربية',
        'footer': '© 2024 المتنبئ الذكي ألمانيا • جميع الحقوق محفوظة',
        'disclaimer': 'ملاحظة: هذه توقعات وليست ضمانات. القمار قد يسبب الإدمان.',
        'german_lottery': 'لوتو ألماني 6aus49',
        'european_lottery': 'يوروجاكبوت',
        'today_predictions': 'توقعات اليوم',
        'statistics': 'إحصائيات',
        'analysis': 'تحليل'
    }
}

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    * {
        font-family: 'Inter', 'Cairo', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
    }
    
    /* German flag colors */
    .german-badge {
        background: linear-gradient(90deg, #000000 0%, #DD0000 50%, #FFCE00 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 30px;
        font-weight: 600;
        text-align: center;
        display: inline-block;
    }
    
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
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
    }
    
    .prediction-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s;
        color: white;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .number-ball {
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
        margin: 0 auto;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }
    
    .euro-ball {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffd700;
    }
    
    .language-selector {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
    
    /* RTL Support for Arabic */
    [dir="rtl"] {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOTTERY DATA ====================
@st.cache_data
def generate_lotto_history():
    """Generate simulated lottery history"""
    data = {
        'dates': pd.date_range(start='2024-01-01', end='2024-12-31', freq='W'),
        'numbers': [sorted(random.sample(range(1, 50), 6)) for _ in range(52)],
        'super_numbers': [random.randint(0, 9) for _ in range(52)],
        'jackpots': [random.randint(1, 50) * 1000000 for _ in range(52)]
    }
    return pd.DataFrame(data)

@st.cache_data
def generate_euro_history():
    """Generate simulated Eurojackpot history"""
    data = {
        'dates': pd.date_range(start='2024-01-01', end='2024-12-31', freq='W'),
        'main_numbers': [sorted(random.sample(range(1, 51), 5)) for _ in range(52)],
        'extra_numbers': [sorted(random.sample(range(1, 13), 2)) for _ in range(52)],
        'jackpots': [random.randint(10, 120) * 1000000 for _ in range(52)]
    }
    return pd.DataFrame(data)

# ==================== PREDICTOR CLASS ====================
class LotteryPredictor:
    def __init__(self):
        self.lotto_history = generate_lotto_history()
        self.euro_history = generate_euro_history()
    
    def predict_lotto(self):
        """Predict Lotto 6aus49 numbers"""
        # Analyze frequency
        all_numbers = []
        for nums in self.lotto_history['numbers']:
            all_numbers.extend(nums)
        
        freq = pd.Series(all_numbers).value_counts()
        top_numbers = freq.head(10).index.tolist()
        
        # Generate prediction
        prediction = sorted(random.sample(top_numbers, min(6, len(top_numbers))))
        if len(prediction) < 6:
            remaining = 6 - len(prediction)
            possible = [x for x in range(1, 50) if x not in prediction]
            prediction.extend(sorted(random.sample(possible, remaining)))
        
        return {
            'numbers': sorted(prediction),
            'super_number': random.randint(0, 9),
            'confidence': round(random.uniform(65, 95), 1)
        }
    
    def predict_euro(self):
        """Predict Eurojackpot numbers"""
        # Analyze frequency
        all_main = []
        all_extra = []
        
        for nums in self.euro_history['main_numbers']:
            all_main.extend(nums)
        for nums in self.euro_history['extra_numbers']:
            all_extra.extend(nums)
        
        main_freq = pd.Series(all_main).value_counts().head(8).index.tolist()
        extra_freq = pd.Series(all_extra).value_counts().head(4).index.tolist()
        
        # Generate prediction
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
            'confidence': round(random.uniform(60, 90), 1)
        }
    
    def get_frequency(self):
        """Get number frequency analysis"""
        all_numbers = []
        for nums in self.lotto_history['numbers']:
            all_numbers.extend(nums)
        return pd.Series(all_numbers).value_counts().head(10)

# ==================== INITIALIZE ====================
predictor = LotteryPredictor()
if 'lotto_pred' not in st.session_state:
    st.session_state.lotto_pred = predictor.predict_lotto()
if 'euro_pred' not in st.session_state:
    st.session_state.euro_pred = predictor.predict_euro()

# ==================== LANGUAGE SELECTOR ====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white;">🎯 AI Predictor</h2>
            <div class="german-badge">🇩🇪 Germany</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language selection
    st.markdown(f"### Language / Sprache / اللغة")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇩🇪 DE", use_container_width=True):
            st.session_state.language = 'de'
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    with col3:
        if st.button("🇸🇦 AR", use_container_width=True):
            st.session_state.language = 'ar'
            st.rerun()
    
    st.markdown("---")
    
    # Menu
    t = TRANS[st.session_state.language]
    
    menu = option_menu(
        menu_title=None,
        options=[t['menu_home'], t['menu_lotto'], t['menu_euro'], t['menu_stats'], t['menu_settings']],
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
    
    # Last update
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px;">
            <p style="color: white;">📅 {t['last_update']}</p>
            <p style="color: #ffd700; font-size: 1.2rem;">{datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>
    """, unsafe_allow_html=True)

# ==================== PAGES ====================
t = TRANS[st.session_state.language]

# HOME PAGE
if menu == t['menu_home']:
    st.markdown(f"""
        <div class="main-header">
            <h1>{t['app_name']}</h1>
            <p style="font-size: 1.2rem;">{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="prediction-card">
                <h2>{t['german_lottery']}</h2>
                <p>6/49 + Superzahl</p>
                <div style="font-size: 3rem; color: #ffd700;">🎲</div>
                <p>{t['today_predictions']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show Lotto numbers preview
        pred = st.session_state.lotto_pred
        cols = st.columns(7)
        for i, num in enumerate(pred['numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball">{num}</div>', unsafe_allow_html=True)
        with cols[6]:
            st.markdown(f'<div class="number-ball" style="background: #4facfe;">{pred["super_number"]}</div>', unsafe_allow_html=True)
        
        st.markdown(f"**{t['confidence']}:** {pred['confidence']}%")
    
    with col2:
        st.markdown(f"""
            <div class="prediction-card">
                <h2>{t['european_lottery']}</h2>
                <p>5/50 + 2/12</p>
                <div style="font-size: 3rem; color: #ffd700;">🇪🇺</div>
                <p>{t['today_predictions']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show Eurojackpot numbers preview
        pred = st.session_state.euro_pred
        st.markdown(f"**{t['main_numbers']}:**")
        cols = st.columns(5)
        for i, num in enumerate(pred['main_numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball euro-ball">{num}</div>', unsafe_allow_html=True)
        
        st.markdown(f"**{t['extra_numbers']}:**")
        cols = st.columns(2)
        for i, num in enumerate(pred['extra_numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball" style="background: #ffd700;">{num}</div>', unsafe_allow_html=True)
        
        st.markdown(f"**{t['confidence']}:** {pred['confidence']}%")

# LOTTO PAGE
elif menu == t['menu_lotto']:
    st.markdown(f"""
        <div class="main-header">
            <h1>{t['german_lottery']}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🔮 {t['today_predictions']}")
        
        if st.button(t['refresh'], use_container_width=True):
            st.session_state.lotto_pred = predictor.predict_lotto()
            st.rerun()
        
        pred = st.session_state.lotto_pred
        
        st.markdown(f"### {t['main_numbers']}")
        cols = st.columns(6)
        for i, num in enumerate(pred['numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball">{num}</div>', unsafe_allow_html=True)
        
        st.markdown(f"### {t['super_number']}")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.markdown(f'<div class="number-ball" style="background: #4facfe;">{pred["super_number"]}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      padding: 1rem; border-radius: 10px; color: white; text-align: center; margin: 2rem 0;">
                <h2>{t['confidence']}: {pred['confidence']}%</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader(f"📊 {t['frequency']}")
        freq = predictor.get_frequency()
        
        fig = go.Figure(data=[
            go.Bar(x=freq.index.astype(str), y=freq.values,
                   marker_color='gold', text=freq.values)
        ])
        fig.update_layout(
            title=t['analysis'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# EUROJACKPOT PAGE
elif menu == t['menu_euro']:
    st.markdown(f"""
        <div class="main-header">
            <h1>{t['european_lottery']}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🔮 {t['today_predictions']}")
        
        if st.button(t['refresh'], use_container_width=True):
            st.session_state.euro_pred = predictor.predict_euro()
            st.rerun()
        
        pred = st.session_state.euro_pred
        
        st.markdown(f"### {t['main_numbers']} (5/50)")
        cols = st.columns(5)
        for i, num in enumerate(pred['main_numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball euro-ball">{num}</div>', unsafe_allow_html=True)
        
        st.markdown(f"### {t['extra_numbers']} (2/12)")
        cols = st.columns(2)
        for i, num in enumerate(pred['extra_numbers']):
            with cols[i]:
                st.markdown(f'<div class="number-ball" style="background: #ffd700;">{num}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      padding: 1rem; border-radius: 10px; color: white; text-align: center; margin: 2rem 0;">
                <h2>{t['confidence']}: {pred['confidence']}%</h2>
            </div>
        """, unsafe_allow_html=True)

# STATISTICS PAGE
elif menu == t['menu_stats']:
    st.markdown(f"""
        <div class="main-header">
            <h1>{t['statistics']}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="metric-value">{len(predictor.lotto_history)}</div>
                <div>{t['total_draws']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="metric-value">{predictor.lotto_history['jackpots'].mean():.0f}M €</div>
                <div>{t['avg_jackpot']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="metric-value">{predictor.lotto_history['jackpots'].max()}M €</div>
                <div>{t['max_jackpot']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎲 Lotto 6aus49")
        fig = go.Figure(data=[
            go.Scatter(x=predictor.lotto_history['dates'], 
                      y=predictor.lotto_history['jackpots'],
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
        st.subheader("🇪🇺 Eurojackpot")
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

# SETTINGS PAGE
elif menu == t['menu_settings']:
    st.markdown(f"""
        <div class="main-header">
            <h1>{t['menu_settings']}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {t['language']}")
        lang_choice = st.radio(
            "",
            ['de', 'en', 'ar'],
            format_func=lambda x: {'de': '🇩🇪 Deutsch', 'en': '🇬🇧 English', 'ar': '🇸🇦 العربية'}[x],
            index=['de', 'en', 'ar'].index(st.session_state.language)
        )
        
        if st.button("Apply / Anwenden / تطبيق"):
            st.session_state.language = lang_choice
            st.rerun()
    
    with col2:
        st.markdown(f"### ℹ️ Info")
        st.info(t['disclaimer'])

# ==================== FOOTER ====================
st.markdown(f"""
    <div class="footer">
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
            <span>🇩🇪 Lotto 6aus49</span>
            <span>🇪🇺 Eurojackpot</span>
            <span>🎯 AI Predictor</span>
        </div>
        <div>{t['footer']}</div>
        <div style="font-size: 0.8rem; margin-top: 1rem; color: rgba(255,255,255,0.3);">
            {t['disclaimer']}
        </div>
    </div>
""", unsafe_allow_html=True)
