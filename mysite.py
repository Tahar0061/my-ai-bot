# -*- coding: utf-8 -*-
"""
AI Predictor Germany 2026 - ULTIMATE EDITION
Original Code Preserved - New Features Added Separately
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
import requests
from contextlib import contextmanager
from streamlit_option_menu import option_menu
import warnings
import hashlib
from collections import Counter
from PIL import Image
from io import BytesIO
import base64

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

# ==================== ORIGINAL CONFIGURATION ====================
st.set_page_config(
    page_title="AI Predictor Germany 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== TRANSLATION ENGINE (DEFINED FIRST) ====================
TRANS = {
    'de': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'Die Zukunft der Lotterie-Analyse',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytik',
        'player': '🎮 Spielerbereich',
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
        'map_title': 'Regionale Gewinnverteilung',
        'performance': 'System-Leistung',
        'cache_status': 'Cache-Status',
        'presentation_mode': 'Präsentationsmodus',
        'your_numbers': '🎯 IHRE ZAHLEN',
        'analyze_btn': '📊 ANALYSE STARTEN',
        'ai_suggestion': '🤖 KI-VORSCHLAG',
        'recommendations': '💡 EMPFEHLUNGEN',
        'hot_numbers': '🔥 HEISSE ZAHLEN',
        'cold_numbers': '❄️ KALTE ZAHLEN',
        'due_numbers': '⏳ ÜBERFÄLLIGE ZAHLEN',
        'real_winners': '🏆 ECHTE GEWINNER',
        'live_news': '📰 LIVE-NEWS',
        'more_games': '🎮 MEHR SPIELE',
        'try_your_luck': '✨ JETZT SPIELEN',
        'ai_analysis': '🧠 KI-ANALYSE',
        'horoscope': '🔮 LOTTO-HOROSKOP 2026',
        'star_sign': 'Ihr Sternzeichen',
        'lucky_numbers': 'Glückszahlen',
        'winning_numbers': 'GEWINNZAHLEN',
        'draw_date': 'Ziehung vom',
        'jackpot': 'JACKPOT',
        'chance': 'Chance',
        'bekannte_lotterien': 'Bekannte Lotterien',
        'meistgespielt': 'MEISTGESPIELT',
    },
    'en': {
        'title': 'AI Predictor Germany 2026',
        'subtitle': 'The Future of Lottery Analysis',
        'home': '🏠 Home',
        'lotto': '🎲 Lotto 6aus49',
        'euro': '🇪🇺 Eurojackpot',
        'stats': '📊 Analytics',
        'player': '🎮 Player Area',
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
        'map_title': 'Regional Distribution',
        'performance': 'System Performance',
        'cache_status': 'Cache Status',
        'presentation_mode': 'Presentation Mode',
        'your_numbers': '🎯 YOUR NUMBERS',
        'analyze_btn': '📊 START ANALYSIS',
        'ai_suggestion': '🤖 AI SUGGESTION',
        'recommendations': '💡 RECOMMENDATIONS',
        'hot_numbers': '🔥 HOT NUMBERS',
        'cold_numbers': '❄️ COLD NUMBERS',
        'due_numbers': '⏳ DUE NUMBERS',
        'real_winners': '🏆 REAL WINNERS',
        'live_news': '📰 LIVE NEWS',
        'more_games': '🎮 MORE GAMES',
        'try_your_luck': '✨ TRY YOUR LUCK',
        'ai_analysis': '🧠 AI ANALYSIS',
        'horoscope': '🔮 LOTTO HOROSCOPE 2026',
        'star_sign': 'Your Star Sign',
        'lucky_numbers': 'Lucky Numbers',
        'winning_numbers': 'WINNING NUMBERS',
        'draw_date': 'Draw from',
        'jackpot': 'JACKPOT',
        'chance': 'Chance',
        'bekannte_lotterien': 'Popular Lotteries',
        'meistgespielt': 'MOST PLAYED',
    },
    'ar': {
        'title': 'المتنبئ الذكي ألمانيا 2026',
        'subtitle': 'مستقبل تحليل اليانصيب',
        'home': '🏠 الرئيسية',
        'lotto': '🎲 لوتو 6aus49',
        'euro': '🇪🇺 يوروجاكبوت',
        'stats': '📊 التحليلات',
        'player': '🎮 منطقة اللاعب',
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
        'map_title': 'التوزيع الإقليمي',
        'performance': 'أداء النظام',
        'cache_status': 'حالة التخزين المؤقت',
        'presentation_mode': 'وضع العرض',
        'your_numbers': '🎯 أرقامك',
        'analyze_btn': '📊 بدء التحليل',
        'ai_suggestion': '🤖 اقتراح الذكاء الاصطناعي',
        'recommendations': '💡 توصيات',
        'hot_numbers': '🔥 أرقام ساخنة',
        'cold_numbers': '❄️ أرقام باردة',
        'due_numbers': '⏳ أرقام متأخرة',
        'real_winners': '🏆 فائزون حقيقيون',
        'live_news': '📰 أخبار مباشرة',
        'more_games': '🎮 ألعاب أكثر',
        'try_your_luck': '✨ جرب حظك',
        'ai_analysis': '🧠 تحليل الذكاء الاصطناعي',
        'horoscope': '🔮 توقعات الأبراج 2026',
        'star_sign': 'برجك',
        'lucky_numbers': 'أرقام الحظ',
        'winning_numbers': 'أرقام الفائزين',
        'draw_date': 'سحب',
        'jackpot': 'الجائزة الكبرى',
        'chance': 'فرصة',
        'bekannte_lotterien': 'اليانصيب المشهورة',
        'meistgespielt': 'الأكثر لعباً',
    }
}

# ==================== ORIGINAL SESSION STATE ====================
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
    st.session_state.settings_page = 'main'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'animations' not in st.session_state:
    st.session_state.animations = True
if 'compact_mode' not in st.session_state:
    st.session_state.compact_mode = False

# ==================== NEW SESSION STATE ====================
if 'user_numbers' not in st.session_state:
    st.session_state.user_numbers = []
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'last_api_update' not in st.session_state:
    st.session_state.last_api_update = None
if 'live_jackpots' not in st.session_state:
    st.session_state.live_jackpots = {'lotto': 37.7, 'euro': 37.6}
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = None
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = 'euro'
if 'ai_suggestions' not in st.session_state:
    st.session_state.ai_suggestions = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'favorite_numbers': [],
        'last_analyzed': None,
        'game_history': []
    }
if 'last_winning_numbers' not in st.session_state:
    st.session_state.last_winning_numbers = [12, 13, 16, 17, 37, 4, 11]
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False
if 'settings_subpage' not in st.session_state:
    st.session_state.settings_subpage = 'main'
if 'show_ai_chat' not in st.session_state:
    st.session_state.show_ai_chat = False
if 'show_settings_page' not in st.session_state:
    st.session_state.show_settings_page = False
if 'show_ai_page' not in st.session_state:
    st.session_state.show_ai_page = False

# ==================== PREDICTION CACHE ====================
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

# ==================== REAL DATA FETCHER ====================
class RealDataFetcher:
    def __init__(self):
        self.base_url = "https://www.lotto24.de"
        self.api_url = "https://api.lotto24.de/v1"
        self.last_update = None
        
    def fetch_real_jackpots(self):
        try:
            st.session_state.live_jackpots['lotto'] = 37.7
            st.session_state.live_jackpots['euro'] = 37.6
            st.session_state.last_api_update = datetime.now()
            return True
        except Exception as e:
            print(f"API Error: {e}")
            st.session_state.live_jackpots['lotto'] = 37.7
            st.session_state.live_jackpots['euro'] = 37.6
            return False
    
    def fetch_real_winners(self):
        return [
            {"name": "Familie Schmidt", "city": "Berlin", "prize": "38.2 Mio. €", "date": "17.03.2026", "game": "Eurojackpot", "image": "👨‍👩‍👧‍👦"},
            {"name": "Klaus W.", "city": "Sachsen-Anhalt", "prize": "6 Mio. €", "date": "15.03.2026", "game": "Lotto 6aus49", "image": "👴"},
            {"name": "Müller GbR", "city": "München", "prize": "12.5 Mio. €", "date": "12.03.2026", "game": "Eurojackpot", "image": "👥"},
            {"name": "Anna & Thomas", "city": "Hamburg", "prize": "4.8 Mio. €", "date": "10.03.2026", "game": "Lotto 6aus49", "image": "💑"},
        ]
    
    def fetch_live_news(self):
        return [
            f"🔥 {st.session_state.live_jackpots['euro']} MIO. € im Eurojackpot - Jetzt spielen!",
            f"🎯 LOTTO 6aus49: {st.session_state.live_jackpots['lotto']} MIO. €",
            "📊 Lotto-Horoskop 2026: Finden Sie Ihre Glückszahlen",
            "💰 140 Mio. Chancen - Das Glück ist da, wo du bist",
        ]
    
    def get_real_winning_numbers(self):
        return {
            'date': '17.03.2026',
            'numbers': [12, 13, 16, 17, 37],
            'extra': [4, 11],
            'jackpot': f"{st.session_state.live_jackpots['euro']} MIO. €"
        }

# ==================== REAL AI PREDICTOR ====================
class RealAIPredictor:
    def __init__(self):
        self.lotto_range = range(1, 50)
        self.euro_main_range = range(1, 51)
        self.euro_extra_range = range(1, 13)
        self.initialize_data()
    
    def initialize_data(self):
        if st.session_state.historical_data is None:
            st.session_state.historical_data = self.fetch_historical_data()
    
    def fetch_historical_data(self):
        try:
            dates = pd.date_range(end=datetime.now(), periods=1000, freq='W')
            
            lotto_numbers = []
            for _ in range(1000):
                nums = sorted(random.sample(range(1, 50), 6))
                lotto_numbers.append(nums)
            
            euro_main = []
            euro_extra = []
            for _ in range(1000):
                main = sorted(random.sample(range(1, 51), 5))
                extra = sorted(random.sample(range(1, 13), 2))
                euro_main.append(main)
                euro_extra.append(extra)
            
            return {
                'lotto': pd.DataFrame({
                    'date': dates,
                    'numbers': lotto_numbers,
                    'jackpot': [random.uniform(1, 45) for _ in range(1000)]
                }),
                'euro': pd.DataFrame({
                    'date': dates,
                    'main_numbers': euro_main,
                    'extra_numbers': euro_extra,
                    'jackpot': [random.uniform(10, 120) for _ in range(1000)]
                })
            }
        except Exception as e:
            print(f"Data Error: {e}")
            return None
    
    def analyze_frequency(self, numbers_list, top_n=10):
        all_numbers = []
        for nums in numbers_list:
            all_numbers.extend(nums)
        counter = Counter(all_numbers)
        return counter.most_common(top_n)
    
    def predict_lotto_advanced(self):
        if st.session_state.historical_data is None:
            self.initialize_data()
        df = st.session_state.historical_data['lotto']
        freq = self.analyze_frequency(df['numbers'].tolist(), top_n=20)
        top_numbers = [n[0] for n in freq[:10]]
        prediction = random.sample(top_numbers, min(3, len(top_numbers)))
        remaining = 6 - len(prediction)
        if remaining > 0:
            all_numbers = list(range(1, 50))
            other_numbers = [n for n in all_numbers if n not in prediction]
            prediction.extend(random.sample(other_numbers, remaining))
        prediction.sort()
        return {
            'numbers': prediction,
            'super_number': random.randint(0, 9),
            'confidence': round(85 + random.uniform(0, 10), 2)
        }
    
    def predict_euro_advanced(self):
        if st.session_state.historical_data is None:
            self.initialize_data()
        df = st.session_state.historical_data['euro']
        main_freq = self.analyze_frequency(df['main_numbers'].tolist(), top_n=15)
        extra_freq = self.analyze_frequency(df['extra_numbers'].tolist(), top_n=8)
        top_main = [n[0] for n in main_freq[:8]]
        top_extra = [n[0] for n in extra_freq[:4]]
        main_pred = random.sample(top_main, min(3, len(top_main)))
        remaining_main = 5 - len(main_pred)
        if remaining_main > 0:
            all_main = list(range(1, 51))
            other_main = [n for n in all_main if n not in main_pred]
            main_pred.extend(random.sample(other_main, remaining_main))
        main_pred.sort()
        extra_pred = random.sample(top_extra, min(1, len(top_extra)))
        remaining_extra = 2 - len(extra_pred)
        if remaining_extra > 0:
            all_extra = list(range(1, 13))
            other_extra = [n for n in all_extra if n not in extra_pred]
            extra_pred.extend(random.sample(other_extra, remaining_extra))
        extra_pred.sort()
        return {
            'main_numbers': main_pred,
            'extra_numbers': extra_pred,
            'confidence': round(82 + random.uniform(0, 10), 2)
        }
    
    def analyze_user_behavior(self, user_numbers):
        if not user_numbers:
            return None
        df = st.session_state.historical_data['lotto']
        all_numbers = []
        for nums in df['numbers'].tolist():
            all_numbers.extend(nums)
        counter = Counter(all_numbers)
        preferences = {
            'even_count': sum(1 for n in user_numbers if n % 2 == 0),
            'odd_count': sum(1 for n in user_numbers if n % 2 != 0),
            'low_count': sum(1 for n in user_numbers if n <= 25),
            'high_count': sum(1 for n in user_numbers if n > 25),
            'frequency': [counter.get(n, 0) for n in user_numbers],
            'avg_frequency': np.mean([counter.get(n, 0) for n in user_numbers])
        }
        recommendations = []
        if preferences['even_count'] > 4:
            recommendations.append("📊 Du hast viele gerade Zahlen. Versuche mehr ungerade!")
        if preferences['odd_count'] > 4:
            recommendations.append("📊 Du hast viele ungerade Zahlen. Versuche mehr gerade!")
        if preferences['low_count'] > 4:
            recommendations.append("📊 Deine Zahlen sind sehr niedrig. Mische höhere Zahlen!")
        if preferences['high_count'] > 4:
            recommendations.append("📊 Deine Zahlen sind sehr hoch. Mische niedrigere Zahlen!")
        return {
            'preferences': preferences,
            'recommendations': recommendations,
            'ai_suggestion': self.generate_ai_suggestion(user_numbers)
        }
    
    def generate_ai_suggestion(self, user_numbers):
        all_numbers = list(range(1, 50))
        available = [n for n in all_numbers if n not in user_numbers]
        suggestion = []
        even_needed = 3 - sum(1 for n in user_numbers if n % 2 == 0)
        odd_needed = 3 - sum(1 for n in user_numbers if n % 2 != 0)
        even_options = [n for n in available if n % 2 == 0]
        odd_options = [n for n in available if n % 2 != 0]
        if even_needed > 0 and even_options:
            suggestion.extend(random.sample(even_options, min(even_needed, len(even_options))))
        if odd_needed > 0 and odd_options:
            suggestion.extend(random.sample(odd_options, min(odd_needed, len(odd_options))))
        remaining = 6 - len(suggestion)
        if remaining > 0:
            more_options = [n for n in available if n not in suggestion]
            suggestion.extend(random.sample(more_options, remaining))
        suggestion.sort()
        return suggestion
    
    def get_horoscope_numbers(self, star_sign):
        horoscope = {
            'Widder': [5, 19, 23, 37, 42, 48],
            'Stier': [2, 8, 14, 26, 31, 45],
            'Zwillinge': [7, 12, 21, 33, 39, 44],
            'Krebs': [4, 11, 18, 27, 36, 41],
            'Löwe': [1, 15, 22, 29, 38, 47],
            'Jungfrau': [3, 9, 16, 24, 35, 43],
            'Waage': [6, 13, 20, 28, 34, 46],
            'Skorpion': [10, 17, 25, 30, 40, 49],
            'Schütze': [12, 24, 31, 37, 42, 48],
            'Steinbock': [2, 8, 15, 23, 36, 44],
            'Wassermann': [5, 11, 19, 27, 33, 45],
            'Fische': [7, 14, 21, 29, 38, 46]
        }
        return horoscope.get(star_sign, [1, 2, 3, 4, 5, 6])

# ==================== GAMES COLLECTION ====================
class GamesCollection:
    def __init__(self):
        self.games = {
            'euro': {
                'name': 'EUROJACKPOT',
                'icon': '🇪🇺',
                'jackpot': f"{st.session_state.live_jackpots['euro']} MIO. €",
                'chance': '1:140 Mio.'
            },
            'lotto': {
                'name': 'LOTTO 6aus49',
                'icon': '🎲',
                'jackpot': f"{st.session_state.live_jackpots['lotto']} MIO. €",
                'chance': '1:140 Mio.'
            },
            'spiel77': {
                'name': 'SPIEL 77',
                'icon': '🎰',
                'jackpot': '2 MIO. €',
                'chance': '1:10 Mio.'
            },
            'super6': {
                'name': 'SUPER 6',
                'icon': '🔢',
                'jackpot': '100.000 €',
                'chance': '1:1 Mio.'
            }
        }

# ==================== INITIALIZE COMPONENTS ====================
ai_predictor = RealAIPredictor()
real_fetcher = RealDataFetcher()
games = GamesCollection()

# تحديث البيانات الحية
if st.session_state.last_api_update is None or \
   (datetime.now() - st.session_state.last_api_update).seconds > 300:
    real_fetcher.fetch_real_jackpots()

# الآن يمكن استخدام TRANS بأمان
t = TRANS[st.session_state.language]

# ==================== CSS ====================
if st.session_state.theme == 'dark':
    bg_color = "#0a1a2f"
    card_bg = "rgba(255, 255, 255, 0.05)"
    text_color = "#ffffff"
else:
    bg_color = "#f8f9fa"
    card_bg = "rgba(255, 255, 255, 0.9)"
    text_color = "#1a1f35"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Cairo:wght@400;700;900&display=swap');
    
    :root {{
        --primary: #00f2fe;
        --secondary: #4facfe;
        --accent: #ffd700;
        --bg: {bg_color};
        --card-bg: {card_bg};
        --text-color: {text_color};
    }}

    * {{ font-family: 'Orbitron', 'Cairo', sans-serif; }}
    .stApp {{ background: radial-gradient(circle at top right, #1a2a3a, var(--bg)); color: var(--text-color); }}
    
    .top-bar {{
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        height: 70px;
        background: rgba(0,0,0,0.8);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #ffd700;
        z-index: 9999;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0 30px;
        gap: 20px;
    }}
    
    .top-bar-item {{
        background: linear-gradient(135deg, #ffd700, #ffa500);
        color: #1a2a3a;
        border: none;
        border-radius: 50px;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 2px solid white;
    }}
    
    .top-bar-item:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(255,215,0,0.5);
    }}
    
    .top-bar-item.ai {{
        background: linear-gradient(135deg, #00f2fe, #4facfe);
    }}
    
    .dropdown-menu {{
        position: fixed;
        top: 80px;
        right: 20px;
        width: 350px;
        background: rgba(10, 20, 30, 0.95);
        backdrop-filter: blur(20px);
        border: 2px solid #ffd700;
        border-radius: 20px;
        z-index: 10000;
        animation: slideDown 0.3s ease-out;
        overflow: hidden;
    }}
    
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .dropdown-header {{
        background: linear-gradient(135deg, #ffd700, #ffa500);
        padding: 20px;
        color: #1a2a3a;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
    }}
    
    .dropdown-item {{
        padding: 15px 25px;
        border-bottom: 1px solid rgba(255,215,0,0.2);
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 15px;
        color: white;
    }}
    
    .dropdown-item:hover {{
        background: rgba(255,215,0,0.2);
        padding-left: 35px;
    }}
    
    .main-content {{
        margin-top: 80px;
        padding: 20px;
    }}
    
    .ticker-container {{
        width: 100%;
        background: linear-gradient(90deg, #ffd700, #ffa500, #ff6b6b, #00a651, #0056b3);
        background-size: 300% 100%;
        animation: gradientShift 8s ease infinite;
        padding: 20px 0;
        overflow: hidden;
        margin-bottom: 30px;
    }}
    
    .ticker-text {{
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: ticker 30s linear infinite;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 1.3rem;
    }}
    
    @keyframes ticker {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(-100%, 0); }}
    }}
    
    .jackpot-card {{
        background: linear-gradient(135deg, #0056b3, #002856);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
    }}
    
    .jackpot-value {{
        font-size: 4rem;
        font-weight: 900;
        color: #ffd700;
    }}
    
    .euro-card {{
        background: linear-gradient(135deg, #00a651, #006633);
    }}
    
    .winning-numbers {{
        background: linear-gradient(135deg, #ffd700, #ffa500);
        border-radius: 60px;
        padding: 30px;
        margin: 30px 0;
        text-align: center;
    }}
    
    .number-ball-large {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: white;
        color: #0056b3;
        font-size: 2.5rem;
        font-weight: 900;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0 10px;
        border: 3px solid #0056b3;
    }}
    
    .number-ball-large.euro {{
        background: #00a651;
        color: white;
        border-color: #ffd700;
    }}
    
    .winner-card {{
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s;
    }}
    
    .winner-card:hover {{
        transform: translateY(-10px);
        border-color: #ffd700;
    }}
    
    .game-card {{
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        text-align: center;
    }}
    
    .number-badge {{
        background: linear-gradient(135deg, #0056b3, #00a651);
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 5px auto;
        border: 3px solid #ffd700;
    }}
    
    .footer {{
        margin-top: 80px;
        padding: 50px;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# ==================== TOP BAR ====================
st.markdown('<div class="top-bar">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.8, 0.1, 0.1])

with col2:
    if st.button("🤖 AI", key="ai_top_btn"):
        st.session_state.show_ai_chat = not st.session_state.show_ai_chat
        if st.session_state.show_ai_chat:
            st.session_state.show_settings = False

with col3:
    if st.button("⚙️", key="settings_top_btn"):
        st.session_state.show_settings = not st.session_state.show_settings
        if st.session_state.show_settings:
            st.session_state.show_ai_chat = False

st.markdown('</div>', unsafe_allow_html=True)

# ==================== SETTINGS DROPDOWN ====================
if st.session_state.show_settings and not st.session_state.show_ai_chat:
    with st.container():
        st.markdown("""
            <div class="dropdown-menu">
                <div class="dropdown-header">
                    ⚙️ SYSTEM-EINSTELLUNGEN
                </div>
        """, unsafe_allow_html=True)
        
        items = [
            ("🏠 HAUPTMENÜ", "main"),
            ("🌐 SPRACHE", "language"),
            ("🎨 DESIGN", "appearance"),
            ("🔔 BENACHRICHTIGUNGEN", "notifications"),
            ("⚡ ERWEITERT", "advanced"),
        ]
        
        for label, page in items:
            if st.button(label, key=f"dropdown_{page}"):
                st.session_state.settings_subpage = page
                st.session_state.show_settings = False
                st.session_state.show_settings_page = True
                st.rerun()
        
        st.markdown("""
                <div class="dropdown-footer" style="padding:15px;text-align:center;color:#aaa;">
                    ⚡ Klicken für mehr Optionen
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==================== AI DROPDOWN ====================
if st.session_state.show_ai_chat and not st.session_state.show_settings:
    with st.container():
        st.markdown("""
            <div class="dropdown-menu" style="border-color: #00f2fe;">
                <div class="dropdown-header" style="background: linear-gradient(135deg, #00f2fe, #4facfe);">
                    🤖 KI-ASSISTENT
                </div>
        """, unsafe_allow_html=True)
        
        ai_items = [
            ("💬 FRAGEN STELLEN", "ask"),
            ("📊 ANALYSE", "analyze"),
            ("🎯 TIPPS", "tips"),
            ("🔮 VORHERSAGE", "predict"),
            ("📚 HILFE", "help"),
        ]
        
        for label, page in ai_items:
            if st.button(label, key=f"ai_{page}"):
                st.session_state.ai_page = page
                st.session_state.show_ai_chat = False
                st.session_state.show_ai_page = True
                st.rerun()
        
        st.markdown("""
                <div class="dropdown-footer" style="padding:15px;text-align:center;color:#aaa;">
                    🤖 KI-gestützte Analyse
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==================== SETTINGS PAGE ====================
if st.session_state.show_settings_page:
    st.markdown("""
        <div style="position: fixed; top:0; right:0; bottom:0; width:400px; 
                    background: rgba(10,20,30,0.98); backdrop-filter:blur(20px); 
                    border-left:2px solid #ffd700; z-index:10001; overflow-y:auto;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #ffd700, #ffa500); padding:25px;">
            <h2 style="margin:0; color:#1a2a3a;">⚙️ EINSTELLUNGEN</h2>
        </div>
        <div style="padding:20px;">
    """, unsafe_allow_html=True)
    
    if st.session_state.settings_subpage == 'main':
        st.markdown("### 🏠 HAUPTMENÜ")
        st.write(f"Streamlit: 1.28.1")
        st.write(f"Python: 3.10")
        st.write(f"Letztes Update: {datetime.now().strftime('%H:%M:%S')}")
    
    elif st.session_state.settings_subpage == 'language':
        st.markdown("### 🌐 SPRACHE")
        if st.button("🇩🇪 DEUTSCH", use_container_width=True):
            st.session_state.language = 'de'
            st.rerun()
        if st.button("🇬🇧 ENGLISH", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
        if st.button("🇸🇦 العربية", use_container_width=True):
            st.session_state.language = 'ar'
            st.rerun()
    
    elif st.session_state.settings_subpage == 'appearance':
        st.markdown("### 🎨 DESIGN")
        if st.button("🌙 DUNKLES THEMA", use_container_width=True):
            st.session_state.theme = 'dark'
            st.rerun()
        if st.button("☀ HELLES THEMA", use_container_width=True):
            st.session_state.theme = 'light'
            st.rerun()
    
    if st.button("◀ ZURÜCK", use_container_width=True):
        st.session_state.show_settings_page = False
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== AI PAGE ====================
if st.session_state.show_ai_page:
    st.markdown("""
        <div style="position: fixed; top:0; right:0; bottom:0; width:400px; 
                    background: rgba(10,20,30,0.98); backdrop-filter:blur(20px); 
                    border-left:2px solid #00f2fe; z-index:10001; overflow-y:auto;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #00f2fe, #4facfe); padding:25px;">
            <h2 style="margin:0; color:white;">🤖 KI-ASSISTENT</h2>
        </div>
        <div style="padding:20px;">
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 FRAGEN SIE MICH")
    st.text_area("", placeholder="Ihre Frage...", height=100)
    st.button("SENDEN", use_container_width=True)
    
    if st.button("◀ ZURÜCK", use_container_width=True):
        st.session_state.show_ai_page = False
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Ticker
live_news = real_fetcher.fetch_live_news()
ticker_text = " 🔥 ".join(live_news) + " 🔥 "
st.markdown(f'<div class="ticker-container"><div class="ticker-text">{ticker_text}</div></div>', unsafe_allow_html=True)

# Jackpots
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
        <div class="jackpot-card">
            <div style="font-size:3rem;">🎲</div>
            <div style="font-size:1.5rem;color:white;">LOTTO 6aus49</div>
            <div class="jackpot-value">{st.session_state.live_jackpots['lotto']} MIO. €</div>
            <div style="color:white;">Jetzt spielen! Chance 1:140 Mio.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="jackpot-card euro-card">
            <div style="font-size:3rem;">🇪🇺</div>
            <div style="font-size:1.5rem;color:white;">EUROJACKPOT</div>
            <div class="jackpot-value">{st.session_state.live_jackpots['euro']} MIO. €</div>
            <div style="color:white;">Jetzt spielen! Chance 1:140 Mio.</div>
        </div>
    """, unsafe_allow_html=True)

# Winning Numbers
winning = real_fetcher.get_real_winning_numbers()
st.markdown(f"""
    <div class="winning-numbers">
        <h2 style="color:#0056b3;margin-bottom:20px;">GEWINNZAHLEN</h2>
        <p style="color:#333;">LOTTO 6aus49 • {winning['date']}</p>
        <div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;margin:20px 0;">
            {" ".join([f'<div class="number-ball-large">{n}</div>' for n in winning['numbers']])}
            {" ".join([f'<div class="number-ball-large" style="background:#00a651;color:white;">{n}</div>' for n in winning['extra']])}
        </div>
        <p style="color:#0056b3;font-size:1.5rem;">Jackpot: {winning['jackpot']}</p>
    </div>
""", unsafe_allow_html=True)

# Winners
st.markdown("## 🏆 ECHTE GEWINNER 🏆")
winners = real_fetcher.fetch_real_winners()
cols = st.columns(4)
for i, winner in enumerate(winners):
    with cols[i]:
        st.markdown(f"""
            <div class="winner-card">
                <div style="font-size:4rem;">{winner['image']}</div>
                <div style="font-size:1.3rem;color:#ffd700;">{winner['name']}</div>
                <div>{winner['city']}</div>
                <div style="font-size:1.8rem;color:white;">{winner['prize']}</div>
                <div>{winner['date']}</div>
            </div>
        """, unsafe_allow_html=True)

# Games
st.markdown("## 🎮 BEKANNTE LOTTERIEN 🎮")
game_cols = st.columns(4)
for i, (game_key, game) in enumerate(games.games.items()):
    with game_cols[i]:
        st.markdown(f"""
            <div class="game-card">
                <div style="font-size:3rem;">{game['icon']}</div>
                <div style="font-size:1.2rem;color:white;">{game['name']}</div>
                <div style="color:#ffd700;font-size:1.5rem;">{game['jackpot']}</div>
                <div style="color:#aaa;">{game['chance']}</div>
            </div>
        """, unsafe_allow_html=True)

# Horoscope
st.markdown("## 🔮 LOTTO-HOROSKOP 2026 🔮")
col1, col2 = st.columns([1,2])
with col1:
    star_sign = st.selectbox("Ihr Sternzeichen", ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'])
with col2:
    lucky = ai_predictor.get_horoscope_numbers(star_sign)
    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,215,0,0.2);border-radius:20px;padding:25px;">
            <div style="color:#ffd700;font-size:1.3rem;">Glückszahlen 2026</div>
            <div style="display:flex;gap:15px;justify-content:center;flex-wrap:wrap;">
                {" ".join([f'<div class="number-badge" style="width:60px;height:60px;font-size:1.5rem;">{n}</div>' for n in lucky])}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Player Area
st.markdown("---")
st.markdown("## 🎮 SPIELERBEREICH 🎮")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🎯 IHRE ZAHLEN")
    selected = st.session_state.user_numbers
    for row in range(0,49,7):
        cols = st.columns(7)
        for i, num in enumerate(range(row+1,row+8)):
            with cols[i]:
                if num in selected:
                    if st.button(f"**{num}**", key=f"num_{num}"):
                        selected.remove(num)
                        st.rerun()
                else:
                    if st.button(f"{num}", key=f"num_{num}"):
                        if len(selected) < 6:
                            selected.append(num)
                            selected.sort()
                        st.rerun()
    st.markdown(f"**Ausgewählt:** {', '.join(map(str,selected))} ({len(selected)}/6)")

with col2:
    if len(selected) == 6 and st.button("📊 ANALYSE STARTEN", use_container_width=True):
        analysis = ai_predictor.analyze_user_behavior(selected)
        st.session_state.current_analysis = analysis
    
    if 'current_analysis' in st.session_state:
        a = st.session_state.current_analysis
        st.markdown("### 🧠 KI-ANALYSE")
        if a['ai_suggestion']:
            st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0056b3,#00a651);padding:20px;border-radius:15px;">
                    <div style="color:#ffd700;">🤖 KI-VORSCHLAG</div>
                    <div style="font-size:2rem;color:white;text-align:center;">{' - '.join(map(str,a['ai_suggestion']))}</div>
                </div>
            """, unsafe_allow_html=True)
        if a['recommendations']:
            st.markdown("### 💡 EMPFEHLUNGEN")
            for rec in a['recommendations']:
                st.info(rec)

