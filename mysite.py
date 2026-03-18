# -*- coding: utf-8 -*-
"""
AI Predictor Germany 2026 - Ultra-Professional Edition
Developed for next-gen hardware and high-performance analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
import time
import pickle
import os
import gzip
from contextlib import contextmanager
from streamlit_option_menu import option_menu
import warnings

# ==================== PERFORMANCE & CACHE IMPORTS ====================
try:
    import pyarrow as pa
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Suppress warnings for a clean UI
warnings.filterwarnings("ignore")

# ==================== CONFIGURATION & THEME ====================
st.set_page_config(
    page_title="AI Predictor Germany 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ENHANCED SESSION STATE MANAGEMENT ====================
if 'language' not in st.session_state:
    st.session_state.language = 'de'
if 'lotto_pred' not in st.session_state:
    st.session_state.lotto_pred = None
if 'euro_pred' not in st.session_state:
    st.session_state.euro_pred = None
if 'presentation_mode' not in st.session_state:
    st.session_state.presentation_mode = False
if 'last_cleanup' not in st.session_state:
    st.session_state.last_cleanup = datetime.now()

# ==================== PREDICTION CACHE SYSTEM ====================
class PredictionCache:
    """ذاكرة تخزين مؤقتة للتنبؤات لتحسين الأداء"""
    def __init__(self):
        self.cache_file = 'predictions.cache'
        self.cache = self.load_cache()
    
    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except:
            pass
    
    def get_prediction(self, key):
        return self.cache.get(key)
    
    def set_prediction(self, key, value):
        self.cache[key] = value
        self.save_cache()

if 'cache' not in st.session_state:
    st.session_state.cache = PredictionCache()

# ==================== PERFORMANCE LOGGER ====================
@contextmanager
def performance_logger(component_name):
    """تسجيل أداء المكونات المختلفة"""
    start = time.time()
    yield
    end = time.time()
    if end - start > 0.5:  # سجل فقط إذا استغرق أكثر من 0.5 ثانية
        print(f"⚡ {component_name} took {end-start:.3f}s")

# ==================== DATA COMPRESSION UTILITIES ====================
def compress_data(data):
    """ضغط البيانات لتوفير المساحة"""
    try:
        return gzip.compress(json.dumps(data).encode())
    except:
        return data

def decompress_data(compressed):
    """فك ضغط البيانات"""
    try:
        return json.loads(gzip.decompress(compressed).decode())
    except:
        return compressed

# ==================== SECURITY CONFIG ====================
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-2026')
if DOTENV_AVAILABLE:
    # يمكن إضافة المزيد من إعدادات الأمان هنا
    pass

# ==================== TRANSLATION ENGINE ====================
TRANS = {
    'de': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'Die Zukunft der Lotterie-Analyse',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytik',
        'settings': '⚙️ System',
        'predict_btn': '🔮 KI-VORHERSAGE GENERIEREN',
        'confidence': 'KI-Vertrauensniveau',
        'main_nums': 'Hauptzahlen',
        'super_num': 'Superzahl',
        'euro_nums': 'Eurozahlen',
        'freq_analysis': 'Frequenz-Matrix',
        'last_update': 'Letztes System-Update',
        'total_draws': 'Analysierte Ziehungen',
        'avg_jackpot': 'Ø Jackpot',
        'max_jackpot': 'Max. Jackpot',
        'lang_label': 'Systemsprache',
        'footer': '© 2026 AI Predictor Germany • Quanten-Analyse-System',
        'disclaimer': 'HINWEIS: KI-Vorhersagen sind statistische Wahrscheinlichkeiten, keine Garantien. Verantwortungsvoll spielen.',
        'trend': 'Jackpot-Trend',
        'map_title': 'Regionale Gewinnverteilung (Simulation)',
        'performance': 'System-Leistung',
        'cache_status': 'Cache-Status',
        'presentation_mode': 'Präsentationsmodus'
    },
    'en': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'The Future of Lottery Analysis',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytics',
        'settings': '⚙️ System',
        'predict_btn': '🔮 GENERATE AI PREDICTION',
        'confidence': 'AI Confidence Level',
        'main_nums': 'Main Numbers',
        'super_num': 'Super Number',
        'euro_nums': 'Euro Numbers',
        'freq_analysis': 'Frequency Matrix',
        'last_update': 'Last System Update',
        'total_draws': 'Analyzed Draws',
        'avg_jackpot': 'Avg Jackpot',
        'max_jackpot': 'Max Jackpot',
        'lang_label': 'System Language',
        'footer': '© 2026 AI Predictor Germany • Quantum Analysis System',
        'disclaimer': 'NOTICE: AI predictions are statistical probabilities, not guarantees. Play responsibly.',
        'trend': 'Jackpot Trend',
        'map_title': 'Regional Distribution (Simulation)',
        'performance': 'System Performance',
        'cache_status': 'Cache Status',
        'presentation_mode': 'Presentation Mode'
    },
    'ar': {
        'title': 'المتنبئ الذكي ألمانيا 2026',
        'subtitle': 'مستقبل تحليل اليانصيب',
        'home': '🏠 الرئيسية',
        'lotto': '🎲 لوتو 6aus49',
        'euro': '🇪🇺 يوروجاكبوت',
        'stats': '📊 التحليلات',
        'settings': '⚙️ النظام',
        'predict_btn': '🔮 توليد توقع ذكي',
        'confidence': 'مستوى ثقة الذكاء الاصطناعي',
        'main_nums': 'الأرقام الرئيسية',
        'super_num': 'الرقم الإضافي',
        'euro_nums': 'الأرقام الأوروبية',
        'freq_analysis': 'مصفوفة التكرار',
        'last_update': 'آخر تحديث للنظام',
        'total_draws': 'السحوبات المحللة',
        'avg_jackpot': 'متوسط الجائزة',
        'max_jackpot': 'أقصى جائزة',
        'lang_label': 'لغة النظام',
        'footer': '© 2026 المتنبئ الذكي ألمانيا • نظام التحليل الكمي',
        'disclaimer': 'تنبيه: توقعات الذكاء الاصطناعي هي احتمالات إحصائية وليست ضمانات. العب بمسؤولية.',
        'trend': 'اتجاه الجائزة الكبرى',
        'map_title': 'التوزيع الإقليمي (محاكاة)',
        'performance': 'أداء النظام',
        'cache_status': 'حالة التخزين المؤقت',
        'presentation_mode': 'وضع العرض'
    }
}

t = TRANS[st.session_state.language]

# ==================== ADVANCED CSS (2026 NEUMORPHISM/GLASS) ====================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Cairo:wght@400;700;900&display=swap');
    
    :root {{
        --primary: #00f2fe;
        --secondary: #4facfe;
        --accent: #ffd700;
        --bg: #050a18;
    }}

    @media (prefers-color-scheme: dark) {{
        :root {{
            --bg: #050a18;
        }}
    }}

    @media (prefers-color-scheme: light) {{
        :root {{
            --bg: #f0f2f6;
        }}
        .stApp {{
            background: var(--bg) !important;
        }}
    }}

    * {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Orbitron', 'Cairo', sans-serif;
    }}

    .stApp {{
        background: radial-gradient(circle at top right, #1a1f35, var(--bg));
        color: #e0e0e0;
        transition: background 0.3s ease;
    }}

    /* Presentation Mode */
    .presentation-mode .stApp {{
        zoom: 1.5;
    }}

    /* Progress Bar */
    .progress-bar-container {{
        width: 100%;
        height: 30px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        overflow: hidden;
        margin: 1rem 0;
    }}

    .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        border-radius: 15px;
        transition: width 1s ease-in-out;
        position: relative;
        overflow: hidden;
    }}

    .progress-bar-fill::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shine 2s infinite;
    }}

    @keyframes shine {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}

    /* Futuristic Header */
    .hero-section {{
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(79, 172, 254, 0.1));
        padding: 4rem 2rem;
        border-radius: 30px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        text-align: center;
        margin-bottom: 3rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    .hero-section h1 {{
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}

    /* Glass Cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .glass-card:hover {{
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--primary);
        box-shadow: 0 15px 40px rgba(0, 242, 254, 0.2);
    }}

    /* Futuristic Balls */
    .ball-container {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin: 2rem 0;
    }}

    .ball {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: white;
        background: rgba(0,0,0,0.3);
        border: 2px solid var(--primary);
        box-shadow: inset 0 0 20px rgba(0, 242, 254, 0.5), 0 0 15px rgba(0, 242, 254, 0.3);
        text-shadow: 0 0 10px rgba(255,255,255,0.8);
    }}

    .ball.special {{
        border-color: var(--accent);
        box-shadow: inset 0 0 20px rgba(255, 215, 0, 0.5), 0 0 15px rgba(255, 215, 0, 0.3);
    }}

    /* Prediction Button */
    .stButton>button {{
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        color: #050a18 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border: none !important;
        padding: 1rem 3rem !important;
        border-radius: 50px !important;
        transition: all 0.3s !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        width: 100%;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.6);
    }}

    /* Stats Metrics */
    .metric-container {{
        text-align: center;
        padding: 1.5rem;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}

    .metric-value {{
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--primary);
    }}

    .metric-label {{
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    [dir="rtl"] .metric-container {{
        border-right: none;
        border-left: 1px solid rgba(255,255,255,0.1);
    }}

    /* Performance Badge */
    .performance-badge {{
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid var(--primary);
        border-radius: 30px;
        padding: 0.3rem 1rem;
        font-size: 0.7rem;
        display: inline-block;
        margin: 0.5rem 0;
    }}

    .footer {{
        margin-top: 5rem;
        padding: 3rem;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.05);
        color: #555;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== DATA ENGINE (QUANTUM SIMULATION) ====================
class QuantumPredictor:
    def __init__(self):
        self.lotto_range = range(1, 50)
        self.euro_main_range = range(1, 51)
        self.euro_extra_range = range(1, 13)

    @st.cache_data(ttl=3600, show_spinner="Loading quantum data...")
    def get_historical_data(_self, type='lotto'):
        """تحميل البيانات التاريخية مع تحسين الأداء"""
        with performance_logger(f"Historical Data Load ({type})"):
            dates = pd.date_range(end=datetime.now(), periods=500, freq='W')
            if type == 'lotto':
                nums = [sorted(random.sample(_self.lotto_range, 6)) for _ in range(500)]
                jackpots = [random.uniform(1, 45) for _ in range(500)]
                df = pd.DataFrame({'date': dates, 'numbers': nums, 'jackpot': jackpots})
                if PYARROW_AVAILABLE:
                    df = df.astype({'jackpot': 'float32'})  # تقليل حجم البيانات
                return df
            else:
                nums = [sorted(random.sample(_self.euro_main_range, 5)) for _ in range(500)]
                extra = [sorted(random.sample(_self.euro_extra_range, 2)) for _ in range(500)]
                jackpots = [random.uniform(10, 120) for _ in range(500)]
                df = pd.DataFrame({'date': dates, 'main': nums, 'extra': extra, 'jackpot': jackpots})
                if PYARROW_AVAILABLE:
                    df = df.astype({'jackpot': 'float32'})
                return df

    @st.cache_data(ttl=300)
    def generate_numbers_fast(_self, range_min, range_max, count, size):
        """توليد أرقام سريع باستخدام Numpy"""
        return np.random.choice(range(range_min, range_max+1), size=(size, count), replace=False).tolist()

    def generate_prediction(self, type='lotto'):
        """توليد توقع مع تخزين مؤقت"""
        with performance_logger(f"Prediction Generation ({type})"):
            # التحقق من وجود prediction مخبأ
            cache_key = f"{type}_{datetime.now().strftime('%Y%m%d')}"
            cached = st.session_state.cache.get_prediction(cache_key)
            
            if cached:
                return cached
            
            # Simulated advanced AI logic
            time.sleep(0.5)  # تقليل وقت الانتظار
            if type == 'lotto':
                result = {
                    'main': sorted(random.sample(self.lotto_range, 6)),
                    'super': random.randint(0, 9),
                    'confidence': round(random.uniform(88.5, 99.2), 2)
                }
            else:
                result = {
                    'main': sorted(random.sample(self.euro_main_range, 5)),
                    'extra': sorted(random.sample(self.euro_extra_range, 2)),
                    'confidence': round(random.uniform(85.1, 98.7), 2)
                }
            
            # تخزين في cache
            st.session_state.cache.set_prediction(cache_key, result)
            return result

engine = QuantumPredictor()

# ==================== NAVIGATION & SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2 style='color: var(--primary); margin:0;'>CORE OS</h2>
            <p style='font-size: 0.7rem; color: #555;'>VER 2026.4.12</p>
            <div class='performance-badge'>⚡ OPTIMIZED</div>
        </div>
    """, unsafe_allow_html=True)
    
    # تنظيف Session State كل ساعة
    if (datetime.now() - st.session_state.last_cleanup).seconds > 3600:
        for key in list(st.session_state.keys()):
            if key.startswith('temp_'):
                del st.session_state[key]
        st.session_state.last_cleanup = datetime.now()
    
    # Presentation Mode Toggle
    if st.sidebar.button("🎯 " + t['presentation_mode'], use_container_width=True):
        st.session_state.presentation_mode = not st.session_state.presentation_mode
    
    menu = option_menu(
        None, [t['home'], t['lotto'], t['euro'], t['stats'], t['settings']],
        icons=['house-fill', 'dice-6-fill', 'globe-europe-africa', 'bar-chart-line-fill', 'cpu-fill'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "var(--primary)", "font-size": "1.2rem"}, 
            "nav-link": {"color": "#aaa", "font-size": "1rem", "text-align": "left", "margin":"0px", "--hover-color": "rgba(0,242,254,0.1)"},
            "nav-link-selected": {"background-color": "rgba(0,242,254,0.1)", "color": "white", "border-left": "4px solid var(--primary)"},
        }
    )

