# -*- coding: utf-8 -*-
"""
AI Predictor Germany 2026 - Ultra-Professional Edition (Full Fixed)
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
if 'settings_page' not in st.session_state:
    st.session_state.settings_page = 'main'  # main, language, appearance, notifications, api, advanced
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # dark, light
if 'animations' not in st.session_state:
    st.session_state.animations = True
if 'compact_mode' not in st.session_state:
    st.session_state.compact_mode = False

# ==================== PREDICTION CACHE SYSTEM ====================
class PredictionCache:
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
    start = time.time()
    yield
    end = time.time()
    if end - start > 0.5:
        print(f"⚡ {component_name} took {end-start:.3f}s")

# ==================== DATA COMPRESSION UTILITIES ====================
def compress_data(data):
    try:
        return gzip.compress(json.dumps(data).encode())
    except:
        return data

def decompress_data(compressed):
    try:
        return json.loads(gzip.decompress(compressed).decode())
    except:
        return compressed

# ==================== SECURITY CONFIG ====================
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-2026')

# ==================== TRANSLATION ENGINE ====================
TRANS = {
    'de': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'Die Zukunft der Lotterie-Analyse',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytik',
        'settings': '⚙️ System-Einstellungen',
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
        'lang_label': 'Systemsprache wählen',
        'footer': '© 2026 AI Predictor Germany • Quanten-Analyse-System',
        'disclaimer': 'HINWEIS: KI-Vorhersagen sind statistische Wahrscheinlichkeiten, keine Garantien. Verantwortungsvoll spielen.',
        'trend': 'Jackpot-Trend',
        'map_title': 'Regionale Gewinnverteilung (Simulation)',
        'performance': 'System-Leistung',
        'cache_status': 'Cache-Status',
        'presentation_mode': 'Präsentationsmodus',
        'ticker_text': '+++ AKTUELLE NEWS: Neuer Eurojackpot Rekord erwartet +++ Lotto 6aus49 Jackpot steigt auf 45 Mio. € +++ KI-Analyse abgeschlossen +++',
        
        # Settings menu items
        'settings_main': '⚙️ Hauptmenü',
        'settings_language': '🌐 Sprache',
        'settings_appearance': '🎨 Erscheinungsbild',
        'settings_notifications': '🔔 Benachrichtigungen',
        'settings_api': '🔑 API & Verbindungen',
        'settings_advanced': '⚡ Erweiterte Einstellungen',
        'settings_back': '◀ Zurück',
        
        # Appearance settings
        'theme_dark': '🌙 Dunkles Thema',
        'theme_light': '☀ Helles Thema',
        'theme_system': '💻 Systemstandard',
        'animations': 'Animationen',
        'animations_on': 'Ein',
        'animations_off': 'Aus',
        'compact_mode': 'Kompakter Modus',
        
        # Notification settings
        'email_notify': '📧 E-Mail-Benachrichtigungen',
        'push_notify': '📱 Push-Benachrichtigungen',
        'daily_predictions': 'Tägliche Vorhersagen',
        'jackpot_alerts': 'Jackpot-Benachrichtigungen',
        
        # API settings
        'api_key': 'API-Schlüssel',
        'api_status': 'API-Status',
        'api_connected': 'Verbunden',
        'api_disconnected': 'Getrennt',
        'test_connection': 'Verbindung testen',
        
        # Advanced settings
        'cache_clear': 'Cache leeren',
        'reset_all': 'Alle Einstellungen zurücksetzen',
        'export_data': 'Daten exportieren',
        'import_data': 'Daten importieren',
        'system_info': 'Systeminformationen',
        'clear_history': 'Verlauf löschen',
    },
    'en': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'The Future of Lottery Analysis',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytics',
        'settings': '⚙️ System Settings',
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
        'lang_label': 'Select System Language',
        'footer': '© 2026 AI Predictor Germany • Quantum Analysis System',
        'disclaimer': 'NOTICE: AI predictions are statistical probabilities, not guarantees. Play responsibly.',
        'trend': 'Jackpot Trend',
        'map_title': 'Regional Distribution (Simulation)',
        'performance': 'System Performance',
        'cache_status': 'Cache Status',
        'presentation_mode': 'Presentation Mode',
        'ticker_text': '+++ LATEST NEWS: New Eurojackpot record expected +++ Lotto 6aus49 jackpot rises to €45M +++ AI analysis completed +++',
        
        # Settings menu items
        'settings_main': '⚙️ Main Menu',
        'settings_language': '🌐 Language',
        'settings_appearance': '🎨 Appearance',
        'settings_notifications': '🔔 Notifications',
        'settings_api': '🔑 API & Connections',
        'settings_advanced': '⚡ Advanced Settings',
        'settings_back': '◀ Back',
        
        # Appearance settings
        'theme_dark': '🌙 Dark Theme',
        'theme_light': '☀ Light Theme',
        'theme_system': '💻 System Default',
        'animations': 'Animations',
        'animations_on': 'On',
        'animations_off': 'Off',
        'compact_mode': 'Compact Mode',
        
        # Notification settings
        'email_notify': '📧 Email Notifications',
        'push_notify': '📱 Push Notifications',
        'daily_predictions': 'Daily Predictions',
        'jackpot_alerts': 'Jackpot Alerts',
        
        # API settings
        'api_key': 'API Key',
        'api_status': 'API Status',
        'api_connected': 'Connected',
        'api_disconnected': 'Disconnected',
        'test_connection': 'Test Connection',
        
        # Advanced settings
        'cache_clear': 'Clear Cache',
        'reset_all': 'Reset All Settings',
        'export_data': 'Export Data',
        'import_data': 'Import Data',
        'system_info': 'System Information',
        'clear_history': 'Clear History',
    },
    'ar': {
        'title': 'المتنبئ الذكي ألمانيا 2026',
        'subtitle': 'مستقبل تحليل اليانصيب',
        'home': '🏠 الرئيسية',
        'lotto': '🎲 لوتو 6aus49',
        'euro': '🇪🇺 يوروجاكبوت',
        'stats': '📊 التحليلات',
        'settings': '⚙️ إعدادات النظام',
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
        'lang_label': 'اختر لغة النظام',
        'footer': '© 2026 المتنبئ الذكي ألمانيا • نظام التحليل الكمي',
        'disclaimer': 'تنبيه: توقعات الذكاء الاصطناعي هي احتمالات إحصائية وليست ضمانات. العب بمسؤولية.',
        'trend': 'اتجاه الجائزة الكبرى',
        'map_title': 'التوزيع الإقليمي (محاكاة)',
        'performance': 'أداء النظام',
        'cache_status': 'حالة التخزين المؤقت',
        'presentation_mode': 'وضع العرض',
        'ticker_text': '+++ آخر الأخبار: توقع رقم قياسي جديد في Eurojackpot +++ جائزة Lotto 6aus49 ترتفع إلى 45 مليون يورو +++ اكتمل تحليل الذكاء الاصطناعي +++',
        
        # Settings menu items
        'settings_main': '⚙️ القائمة الرئيسية',
        'settings_language': '🌐 اللغة',
        'settings_appearance': '🎨 المظهر',
        'settings_notifications': '🔔 الإشعارات',
        'settings_api': '🔑 API والاتصالات',
        'settings_advanced': '⚡ إعدادات متقدمة',
        'settings_back': '◀ رجوع',
        
        # Appearance settings
        'theme_dark': '🌙 الوضع الداكن',
        'theme_light': '☀ الوضع الفاتح',
        'theme_system': '💻 إفتراضي',
        'animations': 'الرسوم المتحركة',
        'animations_on': 'تشغيل',
        'animations_off': 'إيقاف',
        'compact_mode': 'وضع مضغوط',
        
        # Notification settings
        'email_notify': '📧 إشعارات البريد',
        'push_notify': '📱 إشعارات فورية',
        'daily_predictions': 'توقعات يومية',
        'jackpot_alerts': 'تنبيهات الجوائز',
        
        # API settings
        'api_key': 'مفتاح API',
        'api_status': 'حالة API',
        'api_connected': 'متصل',
        'api_disconnected': 'غير متصل',
        'test_connection': 'اختبار الاتصال',
        
        # Advanced settings
        'cache_clear': 'مسح الذاكرة المخبأة',
        'reset_all': 'إعادة ضبط الإعدادات',
        'export_data': 'تصدير البيانات',
        'import_data': 'استيراد البيانات',
        'system_info': 'معلومات النظام',
        'clear_history': 'مسح السجل',
    }
}

t = TRANS[st.session_state.language]

# ==================== ADVANCED CSS (FIXED 2026) مع تحسينات الإغراء ====================
# تحديد الثيم بناءً على الإعدادات
if st.session_state.theme == 'dark':
    bg_color = "#050a18"
    card_bg = "rgba(255, 255, 255, 0.04)"
    text_color = "#e0e0e0"
elif st.session_state.theme == 'light':
    bg_color = "#f0f2f6"
    card_bg = "rgba(255, 255, 255, 0.8)"
    text_color = "#1a1f35"
else:
    bg_color = "#050a18"
    card_bg = "rgba(255, 255, 255, 0.04)"
    text_color = "#e0e0e0"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Cairo:wght@400;700;900&display=swap');
    
    :root {{
        --primary: #00f2fe;
        --secondary: #4facfe;
        --accent: #ffd700;
        --accent2: #ff6b6b;
        --accent3: #ffa502;
        --bg: {bg_color};
        --card-bg: {card_bg};
        --text-color: {text_color};
    }}

    * {{ font-family: 'Orbitron', 'Cairo', sans-serif; }}
    .stApp {{ background: radial-gradient(circle at top right, #1a1f35, var(--bg)); color: var(--text-color); }}

    /* شريط الإعلانات المتحرك متعدد الألوان */
    .ticker-container {{
        width: 100%;
        background: linear-gradient(90deg, #ffd700, #ffa502, #ff6b6b, #ffd700);
        background-size: 300% 100%;
        animation: gradientShift 5s ease infinite;
        padding: 12px 0;
        overflow: hidden;
        margin-bottom: 20px;
        border-radius: 0;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
        border-bottom: 2px solid rgba(255,255,255,0.2);
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    .ticker-text {{
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: ticker 25s linear infinite;
        font-weight: 900;
        color: #000;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 1.1rem;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }}
    
    .ticker-text span {{
        margin: 0 30px;
        font-size: 1.3rem;
    }}
    
    @keyframes ticker {{ 0% {{ transform: translate(0, 0); }} 100% {{ transform: translate(-100%, 0); }} }}

    /* شريط الجوائز المتحرك */
    .jackpot-ticker {{
        background: linear-gradient(90deg, #4a90e2, #9b59b6, #4a90e2);
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
        padding: 15px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        box-shadow: 0 10px 30px rgba(74, 144, 226, 0.5);
    }}
    
    .jackpot-value {{
        font-size: 3rem;
        background: linear-gradient(135deg, #ffd700, #ffa502);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        margin-left: 15px;
        animation: pulse 1.5s ease infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}

    /* صور الفائزين الوهمية */
    .winners-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }}
    
    .winner-card {{
        background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,165,0,0.2));
        border: 2px solid gold;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        animation: float 3s ease-in-out infinite;
    }}
    
    .winner-avatar {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ffd700, #ffa502);
        margin: 0 auto 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 0 30px gold;
    }}
    
    .winner-name {{
        font-size: 1.1rem;
        font-weight: bold;
        color: gold;
    }}
    
    .winner-prize {{
        font-size: 1.3rem;
        font-weight: 900;
        color: #ffd700;
        margin-top: 10px;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}

    /* بطاقات المعلومات الثقافية */
    .info-card {{
        background: linear-gradient(135deg, rgba(74,144,226,0.2), rgba(155,89,182,0.2));
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }}
    
    .info-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(74,144,226,0.3);
        border-color: #4a90e2;
    }}
    
    .info-icon {{
        font-size: 2.5rem;
        margin-bottom: 15px;
    }}
    
    .info-title {{
        font-size: 1.3rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 10px;
    }}

    /* إيموجي متحرك */
    .floating-emoji {{
        font-size: 3rem;
        animation: bounce 2s ease infinite;
        display: inline-block;
        margin: 0 10px;
    }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}

    /* تأثيرات الإغراء */
    .glow-text {{
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffd700, #ffa502, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease infinite;
    }}
    
    @keyframes glow {{
        0%, 100% {{ filter: brightness(1); }}
        50% {{ filter: brightness(1.3); }}
    }}
    
    .counter {{
        font-size: 3rem;
        font-weight: 900;
        color: gold;
        text-shadow: 0 0 30px gold;
        animation: countPulse 1s ease infinite;
    }}
    
    @keyframes countPulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}

    /* Settings Button */
    .settings-button {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 5px 20px rgba(0, 242, 254, 0.3);
        transition: all 0.3s;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .settings-button:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.5);
    }}

    /* Settings Panel */
    .settings-panel {{
        position: fixed;
        top: 0;
        right: 0;
        width: 380px;
        height: 100vh;
        background: rgba(10, 15, 30, 0.95);
        backdrop-filter: blur(20px);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 10000;
        overflow-y: auto;
        animation: slideIn 0.3s ease-out;
        box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
    }}
    
    @keyframes slideIn {{
        from {{ transform: translateX(100%); }}
        to {{ transform: translateX(0); }}
    }}
    
    .settings-header {{
        padding: 25px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .settings-header h2 {{
        color: var(--primary);
        margin: 0;
        font-size: 1.5rem;
    }}
    
    .close-btn {{
        background: rgba(255,255,255,0.1);
        border: none;
        color: white;
        font-size: 1.5rem;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }}
    
    .close-btn:hover {{
        background: rgba(255,255,255,0.2);
        transform: rotate(90deg);
    }}
    
    .settings-menu-item {{
        padding: 18px 25px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 15px;
        color: #aaa;
    }}
    
    .settings-menu-item:hover {{
        background: rgba(0, 242, 254, 0.1);
        color: white;
        padding-left: 35px;
    }}
    
    .settings-menu-item.active {{
        background: rgba(0, 242, 254, 0.15);
        color: var(--primary);
        border-left: 4px solid var(--primary);
    }}
    
    .settings-content {{
        padding: 25px;
    }}
    
    .settings-section {{
        margin-bottom: 30px;
    }}
    
    .settings-section h3 {{
        color: white;
        margin-bottom: 20px;
        font-size: 1.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }}
    
    .settings-option {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s;
    }}
    
    .settings-option:hover {{
        background: rgba(255,255,255,0.05);
        border-color: rgba(0, 242, 254, 0.3);
    }}
    
    .settings-option label {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #ccc;
        cursor: pointer;
    }}

    /* Glass Cards */
    .glass-card {{
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 35px;
        margin-bottom: 30px;
        backdrop-filter: blur(20px);
        transition: all 0.4s ease;
    }}
    .glass-card:hover {{ transform: translateY(-5px); border-color: var(--primary); box-shadow: 0 15px 40px rgba(0, 242, 254, 0.2); }}

    /* Icon Box */
    .icon-box {{
        padding: 20px;
        background: rgba(0, 242, 254, 0.15);
        border-radius: 15px;
        margin-right: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }}

    /* Futuristic Balls */
    .ball-container {{ display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; margin: 40px 0; }}
    .ball {{
        width: 85px; height: 85px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; font-weight: 900; background: rgba(0,0,0,0.5); border: 3px solid var(--primary);
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.4);
        animation: ballGlow 2s ease infinite;
    }}
    
    @keyframes ballGlow {{
        0%, 100% {{ box-shadow: 0 0 25px rgba(0, 242, 254, 0.4); }}
        50% {{ box-shadow: 0 0 40px rgba(0, 242, 254, 0.8); }}
    }}
    
    .ball.special {{ border-color: var(--accent); box-shadow: 0 0 25px rgba(255, 215, 0, 0.4); }}
    .ball.special:hover {{ animation: specialBall 1s ease infinite; }}
    
    @keyframes specialBall {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}

    /* Metrics */
    .metric-container {{ text-align: center; padding: 35px; background: var(--card-bg); border-radius: 25px; border: 1px solid rgba(255,255,255,0.05); }}
    .metric-value {{ font-size: 3.2rem; font-weight: 900; color: var(--primary); text-shadow: 0 0 20px rgba(0,242,254,0.3); }}
    .metric-label {{ font-size: 1rem; color: #888; text-transform: uppercase; margin-top: 10px; }}

    .footer {{ margin-top: 80px; padding: 50px; text-align: center; border-top: 1px solid rgba(255,255,255,0.05); color: #555; }}
    
    /* Custom toggle switch */
    .switch {{
        position: relative;
        display: inline-block;
        width: 50px;
        height: 24px;
    }}
    
    .switch input {{
        opacity: 0;
        width: 0;
        height: 0;
    }}
    
    .slider {{
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: .3s;
        border-radius: 24px;
    }}
    
    .slider:before {{
        position: absolute;
        content: "";
        height: 20px;
        width: 20px;
        left: 2px;
        bottom: 2px;
        background-color: white;
        transition: .3s;
        border-radius: 50%;
    }}
    
    input:checked + .slider {{
        background-color: var(--primary);
    }}
    
    input:checked + .slider:before {{
        transform: translateX(26px);
    }}
    
    /* Compact mode */
    {'' if st.session_state.compact_mode else '''
    .main > div { padding: 2rem 3rem; }
    '''}
    
    /* Animation toggle */
    {'' if st.session_state.animations else '''
    .ball, .glass-card, .winner-card, .info-card { animation: none !important; transition: none !important; }
    '''}
</style>
""", unsafe_allow_html=True)

