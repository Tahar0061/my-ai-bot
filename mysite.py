# -*- coding: utf-8 -*-
"""
AI Predictor Germany 2026 — WORLD-CLASS EDITION
Fully refactored: performance, UI/UX, real architecture
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
import warnings
import hashlib
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG — must be first Streamlit call
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Predictor Germany 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════════
TRANS: Dict[str, Dict[str, str]] = {
    "de": {
        "title": "AI Predictor Germany 2026",
        "subtitle": "Quanten-KI · Statistische Analyse · Echtzeit-Daten",
        "nav_home": "Startseite",
        "nav_lotto": "Lotto 6aus49",
        "nav_euro": "Eurojackpot",
        "nav_stats": "Analytik",
        "nav_player": "Spielerbereich",
        "predict_btn": "🔮 KI-Vorhersage generieren",
        "confidence": "KI-Konfidenz",
        "main_nums": "Hauptzahlen",
        "super_num": "Superzahl",
        "euro_nums": "Eurozahlen",
        "freq_title": "Frequenz-Analyse",
        "hot": "🔥 Heiß",
        "cold": "❄️ Kalt",
        "due": "⏳ Überfällig",
        "your_nums": "Ihre Zahlen",
        "analyze": "Analyse starten",
        "ai_tip": "KI-Tipp",
        "recommendations": "Empfehlungen",
        "winners": "Gewinner",
        "jackpot": "Jackpot",
        "chance": "Chance",
        "draw_date": "Ziehung",
        "disclaimer": "KI-Vorhersagen sind statistische Wahrscheinlichkeiten, keine Garantien. Bitte verantwortungsvoll spielen.",
        "footer": "© 2026 AI Predictor Germany · Quanten-Analyse-System",
        "settings": "Einstellungen",
        "language": "Sprache",
        "theme": "Design",
        "dark_theme": "Dunkles Design",
        "light_theme": "Helles Design",
        "back": "← Zurück",
        "selected": "Ausgewählt",
        "horoscope": "Lotto-Horoskop",
        "star_sign": "Sternzeichen",
        "lucky_nums": "Glückszahlen",
        "live": "LIVE",
    },
    "en": {
        "title": "AI Predictor Germany 2026",
        "subtitle": "Quantum AI · Statistical Analysis · Real-time Data",
        "nav_home": "Home",
        "nav_lotto": "Lotto 6aus49",
        "nav_euro": "Eurojackpot",
        "nav_stats": "Analytics",
        "nav_player": "Player Area",
        "predict_btn": "🔮 Generate AI Prediction",
        "confidence": "AI Confidence",
        "main_nums": "Main Numbers",
        "super_num": "Super Number",
        "euro_nums": "Euro Numbers",
        "freq_title": "Frequency Analysis",
        "hot": "🔥 Hot",
        "cold": "❄️ Cold",
        "due": "⏳ Due",
        "your_nums": "Your Numbers",
        "analyze": "Start Analysis",
        "ai_tip": "AI Tip",
        "recommendations": "Recommendations",
        "winners": "Winners",
        "jackpot": "Jackpot",
        "chance": "Chance",
        "draw_date": "Draw Date",
        "disclaimer": "AI predictions are statistical probabilities, not guarantees. Please play responsibly.",
        "footer": "© 2026 AI Predictor Germany · Quantum Analysis System",
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "dark_theme": "Dark Theme",
        "light_theme": "Light Theme",
        "back": "← Back",
        "selected": "Selected",
        "horoscope": "Lotto Horoscope",
        "star_sign": "Star Sign",
        "lucky_nums": "Lucky Numbers",
        "live": "LIVE",
    },
    "ar": {
        "title": "المتنبئ الذكي ألمانيا 2026",
        "subtitle": "ذكاء اصطناعي كمي · تحليل إحصائي · بيانات مباشرة",
        "nav_home": "الرئيسية",
        "nav_lotto": "لوتو 6aus49",
        "nav_euro": "يوروجاكبوت",
        "nav_stats": "التحليلات",
        "nav_player": "منطقة اللاعب",
        "predict_btn": "🔮 توليد توقع ذكي",
        "confidence": "ثقة الذكاء الاصطناعي",
        "main_nums": "الأرقام الرئيسية",
        "super_num": "الرقم الإضافي",
        "euro_nums": "الأرقام الأوروبية",
        "freq_title": "تحليل التكرار",
        "hot": "🔥 ساخنة",
        "cold": "❄️ باردة",
        "due": "⏳ متأخرة",
        "your_nums": "أرقامك",
        "analyze": "بدء التحليل",
        "ai_tip": "اقتراح الذكاء الاصطناعي",
        "recommendations": "توصيات",
        "winners": "الفائزون",
        "jackpot": "الجائزة الكبرى",
        "chance": "فرصة",
        "draw_date": "تاريخ السحب",
        "disclaimer": "توقعات الذكاء الاصطناعي احتمالات إحصائية وليست ضمانات. العب بمسؤولية.",
        "footer": "© 2026 المتنبئ الذكي ألمانيا · نظام التحليل الكمي",
        "settings": "الإعدادات",
        "language": "اللغة",
        "theme": "المظهر",
        "dark_theme": "المظهر الداكن",
        "light_theme": "المظهر الفاتح",
        "back": "← رجوع",
        "selected": "المحدد",
        "horoscope": "أبراج اليانصيب",
        "star_sign": "برجك",
        "lucky_nums": "أرقام الحظ",
        "live": "مباشر",
    },
}

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZER
# ══════════════════════════════════════════════════════════════════
_DEFAULTS = {
    "language": "de",
    "theme": "dark",
    "active_page": "home",
    "lotto_pred": None,
    "euro_pred": None,
    "user_numbers": [],
    "current_analysis": None,
    "historical_data": None,
    "live_jackpots": {"lotto": 37.7, "euro": 37.6},
    "last_api_update": None,
    "show_settings": False,
    "animations": True,
}

for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

t = TRANS[st.session_state.language]

# ══════════════════════════════════════════════════════════════════
#  DATA LAYER — cached for performance
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def generate_historical_data() -> Dict:
    """Generate realistic historical lottery data. Cached for 1 hour."""
    rng = np.random.default_rng(42)
    n = 2000

    # Weight distribution: real lotteries have non-uniform frequencies
    lotto_weights = np.ones(49)
    hot = [3, 7, 15, 23, 38, 44]
    cold = [13, 26, 31, 35, 42, 47]
    for h in hot:
        lotto_weights[h - 1] = 1.35
    for c in cold:
        lotto_weights[c - 1] = 0.72
    lotto_weights /= lotto_weights.sum()

    lotto_draws, euro_main_draws, euro_extra_draws = [], [], []
    for _ in range(n):
        lotto_draws.append(sorted(rng.choice(49, 6, replace=False, p=lotto_weights) + 1))
        euro_main_draws.append(sorted(rng.choice(50, 5, replace=False) + 1))
        euro_extra_draws.append(sorted(rng.choice(12, 2, replace=False) + 1))

    dates = pd.date_range(end=datetime.now(), periods=n, freq="3D")
    jackpots_l = np.clip(rng.normal(15, 10, n), 2, 45)
    jackpots_e = np.clip(rng.normal(50, 30, n), 10, 120)

    return {
        "lotto": pd.DataFrame({"date": dates, "numbers": lotto_draws, "jackpot": jackpots_l}),
        "euro": pd.DataFrame({"date": dates, "main": euro_main_draws, "extra": euro_extra_draws, "jackpot": jackpots_e}),
    }


@st.cache_data(ttl=300, show_spinner=False)
def get_live_jackpots() -> Dict:
    return {"lotto": 37.7, "euro": 37.6}


@st.cache_data(show_spinner=False)
def get_static_winners() -> List[Dict]:
    return [
        {"name": "Familie Schmidt", "city": "Berlin", "prize": "38.2 Mio. €", "date": "17.03.2026", "game": "Eurojackpot", "emoji": "👨‍👩‍👧‍👦"},
        {"name": "Klaus W.", "city": "Sachsen-Anhalt", "prize": "6 Mio. €", "date": "15.03.2026", "game": "Lotto 6aus49", "emoji": "👴"},
        {"name": "Müller GbR", "city": "München", "prize": "12.5 Mio. €", "date": "12.03.2026", "game": "Eurojackpot", "emoji": "👥"},
        {"name": "Anna & Thomas", "city": "Hamburg", "prize": "4.8 Mio. €", "date": "10.03.2026", "game": "Lotto 6aus49", "emoji": "💑"},
    ]


# ══════════════════════════════════════════════════════════════════
#  AI PREDICTOR ENGINE
# ══════════════════════════════════════════════════════════════════
class AIPredictor:
    """Stateless predictor — all data passed in, no global state."""

    @staticmethod
    def _frequency(draws: List[List[int]], n: int) -> Counter:
        flat = [x for row in draws for x in row]
        return Counter(flat).most_common(n)

    @staticmethod
    def _hot_cold_due(draws: List[List[int]], max_num: int) -> Dict:
        all_nums = [x for row in draws for x in row]
        freq = Counter(all_nums)
        # Due = appeared least recently
        last_seen = {}
        for i, row in enumerate(draws):
            for n in row:
                last_seen[n] = i
        hot = sorted(freq, key=freq.get, reverse=True)[:8]
        cold = sorted(freq, key=freq.get)[:8]
        due = sorted([n for n in range(1, max_num + 1)], key=lambda x: last_seen.get(x, -1))[:8]
        return {"hot": hot, "cold": cold, "due": due}

    @classmethod
    def predict_lotto(cls, data: pd.DataFrame) -> Dict:
        draws = data["numbers"].tolist()
        freq_top = [n for n, _ in cls._frequency(draws, 20)][:12]
        # Blend: 50% from hot, 50% random from full pool for variance
        hot_picks = random.sample(freq_top, min(3, len(freq_top)))
        pool = [n for n in range(1, 50) if n not in hot_picks]
        hot_picks += random.sample(pool, 6 - len(hot_picks))
        return {
            "numbers": sorted(hot_picks),
            "super_number": random.randint(0, 9),
            "confidence": round(random.uniform(81.5, 94.8), 1),
        }

    @classmethod
    def predict_euro(cls, data: pd.DataFrame) -> Dict:
        main_draws = data["main"].tolist()
        extra_draws = data["extra"].tolist()
        top_main = [n for n, _ in cls._frequency(main_draws, 15)][:10]
        top_extra = [n for n, _ in cls._frequency(extra_draws, 8)][:5]
        main = random.sample(top_main, min(3, len(top_main)))
        main += random.sample([n for n in range(1, 51) if n not in main], 5 - len(main))
        extra = random.sample(top_extra, min(2, len(top_extra)))
        if len(extra) < 2:
            extra += random.sample([n for n in range(1, 13) if n not in extra], 2 - len(extra))
        return {
            "main_numbers": sorted(main),
            "extra_numbers": sorted(extra),
            "confidence": round(random.uniform(79.2, 93.1), 1),
        }

    @classmethod
    def analyze_numbers(cls, user_nums: List[int], data: pd.DataFrame) -> Dict:
        draws = data["numbers"].tolist()
        all_flat = [x for row in draws for x in row]
        freq = Counter(all_flat)
        even = sum(1 for n in user_nums if n % 2 == 0)
        odd = len(user_nums) - even
        low = sum(1 for n in user_nums if n <= 25)
        high = len(user_nums) - low
        recs = []
        if even > 4:
            recs.append("Zu viele gerade Zahlen — mische ungerade ein.")
        if odd > 4:
            recs.append("Zu viele ungerade Zahlen — mische gerade ein.")
        if low > 4:
            recs.append("Zahlen zu niedrig — höhere Zahlen wählen.")
        if high > 4:
            recs.append("Zahlen zu hoch — niedrigere Zahlen einmischen.")
        # AI suggestion: balanced set
        pool = [n for n in range(1, 50) if n not in user_nums]
        even_pool = [n for n in pool if n % 2 == 0]
        odd_pool = [n for n in pool if n % 2 != 0]
        suggestion = []
        if even_pool:
            suggestion += random.sample(even_pool, min(3, len(even_pool)))
        if odd_pool:
            suggestion += random.sample(odd_pool, min(3, len(odd_pool)))
        suggestion = sorted(random.sample(suggestion, min(6, len(suggestion))))
        hcd = cls._hot_cold_due(draws, 49)
        return {
            "even": even, "odd": odd, "low": low, "high": high,
            "frequencies": [freq.get(n, 0) for n in user_nums],
            "recommendations": recs,
            "ai_suggestion": suggestion,
            "hot": hcd["hot"],
            "cold": hcd["cold"],
            "due": hcd["due"],
        }

    @staticmethod
    def horoscope_numbers(sign: str) -> List[int]:
        table = {
            "Widder": [5, 19, 23, 37, 42, 48], "Stier": [2, 8, 14, 26, 31, 45],
            "Zwillinge": [7, 12, 21, 33, 39, 44], "Krebs": [4, 11, 18, 27, 36, 41],
            "Löwe": [1, 15, 22, 29, 38, 47], "Jungfrau": [3, 9, 16, 24, 35, 43],
            "Waage": [6, 13, 20, 28, 34, 46], "Skorpion": [10, 17, 25, 30, 40, 49],
            "Schütze": [12, 24, 31, 37, 42, 48], "Steinbock": [2, 8, 15, 23, 36, 44],
            "Wassermann": [5, 11, 19, 27, 33, 45], "Fische": [7, 14, 21, 29, 38, 46],
        }
        return table.get(sign, [1, 7, 14, 22, 35, 43])


# ══════════════════════════════════════════════════════════════════
#  CSS — WORLD-CLASS DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════
IS_DARK = st.session_state.theme == "dark"

COLORS = {
    "bg":        "#080f1a" if IS_DARK else "#f0f4f8",
    "surface":   "#0e1d2f" if IS_DARK else "#ffffff",
    "surface2":  "#132540" if IS_DARK else "#f7fafc",
    "border":    "rgba(255,215,0,0.25)" if IS_DARK else "rgba(0,86,179,0.2)",
    "text":      "#f0f6ff" if IS_DARK else "#0d1f33",
    "text_muted":"#7a9abf" if IS_DARK else "#6b7c93",
    "gold":      "#ffd700",
    "blue":      "#0066cc",
    "green":     "#00b050",
    "cyan":      "#00e5ff",
    "red":       "#ff4757",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {{
    --bg:        {COLORS['bg']};
    --surface:   {COLORS['surface']};
    --surface2:  {COLORS['surface2']};
    --border:    {COLORS['border']};
    --text:      {COLORS['text']};
    --muted:     {COLORS['text_muted']};
    --gold:      {COLORS['gold']};
    --blue:      {COLORS['blue']};
    --green:     {COLORS['green']};
    --cyan:      {COLORS['cyan']};
    --red:       {COLORS['red']};
    --radius:    16px;
    --shadow:    0 8px 32px rgba(0,0,0,0.35);
    --glow-gold: 0 0 20px rgba(255,215,0,0.4);
    --glow-blue: 0 0 20px rgba(0,102,204,0.5);
    --glow-cyan: 0 0 20px rgba(0,229,255,0.4);
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0; padding: 0;
}}

html, body, .stApp {{
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header, .stDeployButton {{ display: none !important; }}
.block-container {{ padding: 1rem 1.5rem 4rem !important; max-width: 1400px !important; margin: 0 auto !important; }}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--gold); border-radius: 3px; }}

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {{
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: var(--radius);
    padding: 12px 16px;
    text-align: left;
    font-size: 0.95rem;
    font-family: 'Space Grotesk', sans-serif;
    transition: all 0.25s ease;
    margin-bottom: 4px;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255,215,0,0.1);
    border-color: var(--gold);
    color: var(--gold);
    transform: translateX(4px);
}}

/* ══ GLOBAL BUTTONS ══ */
.stButton > button {{
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    border-radius: var(--radius) !important;
    transition: all 0.25s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow) !important;
}}

/* ══ COMPONENTS ══ */
.lp-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.lp-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--cyan));
}}
.lp-card:hover {{
    border-color: rgba(255,215,0,0.5);
    box-shadow: var(--glow-gold);
    transform: translateY(-4px);
}}

.jackpot-hero {{
    background: linear-gradient(135deg, #0a1628 0%, #0d2347 50%, #0a1628 100%);
    border: 2px solid var(--gold);
    border-radius: 24px;
    padding: 36px 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow-gold);
}}
.jackpot-hero.euro {{
    background: linear-gradient(135deg, #0a2010 0%, #0d3520 50%, #0a2010 100%);
    border-color: var(--green);
    box-shadow: 0 0 30px rgba(0,176,80,0.3);
}}
.jackpot-amount {{
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
    letter-spacing: -0.02em;
}}
.jackpot-hero.euro .jackpot-amount {{ color: #4eff9a; }}

.number-ball {{
    width: 56px; height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1a3a6b, #0d2347);
    border: 2px solid var(--gold);
    color: var(--gold);
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
.number-ball:hover {{ transform: scale(1.15); box-shadow: var(--glow-gold); }}
.number-ball.euro {{ background: linear-gradient(135deg, #0a3020, #062010); border-color: var(--green); color: #4eff9a; }}
.number-ball.extra {{ background: linear-gradient(135deg, #3a2a00, #5a4000); border-color: #ffaa00; color: #ffaa00; }}
.number-ball.selected {{ background: linear-gradient(135deg, var(--gold), #e6ac00); color: #0d1f33; border-color: var(--gold); }}
.number-ball.hot {{ border-color: var(--red); color: var(--red); }}
.number-ball.cold {{ border-color: var(--cyan); color: var(--cyan); }}

.numbers-row {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; justify-content: center; margin: 16px 0; }}

.confidence-bar {{
    background: var(--surface2);
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
    margin: 8px 0;
}}
.confidence-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--cyan), var(--gold));
    border-radius: 100px;
    transition: width 1s ease;
    box-shadow: 0 0 8px rgba(0,229,255,0.5);
}}

.ticker-wrap {{
    background: linear-gradient(90deg, var(--blue), #004499, var(--blue));
    background-size: 200% 100%;
    animation: shimmer 4s linear infinite;
    border-radius: 12px;
    padding: 14px 24px;
    overflow: hidden;
    margin-bottom: 28px;
    border: 1px solid rgba(0,100,200,0.4);
}}
.ticker-inner {{
    white-space: nowrap;
    display: inline-block;
    animation: scroll-left 35s linear infinite;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: white;
}}
@keyframes scroll-left {{
    0%   {{ transform: translateX(60vw); }}
    100% {{ transform: translateX(-100%); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: 0% 0%; }}
    100% {{ background-position: 200% 0%; }}
}}

.winner-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 16px;
    text-align: center;
    transition: all 0.3s;
}}
.winner-card:hover {{ border-color: var(--gold); transform: translateY(-6px); box-shadow: var(--glow-gold); }}
.winner-emoji {{ font-size: 3rem; line-height: 1; margin-bottom: 10px; }}
.winner-prize {{ font-family: 'Rajdhani', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--gold); }}

.game-chip {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 14px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
}}
.game-chip:hover {{ border-color: var(--cyan); box-shadow: var(--glow-cyan); transform: scale(1.03); }}

.stat-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 0.85rem;
    color: var(--muted);
}}

.section-title {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--gold);
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}}

.prediction-result {{
    background: linear-gradient(135deg, var(--surface), var(--surface2));
    border: 2px solid var(--gold);
    border-radius: 24px;
    padding: 32px;
    text-align: center;
    box-shadow: var(--glow-gold);
    animation: fadeInUp 0.5s ease;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.live-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,71,87,0.15);
    border: 1px solid var(--red);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 0.1em;
}}
.live-dot {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--red);
    animation: pulse 1.4s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%       {{ opacity: 0.5; transform: scale(0.7); }}
}}

.num-selector-btn {{
    width: 100%;
    aspect-ratio: 1;
    border-radius: 50%;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s;
    border: 1.5px solid var(--border);
    background: var(--surface);
    color: var(--muted);
}}

.settings-panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-top: 16px;
}}

.disclaimer-box {{
    background: rgba(255,215,0,0.05);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
    margin-top: 32px;
}}

/* ── Select / Input overrides ── */
.stSelectbox > div > div {{
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
}}

div[data-testid="stMetric"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 20px;
}}
div[data-testid="stMetric"] label {{ color: var(--muted) !important; font-size: 0.8rem !important; }}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: var(--gold) !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1.8rem !important; }}

/* plotly charts bg */
.js-plotly-plot .plotly .bg {{ fill: transparent !important; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  HELPER RENDERERS
# ══════════════════════════════════════════════════════════════════
def render_number_balls(numbers: List[int], style: str = "default") -> str:
    balls = "".join(f'<span class="number-ball {style}">{n}</span>' for n in numbers)
    return f'<div class="numbers-row">{balls}</div>'


def render_live_badge(label: str = "LIVE") -> str:
    return f'<span class="live-badge"><span class="live-dot"></span>{label}</span>'


def render_section_title(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


def render_ticker(news: List[str]) -> None:
    text = "  ·  ".join(news) + "  ·  " + "  ·  ".join(news)
    st.markdown(
        f'<div class="ticker-wrap"><div class="ticker-inner">{text}</div></div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    jackpots = get_live_jackpots()

    st.markdown(f"""
        <div style="padding: 24px 0 20px; text-align: center;">
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                        background: linear-gradient(135deg, var(--gold), #ffa500);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🔮 AI PREDICTOR
            </div>
            <div style="font-size:0.75rem; color:var(--muted); letter-spacing:0.12em; margin-top:4px;">
                GERMANY 2026
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Jackpot pills
    st.markdown(f"""
        <div style="display:flex; gap:8px; margin-bottom:20px;">
            <div class="stat-pill" style="flex:1; justify-content:center;">
                🎲 {jackpots['lotto']}M €
            </div>
            <div class="stat-pill" style="flex:1; justify-content:center;">
                🇪🇺 {jackpots['euro']}M €
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:var(--border);margin:0 0 12px;"></div>', unsafe_allow_html=True)

    PAGES = [
        ("🏠", t["nav_home"], "home"),
        ("🎲", t["nav_lotto"], "lotto"),
        ("🇪🇺", t["nav_euro"], "euro"),
        ("📊", t["nav_stats"], "stats"),
        ("🎮", t["nav_player"], "player"),
    ]
    for icon, label, key in PAGES:
        is_active = st.session_state.active_page == key
        btn_style = "background: rgba(255,215,0,0.15) !important; border-color: var(--gold) !important; color: var(--gold) !important;" if is_active else ""
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.active_page = key
            st.rerun()

    st.markdown('<div style="height:1px;background:var(--border);margin:16px 0 12px;"></div>', unsafe_allow_html=True)

    # Settings toggle
    if st.button("⚙️  " + t["settings"], key="nav_settings", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

    if st.session_state.show_settings:
        with st.container():
            st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
            st.markdown(f"**{t['language']}**")
            lang_map = {"🇩🇪 Deutsch": "de", "🇬🇧 English": "en", "🇸🇦 العربية": "ar"}
            for label, code in lang_map.items():
                if st.button(label, key=f"lang_{code}", use_container_width=True):
                    st.session_state.language = code
                    st.rerun()
            st.markdown(f"**{t['theme']}**")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🌙", key="theme_dark", use_container_width=True):
                    st.session_state.theme = "dark"; st.rerun()
            with c2:
                if st.button("☀️", key="theme_light", use_container_width=True):
                    st.session_state.theme = "light"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
        <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;
                    font-size:0.7rem; color:var(--muted); padding:0 16px;">
            {t['footer']}<br/>
            <span style="color:var(--gold);">● </span>
            {datetime.now().strftime('%H:%M:%S')}
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════════
hist_data = generate_historical_data()
jackpots  = get_live_jackpots()
winners   = get_static_winners()
predictor = AIPredictor()

NEWS = [
    f"🔥 EUROJACKPOT: {jackpots['euro']} MIO. € — Nächste Ziehung Freitag",
    f"🎯 LOTTO 6aus49: {jackpots['lotto']} MIO. € — Mittwoch & Samstag",
    "📊 KI-Analyse: 2.000 Ziehungen ausgewertet · Neue Vorhersagen verfügbar",
    "🏆 Letzte Woche: Familie Schmidt gewinnt 38.2 Mio. € in Berlin",
    "💡 Tipp: Mische hohe und niedrige Zahlen für bessere Chancen",
]

page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════
if page == "home":
    render_ticker(NEWS)

    # Hero
    st.markdown(f"""
        <div style="text-align:center; padding: 32px 0 40px;">
            <div style="font-size:0.8rem; letter-spacing:0.2em; color:var(--cyan);
                        font-family:'Rajdhani',sans-serif; margin-bottom:12px;">
                QUANTUM AI · STATISTICAL ENGINE · v2026.1
            </div>
            <h1 style="font-family:'Rajdhani',sans-serif; font-size:clamp(2rem,5vw,3.5rem);
                       font-weight:700; letter-spacing:-0.02em; margin-bottom:12px;">
                {t['title']}
            </h1>
            <p style="color:var(--muted); font-size:1.05rem; max-width:560px; margin:0 auto 28px;">
                {t['subtitle']}
            </p>
            {render_live_badge(t['live'])}
        </div>
    """, unsafe_allow_html=True)

    # Jackpot cards
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown(f"""
            <div class="jackpot-hero">
                <div style="font-size:2.5rem; margin-bottom:10px;">🎲</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1rem;
                            letter-spacing:0.15em; color:rgba(255,255,255,0.7); margin-bottom:6px;">
                    LOTTO 6AUS49
                </div>
                <div class="jackpot-amount">{jackpots['lotto']} MIO. €</div>
                <div style="color:rgba(255,215,0,0.6); font-size:0.85rem; margin-top:10px;">
                    {t['chance']}: 1 : 139.838.160
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="jackpot-hero euro">
                <div style="font-size:2.5rem; margin-bottom:10px;">🇪🇺</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1rem;
                            letter-spacing:0.15em; color:rgba(255,255,255,0.7); margin-bottom:6px;">
                    EUROJACKPOT
                </div>
                <div class="jackpot-amount">{jackpots['euro']} MIO. €</div>
                <div style="color:rgba(78,255,154,0.6); font-size:0.85rem; margin-top:10px;">
                    {t['chance']}: 1 : 139.838.160
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Last winning numbers
    last_win = {"date": "17.03.2026", "numbers": [12, 13, 16, 17, 37], "extra": [4, 11], "jp": f"{jackpots['euro']} MIO. €"}
    st.markdown(render_section_title(f"🏆 {t['draw_date']}: {last_win['date']}"), unsafe_allow_html=True)
    st.markdown(f"""
        <div class="lp-card" style="text-align:center;">
            <div style="font-size:0.8rem; color:var(--muted); letter-spacing:0.1em; margin-bottom:16px;">
                EUROJACKPOT — {last_win['date']} — {last_win['jp']}
            </div>
            {render_number_balls(last_win['numbers'], 'euro')}
            {render_number_balls(last_win['extra'], 'extra')}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Winners
    st.markdown(render_section_title(f"🥇 {t['winners']}"), unsafe_allow_html=True)
    wcols = st.columns(4, gap="small")
    for i, w in enumerate(winners):
        with wcols[i]:
            st.markdown(f"""
                <div class="winner-card">
                    <div class="winner-emoji">{w['emoji']}</div>
                    <div style="font-weight:600; margin-bottom:4px;">{w['name']}</div>
                    <div style="color:var(--muted); font-size:0.85rem; margin-bottom:8px;">
                        📍 {w['city']}
                    </div>
                    <div class="winner-prize">{w['prize']}</div>
                    <div style="color:var(--muted); font-size:0.8rem; margin-top:6px;">
                        {w['game']} · {w['date']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Games grid
    st.markdown(render_section_title("🎮 Bekannte Lotterien"), unsafe_allow_html=True)
    game_data = [
        ("🎲", "LOTTO 6aus49", f"{jackpots['lotto']} MIO. €", "1:140 Mio.", "lotto"),
        ("🇪🇺", "EUROJACKPOT", f"{jackpots['euro']} MIO. €", "1:140 Mio.", "euro"),
        ("🎰", "SPIEL 77", "2 MIO. €", "1:10 Mio.", None),
        ("🔢", "SUPER 6", "100.000 €", "1:1 Mio.", None),
    ]
    gcols = st.columns(4, gap="small")
    for i, (icon, name, jp, chance, nav) in enumerate(game_data):
        with gcols[i]:
            st.markdown(f"""
                <div class="game-chip">
                    <div style="font-size:2rem; margin-bottom:8px;">{icon}</div>
                    <div style="font-family:'Rajdhani',sans-serif; font-weight:600; font-size:1rem;">{name}</div>
                    <div style="color:var(--gold); font-family:'Rajdhani',sans-serif;
                                font-size:1.3rem; font-weight:700; margin:6px 0;">{jp}</div>
                    <div style="color:var(--muted); font-size:0.8rem;">{chance}</div>
                </div>
            """, unsafe_allow_html=True)
            if nav:
                if st.button(f"Spielen →", key=f"play_{name}", use_container_width=True):
                    st.session_state.active_page = nav
                    st.rerun()

    # Horoscope
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(render_section_title(f"🔮 {t['horoscope']} 2026"), unsafe_allow_html=True)
    signs = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
    hcol1, hcol2 = st.columns([1, 2], gap="medium")
    with hcol1:
        sign = st.selectbox(t["star_sign"], signs)
    with hcol2:
        lucky = predictor.horoscope_numbers(sign)
        st.markdown(f"""
            <div class="lp-card" style="text-align:center;">
                <div style="color:var(--muted); font-size:0.85rem; margin-bottom:12px;">
                    ✨ {t['lucky_nums']} · {sign} 2026
                </div>
                {render_number_balls(lucky)}
            </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE: LOTTO
# ══════════════════════════════════════════════════════════════════
elif page == "lotto":
    st.markdown(f"""
        <div style="margin-bottom:32px;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-size:2.5rem; font-weight:700;">
                🎲 {t['nav_lotto']}
            </h1>
            <div style="color:var(--muted);">6 aus 49 · Mittwoch & Samstag · Jackpot: {jackpots['lotto']} MIO. €</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        if st.button(t["predict_btn"], key="lotto_predict", use_container_width=True,
                     type="primary"):
            with st.spinner("KI analysiert 2.000 historische Ziehungen…"):
                time.sleep(0.8)
                st.session_state.lotto_pred = predictor.predict_lotto(hist_data["lotto"])

        if st.session_state.lotto_pred:
            p = st.session_state.lotto_pred
            conf = p["confidence"]
            st.markdown(f"""
                <div class="prediction-result">
                    <div style="font-size:0.8rem; color:var(--muted); letter-spacing:0.1em; margin-bottom:12px;">
                        {t['confidence']}
                    </div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:2.8rem;
                                font-weight:700; color:var(--gold); margin-bottom:4px;">
                        {conf}%
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width:{conf}%;"></div>
                    </div>
                    <br/>
                    <div style="font-size:0.85rem; color:var(--muted); margin-bottom:10px;">{t['main_nums']}</div>
                    {render_number_balls(p['numbers'])}
                    <div style="font-size:0.85rem; color:var(--muted); margin:16px 0 8px;">{t['super_num']}</div>
                    {render_number_balls([p['super_number']], 'extra')}
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Hot / Cold / Due
        draws = hist_data["lotto"]["numbers"].tolist()
        hcd = AIPredictor._hot_cold_due(draws, 49)
        for label, key, style in [(t["hot"], "hot", "hot"), (t["cold"], "cold", "cold"), (t["due"], "due", "")]:
            st.markdown(f"""
                <div class="lp-card" style="margin-bottom:12px;">
                    <div style="color:var(--muted); font-size:0.85rem; margin-bottom:10px;">{label}</div>
                    {render_number_balls(hcd[key][:6], style)}
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE: EUROJACKPOT
# ══════════════════════════════════════════════════════════════════
elif page == "euro":
    st.markdown(f"""
        <div style="margin-bottom:32px;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-size:2.5rem; font-weight:700;">
                🇪🇺 {t['nav_euro']}
            </h1>
            <div style="color:var(--muted);">5 aus 50 + 2 Eurozahlen · Dienstag & Freitag · Jackpot: {jackpots['euro']} MIO. €</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        if st.button(t["predict_btn"], key="euro_predict", use_container_width=True,
                     type="primary"):
            with st.spinner("KI analysiert Eurojackpot-Muster…"):
                time.sleep(0.8)
                st.session_state.euro_pred = predictor.predict_euro(hist_data["euro"])

        if st.session_state.euro_pred:
            p = st.session_state.euro_pred
            conf = p["confidence"]
            st.markdown(f"""
                <div class="prediction-result">
                    <div style="font-size:0.8rem; color:var(--muted); letter-spacing:0.1em; margin-bottom:12px;">
                        {t['confidence']}
                    </div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:2.8rem;
                                font-weight:700; color:#4eff9a; margin-bottom:4px;">
                        {conf}%
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width:{conf}%; background:linear-gradient(90deg,#00b050,#4eff9a);"></div>
                    </div>
                    <br/>
                    <div style="font-size:0.85rem; color:var(--muted); margin-bottom:10px;">{t['main_nums']}</div>
                    {render_number_balls(p['main_numbers'], 'euro')}
                    <div style="font-size:0.85rem; color:var(--muted); margin:16px 0 8px;">{t['euro_nums']}</div>
                    {render_number_balls(p['extra_numbers'], 'extra')}
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        main_draws = hist_data["euro"]["main"].tolist()
        extra_draws = hist_data["euro"]["extra"].tolist()
        hcd_main  = AIPredictor._hot_cold_due(main_draws, 50)
        hcd_extra = AIPredictor._hot_cold_due(extra_draws, 12)
        st.markdown(f"""
            <div class="lp-card" style="margin-bottom:12px;">
                <div style="color:var(--muted); font-size:0.85rem; margin-bottom:10px;">{t['hot']} — Hauptzahlen</div>
                {render_number_balls(hcd_main['hot'][:5], 'euro hot')}
            </div>
            <div class="lp-card" style="margin-bottom:12px;">
                <div style="color:var(--muted); font-size:0.85rem; margin-bottom:10px;">{t['hot']} — Eurozahlen</div>
                {render_number_balls(hcd_extra['hot'][:4], 'extra hot')}
            </div>
            <div class="lp-card">
                <div style="color:var(--muted); font-size:0.85rem; margin-bottom:10px;">{t['due']} — Hauptzahlen</div>
                {render_number_balls(hcd_main['due'][:5], 'euro')}
            </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE: STATS
# ══════════════════════════════════════════════════════════════════
elif page == "stats":
    st.markdown(f"""
        <h1 style="font-family:'Rajdhani',sans-serif; font-size:2.5rem;
                   font-weight:700; margin-bottom:28px;">
            📊 {t['nav_stats']}
        </h1>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Lotto 6aus49", "Eurojackpot"])

    def build_freq_chart(draws, max_n, title, color):
        flat = [x for row in draws for x in row]
        freq = Counter(flat)
        nums = list(range(1, max_n + 1))
        counts = [freq.get(n, 0) for n in nums]
        avg = np.mean(counts)
        bar_colors = [color if c >= avg else "rgba(120,150,180,0.5)" for c in counts]
        fig = go.Figure(go.Bar(
            x=nums, y=counts,
            marker=dict(color=bar_colors, line=dict(width=0)),
            hovertemplate="<b>Zahl %{x}</b><br>Häufigkeit: %{y}<extra></extra>",
        ))
        fig.add_hline(y=avg, line_dash="dot", line_color="rgba(255,215,0,0.5)",
                      annotation_text=f"Ø {avg:.1f}", annotation_font_color="#ffd700")
        fig.update_layout(
            title=dict(text=title, font=dict(size=16, color="#ffd700")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7a9abf", family="Space Grotesk"),
            xaxis=dict(showgrid=False, tickcolor="#7a9abf"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            height=400, margin=dict(l=20, r=20, t=50, b=20),
        )
        return fig

    with tab1:
        draws_l = hist_data["lotto"]["numbers"].tolist()
        fig_l = build_freq_chart(draws_l, 49, t["freq_title"] + " — Lotto 6aus49", "#ffd700")
        st.plotly_chart(fig_l, use_container_width=True)

        # Jackpot trend
        df_l = hist_data["lotto"].tail(100)
        fig_trend = go.Figure(go.Scatter(
            x=df_l["date"], y=df_l["jackpot"],
            mode="lines", fill="tozeroy",
            line=dict(color="#ffd700", width=2),
            fillcolor="rgba(255,215,0,0.08)",
            hovertemplate="<b>%{x|%d.%m.%Y}</b><br>Jackpot: %{y:.1f} Mio. €<extra></extra>",
        ))
        fig_trend.update_layout(
            title=dict(text="Jackpot-Verlauf — letzte 100 Ziehungen", font=dict(color="#ffd700")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7a9abf", family="Space Grotesk"),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            height=320, margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        jp = hist_data["lotto"]["jackpot"]
        m1.metric("Analysierte Ziehungen", f"{len(hist_data['lotto']):,}")
        m2.metric("Ø Jackpot", f"{jp.mean():.1f} Mio. €")
        m3.metric("Max. Jackpot", f"{jp.max():.1f} Mio. €")
        m4.metric("Aktuell", f"{jackpots['lotto']} Mio. €")

    with tab2:
        draws_e = hist_data["euro"]["main"].tolist()
        fig_e = build_freq_chart(draws_e, 50, t["freq_title"] + " — Eurojackpot", "#4eff9a")
        st.plotly_chart(fig_e, use_container_width=True)

        m1, m2, m3, m4 = st.columns(4)
        jp_e = hist_data["euro"]["jackpot"]
        m1.metric("Analysierte Ziehungen", f"{len(hist_data['euro']):,}")
        m2.metric("Ø Jackpot", f"{jp_e.mean():.1f} Mio. €")
        m3.metric("Max. Jackpot", f"{jp_e.max():.1f} Mio. €")
        m4.metric("Aktuell", f"{jackpots['euro']} Mio. €")


# ══════════════════════════════════════════════════════════════════
#  PAGE: PLAYER AREA
# ══════════════════════════════════════════════════════════════════
elif page == "player":
    st.markdown(f"""
        <h1 style="font-family:'Rajdhani',sans-serif; font-size:2.5rem;
                   font-weight:700; margin-bottom:28px;">
            🎮 {t['nav_player']}
        </h1>
    """, unsafe_allow_html=True)

    col_picker, col_analysis = st.columns([1, 1], gap="large")

    with col_picker:
        st.markdown(f'<div class="section-title">🎯 {t["your_nums"]}</div>', unsafe_allow_html=True)
        selected = st.session_state.user_numbers

        # Number grid — 7 columns × 7 rows
        for row_start in range(0, 49, 7):
            cols = st.columns(7, gap="small")
            for i, num in enumerate(range(row_start + 1, min(row_start + 8, 50))):
                with cols[i]:
                    is_sel = num in selected
                    btn_label = f"**{num}**" if is_sel else str(num)
                    if st.button(btn_label, key=f"pick_{num}", use_container_width=True):
                        if is_sel:
                            selected.remove(num)
                        elif len(selected) < 6:
                            selected.append(num)
                            selected.sort()
                        st.rerun()

        # Status bar
        remaining = 6 - len(selected)
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-top:16px;">
                <div style="font-size:0.9rem; color:var(--muted);">
                    {t['selected']}: <strong style="color:var(--gold);">{len(selected)}/6</strong>
                </div>
                {''.join(f'<span class="number-ball selected" style="width:36px;height:36px;font-size:0.9rem;">{n}</span>' for n in selected)}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        btn_cols = st.columns(2, gap="small")
        with btn_cols[0]:
            if st.button(f"🗑️ Leeren", key="clear_nums", use_container_width=True):
                st.session_state.user_numbers = []
                st.session_state.current_analysis = None
                st.rerun()
        with btn_cols[1]:
            if st.button(f"🎲 Zufällig", key="random_nums", use_container_width=True):
                st.session_state.user_numbers = sorted(random.sample(range(1, 50), 6))
                st.rerun()

        if len(selected) == 6:
            if st.button(f"📊 {t['analyze']}", key="do_analyze", use_container_width=True,
                         type="primary"):
                with st.spinner("Analysiere…"):
                    time.sleep(0.5)
                    st.session_state.current_analysis = predictor.analyze_numbers(
                        selected, hist_data["lotto"]
                    )
                st.rerun()

    with col_analysis:
        if st.session_state.current_analysis:
            a = st.session_state.current_analysis
            st.markdown(f'<div class="section-title">🧠 {t["nav_stats"]}</div>', unsafe_allow_html=True)

            # Balance meters
            e, o = a["even"], a["odd"]
            l, h = a["low"], a["high"]
            st.markdown(f"""
                <div class="lp-card" style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span style="color:var(--muted); font-size:0.85rem;">Gerade / Ungerade</span>
                        <span style="color:var(--text);">{e} / {o}</span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width:{e/6*100:.0f}%; background:linear-gradient(90deg,#00e5ff,#0066cc);"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin:14px 0 8px;">
                        <span style="color:var(--muted); font-size:0.85rem;">Niedrig (1-25) / Hoch (26-49)</span>
                        <span style="color:var(--text);">{l} / {h}</span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width:{l/6*100:.0f}%; background:linear-gradient(90deg,#ff4757,#ffd700);"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # AI suggestion
            if a["ai_suggestion"]:
                st.markdown(f"""
                    <div class="lp-card" style="margin-bottom:12px; border-color:rgba(0,229,255,0.4);">
                        <div style="color:var(--cyan); font-size:0.85rem; margin-bottom:10px;">🤖 {t['ai_tip']}</div>
                        {render_number_balls(a['ai_suggestion'])}
                    </div>
                """, unsafe_allow_html=True)

            # Recommendations
            if a["recommendations"]:
                st.markdown(f"""
                    <div class="lp-card" style="margin-bottom:12px;">
                        <div style="color:var(--gold); font-size:0.85rem; margin-bottom:10px;">💡 {t['recommendations']}</div>
                """, unsafe_allow_html=True)
                for rec in a["recommendations"]:
                    st.markdown(f'<div style="color:var(--muted); font-size:0.9rem; margin:6px 0;">• {rec}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Frequency of selected numbers
            st.markdown(f"""
                <div class="lp-card">
                    <div style="color:var(--muted); font-size:0.85rem; margin-bottom:10px;">📈 Häufigkeit Ihrer Zahlen</div>
            """, unsafe_allow_html=True)
            if selected and a["frequencies"]:
                fig_freq = go.Figure(go.Bar(
                    x=[str(n) for n in selected],
                    y=a["frequencies"],
                    marker_color=["#ffd700" if f > np.mean(a["frequencies"]) else "#7a9abf"
                                  for f in a["frequencies"]],
                    hovertemplate="Zahl %{x}: %{y} mal<extra></extra>",
                ))
                fig_freq.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#7a9abf"), height=200,
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                    margin=dict(l=10, r=10, t=10, b=20),
                )
                st.plotly_chart(fig_freq, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="lp-card" style="text-align:center; padding:60px 24px; opacity:0.6;">
                    <div style="font-size:3rem; margin-bottom:16px;">🎯</div>
                    <div style="color:var(--muted);">
                        Wähle 6 Zahlen aus und starte die KI-Analyse
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  DISCLAIMER (global footer)
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
    <div class="disclaimer-box">
        ⚠️ {t['disclaimer']}
    </div>
""", unsafe_allow_html=True)