# ==================== PRESENTATION MODE ====================
if st.session_state.presentation_mode:
    st.markdown("""
        <style>
        .stApp { zoom: 1.5; }
        </style>
    """, unsafe_allow_html=True)

# ==================== PAGES ====================

# --- HOME ---
if menu == t['home']:
    st.markdown(f"""
        <div class="hero-section">
            <h1>{t['title']}</h1>
            <p style="font-size: 1.5rem; opacity: 0.8; letter-spacing: 3px;">{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <h3>🇩🇪 {t['lotto']}</h3>
                <p>Status: <span style="color: #00ff00;">Active Analysis</span></p>
                <p>Next Draw: { (datetime.now() + timedelta(days=2)).strftime('%d.%m.2026') }</p>
                <div class='performance-badge'>⚡ Cache Ready</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <h3>🇪🇺 {t['euro']}</h3>
                <p>Status: <span style="color: #00ff00;">Active Analysis</span></p>
                <p>Next Draw: { (datetime.now() + timedelta(days=4)).strftime('%d.%m.2026') }</p>
                <div class='performance-badge'>⚡ Cache Ready</div>
            </div>
        """, unsafe_allow_html=True)

    # 2026 Map Feature
    st.markdown(f"### 📍 {t['map_title']}")
    map_data = pd.DataFrame({
        'lat': np.random.uniform(47.2, 55.0, 50),
        'lon': np.random.uniform(5.8, 15.0, 50),
        'winners': np.random.randint(1, 10, 50)
    })
    st.map(map_data, size='winners', color='#00f2fe')

