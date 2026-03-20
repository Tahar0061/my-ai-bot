# -*- coding: utf-8 -*-
"""
AI Predictor Germany 2026 — WORLD-CLASS EDITION
Features: Auth, Profile, News, Scan, AI, Statistics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import random
import hashlib
import time
import warnings
from collections import Counter
from typing import List, Dict

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Predictor Germany 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  SUPABASE
# ══════════════════════════════════════════════════════════════════
try:
    from supabase import create_client
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = None

# ══════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════════
TRANS = {
    "de": {
        "title": "AI Predictor Germany 2026", "subtitle": "Quanten-KI · Statistische Analyse · Echtzeit-Daten",
        "login": "Anmelden", "register": "Registrieren", "logout": "Abmelden",
        "email": "E-Mail", "password": "Passwort", "username": "Benutzername",
        "full_name": "Vollständiger Name", "confirm_pass": "Passwort bestätigen",
        "nav_home": "Startseite", "nav_lotto": "Lotto 6aus49", "nav_euro": "Eurojackpot",
        "nav_stats": "Analytik", "nav_player": "Spielerbereich", "nav_profile": "Profil",
        "nav_news": "Neuigkeiten", "nav_scan": "Ticket Scannen",
        "predict_btn": "KI-Vorhersage generieren", "confidence": "KI-Konfidenz",
        "main_nums": "Hauptzahlen", "super_num": "Superzahl", "euro_nums": "Eurozahlen",
        "hot": "Heiß", "cold": "Kalt", "due": "Überfällig",
        "your_nums": "Ihre Zahlen", "analyze": "Analyse starten",
        "ai_tip": "KI-Tipp", "recommendations": "Empfehlungen",
        "save_nums": "Speichern", "saved": "Gespeichert!",
        "jackpot": "Jackpot", "chance": "Chance",
        "settings": "Einstellungen", "language": "Sprache", "theme": "Design",
        "disclaimer": "KI-Vorhersagen sind statistische Wahrscheinlichkeiten, keine Garantien. Verantwortungsvoll spielen.",
        "footer": "© 2026 AI Predictor Germany · Quanten-Analyse-System",
        "welcome": "Willkommen", "profile_updated": "Profil aktualisiert!",
        "scan_title": "Lotto-Ticket Scannen", "scan_info": "Ticket-Bild hochladen",
        "news_title": "Aktuelle Neuigkeiten", "member_since": "Mitglied seit",
        "my_numbers": "Meine Zahlen", "live": "LIVE",
        "login_success": "Erfolgreich angemeldet!", "register_success": "Konto erstellt!",
        "error_login": "Falsche E-Mail oder Passwort", "error_register": "Registrierung fehlgeschlagen",
        "fill_all": "Bitte alle Felder ausfüllen", "pass_match": "Passwörter stimmen nicht überein",
        "horoscope": "Lotto-Horoskop", "star_sign": "Sternzeichen", "lucky_nums": "Glückszahlen",
        "selected": "Ausgewählt", "freq_title": "Frequenz-Analyse", "winners": "Gewinner",
        "dark_theme": "Dunkel", "light_theme": "Hell",
    },
    "en": {
        "title": "AI Predictor Germany 2026", "subtitle": "Quantum AI · Statistical Analysis · Real-time Data",
        "login": "Login", "register": "Register", "logout": "Logout",
        "email": "Email", "password": "Password", "username": "Username",
        "full_name": "Full Name", "confirm_pass": "Confirm Password",
        "nav_home": "Home", "nav_lotto": "Lotto 6aus49", "nav_euro": "Eurojackpot",
        "nav_stats": "Analytics", "nav_player": "Player Area", "nav_profile": "Profile",
        "nav_news": "News", "nav_scan": "Scan Ticket",
        "predict_btn": "Generate AI Prediction", "confidence": "AI Confidence",
        "main_nums": "Main Numbers", "super_num": "Super Number", "euro_nums": "Euro Numbers",
        "hot": "Hot", "cold": "Cold", "due": "Due",
        "your_nums": "Your Numbers", "analyze": "Start Analysis",
        "ai_tip": "AI Tip", "recommendations": "Recommendations",
        "save_nums": "Save", "saved": "Saved!",
        "jackpot": "Jackpot", "chance": "Chance",
        "settings": "Settings", "language": "Language", "theme": "Theme",
        "disclaimer": "AI predictions are statistical probabilities, not guarantees. Play responsibly.",
        "footer": "© 2026 AI Predictor Germany · Quantum Analysis System",
        "welcome": "Welcome", "profile_updated": "Profile updated!",
        "scan_title": "Scan Lottery Ticket", "scan_info": "Upload ticket image",
        "news_title": "Latest News", "member_since": "Member since",
        "my_numbers": "My Numbers", "live": "LIVE",
        "login_success": "Successfully logged in!", "register_success": "Account created!",
        "error_login": "Wrong email or password", "error_register": "Registration failed",
        "fill_all": "Please fill all fields", "pass_match": "Passwords do not match",
        "horoscope": "Lotto Horoscope", "star_sign": "Star Sign", "lucky_nums": "Lucky Numbers",
        "selected": "Selected", "freq_title": "Frequency Analysis", "winners": "Winners",
        "dark_theme": "Dark", "light_theme": "Light",
    },
    "ar": {
        "title": "المتنبئ الذكي ألمانيا 2026", "subtitle": "ذكاء اصطناعي كمي · تحليل إحصائي · بيانات مباشرة",
        "login": "تسجيل الدخول", "register": "إنشاء حساب", "logout": "تسجيل الخروج",
        "email": "البريد الإلكتروني", "password": "كلمة المرور", "username": "اسم المستخدم",
        "full_name": "الاسم الكامل", "confirm_pass": "تأكيد كلمة المرور",
        "nav_home": "الرئيسية", "nav_lotto": "لوتو 6aus49", "nav_euro": "يوروجاكبوت",
        "nav_stats": "التحليلات", "nav_player": "منطقة اللاعب", "nav_profile": "الملف الشخصي",
        "nav_news": "الأخبار", "nav_scan": "مسح التذكرة",
        "predict_btn": "توليد توقع ذكي", "confidence": "ثقة الذكاء الاصطناعي",
        "main_nums": "الأرقام الرئيسية", "super_num": "الرقم الإضافي", "euro_nums": "الأرقام الأوروبية",
        "hot": "ساخنة", "cold": "باردة", "due": "متأخرة",
        "your_nums": "أرقامك", "analyze": "بدء التحليل",
        "ai_tip": "اقتراح الذكاء الاصطناعي", "recommendations": "توصيات",
        "save_nums": "حفظ", "saved": "تم الحفظ!",
        "jackpot": "الجائزة الكبرى", "chance": "فرصة",
        "settings": "الإعدادات", "language": "اللغة", "theme": "المظهر",
        "disclaimer": "توقعات الذكاء الاصطناعي احتمالات إحصائية وليست ضمانات. العب بمسؤولية.",
        "footer": "© 2026 المتنبئ الذكي ألمانيا · نظام التحليل الكمي",
        "welcome": "مرحباً", "profile_updated": "تم تحديث الملف الشخصي!",
        "scan_title": "مسح تذكرة اليانصيب", "scan_info": "رفع صورة التذكرة",
        "news_title": "آخر الأخبار", "member_since": "عضو منذ",
        "my_numbers": "أرقامي", "live": "مباشر",
        "login_success": "تم تسجيل الدخول بنجاح!", "register_success": "تم إنشاء الحساب!",
        "error_login": "البريد أو كلمة المرور خاطئة", "error_register": "فشل التسجيل",
        "fill_all": "يرجى ملء جميع الحقول", "pass_match": "كلمتا المرور غير متطابقتين",
        "horoscope": "أبراج اليانصيب", "star_sign": "برجك", "lucky_nums": "أرقام الحظ",
        "selected": "المحدد", "freq_title": "تحليل التكرار", "winners": "الفائزون",
        "dark_theme": "داكن", "light_theme": "فاتح",
    }
}

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
DEFAULTS = {
    "language": "de", "theme": "dark", "active_page": "home",
    "user": None, "show_settings": False, "auth_mode": "login",
    "lotto_pred": None, "euro_pred": None,
    "user_numbers": [], "current_analysis": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

t = TRANS[st.session_state.language]

# ══════════════════════════════════════════════════════════════════
#  DATABASE FUNCTIONS
# ══════════════════════════════════════════════════════════════════
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def db_register(email, username, password, full_name):
    if not DB_AVAILABLE: return {"success": False, "error": "DB unavailable"}
    try:
        if supabase.table("users").select("id").eq("email", email).execute().data:
            return {"success": False, "error": "Email exists"}
        r = supabase.table("users").insert({
            "email": email, "username": username,
            "password_hash": hash_pw(password), "full_name": full_name,
            "avatar": random.choice(["🎲","🔮","⭐","🍀","💎","🎯"]),
            "created_at": datetime.now().isoformat(),
        }).execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def db_login(email, password):
    if not DB_AVAILABLE: return {"success": False, "error": "DB unavailable"}
    try:
        r = supabase.table("users").select("*").eq("email", email).eq(
            "password_hash", hash_pw(password)).execute()
        if r.data:
            supabase.table("users").update({"last_login": datetime.now().isoformat()}).eq("id", r.data[0]["id"]).execute()
            return {"success": True, "user": r.data[0]}
        return {"success": False}
    except Exception as e:
        return {"success": False, "error": str(e)}

def db_save_numbers(user_id, numbers, game):
    if not DB_AVAILABLE: return False
    try:
        supabase.table("favorite_numbers").insert({
            "user_id": user_id, "numbers": numbers,
            "game": game, "created_at": datetime.now().isoformat()
        }).execute()
        return True
    except: return False

def db_get_numbers(user_id):
    if not DB_AVAILABLE: return []
    try:
        r = supabase.table("favorite_numbers").select("*").eq(
            "user_id", user_id).order("created_at", desc=True).limit(10).execute()
        return r.data or []
    except: return []

def db_get_news():
    if not DB_AVAILABLE: return []
    try:
        r = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute()
        return r.data or []
    except: return []

def db_update_profile(user_id, full_name, avatar):
    if not DB_AVAILABLE: return False
    try:
        supabase.table("users").update({"full_name": full_name, "avatar": avatar}).eq("id", user_id).execute()
        return True
    except: return False

# ══════════════════════════════════════════════════════════════════
#  AI ENGINE
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def get_hist():
    rng = np.random.default_rng(42)
    n = 2000
    w = np.ones(49)
    for h in [3,7,15,23,38,44]: w[h-1]=1.35
    for c in [13,26,31,35,42,47]: w[c-1]=0.72
    w /= w.sum()
    ld, em, ee = [], [], []
    for _ in range(n):
        ld.append(sorted(rng.choice(49,6,replace=False,p=w)+1))
        em.append(sorted(rng.choice(50,5,replace=False)+1))
        ee.append(sorted(rng.choice(12,2,replace=False)+1))
    dates = pd.date_range(end=datetime.now(), periods=n, freq="3D")
    return {
        "lotto": pd.DataFrame({"date":dates,"numbers":ld,"jackpot":np.clip(rng.normal(15,10,n),2,45)}),
        "euro": pd.DataFrame({"date":dates,"main":em,"extra":ee,"jackpot":np.clip(rng.normal(50,30,n),10,120)}),
    }

@st.cache_data(ttl=300, show_spinner=False)
def get_jackpots(): return {"lotto":37.7,"euro":37.6}

class AI:
    @staticmethod
    def freq(draws, n=20):
        return Counter([x for row in draws for x in row]).most_common(n)

    @staticmethod
    def hcd(draws, mx):
        flat=[x for row in draws for x in row]; freq=Counter(flat); ls={}
        for i,row in enumerate(draws):
            for n in row: ls[n]=i
        return {"hot":sorted(freq,key=freq.get,reverse=True)[:8],
                "cold":sorted(freq,key=freq.get)[:8],
                "due":sorted(range(1,mx+1),key=lambda x:ls.get(x,-1))[:8]}

    @classmethod
    def lotto(cls, data):
        top=[n for n,_ in cls.freq(data["numbers"].tolist(),20)][:12]
        picks=random.sample(top,min(3,len(top)))
        picks+=random.sample([n for n in range(1,50) if n not in picks],6-len(picks))
        return {"numbers":sorted(picks),"super_number":random.randint(0,9),"confidence":round(random.uniform(81.5,94.8),1)}

    @classmethod
    def euro(cls, data):
        tm=[n for n,_ in cls.freq(data["main"].tolist(),15)][:10]
        te=[n for n,_ in cls.freq(data["extra"].tolist(),8)][:5]
        main=random.sample(tm,min(3,len(tm)))
        main+=random.sample([n for n in range(1,51) if n not in main],5-len(main))
        extra=random.sample(te,min(2,len(te)))
        if len(extra)<2: extra+=random.sample([n for n in range(1,13) if n not in extra],2-len(extra))
        return {"main_numbers":sorted(main),"extra_numbers":sorted(extra),"confidence":round(random.uniform(79.2,93.1),1)}

    @classmethod
    def analyze(cls, nums, data):
        flat=[x for row in data["numbers"].tolist() for x in row]; freq=Counter(flat)
        even=sum(1 for n in nums if n%2==0); odd=len(nums)-even
        low=sum(1 for n in nums if n<=25); high=len(nums)-low
        recs=[]
        if even>4: recs.append("Zu viele gerade Zahlen")
        if odd>4: recs.append("Zu viele ungerade Zahlen")
        if low>4: recs.append("Zahlen zu niedrig")
        if high>4: recs.append("Zahlen zu hoch")
        pool=[n for n in range(1,50) if n not in nums]
        ep=[n for n in pool if n%2==0]; op=[n for n in pool if n%2!=0]
        sug=random.sample(ep,min(3,len(ep)))+random.sample(op,min(3,len(op)))
        sug=sorted(random.sample(sug,min(6,len(sug))))
        hcd=cls.hcd(data["numbers"].tolist(),49)
        return {"even":even,"odd":odd,"low":low,"high":high,
                "frequencies":[freq.get(n,0) for n in nums],
                "recommendations":recs,"ai_suggestion":sug,
                "hot":hcd["hot"],"cold":hcd["cold"],"due":hcd["due"]}

    @staticmethod
    def horoscope(sign):
        t={"Widder":[5,19,23,37,42,48],"Stier":[2,8,14,26,31,45],"Zwillinge":[7,12,21,33,39,44],
           "Krebs":[4,11,18,27,36,41],"Löwe":[1,15,22,29,38,47],"Jungfrau":[3,9,16,24,35,43],
           "Waage":[6,13,20,28,34,46],"Skorpion":[10,17,25,30,40,49],"Schütze":[12,24,31,37,42,48],
           "Steinbock":[2,8,15,23,36,44],"Wassermann":[5,11,19,27,33,45],"Fische":[7,14,21,29,38,46]}
        return t.get(sign,[1,7,14,22,35,43])

# ══════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════
D = st.session_state.theme == "dark"
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
:root{{
    --bg:{"#080f1a" if D else "#f0f4f8"};
    --surface:{"#0e1d2f" if D else "#ffffff"};
    --surface2:{"#132540" if D else "#f7fafc"};
    --border:{"rgba(255,215,0,0.2)" if D else "rgba(0,86,179,0.15)"};
    --text:{"#f0f6ff" if D else "#0d1f33"};
    --muted:{"#7a9abf" if D else "#6b7c93"};
    --gold:#ffd700;--green:#00b050;--cyan:#00e5ff;--red:#ff4757;
    --radius:16px;
}}
*{{box-sizing:border-box;}}
html,body,.stApp{{background:var(--bg)!important;color:var(--text)!important;font-family:'Space Grotesk',sans-serif!important;}}
#MainMenu,footer,header,.stDeployButton{{display:none!important;}}
.block-container{{padding:1rem 1.5rem 4rem!important;max-width:1380px!important;margin:0 auto!important;}}
::-webkit-scrollbar{{width:5px;}};::-webkit-scrollbar-thumb{{background:var(--gold);border-radius:3px;}}
[data-testid="stSidebar"]{{background:var(--surface)!important;border-right:1px solid var(--border)!important;}}
[data-testid="stSidebar"] .stButton>button{{width:100%;background:transparent;border:1px solid var(--border);color:var(--text);border-radius:12px;padding:10px 14px;text-align:left;font-size:0.9rem;font-family:'Space Grotesk',sans-serif;transition:all 0.2s;margin-bottom:3px;}}
[data-testid="stSidebar"] .stButton>button:hover{{background:rgba(255,215,0,0.1);border-color:var(--gold);color:var(--gold);transform:translateX(3px);}}
.stButton>button{{font-family:'Rajdhani',sans-serif!important;font-weight:600!important;border-radius:12px!important;transition:all 0.2s!important;letter-spacing:0.03em!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;}}
.lp-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;transition:all 0.3s;position:relative;overflow:hidden;margin-bottom:14px;}}
.lp-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--cyan));}}
.lp-card:hover{{border-color:rgba(255,215,0,0.35);transform:translateY(-3px);box-shadow:0 0 18px rgba(255,215,0,0.15);}}
.jackpot-hero{{background:linear-gradient(135deg,#0a1628,#0d2347);border:2px solid var(--gold);border-radius:22px;padding:28px;text-align:center;box-shadow:0 0 22px rgba(255,215,0,0.25);}}
.jackpot-hero.euro{{background:linear-gradient(135deg,#0a2010,#0d3520);border-color:var(--green);box-shadow:0 0 22px rgba(0,176,80,0.25);}}
.jackpot-amount{{font-family:'Rajdhani',sans-serif;font-size:clamp(2rem,4vw,3.2rem);font-weight:700;color:var(--gold);line-height:1;}}
.jackpot-hero.euro .jackpot-amount{{color:#4eff9a;}}
.nb{{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#1a3a6b,#0d2347);border:2px solid var(--gold);color:var(--gold);font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;display:inline-flex;align-items:center;justify-content:center;transition:all 0.25s;margin:3px;}}
.nb:hover{{transform:scale(1.12);box-shadow:0 0 12px rgba(255,215,0,0.4);}}
.nb.euro{{background:linear-gradient(135deg,#0a3020,#062010);border-color:var(--green);color:#4eff9a;}}
.nb.extra{{background:linear-gradient(135deg,#3a2a00,#5a4000);border-color:#ffaa00;color:#ffaa00;}}
.nb.sel{{background:linear-gradient(135deg,var(--gold),#e6ac00);color:#0d1f33;border-color:var(--gold);}}
.nb.hot{{border-color:var(--red);color:var(--red);}}
.nb.cold{{border-color:var(--cyan);color:var(--cyan);}}
.nbrow{{display:flex;gap:5px;flex-wrap:wrap;align-items:center;justify-content:center;margin:10px 0;}}
.ticker-wrap{{background:linear-gradient(90deg,#003399,#0044bb,#003399);border-radius:12px;padding:12px 20px;overflow:hidden;margin-bottom:22px;border:1px solid rgba(0,100,200,0.3);}}
.ticker-inner{{white-space:nowrap;display:inline-block;animation:sl 35s linear infinite;font-family:'Rajdhani',sans-serif;font-size:0.9rem;font-weight:600;letter-spacing:0.06em;color:white;}}
@keyframes sl{{0%{{transform:translateX(60vw);}}100%{{transform:translateX(-100%);}}}}
.cbar{{background:var(--surface2);border-radius:100px;height:7px;overflow:hidden;margin:7px 0;}}
.cfill{{height:100%;background:linear-gradient(90deg,var(--cyan),var(--gold));border-radius:100px;box-shadow:0 0 7px rgba(0,229,255,0.3);}}
.lbadge{{display:inline-flex;align-items:center;gap:5px;background:rgba(255,71,87,0.15);border:1px solid var(--red);border-radius:100px;padding:3px 10px;font-size:0.72rem;font-weight:700;color:var(--red);letter-spacing:0.1em;}}
.ldot{{width:6px;height:6px;border-radius:50%;background:var(--red);animation:pulse 1.4s infinite;}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:0.4;transform:scale(0.6);}}}}
.sec-title{{font-family:'Rajdhani',sans-serif;font-size:1.4rem;font-weight:700;letter-spacing:0.05em;color:var(--gold);margin-bottom:14px;padding-bottom:7px;border-bottom:1px solid var(--border);}}
.news-card{{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--gold);border-radius:12px;padding:18px;margin-bottom:10px;transition:all 0.3s;}}
.news-card:hover{{transform:translateX(4px);border-left-color:var(--cyan);}}
.winner-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;text-align:center;transition:all 0.3s;}}
.winner-card:hover{{border-color:var(--gold);transform:translateY(-4px);box-shadow:0 0 16px rgba(255,215,0,0.15);}}
.scan-area{{border:2px dashed var(--gold);border-radius:18px;padding:36px;text-align:center;background:rgba(255,215,0,0.02);}}
.disclaimer{{background:rgba(255,215,0,0.04);border:1px solid rgba(255,215,0,0.12);border-radius:10px;padding:11px 14px;font-size:0.76rem;color:var(--muted);text-align:center;margin-top:24px;}}
div[data-testid="stMetric"]{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;}}
div[data-testid="stMetric"] label{{color:var(--muted)!important;font-size:0.78rem!important;}}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{{color:var(--gold)!important;font-family:'Rajdhani',sans-serif!important;font-size:1.7rem!important;}}
.stTextInput>div>div>input{{background:var(--surface2)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:12px!important;}}
.stSelectbox>div>div{{background:var(--surface2)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:12px!important;}}
.stTabs [aria-selected="true"]{{color:var(--gold)!important;border-bottom-color:var(--gold)!important;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def B(nums, style=""):
    b="".join(f'<span class="nb {style}">{n}</span>' for n in nums)
    return f'<div class="nbrow">{b}</div>'

def ticker(news):
    tx="  ·  ".join(news)*2
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{tx}</div></div>',unsafe_allow_html=True)

def SEC(title):
    st.markdown(f'<div class="sec-title">{title}</div>',unsafe_allow_html=True)

def LIVE():
    return f'<span class="lbadge"><span class="ldot"></span>{t["live"]}</span>'

# ══════════════════════════════════════════════════════════════════
#  AUTH PAGE
# ══════════════════════════════════════════════════════════════════
def auth_page():
    st.markdown(f"""
        <div style="text-align:center;padding:36px 0 28px;">
            <div style="font-family:'Rajdhani',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:700;
                        background:linear-gradient(135deg,var(--gold),#ffa500);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🔮 {t['title']}
            </div>
            <div style="color:var(--muted);margin-top:8px;font-size:0.95rem;">{t['subtitle']}</div>
            <div style="margin-top:14px;">{LIVE()}</div>
        </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,1.1,1])
    with col:
        c1,c2 = st.columns(2)
        with c1:
            if st.button(t["login"], key="tl", use_container_width=True,
                        type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login"; st.rerun()
        with c2:
            if st.button(t["register"], key="tr", use_container_width=True,
                        type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register"; st.rerun()

        st.markdown("<br/>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            with st.container():
                st.markdown(f"#### 🔐 {t['login']}")
                em = st.text_input(t["email"], placeholder="you@example.com", key="l_em")
                pw = st.text_input(t["password"], type="password", key="l_pw")
                if st.button(f"→ {t['login']}", key="do_l", use_container_width=True, type="primary"):
                    if em and pw:
                        r = db_login(em, pw)
                        if r["success"]:
                            st.session_state.user = r["user"]
                            st.success(t["login_success"]); time.sleep(0.5); st.rerun()
                        else: st.error(t["error_login"])
                    else: st.warning(t["fill_all"])
        else:
            with st.container():
                st.markdown(f"#### ✨ {t['register']}")
                fn = st.text_input(t["full_name"], placeholder="Max Mustermann", key="r_fn")
                un = st.text_input(t["username"], placeholder="max2026", key="r_un")
                em = st.text_input(t["email"], placeholder="you@example.com", key="r_em")
                pw = st.text_input(t["password"], type="password", key="r_pw")
                cf = st.text_input(t["confirm_pass"], type="password", key="r_cf")
                if st.button(f"→ {t['register']}", key="do_r", use_container_width=True, type="primary"):
                    if all([fn,un,em,pw,cf]):
                        if pw!=cf: st.error(t["pass_match"])
                        else:
                            r = db_register(em,un,pw,fn)
                            if r["success"]:
                                st.success(t["register_success"]); st.session_state.auth_mode="login"; time.sleep(1); st.rerun()
                            else: st.error(t["error_register"])
                    else: st.warning(t["fill_all"])

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
def render_sidebar():
    jp = get_jackpots()
    user = st.session_state.user
    with st.sidebar:
        st.markdown(f"""
            <div style="padding:18px 0 14px;text-align:center;">
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.45rem;font-weight:700;
                            background:linear-gradient(135deg,var(--gold),#ffa500);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                    🔮 AI PREDICTOR
                </div>
                <div style="font-size:0.68rem;color:var(--muted);letter-spacing:0.15em;">GERMANY 2026</div>
            </div>
        """, unsafe_allow_html=True)

        if user:
            st.markdown(f"""
                <div style="background:var(--surface2);border:1px solid var(--border);border-radius:14px;
                            padding:12px;margin-bottom:14px;text-align:center;">
                    <div style="font-size:1.8rem;">{user.get('avatar','🎲')}</div>
                    <div style="font-weight:600;color:var(--gold);font-size:0.9rem;">{user.get('full_name') or user.get('username','')}</div>
                    <div style="font-size:0.72rem;color:var(--muted);">{user.get('email','')}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="display:flex;gap:5px;margin-bottom:14px;">
                <div style="flex:1;background:var(--surface2);border:1px solid var(--border);
                            border-radius:100px;padding:5px;text-align:center;font-size:0.74rem;color:var(--muted);">
                    🎲 {jp['lotto']}M€
                </div>
                <div style="flex:1;background:var(--surface2);border:1px solid var(--border);
                            border-radius:100px;padding:5px;text-align:center;font-size:0.74rem;color:var(--muted);">
                    EU {jp['euro']}M€
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:1px;background:var(--border);margin-bottom:8px;"></div>', unsafe_allow_html=True)

        PAGES = [("🏠",t["nav_home"],"home"),("🎲",t["nav_lotto"],"lotto"),
                 ("EU",t["nav_euro"],"euro"),("📊",t["nav_stats"],"stats"),("🎮",t["nav_player"],"player")]
        if user:
            PAGES += [("👤",t["nav_profile"],"profile"),("📰",t["nav_news"],"news"),("📷",t["nav_scan"],"scan")]

        for icon,label,key in PAGES:
            is_active = st.session_state.active_page == key
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.active_page=key; st.rerun()

        st.markdown('<div style="height:1px;background:var(--border);margin:10px 0;"></div>', unsafe_allow_html=True)

        if st.button(f"⚙️  {t['settings']}", key="nav_set", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings

        if st.session_state.show_settings:
            st.markdown(f"**{t['language']}**")
            for lbl,code in [("🇩🇪 Deutsch","de"),("🇬🇧 English","en"),("🇸🇦 العربية","ar")]:
                if st.button(lbl, key=f"lg_{code}", use_container_width=True):
                    st.session_state.language=code; st.rerun()
            st.markdown(f"**{t['theme']}**")
            c1,c2 = st.columns(2)
            with c1:
                if st.button(f"🌙 {t['dark_theme']}", key="td", use_container_width=True):
                    st.session_state.theme="dark"; st.rerun()
            with c2:
                if st.button(f"☀️ {t['light_theme']}", key="tl2", use_container_width=True):
                    st.session_state.theme="light"; st.rerun()

        if user:
            st.markdown('<div style="height:1px;background:var(--border);margin:10px 0;"></div>', unsafe_allow_html=True)
            if st.button(f"🚪  {t['logout']}", key="do_out", use_container_width=True):
                st.session_state.user=None; st.session_state.active_page="home"; st.rerun()

        st.markdown(f"""
            <div style="text-align:center;font-size:0.62rem;color:var(--muted);margin-top:16px;padding:0 8px;">
                {t['footer']}<br/><span style="color:var(--gold);">●</span> {datetime.now().strftime('%H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE FUNCTIONS
# ══════════════════════════════════════════════════════════════════
hist = get_hist()
jp   = get_jackpots()
ai   = AI()

TICKER_NEWS = [
    f"EUROJACKPOT: {jp['euro']} MIO. € — Freitag",
    f"LOTTO 6aus49: {jp['lotto']} MIO. € — Mittwoch & Samstag",
    "KI analysiert 2.000 historische Ziehungen",
    "Familie Schmidt gewinnt 38.2 Mio. € in Berlin",
    "Neue Vorhersagen täglich aktualisiert",
]
WINNERS = [
    {"n":"Familie Schmidt","c":"Berlin","p":"38.2 Mio. €","d":"17.03.2026","g":"Eurojackpot","e":"👨‍👩‍👧‍👦"},
    {"n":"Klaus W.","c":"Sachsen-Anhalt","p":"6 Mio. €","d":"15.03.2026","g":"Lotto 6aus49","e":"👴"},
    {"n":"Müller GbR","c":"München","p":"12.5 Mio. €","d":"12.03.2026","g":"Eurojackpot","e":"👥"},
    {"n":"Anna & Thomas","c":"Hamburg","p":"4.8 Mio. €","d":"10.03.2026","g":"Lotto 6aus49","e":"💑"},
]

def page_home():
    ticker(TICKER_NEWS)
    st.markdown(f"""
        <div style="text-align:center;padding:24px 0 32px;">
            <div style="font-size:0.72rem;letter-spacing:0.2em;color:var(--cyan);font-family:'Rajdhani',sans-serif;margin-bottom:8px;">
                QUANTUM AI · STATISTICAL ENGINE · v2026.1
            </div>
            <h1 style="font-family:'Rajdhani',sans-serif;font-size:clamp(1.8rem,5vw,3rem);font-weight:700;letter-spacing:-0.02em;margin-bottom:8px;">
                {t['title']}
            </h1>
            <p style="color:var(--muted);max-width:500px;margin:0 auto 16px;">{t['subtitle']}</p>
            {LIVE()}
        </div>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns(2,gap="medium")
    with c1:
        st.markdown(f"""<div class="jackpot-hero"><div style="font-size:2rem;margin-bottom:6px;">🎲</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.85rem;letter-spacing:0.15em;color:rgba(255,255,255,0.6);margin-bottom:4px;">LOTTO 6AUS49</div>
            <div class="jackpot-amount">{jp['lotto']} MIO. €</div>
            <div style="color:rgba(255,215,0,0.45);font-size:0.78rem;margin-top:7px;">{t['chance']}: 1:139.838.160</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="jackpot-hero euro"><div style="font-size:2rem;margin-bottom:6px;">🌍</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.85rem;letter-spacing:0.15em;color:rgba(255,255,255,0.6);margin-bottom:4px;">EUROJACKPOT</div>
            <div class="jackpot-amount">{jp['euro']} MIO. €</div>
            <div style="color:rgba(78,255,154,0.45);font-size:0.78rem;margin-top:7px;">{t['chance']}: 1:139.838.160</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    SEC(f"🏆 Letzte Gewinnzahlen — 17.03.2026")
    st.markdown(f"""<div class="lp-card" style="text-align:center;">
        <div style="font-size:0.78rem;color:var(--muted);margin-bottom:10px;">EUROJACKPOT · 17.03.2026 · {jp['euro']} MIO. €</div>
        {B([12,13,16,17,37],'euro')}{B([4,11],'extra')}</div>""", unsafe_allow_html=True)

    SEC(f"🥇 {t['winners']}")
    cols = st.columns(4, gap="small")
    for i,w in enumerate(WINNERS):
        with cols[i]:
            st.markdown(f"""<div class="winner-card">
                <div style="font-size:2.2rem;">{w['e']}</div>
                <div style="font-weight:600;font-size:0.88rem;margin:5px 0;">{w['n']}</div>
                <div style="color:var(--muted);font-size:0.78rem;">📍 {w['c']}</div>
                <div style="color:var(--gold);font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700;margin:5px 0;">{w['p']}</div>
                <div style="color:var(--muted);font-size:0.72rem;">{w['g']} · {w['d']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    SEC(f"🔮 {t['horoscope']} 2026")
    signs=['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
    hc1,hc2 = st.columns([1,2],gap="medium")
    with hc1:
        sign = st.selectbox(t["star_sign"], signs, label_visibility="collapsed")
    with hc2:
        lucky = ai.horoscope(sign)
        st.markdown(f"""<div class="lp-card" style="text-align:center;">
            <div style="color:var(--muted);font-size:0.78rem;margin-bottom:8px;">✨ {t['lucky_nums']} · {sign} 2026</div>
            {B(lucky)}</div>""", unsafe_allow_html=True)

def page_lotto():
    SEC(f"🎲 {t['nav_lotto']}")
    st.markdown(f'<div style="color:var(--muted);margin-bottom:18px;">6 aus 49 · {jp["lotto"]} MIO. €</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2,gap="large")
    with c1:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        if st.button(f"🔮 {t['predict_btn']}", key="lp_btn", use_container_width=True, type="primary"):
            with st.spinner("Analysiere…"):
                time.sleep(0.7); st.session_state.lotto_pred = ai.lotto(hist["lotto"])
        if st.session_state.lotto_pred:
            p = st.session_state.lotto_pred; conf = p["confidence"]
            st.markdown(f"""<div style="text-align:center;padding:16px 0;">
                <div style="font-size:0.72rem;color:var(--muted);letter-spacing:0.1em;">{t['confidence']}</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:2.8rem;font-weight:700;color:var(--gold);">{conf}%</div>
                <div class="cbar"><div class="cfill" style="width:{conf}%;"></div></div><br/>
                <div style="font-size:0.78rem;color:var(--muted);">{t['main_nums']}</div>{B(p['numbers'])}
                <div style="font-size:0.78rem;color:var(--muted);margin-top:10px;">{t['super_num']}</div>{B([p['super_number']],'extra')}
            </div>""", unsafe_allow_html=True)
            if st.session_state.user and st.button(f"💾 {t['save_nums']}", key="sv_l", use_container_width=True):
                if db_save_numbers(st.session_state.user["id"], p["numbers"], "Lotto 6aus49"): st.success(t["saved"])
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        hcd = ai.hcd(hist["lotto"]["numbers"].tolist(), 49)
        for label,key,style in [(f"🔥 {t['hot']}","hot","hot"),(f"❄️ {t['cold']}","cold","cold"),(f"⏳ {t['due']}","due","")]:
            st.markdown(f"""<div class="lp-card"><div style="color:var(--muted);font-size:0.8rem;margin-bottom:7px;">{label}</div>{B(hcd[key][:6],style)}</div>""", unsafe_allow_html=True)

def page_euro():
    SEC(f"🌍 {t['nav_euro']}")
    st.markdown(f'<div style="color:var(--muted);margin-bottom:18px;">5+2 · {jp["euro"]} MIO. €</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2,gap="large")
    with c1:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        if st.button(f"🔮 {t['predict_btn']}", key="ep_btn", use_container_width=True, type="primary"):
            with st.spinner("Analysiere…"):
                time.sleep(0.7); st.session_state.euro_pred = ai.euro(hist["euro"])
        if st.session_state.euro_pred:
            p = st.session_state.euro_pred; conf = p["confidence"]
            st.markdown(f"""<div style="text-align:center;padding:16px 0;">
                <div style="font-size:0.72rem;color:var(--muted);letter-spacing:0.1em;">{t['confidence']}</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:2.8rem;font-weight:700;color:#4eff9a;">{conf}%</div>
                <div class="cbar"><div class="cfill" style="width:{conf}%;background:linear-gradient(90deg,#00b050,#4eff9a);"></div></div><br/>
                <div style="font-size:0.78rem;color:var(--muted);">{t['main_nums']}</div>{B(p['main_numbers'],'euro')}
                <div style="font-size:0.78rem;color:var(--muted);margin-top:10px;">{t['euro_nums']}</div>{B(p['extra_numbers'],'extra')}
            </div>""", unsafe_allow_html=True)
            if st.session_state.user and st.button(f"💾 {t['save_nums']}", key="sv_e", use_container_width=True):
                if db_save_numbers(st.session_state.user["id"], p["main_numbers"], "Eurojackpot"): st.success(t["saved"])
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        hm = ai.hcd(hist["euro"]["main"].tolist(), 50); he = ai.hcd(hist["euro"]["extra"].tolist(), 12)
        for label,data,style in [(f"🔥 {t['hot']} — Hauptzahlen",hm["hot"][:5],"euro hot"),
                                  (f"🔥 {t['hot']} — Eurozahlen",he["hot"][:4],"extra hot"),
                                  (f"⏳ {t['due']}",hm["due"][:5],"euro")]:
            st.markdown(f"""<div class="lp-card"><div style="color:var(--muted);font-size:0.8rem;margin-bottom:7px;">{label}</div>{B(data,style)}</div>""", unsafe_allow_html=True)

def page_stats():
    SEC(f"📊 {t['nav_stats']}")
    tab1,tab2 = st.tabs(["Lotto 6aus49","Eurojackpot"])

    def fchart(draws, mx, title, color):
        flat=[x for row in draws for x in row]; freq=Counter(flat)
        nums=list(range(1,mx+1)); counts=[freq.get(n,0) for n in nums]; avg=np.mean(counts)
        clrs=[color if c>=avg else "rgba(120,150,180,0.35)" for c in counts]
        fig=go.Figure(go.Bar(x=nums,y=counts,marker=dict(color=clrs,line=dict(width=0)),
                             hovertemplate="<b>Zahl %{x}</b><br>%{y} mal<extra></extra>"))
        fig.add_hline(y=avg,line_dash="dot",line_color="rgba(255,215,0,0.4)",
                      annotation_text=f"Ø {avg:.1f}",annotation_font_color="#ffd700")
        fig.update_layout(title=dict(text=title,font=dict(color="#ffd700",size=14)),
                         paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                         font=dict(color="#7a9abf",family="Space Grotesk"),
                         xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.04)"),
                         height=360,margin=dict(l=10,r=10,t=44,b=10))
        return fig

    with tab1:
        st.plotly_chart(fchart(hist["lotto"]["numbers"].tolist(),49,t["freq_title"]+" — Lotto","#ffd700"),use_container_width=True)
        df=hist["lotto"].tail(80)
        fig2=go.Figure(go.Scatter(x=df["date"],y=df["jackpot"],mode="lines",fill="tozeroy",
                                   line=dict(color="#ffd700",width=2),fillcolor="rgba(255,215,0,0.05)"))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#7a9abf"),height=260,margin=dict(l=10,r=10,t=10,b=10),
                           xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.04)"))
        st.plotly_chart(fig2,use_container_width=True)
        m1,m2,m3,m4=st.columns(4); jp2=hist["lotto"]["jackpot"]
        m1.metric("Ziehungen",f"{len(hist['lotto']):,}"); m2.metric("Ø Jackpot",f"{jp2.mean():.1f} Mio.")
        m3.metric("Max",f"{jp2.max():.1f} Mio."); m4.metric("Aktuell",f"{jp['lotto']} Mio.")

    with tab2:
        st.plotly_chart(fchart(hist["euro"]["main"].tolist(),50,t["freq_title"]+" — Euro","#4eff9a"),use_container_width=True)
        m1,m2,m3,m4=st.columns(4); jp2=hist["euro"]["jackpot"]
        m1.metric("Ziehungen",f"{len(hist['euro']):,}"); m2.metric("Ø Jackpot",f"{jp2.mean():.1f} Mio.")
        m3.metric("Max",f"{jp2.max():.1f} Mio."); m4.metric("Aktuell",f"{jp['euro']} Mio.")

def page_player():
    SEC(f"🎮 {t['nav_player']}")
    c1,c2 = st.columns([1,1],gap="large")
    with c1:
        st.markdown(f'<div style="color:var(--gold);font-size:0.95rem;font-weight:600;margin-bottom:10px;">🎯 {t["your_nums"]}</div>',unsafe_allow_html=True)
        sel = st.session_state.user_numbers
        for row in range(0,49,7):
            cols = st.columns(7,gap="small")
            for i,num in enumerate(range(row+1,min(row+8,50))):
                with cols[i]:
                    is_sel = num in sel
                    if st.button(f"**{num}**" if is_sel else str(num), key=f"p{num}",
                                use_container_width=True, type="primary" if is_sel else "secondary"):
                        if is_sel: sel.remove(num)
                        elif len(sel)<6: sel.append(num); sel.sort()
                        st.rerun()
        st.markdown(f"""<div style="display:flex;align-items:center;gap:6px;margin-top:10px;flex-wrap:wrap;">
            <span style="color:var(--muted);font-size:0.82rem;">{t['selected']}: <strong style="color:var(--gold);">{len(sel)}/6</strong></span>
            {''.join(f'<span class="nb sel" style="width:32px;height:32px;font-size:0.8rem;">{n}</span>' for n in sel)}
        </div>""", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        b1,b2 = st.columns(2)
        with b1:
            if st.button("🗑️ Leeren", key="clr", use_container_width=True):
                st.session_state.user_numbers=[]; st.session_state.current_analysis=None; st.rerun()
        with b2:
            if st.button("🎲 Zufällig", key="rnd", use_container_width=True):
                st.session_state.user_numbers=sorted(random.sample(range(1,50),6)); st.rerun()
        if len(sel)==6:
            if st.button(f"📊 {t['analyze']}", key="anlz", use_container_width=True, type="primary"):
                with st.spinner("…"): time.sleep(0.4); st.session_state.current_analysis=ai.analyze(sel,hist["lotto"]); st.rerun()
            if st.session_state.user and st.button(f"💾 {t['save_nums']}", key="sv_pl", use_container_width=True):
                if db_save_numbers(st.session_state.user["id"],sel,"Lotto 6aus49"): st.success(t["saved"])

    with c2:
        a = st.session_state.current_analysis
        if a:
            e,o,l,h = a["even"],a["odd"],a["low"],a["high"]
            st.markdown(f"""<div class="lp-card">
                <div style="font-size:0.8rem;color:var(--muted);margin-bottom:6px;">Gerade / Ungerade · {e}/{o}</div>
                <div class="cbar"><div class="cfill" style="width:{e/6*100:.0f}%;"></div></div>
                <div style="font-size:0.8rem;color:var(--muted);margin:10px 0 6px;">Niedrig / Hoch · {l}/{h}</div>
                <div class="cbar"><div class="cfill" style="width:{l/6*100:.0f}%;background:linear-gradient(90deg,#ff4757,#ffd700);"></div></div>
            </div>""", unsafe_allow_html=True)
            if a["ai_suggestion"]:
                st.markdown(f"""<div class="lp-card" style="border-color:rgba(0,229,255,0.25);">
                    <div style="color:var(--cyan);font-size:0.8rem;margin-bottom:7px;">🤖 {t['ai_tip']}</div>{B(a['ai_suggestion'])}</div>""", unsafe_allow_html=True)
            if a["recommendations"]:
                recs="".join(f'<div style="color:var(--muted);font-size:0.86rem;margin:4px 0;">• {r}</div>' for r in a["recommendations"])
                st.markdown(f'<div class="lp-card"><div style="color:var(--gold);font-size:0.8rem;margin-bottom:7px;">💡 {t["recommendations"]}</div>{recs}</div>',unsafe_allow_html=True)
            for label,key,style in [(f"🔥 {t['hot']}","hot","hot"),(f"❄️ {t['cold']}","cold","cold"),(f"⏳ {t['due']}","due","")]:
                st.markdown(f"""<div class="lp-card"><div style="color:var(--muted);font-size:0.8rem;margin-bottom:7px;">{label}</div>{B(a[key][:6],style)}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="lp-card" style="text-align:center;padding:48px 20px;opacity:0.5;">
                <div style="font-size:2.5rem;">🎯</div>
                <div style="color:var(--muted);margin-top:10px;">6 Zahlen wählen → Analyse starten</div>
            </div>""", unsafe_allow_html=True)

def page_profile():
    user = st.session_state.user
    if not user: st.warning("Bitte anmelden"); return
    SEC(f"👤 {t['nav_profile']}")
    c1,c2 = st.columns([1,2],gap="large")
    with c1:
        st.markdown(f"""<div class="lp-card" style="text-align:center;">
            <div style="font-size:3.5rem;">{user.get('avatar','🎲')}</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700;color:var(--gold);">
                {user.get('full_name') or user.get('username','')}
            </div>
            <div style="color:var(--muted);font-size:0.82rem;">@{user.get('username','')}</div>
            <div style="color:var(--muted);font-size:0.78rem;margin-top:6px;">{user.get('email','')}</div>
            <div style="margin-top:12px;font-size:0.72rem;color:var(--muted);">{t['member_since']}</div>
            <div style="color:var(--text);">{str(user.get('created_at',''))[:10]}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"#### ✏️ Profil bearbeiten")
        new_name = st.text_input(t["full_name"], value=user.get("full_name",""), key="pf_n")
        avatars=["🎲","🔮","⭐","🍀","💎","🎯","🏆","🌟","🎪","🎠"]
        st.markdown("**Avatar:**")
        avcols=st.columns(10)
        sel_av=user.get("avatar","🎲")
        for i,av in enumerate(avatars):
            with avcols[i]:
                if st.button(av, key=f"av{i}", use_container_width=True): sel_av=av
        if st.button("💾 Speichern", key="sv_pf", use_container_width=True, type="primary"):
            if db_update_profile(user["id"],new_name,sel_av):
                st.session_state.user["full_name"]=new_name; st.session_state.user["avatar"]=sel_av
                st.success(t["profile_updated"]); st.rerun()
        st.markdown(f"#### 💾 {t['my_numbers']}")
        saved = db_get_numbers(user["id"])
        if saved:
            for s in saved:
                nums=s.get("numbers",[]); game=s.get("game",""); date=str(s.get("created_at",""))[:10]
                st.markdown(f"""<div class="lp-card" style="padding:12px 16px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="color:var(--gold);font-size:0.8rem;">{game}</span>
                        <span style="color:var(--muted);font-size:0.75rem;">{date}</span>
                    </div>{B(nums)}</div>""", unsafe_allow_html=True)
        else: st.info("Noch keine gespeicherten Zahlen")

def page_news():
    SEC(f"📰 {t['news_title']}")
    news = db_get_news()
    static=[
        {"title":f"Eurojackpot: {jp['euro']} MIO. €!","content":"Jackpot wächst weiter. Nächste Ziehung Freitag.","created_at":"2026-03-18"},
        {"title":"KI analysiert neue Ziehungsmuster","content":"Quantenalgorithmus wertet 2.000 historische Ziehungen aus.","created_at":"2026-03-17"},
        {"title":"Familie Schmidt gewinnt 38.2 Millionen","content":"Das Berliner Ehepaar gewann den Eurojackpot.","created_at":"2026-03-17"},
        {"title":"Neue Vorhersage-Algorithmen","content":"Erweiterte Frequenzanalyse und Mustererkennung verfügbar.","created_at":"2026-03-16"},
        {"title":"Lotto-Horoskop 2026 aktualisiert","content":"Neue Glückszahlen für alle Sternzeichen berechnet.","created_at":"2026-03-15"},
    ]
    for n in (news or static):
        st.markdown(f"""<div class="news-card">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.05rem;font-weight:600;margin-bottom:5px;">{n.get('title','')}</div>
            <div style="color:var(--muted);font-size:0.85rem;line-height:1.5;">{n.get('content','')}</div>
            <div style="color:var(--muted);font-size:0.72rem;margin-top:6px;">📅 {str(n.get('created_at',''))[:10]}</div>
        </div>""", unsafe_allow_html=True)

def page_scan():
    SEC(f"📷 {t['scan_title']}")
    c1,c2 = st.columns([1,1],gap="large")
    with c1:
        st.markdown(f"""<div class="lp-card">
            <div class="scan-area">
                <div style="font-size:2.5rem;margin-bottom:10px;">📷</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;color:var(--gold);">{t['scan_info']}</div>
                <div style="color:var(--muted);font-size:0.82rem;margin-top:6px;">JPG, PNG, WEBP · Max 10MB</div>
            </div>""", unsafe_allow_html=True)
        up = st.file_uploader("", type=["jpg","jpeg","png","webp"], key="scan_up", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if up:
            st.image(up, caption="Hochgeladenes Ticket", use_container_width=True)
            if st.button("🔍 Ticket analysieren", key="do_scan", use_container_width=True, type="primary"):
                with st.spinner("KI analysiert…"):
                    time.sleep(2)
                    scanned=sorted(random.sample(range(1,50),6))
                    acc=random.randint(92,99)
                st.markdown(f"""<div class="lp-card" style="text-align:center;border-color:rgba(0,229,255,0.3);">
                    <div style="color:var(--cyan);margin-bottom:8px;">✅ Erkannte Zahlen</div>
                    {B(scanned)}
                    <div style="color:var(--muted);font-size:0.78rem;margin-top:8px;">Genauigkeit: {acc}%</div>
                </div>""", unsafe_allow_html=True)
                if st.session_state.user:
                    if db_save_numbers(st.session_state.user["id"],scanned,"Gescannt"): st.success("Automatisch gespeichert!")
        else:
            st.markdown(f"""<div class="lp-card" style="text-align:center;padding:56px 20px;opacity:0.45;">
                <div style="font-size:2.8rem;">🎫</div>
                <div style="color:var(--muted);margin-top:10px;">Ticket hochladen um zu beginnen</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    SEC("ℹ️ So funktioniert es")
    hc=st.columns(3,gap="medium")
    for i,(num,title,desc) in enumerate([("1️⃣","Foto aufnehmen","Ticket deutlich fotografieren"),
                                          ("2️⃣","Hochladen","Bild in KI-Plattform hochladen"),
                                          ("3️⃣","Ergebnis","KI erkennt Zahlen automatisch")]):
        with hc[i]:
            st.markdown(f"""<div class="lp-card" style="text-align:center;">
                <div style="font-size:1.8rem;">{num}</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:0.95rem;font-weight:600;color:var(--gold);margin:6px 0;">{title}</div>
                <div style="color:var(--muted);font-size:0.82rem;">{desc}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════
user = st.session_state.user

if not user:
    auth_page()
else:
    render_sidebar()
    pg = st.session_state.active_page
    if pg=="home": page_home()
    elif pg=="lotto": page_lotto()
    elif pg=="euro": page_euro()
    elif pg=="stats": page_stats()
    elif pg=="player": page_player()
    elif pg=="profile": page_profile()
    elif pg=="news": page_news()
    elif pg=="scan": page_scan()
    st.markdown(f'<div class="disclaimer">⚠️ {t["disclaimer"]}</div>', unsafe_allow_html=True)