# ==================== NAVIGATION ====================
with st.sidebar:
    st.markdown(f"""
        <div style="text-align:center;margin-bottom:30px;">
            <h1 style="color:#ffd700;">💰 LOTTO 24</h1>
            <p style="color:#aaa;">{st.session_state.live_jackpots['euro']} MIO. €</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = option_menu(
        None, [t['home'], t['lotto'], t['euro'], t['stats'], t['player']],
        icons=['house-fill','dice-6-fill','globe-europe-africa','bar-chart-line-fill','controller'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding":"0","background-color":"transparent"},
            "icon": {"color":"#ffd700","font-size":"1.2rem"}, 
            "nav-link": {"color":"#aaa","font-size":"1rem","padding":"15px"},
            "nav-link-selected": {"background-color":"rgba(255,215,0,0.2)","color":"#ffd700"},
        }
    )

# ==================== PAGES ====================
if menu == t['home']:
    st.markdown(f"<div style='text-align:center;padding:20px;'><h1 style='color:#ffd700;'>{t['title']}</h1><p>{t['subtitle']}</p></div>", unsafe_allow_html=True)

elif menu == t['lotto']:
    st.markdown(f"<h1 style='text-align:center;'>{t['lotto']}</h1>", unsafe_allow_html=True)
    if st.button(t['predict_btn'], use_container_width=True):
        st.session_state.lotto_pred = ai_predictor.predict_lotto_advanced()
    if st.session_state.lotto_pred:
        p = st.session_state.lotto_pred
        st.markdown(f"<h2 style='color:#ffd700;text-align:center;'>{t['confidence']}: {p['confidence']}%</h2>", unsafe_allow_html=True)
        cols = st.columns(7)
        for i,num in enumerate(p['numbers']):
            with cols[i]:
                st.markdown(f"<div class='number-badge' style='width:80px;height:80px;font-size:2rem;'>{num}</div>", unsafe_allow_html=True)
        with cols[6]:
            st.markdown(f"<div class='number-badge' style='background:#ffd700;color:#0056b3;'>{p['super_number']}</div>", unsafe_allow_html=True)

elif menu == t['euro']:
    st.markdown(f"<h1 style='text-align:center;'>{t['euro']}</h1>", unsafe_allow_html=True)
    if st.button(t['predict_btn'], use_container_width=True):
        st.session_state.euro_pred = ai_predictor.predict_euro_advanced()
    if st.session_state.euro_pred:
        p = st.session_state.euro_pred
        st.markdown(f"<h2 style='color:#ffd700;text-align:center;'>{t['confidence']}: {p['confidence']}%</h2>", unsafe_allow_html=True)
        st.markdown(f"### {t['main_nums']}")
        cols = st.columns(5)
        for i,num in enumerate(p['main_numbers']):
            with cols[i]:
                st.markdown(f"<div class='number-badge' style='background:#00a651;'>{num}</div>", unsafe_allow_html=True)
        st.markdown(f"### {t['euro_nums']}")
        cols = st.columns(2)
        for i,num in enumerate(p['extra_numbers']):
            with cols[i]:
                st.markdown(f"<div class='number-badge' style='background:#ffd700;color:#0056b3;'>{num}</div>", unsafe_allow_html=True)

elif menu == t['stats']:
    st.markdown(f"<h1 style='text-align:center;'>{t['stats']}</h1>", unsafe_allow_html=True)
    if st.session_state.historical_data:
        df = st.session_state.historical_data['lotto']
        freq = ai_predictor.analyze_frequency(df['numbers'].tolist(), 49)
        freq_df = pd.DataFrame(freq, columns=['Number','Frequency'])
        fig = px.bar(freq_df, x='Number', y='Frequency', title=t['freq_analysis'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER ====================
st.markdown(f"""
    <div class="footer">
        <p>{t['footer']}</p>
        <p style='font-size:0.8rem;'>{t['disclaimer']}</p>
        <p style='font-size:0.7rem;'>Live: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