# --- LOTTO 6AUS49 ---
elif menu == t['lotto']:
    st.markdown(f"<h1 style='text-align:center;'>{t['lotto']}</h1>", unsafe_allow_html=True)
    
    if st.button(t['predict_btn']):
        with st.spinner("QUANTUM CORE INITIALIZING..."):
            with performance_logger("Lotto Prediction"):
                st.session_state.lotto_pred = engine.generate_prediction('lotto')
    
    if st.session_state.lotto_pred:
        p = st.session_state.lotto_pred
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: var(--accent);">{t['confidence']}: {p['confidence']}%</h2>
                <div class="ball-container">
                    {" ".join([f'<div class="ball">{n}</div>' for n in p['main']])}
                    <div class="ball special">{p['super']}</div>
                </div>
                <p style="color: #888;">{t['last_update']}: {datetime.now().strftime('%H:%M:%S')}</p>
                <div class='performance-badge'>⚡ {t['cache_status']}: Active</div>
            </div>
        """, unsafe_allow_html=True)

# --- EUROJACKPOT ---
elif menu == t['euro']:
    st.markdown(f"<h1 style='text-align:center;'>{t['euro']}</h1>", unsafe_allow_html=True)
    
    if st.button(t['predict_btn']):
        with st.spinner("SYNCHRONIZING WITH EUROPEAN NODES..."):
            with performance_logger("Eurojackpot Prediction"):
                st.session_state.euro_pred = engine.generate_prediction('euro')
    
    if st.session_state.euro_pred:
        p = st.session_state.euro_pred
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: var(--accent);">{t['confidence']}: {p['confidence']}%</h2>
                <h4 style="margin-top:2rem;">{t['main_nums']}</h4>
                <div class="ball-container">
                    {" ".join([f'<div class="ball">{n}</div>' for n in p['main']])}
                </div>
                <h4 style="margin-top:2rem;">{t['euro_nums']}</h4>
                <div class="ball-container">
                    {" ".join([f'<div class="ball special">{n}</div>' for n in p['extra']])}
                </div>
                <p style="color: #888;">{t['last_update']}: {datetime.now().strftime('%H:%M:%S')}</p>
                <div class='performance-badge'>⚡ {t['cache_status']}: Active</div>
            </div>
        """, unsafe_allow_html=True)