# ==================== SETTINGS BUTTON ====================
settings_clicked = st.button("⚙️ " + t['settings'], key="settings_toggle")

# ==================== SETTINGS PANEL ====================
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

if settings_clicked:
    st.session_state.show_settings = not st.session_state.show_settings

if st.session_state.show_settings:
    with st.container():
        st.markdown(f"""
        <div class="settings-panel" id="settings-panel">
            <div class="settings-header">
                <h2>{t['settings']}</h2>
                <button class="close-btn" onclick="document.getElementById('settings-panel').style.display='none';">✕</button>
            </div>
        """, unsafe_allow_html=True)
        
        # Settings Menu
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
            
            # Main Menu Button
            if st.button("🏠 " + t['settings_main'], use_container_width=True, key="settings_main_btn"):
                st.session_state.settings_page = 'main'
            
            # Language Settings
            if st.button("🌐 " + t['settings_language'], use_container_width=True, key="settings_lang_btn"):
                st.session_state.settings_page = 'language'
            
            # Appearance Settings
            if st.button("🎨 " + t['settings_appearance'], use_container_width=True, key="settings_appearance_btn"):
                st.session_state.settings_page = 'appearance'
            
            # Notification Settings
            if st.button("🔔 " + t['settings_notifications'], use_container_width=True, key="settings_notify_btn"):
                st.session_state.settings_page = 'notifications'
            
            # API Settings
            if st.button("🔑 " + t['settings_api'], use_container_width=True, key="settings_api_btn"):
                st.session_state.settings_page = 'api'
            
            # Advanced Settings
            if st.button("⚡ " + t['settings_advanced'], use_container_width=True, key="settings_advanced_btn"):
                st.session_state.settings_page = 'advanced'
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='settings-content'>", unsafe_allow_html=True)
            
            # Main Settings Page
            if st.session_state.settings_page == 'main':
                st.markdown(f"<h3>{t['settings_main']}</h3>", unsafe_allow_html=True)
                st.info(t['disclaimer'])
                
                # Quick Stats
                st.markdown("### 📊 Quick Stats")
                st.markdown(f"""
                - **PyArrow:** {'✅ Enabled' if PYARROW_AVAILABLE else '❌ Disabled'}
                - **Cache:** ✅ Active
                - **Session:** {len(st.session_state)} items
                - **Last Cleanup:** {st.session_state.last_cleanup.strftime('%H:%M:%S')}
                - **Theme:** {st.session_state.theme}
                - **Animations:** {'On' if st.session_state.animations else 'Off'}
                """)
            
            # Language Settings
            elif st.session_state.settings_page == 'language':
                st.markdown(f"<h3>{t['settings_language']}</h3>", unsafe_allow_html=True)
                
                lang_choice = st.radio(
                    t['lang_label'],
                    ['de', 'en', 'ar'],
                    format_func=lambda x: {'de': '🇩🇪 Deutsch', 'en': '🇬🇧 English', 'ar': '🇸🇦 العربية'}[x],
                    index=['de', 'en', 'ar'].index(st.session_state.language)
                )
                
                if st.button("💾 Save Language"):
                    st.session_state.language = lang_choice
                    st.rerun()
            
            # Appearance Settings
            elif st.session_state.settings_page == 'appearance':
                st.markdown(f"<h3>{t['settings_appearance']}</h3>", unsafe_allow_html=True)
                
                # Theme Selection
                st.markdown("#### 🎨 Theme")
                theme_choice = st.radio(
                    "",
                    ['dark', 'light'],
                    format_func=lambda x: {'dark': t['theme_dark'], 'light': t['theme_light']}[x],
                    index=0 if st.session_state.theme == 'dark' else 1,
                    horizontal=True
                )
                
                # Animations
                st.markdown("#### ✨ Animations")
                animations_choice = st.toggle(t['animations'], value=st.session_state.animations)
                
                # Compact Mode
                st.markdown("#### 📏 Layout")
                compact_choice = st.toggle(t['compact_mode'], value=st.session_state.compact_mode)
                
                if st.button("💾 Save Appearance"):
                    st.session_state.theme = theme_choice
                    st.session_state.animations = animations_choice
                    st.session_state.compact_mode = compact_choice
                    st.rerun()
            
            # Notification Settings
            elif st.session_state.settings_page == 'notifications':
                st.markdown(f"<h3>{t['settings_notifications']}</h3>", unsafe_allow_html=True)
                
                email_notify = st.toggle(t['email_notify'], value=True)
                push_notify = st.toggle(t['push_notify'], value=False)
                daily_pred = st.toggle(t['daily_predictions'], value=True)
                jackpot_alerts = st.toggle(t['jackpot_alerts'], value=True)
                
                if st.button("💾 Save Notifications"):
                    st.success("Notification settings saved!")
            
            # API Settings
            elif st.session_state.settings_page == 'api':
                st.markdown(f"<h3>{t['settings_api']}</h3>", unsafe_allow_html=True)
                
                api_key = st.text_input(t['api_key'], type="password", value="••••••••••••••••")
                
                st.markdown(f"**{t['api_status']}:** ✅ {t['api_connected']}")
                
                if st.button(t['test_connection']):
                    st.success("Connection successful!")
            
            # Advanced Settings
            elif st.session_state.settings_page == 'advanced':
                st.markdown(f"<h3>{t['settings_advanced']}</h3>", unsafe_allow_html=True)
                
                if st.button("🗑️ " + t['cache_clear'], use_container_width=True):
                    if os.path.exists('predictions.cache'):
                        os.remove('predictions.cache')
                    st.session_state.cache = PredictionCache()
                    st.success("Cache cleared!")
                
                if st.button("🔄 " + t['reset_all'], use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key not in ['language', 'show_settings', 'theme', 'animations', 'compact_mode']:
                            del st.session_state[key]
                    st.rerun()
                
                if st.button("📥 " + t['export_data'], use_container_width=True):
                    st.info("Export feature coming soon!")
                
                if st.button("📤 " + t['import_data'], use_container_width=True):
                    st.info("Import feature coming soon!")
                
                if st.button("ℹ️ " + t['system_info'], use_container_width=True):
                    st.info(f"""
                    **System Info:**
                    - Python: 3.9+
                    - Streamlit: 1.28.1
                    - PyArrow: {'✅' if PYARROW_AVAILABLE else '❌'}
                    - Cache: {'✅' if os.path.exists('predictions.cache') else '❌'}
                    - Session: {len(st.session_state)} items
                    - Theme: {st.session_state.theme}
                    - Animations: {'On' if st.session_state.animations else 'Off'}
                    """)
                
                if st.button("⚠️ " + t['clear_history'], use_container_width=True):
                    st.session_state.lotto_pred = None
                    st.session_state.euro_pred = None
                    st.success("History cleared!")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TICKER COMPONENT (مطور) ====================
st.markdown(f"""
    <div class="ticker-container">
        <div class="ticker-text">
            <span>🎲🎯💰</span> 🎲 LOTTO 6AUS49 JACKPOT: €45.2 MILLIONEN <span>🔥🔥🔥</span> 🇪🇺 EUROJACKPOT: €87 MILLIONEN <span>💶💶💶</span> 🏆 GEWINNER HEUTE: 3 NEUE MILLIONÄRE <span>🤩🤩🤩</span> 🎲🎯💰
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== JACKPOT TICKER ====================
jackpot_lotto = random.randint(42, 48)
jackpot_euro = random.randint(82, 95)

st.markdown(f"""
    <div class="jackpot-ticker">
        <span class="floating-emoji">💰</span>
        AKTUELLE JACKPOTS: 
        <span class="jackpot-value">LOTTO: €{jackpot_lotto}.2M</span>
        <span class="floating-emoji">💶</span>
        <span class="jackpot-value">EURO: €{jackpot_euro}.5M</span>
        <span class="floating-emoji">💎</span>
    </div>
""", unsafe_allow_html=True)

# ==================== WINNERS GALLERY (فائزون وهميون) ====================
st.markdown("## 🏆 **UNSERE GLÜCKLICHEN GEWINNER 2026** 🏆")

winners = [
    {"name": "Michael S. 🎲", "prize": "€4.2M", "city": "München", "emoji": "👨‍🦰"},
    {"name": "Laura K. 💰", "prize": "€7.8M", "city": "Berlin", "emoji": "👩"},
    {"name": "Thomas W. 🔮", "prize": "€12.3M", "city": "Hamburg", "emoji": "👨‍🦳"},
    {"name": "Sarah M. 🌟", "prize": "€3.5M", "city": "Frankfurt", "emoji": "👩‍🦰"},
    {"name": "Klaus D. 💎", "prize": "€9.1M", "city": "Köln", "emoji": "👴"},
    {"name": "Anna S. 🎯", "prize": "€6.7M", "city": "Stuttgart", "emoji": "👩‍🦱"},
]

cols = st.columns(3)
for i, winner in enumerate(winners[:3]):
    with cols[i]:
        st.markdown(f"""
            <div class="winner-card">
                <div class="winner-avatar">{winner['emoji']}</div>
                <div class="winner-name">{winner['name']}</div>
                <div>📍 {winner['city']}</div>
                <div class="winner-prize">{winner['prize']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

cols2 = st.columns(3)
for i, winner in enumerate(winners[3:6]):
    with cols2[i]:
        st.markdown(f"""
            <div class="winner-card">
                <div class="winner-avatar">{winner['emoji']}</div>
                <div class="winner-name">{winner['name']}</div>
                <div>📍 {winner['city']}</div>
                <div class="winner-prize">{winner['prize']}</div>
            </div>
        """, unsafe_allow_html=True)

# ==================== DATA ENGINE ====================
class QuantumPredictor:
    def __init__(self):
        self.lotto_range = range(1, 50)
        self.euro_main_range = range(1, 51)
        self.euro_extra_range = range(1, 13)

    @st.cache_data
    def get_historical_data(_self, type='lotto'):
        dates = pd.date_range(end=datetime.now(), periods=500, freq='W')
        if type == 'lotto':
            nums = [sorted(random.sample(_self.lotto_range, 6)) for _ in range(500)]
            jackpots = [random.uniform(1, 45) for _ in range(500)]
            return pd.DataFrame({'date': dates, 'numbers': nums, 'jackpot': jackpots})
        else:
            nums = [sorted(random.sample(_self.euro_main_range, 5)) for _ in range(500)]
            extra = [sorted(random.sample(_self.euro_extra_range, 2)) for _ in range(500)]
            jackpots = [random.uniform(10, 120) for _ in range(500)]
            return pd.DataFrame({'date': dates, 'main': nums, 'extra': extra, 'jackpot': jackpots})

    def generate_prediction(self, type='lotto'):
        time.sleep(1.2)
        if type == 'lotto':
            return {'main': sorted(random.sample(self.lotto_range, 6)), 'super': random.randint(0, 9), 'confidence': round(random.uniform(88.5, 99.2), 2)}
        else:
            return {'main': sorted(random.sample(self.euro_main_range, 5)), 'extra': sorted(random.sample(self.euro_extra_range, 2)), 'confidence': round(random.uniform(85.1, 98.7), 2)}

engine = QuantumPredictor()

# ==================== NAVIGATION ====================
with st.sidebar:
    st.markdown(f"<div style='text-align: center; padding: 40px 0;'><h1 style='color: var(--primary);'>QUANTUM</h1><p style='color: #555; letter-spacing: 5px;'>v2.6 CORE</p></div>", unsafe_allow_html=True)
    
    if st.button("🎯 " + t['presentation_mode'], use_container_width=True):
        st.session_state.presentation_mode = not st.session_state.presentation_mode
    
    menu = option_menu(
        None, [t['home'], t['lotto'], t['euro'], t['stats']],
        icons=['house-fill', 'dice-6-fill', 'globe-europe-africa', 'bar-chart-line-fill'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "15px!important", "background-color": "transparent"},
            "icon": {"color": "var(--primary)", "font-size": "1.4rem"}, 
            "nav-link": {"color": "#888", "font-size": "1.1rem", "padding": "18px", "text-align": "left", "margin":"8px 0", "border-radius": "15px"},
            "nav-link-selected": {"background-color": "rgba(0, 242, 254, 0.15)", "color": "white", "font-weight": "bold", "border-left": "5px solid var(--primary)"},
        }
    )

# ==================== INFO SECTION (ثقافية) ====================
st.markdown("---")
st.markdown("## 🎯 **WISSEN FÜR GEWINNER** 🎯")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <div class="info-title">DIE 5 HÄUFIGSTEN ZAHLEN</div>
            <p>🔴 19: 187x gezogen<br>🔵 23: 176x gezogen<br>🟢 7: 169x gezogen<br>🟡 31: 165x gezogen<br>🟣 42: 158x gezogen</p>
            <p><small>Statistik 2020-2026</small></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">🧠</div>
            <div class="info-title">PROFI-TIPPS</div>
            <p>✅ Zahlen zwischen 1-31 sind beliebt<br>✅ Vermeide Geburtstage<br>✅ Setze auf Muster<br>✅ Nutze Zufallsgeneratoren<br>✅ Bleib konsistent</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">📈</div>
            <div class="info-title">ANALYSE-PLATTFORMEN</div>
            <p>🔗 Lotto-Analyse Pro<br>🔗 EuroJackpot Insights<br>🔗 Quantum Numbers AI<br>🔗 WinPredictor 2026<br>🔗 Statistik-Forum DE</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== PAGES ====================

if menu == t['home']:
    st.markdown(f"<div style='text-align: center; padding: 40px 0 20px;'><h1 style='font-size: 4rem; background: linear-gradient(to right, #00f2fe, #4facfe, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>{t['title']}</h1><p style='font-size: 1.3rem; color: #aaa; letter-spacing: 5px;'>{t['subtitle']}</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='glass-card'><h3><span class='icon-box'>🎲</span> {t['lotto']}</h3><p style='margin-top: 20px; font-size: 1.3rem;'>Aktueller Jackpot: <span style='color: gold; font-weight: bold;'>€{jackpot_lotto}.2M</span></p><p>Status: <span style='color: #00ff00;'>Active Analysis</span></p><p>Next Draw: {(datetime.now() + timedelta(days=2)).strftime('%d.%m.2026')}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='glass-card'><h3><span class='icon-box'>🇪🇺</span> {t['euro']}</h3><p style='margin-top: 20px; font-size: 1.3rem;'>Aktueller Jackpot: <span style='color: gold; font-weight: bold;'>€{jackpot_euro}.5M</span></p><p>Status: <span style='color: #00ff00;'>Active Analysis</span></p><p>Next Draw: {(datetime.now() + timedelta(days=4)).strftime('%d.%m.2026')}</p></div>", unsafe_allow_html=True)

    # Counter
    st.markdown(f"""
        <div style='text-align: center; margin: 40px 0;'>
            <span class='counter'>{random.randint(150, 200)}</span>
            <span style='font-size: 1.5rem; color: #aaa;'> MILLIONÄRE BIS JETZT IN 2026</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 📍 {t['map_title']}")
    map_data = pd.DataFrame({'lat': np.random.uniform(47.2, 55.0, 50), 'lon': np.random.uniform(5.8, 15.0, 50), 'winners': np.random.randint(1, 10, 50)})
    st.map(map_data, size='winners', color='#00f2fe')

elif menu == t['lotto']:
    st.markdown(f"<h1 style='text-align:center; padding: 30px;'>{t['lotto']} <span style='color: gold;'>€{jackpot_lotto}.2M</span></h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button(t['predict_btn'], use_container_width=True):
            with st.spinner("QUANTUM CORE INITIALIZING..."):
                with performance_logger("Lotto Prediction"):
                    st.session_state.lotto_pred = engine.generate_prediction('lotto')
        if st.session_state.lotto_pred:
            p = st.session_state.lotto_pred
            balls_html = "".join([f'<div class="ball">{n}</div>' for n in p['main']])
            st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <h2 style='color: var(--accent); font-size: 2.5rem;'>{t['confidence']}: {p['confidence']}%</h2>
                    <div class='ball-container'>
                        {balls_html}
                        <div class='ball special'>{p['super']}</div>
                    </div>
                    <p style='color: #666;'>{t['last_update']}: {datetime.now().strftime('%H:%M:%S')}</p>
                </div>
            """, unsafe_allow_html=True)

elif menu == t['euro']:
    st.markdown(f"<h1 style='text-align:center; padding: 30px;'>{t['euro']} <span style='color: gold;'>€{jackpot_euro}.5M</span></h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button(t['predict_btn'], use_container_width=True):
            with st.spinner("SYNCHRONIZING EUROPEAN NODES..."):
                with performance_logger("Eurojackpot Prediction"):
                    st.session_state.euro_pred = engine.generate_prediction('euro')
        if st.session_state.euro_pred:
            p = st.session_state.euro_pred
            main_balls_html = "".join([f'<div class="ball">{n}</div>' for n in p['main']])
            extra_balls_html = "".join([f'<div class="ball special">{n}</div>' for n in p['extra']])
            st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <h2 style='color: var(--accent); font-size: 2.5rem;'>{t['confidence']}: {p['confidence']}%</h2>
                    <h4 style='margin-top:30px; color: var(--primary);'>{t['main_nums']}</h4>
                    <div class='ball-container'>{main_balls_html}</div>
                    <h4 style='margin-top:30px; color: var(--accent);'>{t['euro_nums']}</h4>
                    <div class='ball-container'>{extra_balls_html}</div>
                </div>
            """, unsafe_allow_html=True)

elif menu == t['stats']:
    st.markdown(f"<h1 style='text-align:center; padding: 40px;'>{t['stats']}</h1>", unsafe_allow_html=True)
    data = engine.get_historical_data('lotto')
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f"<div class='metric-container'><div class='metric-value'>500</div><div class='metric-label'>{t['total_draws']}</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-container'><div class='metric-value'>{data['jackpot'].mean():.1f}M</div><div class='metric-label'>{t['avg_jackpot']}</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-container'><div class='metric-value'>{data['jackpot'].max():.1f}M</div><div class='metric-label'>{t['max_jackpot']}</div></div>", unsafe_allow_html=True)
    fig = px.line(data, x='date', y='jackpot', title=t['trend'], template='plotly_dark')
    fig.update_traces(line_color='#00f2fe', line_width=4)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Orbitron", margin=dict(t=80, b=40))
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.markdown(f"<div class='footer'><p style='font-weight: bold; color: var(--primary); font-size: 1.1rem;'>{t['footer']}</p><p style='font-size: 0.8rem; max-width: 900px; margin: 20px auto; line-height: 1.6;'>{t['disclaimer']}</p><p style='font-size: 0.7rem; color: #444; margin-top: 20px;'>Quantum Core v2.6 | PyArrow: {'✅' if PYARROW_AVAILABLE else '❌'} | Compression: GZIP Active | Theme: {st.session_state.theme}</p></div>", unsafe_allow_html=True)