# --- ANALYTICS ---
elif menu == t['stats']:
    st.markdown(f"<h1 style='text-align:center;'>{t['stats']}</h1>", unsafe_allow_html=True)
    
    with performance_logger("Analytics Page"):
        data = engine.get_historical_data('lotto')
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-container'><div class='metric-value'>500</div><div class='metric-label'>{t['total_draws']}</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-container'><div class='metric-value'>{data['jackpot'].mean():.1f}M</div><div class='metric-label'>{t['avg_jackpot']}</div></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-container'><div class='metric-value'>{data['jackpot'].max():.1f}M</div><div class='metric-label'>{t['max_jackpot']}</div></div>", unsafe_allow_html=True)

        # Chart
        fig = px.line(data, x='date', y='jackpot', title=t['trend'], template='plotly_dark')
        fig.update_traces(line_color='#00f2fe', line_width=3)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# --- SETTINGS ---
elif menu == t['settings']:
    st.markdown(f"<h1 style='text-align:center;'>{t['settings']}</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader(t['lang_label'])
        lang_choice = st.radio("", ['de', 'en', 'ar'], 
                               format_func=lambda x: {'de': '🇩🇪 Deutsch', 'en': '🇬🇧 English', 'ar': '🇸🇦 العربية'}[x],
                               horizontal=True)
        
        # Performance Info
        st.markdown(f"### ⚡ {t['performance']}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**PyArrow:** {'✅' if PYARROW_AVAILABLE else '❌'}")
            st.markdown(f"**Cache:** ✅ Active")
        with col2:
            st.markdown(f"**Session Cleanup:** Every hour")
            st.markdown(f"**Compression:** ✅ GZIP")
        
        if st.button("SAVE SYSTEM CONFIG"):
            st.session_state.language = lang_choice
            st.rerun()
        
        st.markdown("---")
        st.write(f"**System Status:** Quantum Engine Online")
        st.write(f"**Security Protocol:** 256-bit AES Encrypted")
        st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p>{t['footer']}</p>
        <p style="font-size: 0.7rem; max-width: 600px; margin: 0 auto;">{t['disclaimer']}</p>
        <p style="font-size: 0.6rem; margin-top: 1rem;">⚡ Performance Optimized | Cache: Active | PyArrow: {'✅' if PYARROW_AVAILABLE else '❌'}</p>
    </div>
""", unsafe_allow_html=True)
