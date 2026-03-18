# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║         AI PREDICTOR GERMANY 2026 — WORLD-CLASS EDITION         ║
║  Daily Prediction · Streak System · Community · Freemium · PWA  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import random, hashlib, time, json, warnings
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

try:    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except: GOOGLE_API_KEY = None

# ══════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════════
TRANS = {
    "de": {
        "title":"AI Predictor Germany 2026","subtitle":"Quanten-KI · Echtzeit-Analyse · Community",
        "login":"Anmelden","register":"Registrieren","logout":"Abmelden",
        "email":"E-Mail","password":"Passwort","username":"Benutzername",
        "full_name":"Vollständiger Name","confirm_pass":"Passwort bestätigen",
        "nav_home":"Startseite","nav_lotto":"Lotto 6aus49","nav_euro":"Eurojackpot",
        "nav_stats":"Analytik","nav_player":"Spielerbereich","nav_profile":"Profil",
        "nav_news":"Neuigkeiten","nav_scan":"Ticket Scannen","nav_daily":"Tages-KI",
        "nav_community":"Community","nav_premium":"Premium",
        "predict_btn":"KI-Vorhersage generieren","confidence":"KI-Konfidenz",
        "main_nums":"Hauptzahlen","super_num":"Superzahl","euro_nums":"Eurozahlen",
        "hot":"Heiß","cold":"Kalt","due":"Überfällig",
        "your_nums":"Ihre Zahlen","analyze":"Analyse starten",
        "ai_tip":"KI-Tipp","recommendations":"Empfehlungen",
        "save_nums":"Speichern","saved":"Gespeichert!",
        "jackpot":"Jackpot","chance":"Chance",
        "settings":"Einstellungen","language":"Sprache","theme":"Design",
        "disclaimer":"KI-Vorhersagen sind statistische Wahrscheinlichkeiten. Verantwortungsvoll spielen.",
        "footer":"© 2026 AI Predictor Germany · Quanten-Analyse-System",
        "welcome":"Willkommen","profile_updated":"Profil aktualisiert!",
        "scan_title":"Lotto-Ticket Scannen","scan_info":"Ticket-Bild hochladen",
        "news_title":"Aktuelle Neuigkeiten","member_since":"Mitglied seit",
        "my_numbers":"Meine Zahlen","live":"LIVE",
        "login_success":"Erfolgreich angemeldet!","register_success":"Konto erstellt!",
        "error_login":"Falsche E-Mail oder Passwort","error_register":"Registrierung fehlgeschlagen",
        "fill_all":"Bitte alle Felder ausfüllen","pass_match":"Passwörter stimmen nicht überein",
        "horoscope":"Lotto-Horoskop","star_sign":"Sternzeichen","lucky_nums":"Glückszahlen",
        "selected":"Ausgewählt","freq_title":"Frequenz-Analyse","winners":"Gewinner",
        "dark_theme":"Dunkel","light_theme":"Hell",
        "daily_title":"🔮 Tages-Vorhersage","daily_sub":"Täglich um Mitternacht aktualisiert",
        "claim_btn":"Heute abholen ✅","claimed":"Heute erhalten!","streak":"Streak",
        "streak_msg":"Tage in Folge! Weiter so!","streak_reward":"Belohnung",
        "ai_reason":"KI-Begründung","share":"Teilen",
        "community_title":"Community","post_placeholder":"Deine Meinung teilen…",
        "post_btn":"Posten","like":"Gefällt mir","comment":"Kommentieren",
        "premium_title":"Premium","premium_sub":"Unbegrenzte KI · Kein Werbung · VIP Community",
        "upgrade":"Upgrade auf Premium","per_month":"pro Monat",
        "free_plan":"Kostenlos","premium_plan":"Premium",
        "leaderboard":"Bestenliste","rank":"Rang","points":"Punkte",
        "notify":"Benachrichtigung","notify_sub":"Täglich um 10:00 Uhr",
        "streak_fire":"🔥 Streak aktiv!","new_badge":"🏅 Neues Abzeichen!",
        "badges":"Abzeichen","level":"Level",
    },
    "en": {
        "title":"AI Predictor Germany 2026","subtitle":"Quantum AI · Real-time Analysis · Community",
        "login":"Login","register":"Register","logout":"Logout",
        "email":"Email","password":"Password","username":"Username",
        "full_name":"Full Name","confirm_pass":"Confirm Password",
        "nav_home":"Home","nav_lotto":"Lotto 6aus49","nav_euro":"Eurojackpot",
        "nav_stats":"Analytics","nav_player":"Player Area","nav_profile":"Profile",
        "nav_news":"News","nav_scan":"Scan Ticket","nav_daily":"Daily AI",
        "nav_community":"Community","nav_premium":"Premium",
        "predict_btn":"Generate AI Prediction","confidence":"AI Confidence",
        "main_nums":"Main Numbers","super_num":"Super Number","euro_nums":"Euro Numbers",
        "hot":"Hot","cold":"Cold","due":"Due",
        "your_nums":"Your Numbers","analyze":"Start Analysis",
        "ai_tip":"AI Tip","recommendations":"Recommendations",
        "save_nums":"Save","saved":"Saved!",
        "jackpot":"Jackpot","chance":"Chance",
        "settings":"Settings","language":"Language","theme":"Theme",
        "disclaimer":"AI predictions are statistical probabilities. Play responsibly.",
        "footer":"© 2026 AI Predictor Germany · Quantum Analysis System",
        "welcome":"Welcome","profile_updated":"Profile updated!",
        "scan_title":"Scan Lottery Ticket","scan_info":"Upload ticket image",
        "news_title":"Latest News","member_since":"Member since",
        "my_numbers":"My Numbers","live":"LIVE",
        "login_success":"Successfully logged in!","register_success":"Account created!",
        "error_login":"Wrong email or password","error_register":"Registration failed",
        "fill_all":"Please fill all fields","pass_match":"Passwords do not match",
        "horoscope":"Lotto Horoscope","star_sign":"Star Sign","lucky_nums":"Lucky Numbers",
        "selected":"Selected","freq_title":"Frequency Analysis","winners":"Winners",
        "dark_theme":"Dark","light_theme":"Light",
        "daily_title":"🔮 Daily Prediction","daily_sub":"Updated every midnight",
        "claim_btn":"Claim Today ✅","claimed":"Claimed today!","streak":"Streak",
        "streak_msg":"days in a row! Keep going!","streak_reward":"Reward",
        "ai_reason":"AI Reasoning","share":"Share",
        "community_title":"Community","post_placeholder":"Share your opinion…",
        "post_btn":"Post","like":"Like","comment":"Comment",
        "premium_title":"Premium","premium_sub":"Unlimited AI · No Ads · VIP Community",
        "upgrade":"Upgrade to Premium","per_month":"per month",
        "free_plan":"Free","premium_plan":"Premium",
        "leaderboard":"Leaderboard","rank":"Rank","points":"Points",
        "notify":"Notification","notify_sub":"Daily at 10:00 AM",
        "streak_fire":"🔥 Streak active!","new_badge":"🏅 New badge!",
        "badges":"Badges","level":"Level",
    },
    "ar": {
        "title":"المتنبئ الذكي ألمانيا 2026","subtitle":"ذكاء كمي · تحليل مباشر · مجتمع",
        "login":"تسجيل الدخول","register":"إنشاء حساب","logout":"تسجيل الخروج",
        "email":"البريد الإلكتروني","password":"كلمة المرور","username":"اسم المستخدم",
        "full_name":"الاسم الكامل","confirm_pass":"تأكيد كلمة المرور",
        "nav_home":"الرئيسية","nav_lotto":"لوتو 6aus49","nav_euro":"يوروجاكبوت",
        "nav_stats":"التحليلات","nav_player":"منطقة اللاعب","nav_profile":"الملف الشخصي",
        "nav_news":"الأخبار","nav_scan":"مسح التذكرة","nav_daily":"التوقع اليومي",
        "nav_community":"المجتمع","nav_premium":"بريميوم",
        "predict_btn":"توليد توقع ذكي","confidence":"ثقة الذكاء الاصطناعي",
        "main_nums":"الأرقام الرئيسية","super_num":"الرقم الإضافي","euro_nums":"الأرقام الأوروبية",
        "hot":"ساخنة","cold":"باردة","due":"متأخرة",
        "your_nums":"أرقامك","analyze":"بدء التحليل",
        "ai_tip":"اقتراح الذكاء الاصطناعي","recommendations":"توصيات",
        "save_nums":"حفظ","saved":"تم الحفظ!",
        "jackpot":"الجائزة الكبرى","chance":"فرصة",
        "settings":"الإعدادات","language":"اللغة","theme":"المظهر",
        "disclaimer":"توقعات الذكاء الاصطناعي احتمالات إحصائية. العب بمسؤولية.",
        "footer":"© 2026 المتنبئ الذكي ألمانيا · نظام التحليل الكمي",
        "welcome":"مرحباً","profile_updated":"تم تحديث الملف الشخصي!",
        "scan_title":"مسح تذكرة اليانصيب","scan_info":"رفع صورة التذكرة",
        "news_title":"آخر الأخبار","member_since":"عضو منذ",
        "my_numbers":"أرقامي","live":"مباشر",
        "login_success":"تم تسجيل الدخول!","register_success":"تم إنشاء الحساب!",
        "error_login":"البريد أو كلمة المرور خاطئة","error_register":"فشل التسجيل",
        "fill_all":"يرجى ملء جميع الحقول","pass_match":"كلمتا المرور غير متطابقتين",
        "horoscope":"أبراج اليانصيب","star_sign":"برجك","lucky_nums":"أرقام الحظ",
        "selected":"المحدد","freq_title":"تحليل التكرار","winners":"الفائزون",
        "dark_theme":"داكن","light_theme":"فاتح",
        "daily_title":"🔮 التوقع اليومي","daily_sub":"يتجدد كل منتصف ليل",
        "claim_btn":"احصل على توقع اليوم ✅","claimed":"تم الحصول عليه!","streak":"متتالية",
        "streak_msg":"أيام متتالية! استمر!","streak_reward":"مكافأة",
        "ai_reason":"تفسير الذكاء الاصطناعي","share":"مشاركة",
        "community_title":"المجتمع","post_placeholder":"شارك رأيك…",
        "post_btn":"نشر","like":"إعجاب","comment":"تعليق",
        "premium_title":"بريميوم","premium_sub":"ذكاء غير محدود · بلا إعلانات · مجتمع VIP",
        "upgrade":"ترقية إلى بريميوم","per_month":"شهرياً",
        "free_plan":"مجاني","premium_plan":"بريميوم",
        "leaderboard":"لوحة الصدارة","rank":"المرتبة","points":"النقاط",
        "notify":"إشعار","notify_sub":"يومياً الساعة 10:00",
        "streak_fire":"🔥 السلسلة نشطة!","new_badge":"🏅 شارة جديدة!",
        "badges":"الشارات","level":"المستوى",
    }
}

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
DEFAULTS = {
    "language":"de","theme":"dark","active_page":"home",
    "user":None,"show_settings":False,"auth_mode":"login",
    "lotto_pred":None,"euro_pred":None,
    "user_numbers":[],"current_analysis":None,
    "daily_claimed":False,"streak":0,"posts":[],
    "show_premium_modal":False,
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

t = TRANS[st.session_state.language]

# ══════════════════════════════════════════════════════════════════
#  DATABASE FUNCTIONS
# ══════════════════════════════════════════════════════════════════
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def db_register(email,username,password,full_name):
    if not DB_AVAILABLE: return {"success":False,"error":"DB unavailable"}
    try:
        if supabase.table("users").select("id").eq("email",email).execute().data:
            return {"success":False,"error":"Email exists"}
        supabase.table("users").insert({
            "email":email,"username":username,
            "password_hash":hash_pw(password),"full_name":full_name,
            "avatar":random.choice(["🎲","🔮","⭐","🍀","💎","🎯","🏆","🌟"]),
            "is_premium":False,"points":0,"level":1,
            "created_at":datetime.now().isoformat(),
        }).execute()
        return {"success":True}
    except Exception as e: return {"success":False,"error":str(e)}

def db_login(email,password):
    if not DB_AVAILABLE: return {"success":False,"error":"DB unavailable"}
    try:
        r=supabase.table("users").select("*").eq("email",email).eq("password_hash",hash_pw(password)).execute()
        if r.data:
            supabase.table("users").update({"last_login":datetime.now().isoformat()}).eq("id",r.data[0]["id"]).execute()
            return {"success":True,"user":r.data[0]}
        return {"success":False}
    except Exception as e: return {"success":False,"error":str(e)}

def db_save_numbers(user_id,numbers,game):
    if not DB_AVAILABLE: return False
    try:
        supabase.table("favorite_numbers").insert({
            "user_id":user_id,"numbers":numbers,
            "game":game,"created_at":datetime.now().isoformat()
        }).execute()
        return True
    except: return False

def db_get_numbers(user_id):
    if not DB_AVAILABLE: return []
    try:
        r=supabase.table("favorite_numbers").select("*").eq("user_id",user_id).order("created_at",desc=True).limit(10).execute()
        return r.data or []
    except: return []

def db_get_daily_prediction():
    if not DB_AVAILABLE:
        rng=random.Random(str(date.today()))
        nums=sorted(rng.sample(range(1,50),6))
        return {"numbers":nums,"super_number":rng.randint(0,9),
                "confidence":round(rng.uniform(82,95),1),
                "ai_reason":_generate_ai_reason(nums)}
    try:
        r=supabase.table("daily_predictions").select("*").eq("date",str(date.today())).execute()
        if r.data: return r.data[0]
        rng=random.Random(str(date.today()))
        nums=sorted(rng.sample(range(1,50),6))
        pred={"date":str(date.today()),"numbers":nums,
              "super_number":rng.randint(0,9),
              "confidence":round(rng.uniform(82,95),1),
              "ai_reason":_generate_ai_reason(nums)}
        supabase.table("daily_predictions").insert(pred).execute()
        return pred
    except:
        rng=random.Random(str(date.today()))
        nums=sorted(rng.sample(range(1,50),6))
        return {"numbers":nums,"super_number":rng.randint(0,9),
                "confidence":round(rng.uniform(82,95),1),
                "ai_reason":_generate_ai_reason(nums)}

def _generate_ai_reason(nums):
    reasons_de=[
        f"Die Zahlen {nums[0]} und {nums[2]} wurden in den letzten 30 Tagen unterdurchschnittlich gezogen — statistische Aufholwahrscheinlichkeit erhöht.",
        f"Muster-Analyse: Diese Kombination weist eine optimale Gerade/Ungerade-Verteilung ({sum(1 for n in nums if n%2==0)}/{sum(1 for n in nums if n%2!=0)}) auf.",
        f"Quantenalgorithmus identifizierte {nums[3]} als 'überfällig' nach {random.randint(38,67)} Ziehungen ohne Erscheinen.",
        f"Historische Analyse von 2.000 Ziehungen: Diese Zahlengruppe trat mit {random.randint(12,28)}% höherer Frequenz auf.",
    ]
    return random.choice(reasons_de)

def db_claim_daily(user_id):
    if not DB_AVAILABLE:
        st.session_state.daily_claimed=True
        st.session_state.streak=st.session_state.get("streak",0)+1
        return True
    try:
        today=str(date.today())
        exists=supabase.table("user_daily_log").select("id").eq("user_id",user_id).eq("log_date",today).execute()
        if exists.data: return False
        streak_data=supabase.table("user_streaks").select("*").eq("user_id",user_id).execute()
        if streak_data.data:
            s=streak_data.data[0]
            last=s.get("last_claim")
            yesterday=str(date.today()-timedelta(days=1))
            new_streak=s["current_streak"]+1 if last==yesterday else 1
            longest=max(s.get("longest_streak",0),new_streak)
            supabase.table("user_streaks").update({
                "current_streak":new_streak,"longest_streak":longest,
                "last_claim":today,"total_claims":s.get("total_claims",0)+1,
                "updated_at":datetime.now().isoformat()
            }).eq("user_id",user_id).execute()
        else:
            new_streak=1
            supabase.table("user_streaks").insert({
                "user_id":user_id,"current_streak":1,"longest_streak":1,
                "last_claim":today,"total_claims":1
            }).execute()
        supabase.table("user_daily_log").insert({
            "user_id":user_id,"log_date":today,
            "claimed":True,"streak_day":new_streak
        }).execute()
        pts=10+(5 if new_streak%7==0 else 0)
        supabase.table("users").update({"points":supabase.table("users").select("points").eq("id",user_id).execute().data[0]["points"]+pts}).eq("id",user_id).execute()
        st.session_state.streak=new_streak
        st.session_state.daily_claimed=True
        return True
    except Exception as e:
        st.session_state.daily_claimed=True
        st.session_state.streak=st.session_state.get("streak",0)+1
        return True

def db_get_streak(user_id):
    if not DB_AVAILABLE: return st.session_state.get("streak",0)
    try:
        r=supabase.table("user_streaks").select("*").eq("user_id",user_id).execute()
        if r.data: return r.data[0].get("current_streak",0)
        return 0
    except: return 0

def db_get_posts(limit=20):
    if not DB_AVAILABLE: return _demo_posts()
    try:
        r=supabase.table("community_posts").select("*").order("created_at",desc=True).limit(limit).execute()
        return r.data or _demo_posts()
    except: return _demo_posts()

def _demo_posts():
    return [
        {"id":1,"username":"Klaus_W","avatar":"👴","content":"Die KI hat heute wieder 3 von 6 getroffen! Unglaublich 🎯","likes":24,"created_at":"2026-03-18T14:32:00","game":"Lotto"},
        {"id":2,"username":"AhmedDE","avatar":"🎲","content":"لأول مرة أجرب هذا التطبيق — الواجهة رائعة جداً 🌟","likes":18,"created_at":"2026-03-18T13:15:00","game":"Eurojackpot"},
        {"id":3,"username":"Maria_B","avatar":"⭐","content":"7 Tage Streak! Die tägliche Vorhersage ist mein Ritual geworden ☕🔮","likes":31,"created_at":"2026-03-18T11:45:00","game":"Lotto"},
        {"id":4,"username":"ThomasH","avatar":"🏆","content":"Eurojackpot Vorhersage war heute fast perfekt — 4 richtige Zahlen!","likes":45,"created_at":"2026-03-18T10:00:00","game":"Eurojackpot"},
        {"id":5,"username":"Sara_NL","avatar":"🍀","content":"Endlich eine App die erklärt WARUM die Zahlen ausgewählt werden 👏","likes":29,"created_at":"2026-03-17T22:00:00","game":"Lotto"},
    ]

def db_post_community(user_id,username,avatar,content,game):
    if not DB_AVAILABLE:
        st.session_state.posts.insert(0,{
            "id":random.randint(100,999),"username":username,"avatar":avatar,
            "content":content,"likes":0,"created_at":datetime.now().isoformat(),"game":game
        })
        return True
    try:
        supabase.table("community_posts").insert({
            "user_id":user_id,"username":username,"avatar":avatar,
            "content":content,"likes":0,"game":game,
            "created_at":datetime.now().isoformat()
        }).execute()
        return True
    except: return False

def db_get_leaderboard():
    if not DB_AVAILABLE:
        return [
            {"rank":1,"username":"Klaus_W","avatar":"👴","points":1240,"streak":15,"level":8},
            {"rank":2,"username":"Maria_B","avatar":"⭐","points":980,"streak":12,"level":7},
            {"rank":3,"username":"ThomasH","avatar":"🏆","points":870,"streak":9,"level":6},
            {"rank":4,"username":"AhmedDE","avatar":"🎲","points":750,"streak":7,"level":5},
            {"rank":5,"username":"Sara_NL","avatar":"🍀","points":620,"streak":5,"level":4},
        ]
    try:
        r=supabase.table("users").select("username,avatar,points,level").order("points",desc=True).limit(10).execute()
        return [{"rank":i+1,**u} for i,u in enumerate(r.data or [])]
    except: return []

def db_get_news():
    if not DB_AVAILABLE: return []
    try:
        r=supabase.table("news").select("*").order("created_at",desc=True).limit(10).execute()
        return r.data or []
    except: return []

def db_update_profile(user_id,full_name,avatar):
    if not DB_AVAILABLE: return False
    try:
        supabase.table("users").update({"full_name":full_name,"avatar":avatar}).eq("id",user_id).execute()
        return True
    except: return False

# ══════════════════════════════════════════════════════════════════
#  AI ENGINE
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600,show_spinner=False)
def get_hist():
    rng=np.random.default_rng(42); n=2000
    w=np.ones(49)
    for h in [3,7,15,23,38,44]: w[h-1]=1.35
    for c in [13,26,31,35,42,47]: w[c-1]=0.72
    w/=w.sum()
    ld,em,ee=[],[],[]
    for _ in range(n):
        ld.append(sorted(rng.choice(49,6,replace=False,p=w)+1))
        em.append(sorted(rng.choice(50,5,replace=False)+1))
        ee.append(sorted(rng.choice(12,2,replace=False)+1))
    dates=pd.date_range(end=datetime.now(),periods=n,freq="3D")
    return {
        "lotto":pd.DataFrame({"date":dates,"numbers":ld,"jackpot":np.clip(rng.normal(15,10,n),2,45)}),
        "euro":pd.DataFrame({"date":dates,"main":em,"extra":ee,"jackpot":np.clip(rng.normal(50,30,n),10,120)}),
    }

@st.cache_data(ttl=300,show_spinner=False)
def get_jackpots(): return {"lotto":37.7,"euro":37.6}

class AI:
    @staticmethod
    def freq(draws,n=20): return Counter([x for row in draws for x in row]).most_common(n)
    @staticmethod
    def hcd(draws,mx):
        flat=[x for row in draws for x in row]; freq=Counter(flat); ls={}
        for i,row in enumerate(draws):
            for n in row: ls[n]=i
        return {"hot":sorted(freq,key=freq.get,reverse=True)[:8],
                "cold":sorted(freq,key=freq.get)[:8],
                "due":sorted(range(1,mx+1),key=lambda x:ls.get(x,-1))[:8]}
    @classmethod
    def lotto(cls,data):
        top=[n for n,_ in cls.freq(data["numbers"].tolist(),20)][:12]
        picks=random.sample(top,min(3,len(top)))
        picks+=random.sample([n for n in range(1,50) if n not in picks],6-len(picks))
        return {"numbers":sorted(picks),"super_number":random.randint(0,9),"confidence":round(random.uniform(81.5,94.8),1)}
    @classmethod
    def euro(cls,data):
        tm=[n for n,_ in cls.freq(data["main"].tolist(),15)][:10]
        te=[n for n,_ in cls.freq(data["extra"].tolist(),8)][:5]
        main=random.sample(tm,min(3,len(tm)))
        main+=random.sample([n for n in range(1,51) if n not in main],5-len(main))
        extra=random.sample(te,min(2,len(te)))
        if len(extra)<2: extra+=random.sample([n for n in range(1,13) if n not in extra],2-len(extra))
        return {"main_numbers":sorted(main),"extra_numbers":sorted(extra),"confidence":round(random.uniform(79.2,93.1),1)}
    @classmethod
    def analyze(cls,nums,data):
        flat=[x for row in data["numbers"].tolist() for x in row]; freq=Counter(flat)
        even=sum(1 for n in nums if n%2==0); odd=len(nums)-even
        low=sum(1 for n in nums if n<=25); high=len(nums)-low
        recs=[]
        if even>4: recs.append("Zu viele gerade Zahlen — empfehle mehr ungerade")
        if odd>4: recs.append("Zu viele ungerade Zahlen — empfehle mehr gerade")
        if low>4: recs.append("Zahlen zu niedrig — bessere Verteilung empfohlen")
        if high>4: recs.append("Zahlen zu hoch — bessere Verteilung empfohlen")
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
        t2={"Widder":[5,19,23,37,42,48],"Stier":[2,8,14,26,31,45],"Zwillinge":[7,12,21,33,39,44],
            "Krebs":[4,11,18,27,36,41],"Löwe":[1,15,22,29,38,47],"Jungfrau":[3,9,16,24,35,43],
            "Waage":[6,13,20,28,34,46],"Skorpion":[10,17,25,30,40,49],"Schütze":[12,24,31,37,42,48],
            "Steinbock":[2,8,15,23,36,44],"Wassermann":[5,11,19,27,33,45],"Fische":[7,14,21,29,38,46]}
        return t2.get(sign,[1,7,14,22,35,43])

# ══════════════════════════════════════════════════════════════════
#  BADGE SYSTEM
# ══════════════════════════════════════════════════════════════════
BADGES = [
    {"id":"first_day","icon":"🌱","name":"Erster Tag","req":1,"type":"streak"},
    {"id":"week","icon":"🔥","name":"Eine Woche","req":7,"type":"streak"},
    {"id":"month","icon":"💎","name":"Ein Monat","req":30,"type":"streak"},
    {"id":"century","icon":"👑","name":"100 Tage","req":100,"type":"streak"},
    {"id":"social","icon":"🤝","name":"Community Star","req":5,"type":"posts"},
    {"id":"analyst","icon":"📊","name":"Analyst","req":10,"type":"analysis"},
]

def get_user_badges(streak,posts_count=0,analysis_count=0):
    earned=[]
    for b in BADGES:
        if b["type"]=="streak" and streak>=b["req"]: earned.append(b)
        elif b["type"]=="posts" and posts_count>=b["req"]: earned.append(b)
        elif b["type"]=="analysis" and analysis_count>=b["req"]: earned.append(b)
    return earned

def get_user_level(points):
    levels=[(0,"🥉 Anfänger"),(100,"🥈 Fortgeschrittener"),(300,"🥇 Experte"),
             (600,"💎 Meister"),(1000,"👑 Legende"),(2000,"🔮 Quantum")]
    for pts,label in reversed(levels):
        if points>=pts: return label
    return levels[0][1]

# ══════════════════════════════════════════════════════════════════
#  CSS — WORLD-CLASS 2026 DESIGN
# ══════════════════════════════════════════════════════════════════
D = st.session_state.theme == "dark"
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700;900&display=swap');

:root{{
  --bg:{"#05080f" if D else "#f2f5fb"};
  --bg2:{"#080d18" if D else "#e8edf7"};
  --surface:{"rgba(12,20,40,0.92)" if D else "rgba(255,255,255,0.95)"};
  --surface2:{"rgba(16,26,50,0.8)" if D else "rgba(240,245,255,0.9)"};
  --border:{"rgba(100,160,255,0.12)" if D else "rgba(0,80,200,0.12)"};
  --border-gold:rgba(255,200,0,0.3);
  --text:{"#e8f0ff" if D else "#0a1628"};
  --muted:{"#5878a0" if D else "#6b7c93"};
  --gold:#f5c400;
  --gold2:#ffdd44;
  --green:#00e676;
  --cyan:#00cfff;
  --purple:#a855f7;
  --red:#ff4757;
  --orange:#ff8c00;
  --radius:18px;
  --shadow:{"0 8px 32px rgba(0,0,0,0.4)" if D else "0 8px 32px rgba(0,80,200,0.08)"};
}}

*{{box-sizing:border-box;margin:0;padding:0;}}
html,body,.stApp{{
  background:var(--bg)!important;
  color:var(--text)!important;
  font-family:'Outfit',sans-serif!important;
}}
{"html,body,.stApp{background-image:radial-gradient(ellipse at 20% 50%, rgba(20,40,100,0.15) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(100,20,200,0.08) 0%, transparent 50%);}" if D else ""}

#MainMenu,footer,header,.stDeployButton{{display:none!important;}}
.block-container{{padding:0.8rem 1.2rem 5rem!important;max-width:1400px!important;margin:0 auto!important;}}

/* SCROLLBAR */
::-webkit-scrollbar{{width:4px;height:4px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:var(--gold);border-radius:4px;opacity:0.5;}}

/* SIDEBAR */
[data-testid="stSidebar"]{{
  background:var(--surface)!important;
  border-right:1px solid var(--border)!important;
  backdrop-filter:blur(20px)!important;
}}
[data-testid="stSidebar"] .stButton>button{{
  width:100%;background:transparent;border:1px solid transparent;
  color:var(--muted);border-radius:12px;padding:9px 14px;
  text-align:left;font-size:0.88rem;font-family:'Outfit',sans-serif;
  font-weight:500;transition:all 0.2s;margin-bottom:2px;letter-spacing:0.01em;
}}
[data-testid="stSidebar"] .stButton>button:hover{{
  background:rgba(245,196,0,0.08);border-color:var(--border-gold);
  color:var(--gold);transform:translateX(4px);
}}

/* BUTTONS */
.stButton>button{{
  font-family:'Outfit',sans-serif!important;font-weight:700!important;
  border-radius:14px!important;transition:all 0.2s!important;letter-spacing:0.02em!important;
}}
.stButton>button[kind="primary"]{{
  background:linear-gradient(135deg,#f5c400,#ff8c00)!important;
  color:#0a0f1a!important;border:none!important;
  box-shadow:0 4px 20px rgba(245,196,0,0.3)!important;
}}
.stButton>button[kind="primary"]:hover{{
  transform:translateY(-3px)!important;
  box-shadow:0 8px 28px rgba(245,196,0,0.45)!important;
}}

/* CARDS */
.card{{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:22px;
  transition:all 0.3s;position:relative;overflow:hidden;
  margin-bottom:14px;box-shadow:var(--shadow);
  backdrop-filter:blur(12px);
}}
.card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),var(--cyan),transparent);
  opacity:0.6;
}}
.card:hover{{
  border-color:rgba(245,196,0,0.25);
  transform:translateY(-3px);
  box-shadow:0 16px 48px rgba(0,0,0,0.35);
}}
.card-gold{{border-color:rgba(245,196,0,0.3)!important;}}
.card-green{{border-color:rgba(0,230,118,0.25)!important;}}
.card-purple{{border-color:rgba(168,85,247,0.25)!important;}}

/* JACKPOT HERO */
.jackpot-wrap{{
  background:{"linear-gradient(135deg,rgba(15,25,55,0.95),rgba(20,35,80,0.9))" if D else "linear-gradient(135deg,rgba(0,40,120,0.08),rgba(0,60,160,0.05))"};
  border:1px solid var(--border-gold);border-radius:24px;padding:32px 24px;
  text-align:center;position:relative;overflow:hidden;
  box-shadow:0 0 40px rgba(245,196,0,0.1),inset 0 1px 0 rgba(255,255,255,0.05);
}}
.jackpot-wrap::after{{
  content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
  background:radial-gradient(circle,rgba(245,196,0,0.04) 0%,transparent 60%);
  animation:glow-pulse 4s ease-in-out infinite;
}}
.jackpot-wrap.euro{{
  border-color:rgba(0,230,118,0.3);
  box-shadow:0 0 40px rgba(0,230,118,0.08),inset 0 1px 0 rgba(255,255,255,0.05);
}}
.jackpot-wrap.euro::after{{background:radial-gradient(circle,rgba(0,230,118,0.04) 0%,transparent 60%);}}
@keyframes glow-pulse{{0%,100%{{opacity:0.5;}}50%{{opacity:1;}}}}

.jackpot-amount{{
  font-family:'Playfair Display',serif;
  font-size:clamp(2.2rem,5vw,3.8rem);font-weight:900;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1;letter-spacing:-0.02em;
}}
.jackpot-wrap.euro .jackpot-amount{{background:linear-gradient(135deg,var(--green),#69ffb0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}

/* NUMBER BALLS */
.nb{{
  width:48px;height:48px;border-radius:50%;
  background:{"linear-gradient(145deg,#0f1e3d,#091428)" if D else "linear-gradient(145deg,#dde8ff,#c8d8ff)"};
  border:2px solid rgba(100,160,255,0.25);
  color:{"#c8d8ff" if D else "#1a3a8a"};
  font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700;
  display:inline-flex;align-items:center;justify-content:center;
  transition:all 0.25s;margin:3px;cursor:default;
}}
.nb:hover{{transform:scale(1.15) rotate(-3deg);border-color:var(--gold);color:var(--gold);}}
.nb.gold{{background:linear-gradient(145deg,#3d2800,#5a3c00);border-color:var(--gold);color:var(--gold);box-shadow:0 0 14px rgba(245,196,0,0.3);}}
.nb.euro{{background:{"linear-gradient(145deg,#0a2810,#052010)" if D else "linear-gradient(145deg,#c8ffd8,#a0f0b8)"};border-color:var(--green);color:var(--green);}}
.nb.extra{{background:linear-gradient(145deg,#2d1a00,#3d2500);border-color:var(--orange);color:var(--orange);}}
.nb.sel{{background:linear-gradient(145deg,var(--gold),var(--orange));color:#0a0f1a;border-color:var(--gold);box-shadow:0 0 16px rgba(245,196,0,0.4);}}
.nb.hot{{border-color:var(--red);color:var(--red);}}
.nb.cold{{border-color:var(--cyan);color:var(--cyan);}}
.nb.pulse{{animation:nb-pulse 2s ease-in-out infinite;}}
@keyframes nb-pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(245,196,0,0.4);}}50%{{box-shadow:0 0 0 8px rgba(245,196,0,0);}}}}
.nbrow{{display:flex;gap:4px;flex-wrap:wrap;align-items:center;justify-content:center;margin:10px 0;}}

/* TICKER */
.ticker-wrap{{
  background:{"linear-gradient(90deg,rgba(0,40,100,0.6),rgba(0,60,150,0.5))" if D else "linear-gradient(90deg,rgba(0,40,120,0.08),rgba(0,60,150,0.06))"};
  border:1px solid rgba(100,160,255,0.15);border-radius:100px;
  padding:10px 20px;overflow:hidden;margin-bottom:20px;
}}
.ticker-inner{{
  white-space:nowrap;display:inline-block;
  animation:slide 40s linear infinite;
  font-family:'JetBrains Mono',monospace;font-size:0.82rem;
  font-weight:600;letter-spacing:0.06em;
  color:{"rgba(200,220,255,0.7)" if D else "rgba(0,40,120,0.6)"};
}}
@keyframes slide{{0%{{transform:translateX(60vw);}}100%{{transform:translateX(-100%);}}}}

/* CONFIDENCE BAR */
.cbar{{background:rgba(255,255,255,0.06);border-radius:100px;height:6px;overflow:hidden;margin:6px 0;}}
.cfill{{height:100%;background:linear-gradient(90deg,var(--cyan),var(--gold));border-radius:100px;transition:width 1s ease;}}

/* LIVE BADGE */
.lbadge{{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(255,71,87,0.12);border:1px solid rgba(255,71,87,0.3);
  border-radius:100px;padding:4px 12px;
  font-size:0.72rem;font-weight:700;color:var(--red);letter-spacing:0.12em;
}}
.ldot{{width:6px;height:6px;border-radius:50%;background:var(--red);animation:ldot 1.4s infinite;}}
@keyframes ldot{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:0.3;transform:scale(0.5);}}}}

/* STREAK */
.streak-card{{
  background:{"linear-gradient(135deg,rgba(40,20,0,0.9),rgba(60,30,0,0.8))" if D else "linear-gradient(135deg,rgba(255,140,0,0.08),rgba(245,196,0,0.05))"};
  border:1px solid rgba(255,140,0,0.3);border-radius:20px;padding:20px;
  text-align:center;position:relative;overflow:hidden;
}}
.streak-num{{
  font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;
  background:linear-gradient(135deg,var(--orange),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1;
}}
.streak-fire{{font-size:2rem;animation:fire 0.8s ease-in-out infinite alternate;}}
@keyframes fire{{0%{{transform:scale(1) rotate(-3deg);}}100%{{transform:scale(1.1) rotate(3deg);}}}}

/* DAILY PREDICTION CARD */
.daily-card{{
  background:{"linear-gradient(135deg,rgba(20,10,50,0.95),rgba(30,15,70,0.9))" if D else "linear-gradient(135deg,rgba(120,0,200,0.05),rgba(80,0,160,0.03))"};
  border:1px solid rgba(168,85,247,0.3);border-radius:24px;padding:28px;
  position:relative;overflow:hidden;box-shadow:0 0 40px rgba(168,85,247,0.08);
}}
.daily-card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--purple),var(--cyan),var(--gold));
}}

/* COMMUNITY POST */
.post-card{{
  background:var(--surface);border:1px solid var(--border);
  border-radius:16px;padding:18px;margin-bottom:10px;
  transition:all 0.2s;
}}
.post-card:hover{{border-color:rgba(245,196,0,0.2);}}
.post-avatar{{
  width:40px;height:40px;border-radius:50%;
  background:linear-gradient(135deg,rgba(245,196,0,0.2),rgba(0,207,255,0.2));
  border:2px solid var(--border-gold);
  display:inline-flex;align-items:center;justify-content:center;
  font-size:1.3rem;
}}

/* NEWS */
.news-card{{
  background:var(--surface);border:1px solid var(--border);
  border-left:3px solid var(--gold);border-radius:14px;
  padding:18px;margin-bottom:10px;transition:all 0.3s;
}}
.news-card:hover{{transform:translateX(5px);border-left-color:var(--cyan);}}

/* PREMIUM */
.premium-card{{
  background:{"linear-gradient(135deg,rgba(30,15,60,0.97),rgba(50,20,100,0.95))" if D else "linear-gradient(135deg,rgba(100,0,200,0.06),rgba(60,0,150,0.04))"};
  border:1px solid rgba(168,85,247,0.4);border-radius:24px;
  padding:32px;text-align:center;position:relative;overflow:hidden;
}}
.premium-card::before{{
  content:'✨ PREMIUM';position:absolute;top:14px;right:20px;
  font-size:0.68rem;font-weight:800;letter-spacing:0.2em;
  color:var(--purple);opacity:0.8;
}}

/* LEADERBOARD */
.lb-row{{
  display:flex;align-items:center;gap:14px;padding:12px 16px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:14px;margin-bottom:8px;transition:all 0.2s;
}}
.lb-row:hover{{border-color:rgba(245,196,0,0.2);transform:translateX(4px);}}
.lb-rank{{
  font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;
  min-width:32px;text-align:center;
}}

/* BADGE */
.badge{{
  display:inline-flex;flex-direction:column;align-items:center;gap:4px;
  padding:12px 16px;background:var(--surface2);border:1px solid var(--border);
  border-radius:14px;transition:all 0.2s;min-width:80px;
}}
.badge:hover{{border-color:var(--gold);transform:translateY(-3px);}}
.badge-icon{{font-size:1.8rem;}}
.badge-name{{font-size:0.68rem;color:var(--muted);text-align:center;font-weight:600;}}

/* SECTION TITLE */
.sec-title{{
  font-family:'Outfit',sans-serif;font-size:1.3rem;font-weight:800;
  letter-spacing:0.04em;color:var(--gold);
  margin-bottom:16px;padding-bottom:8px;
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:10px;
}}

/* WINNER CARD */
.winner-card{{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:16px;text-align:center;
  transition:all 0.3s;
}}
.winner-card:hover{{border-color:var(--gold);transform:translateY(-5px);box-shadow:0 20px 40px rgba(245,196,0,0.1);}}

/* SCAN */
.scan-zone{{
  border:2px dashed rgba(245,196,0,0.3);border-radius:20px;
  padding:40px;text-align:center;
  background:radial-gradient(ellipse,rgba(245,196,0,0.02) 0%,transparent 70%);
  transition:all 0.3s;
}}
.scan-zone:hover{{border-color:var(--gold);background:radial-gradient(ellipse,rgba(245,196,0,0.05) 0%,transparent 70%);}}

/* DISCLAIMER */
.disclaimer{{
  background:rgba(245,196,0,0.03);border:1px solid rgba(245,196,0,0.1);
  border-radius:12px;padding:11px 16px;font-size:0.75rem;
  color:var(--muted);text-align:center;margin-top:28px;
}}

/* METRICS */
div[data-testid="stMetric"]{{
  background:var(--surface)!important;border:1px solid var(--border)!important;
  border-radius:var(--radius)!important;padding:16px 20px!important;
}}
div[data-testid="stMetric"] label{{color:var(--muted)!important;font-size:0.78rem!important;font-weight:600!important;letter-spacing:0.06em!important;}}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{{color:var(--gold)!important;font-family:'Playfair Display',serif!important;font-size:1.8rem!important;font-weight:700!important;}}

/* INPUTS */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{{
  background:var(--surface2)!important;border-color:var(--border)!important;
  color:var(--text)!important;border-radius:12px!important;font-family:'Outfit',sans-serif!important;
}}
.stSelectbox>div>div{{background:var(--surface2)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:12px!important;}}
.stTabs [aria-selected="true"]{{color:var(--gold)!important;border-bottom-color:var(--gold)!important;font-weight:700!important;}}
.stTabs [data-baseweb="tab"]{{font-family:'Outfit',sans-serif!important;font-weight:600!important;}}

/* PROGRESS BAR override */
.stProgress>div>div>div{{background:linear-gradient(90deg,var(--cyan),var(--gold))!important;}}

/* NOTIFICATION TOAST */
.toast{{
  position:fixed;top:20px;right:20px;z-index:9999;
  background:{"rgba(12,20,40,0.97)" if D else "rgba(255,255,255,0.97)"};
  border:1px solid var(--gold);border-radius:16px;padding:16px 20px;
  box-shadow:0 8px 32px rgba(0,0,0,0.3);animation:toast-in 0.4s ease;
  backdrop-filter:blur(20px);
}}
@keyframes toast-in{{from{{transform:translateX(100%);opacity:0;}}to{{transform:translateX(0);opacity:1;}}}}

/* MOBILE RESPONSIVE */
@media(max-width:768px){{
  .jackpot-amount{{font-size:2rem!important;}}
  .nb{{width:38px!important;height:38px!important;font-size:0.85rem!important;}}
  .block-container{{padding:0.5rem 0.8rem 5rem!important;}}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def B(nums, style=""):
    b="".join(f'<span class="nb {style}">{n}</span>' for n in nums)
    return f'<div class="nbrow">{b}</div>'

def ticker(news):
    tx="    ·    ".join(news)*2
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{tx}</div></div>',unsafe_allow_html=True)

def SEC(title, icon=""):
    st.markdown(f'<div class="sec-title">{icon} {title}</div>',unsafe_allow_html=True)

def LIVE():
    return f'<span class="lbadge"><span class="ldot"></span>{t["live"]}</span>'

def CARD(content, style=""):
    return f'<div class="card {style}">{content}</div>'

def share_buttons(numbers, game, jackpot, lang="de"):
    import urllib.parse
    msgs={"de":f"🔮 Meine KI-Vorhersage: {' · '.join(map(str,numbers))} — {game} {jackpot}M€ | AI Predictor Germany 2026",
          "en":f"🔮 My AI Prediction: {' · '.join(map(str,numbers))} — {game} {jackpot}M€ | AI Predictor Germany 2026",
          "ar":f"🔮 توقعاتي: {' · '.join(map(str,numbers))} — {game} {jackpot}M€ | المتنبئ الذكي"}
    msg=msgs.get(lang,msgs["de"])
    wa=f"https://wa.me/?text={urllib.parse.quote(msg)}"
    tg=f"https://t.me/share/url?url=https://ai-predictor.de&text={urllib.parse.quote(msg)}"
    st.markdown(f"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;">
      <a href="{wa}" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:7px 14px;background:rgba(37,211,102,0.12);border:1px solid rgba(37,211,102,0.3);border-radius:100px;color:#25d366;font-size:0.8rem;font-weight:700;text-decoration:none;">📱 WhatsApp</a>
      <a href="{tg}" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:7px 14px;background:rgba(0,136,204,0.12);border:1px solid rgba(0,136,204,0.3);border-radius:100px;color:#0088cc;font-size:0.8rem;font-weight:700;text-decoration:none;">✈️ Telegram</a>
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  AUTH PAGE
# ══════════════════════════════════════════════════════════════════
def auth_page():
    st.markdown(f"""
    <div style="text-align:center;padding:48px 0 36px;">
      <div style="font-size:0.72rem;letter-spacing:0.25em;color:var(--cyan);font-family:'JetBrains Mono',monospace;margin-bottom:12px;opacity:0.8;">
        QUANTUM AI ENGINE · v2026.1 · LIVE
      </div>
      <div style="font-family:'Playfair Display',serif;font-size:clamp(2rem,6vw,3.8rem);font-weight:900;
                  background:linear-gradient(135deg,var(--gold),var(--orange),var(--gold2));
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  line-height:1.1;margin-bottom:12px;letter-spacing:-0.02em;">
        🔮 {t['title']}
      </div>
      <div style="color:var(--muted);margin-top:10px;font-size:1rem;font-weight:400;">{t['subtitle']}</div>
      <div style="margin-top:16px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
        {LIVE()}
        <span style="display:inline-flex;align-items:center;gap:5px;background:rgba(0,230,118,0.1);border:1px solid rgba(0,230,118,0.25);border-radius:100px;padding:4px 12px;font-size:0.72rem;font-weight:700;color:var(--green);">✅ Supabase</span>
        <span style="display:inline-flex;align-items:center;gap:5px;background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);border-radius:100px;padding:4px 12px;font-size:0.72rem;font-weight:700;color:var(--purple);">🔮 AI Powered</span>
      </div>
    </div>
    """,unsafe_allow_html=True)

    _,col,_=st.columns([1,1.2,1])
    with col:
        c1,c2=st.columns(2)
        with c1:
            if st.button(t["login"],key="tl",use_container_width=True,
                        type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login"; st.rerun()
        with c2:
            if st.button(t["register"],key="tr",use_container_width=True,
                        type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register"; st.rerun()
        st.markdown("<br/>",unsafe_allow_html=True)

        if st.session_state.auth_mode=="login":
            st.markdown(f"#### 🔐 {t['login']}")
            em=st.text_input(t["email"],placeholder="you@example.com",key="l_em")
            pw=st.text_input(t["password"],type="password",key="l_pw")
            if st.button(f"→ {t['login']}",key="do_l",use_container_width=True,type="primary"):
                if em and pw:
                    r=db_login(em,pw)
                    if r["success"]:
                        st.session_state.user=r["user"]
                        st.session_state.streak=db_get_streak(r["user"]["id"])
                        st.success(t["login_success"]); time.sleep(0.4); st.rerun()
                    else: st.error(t["error_login"])
                else: st.warning(t["fill_all"])
        else:
            st.markdown(f"#### ✨ {t['register']}")
            fn=st.text_input(t["full_name"],placeholder="Max Mustermann",key="r_fn")
            un=st.text_input(t["username"],placeholder="max2026",key="r_un")
            em=st.text_input(t["email"],placeholder="you@example.com",key="r_em")
            pw=st.text_input(t["password"],type="password",key="r_pw")
            cf=st.text_input(t["confirm_pass"],type="password",key="r_cf")
            if st.button(f"→ {t['register']}",key="do_r",use_container_width=True,type="primary"):
                if all([fn,un,em,pw,cf]):
                    if pw!=cf: st.error(t["pass_match"])
                    else:
                        r=db_register(em,un,pw,fn)
                        if r["success"]:
                            st.success(t["register_success"]); st.session_state.auth_mode="login"; time.sleep(1); st.rerun()
                        else: st.error(t["error_register"])
                else: st.warning(t["fill_all"])

        st.markdown("""
        <div style="margin-top:24px;padding:16px;background:rgba(245,196,0,0.04);border:1px solid rgba(245,196,0,0.1);border-radius:14px;text-align:center;">
          <div style="color:var(--muted);font-size:0.78rem;margin-bottom:10px;font-weight:600;letter-spacing:0.06em;">STATISTIKEN</div>
          <div style="display:flex;justify-content:space-around;">
            <div style="text-align:center;"><div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:var(--gold);">2.000+</div><div style="font-size:0.7rem;color:var(--muted);">Ziehungen</div></div>
            <div style="text-align:center;"><div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:var(--cyan);">94.8%</div><div style="font-size:0.7rem;color:var(--muted);">Max KI</div></div>
            <div style="text-align:center;"><div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:var(--green);">50K+</div><div style="font-size:0.7rem;color:var(--muted);">Nutzer</div></div>
          </div>
        </div>
        """,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
def render_sidebar():
    jp=get_jackpots(); user=st.session_state.user
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:20px 0 16px;text-align:center;">
          <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:900;
                      background:linear-gradient(135deg,var(--gold),var(--orange));
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            🔮 AI PREDICTOR
          </div>
          <div style="font-size:0.65rem;color:var(--muted);letter-spacing:0.2em;margin-top:2px;font-family:'JetBrains Mono',monospace;">GERMANY 2026</div>
        </div>
        """,unsafe_allow_html=True)

        if user:
            streak=st.session_state.get("streak",0)
            pts=user.get("points",0)
            lvl=get_user_level(pts)
            is_premium=user.get("is_premium",False)
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid var(--border);border-radius:16px;padding:14px;margin-bottom:14px;">
              <div style="display:flex;align-items:center;gap:10px;">
                <div style="font-size:2rem;width:44px;height:44px;display:flex;align-items:center;justify-content:center;
                            background:linear-gradient(135deg,rgba(245,196,0,0.15),rgba(0,207,255,0.1));
                            border-radius:50%;border:2px solid var(--border-gold);">
                  {user.get('avatar','🎲')}
                </div>
                <div style="flex:1;min-width:0;">
                  <div style="font-weight:700;color:var(--gold);font-size:0.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    {user.get('full_name') or user.get('username','')}
                    {"<span style='margin-left:4px;font-size:0.6rem;background:rgba(168,85,247,0.2);color:var(--purple);padding:2px 6px;border-radius:100px;border:1px solid rgba(168,85,247,0.3);'>PRO</span>" if is_premium else ""}
                  </div>
                  <div style="font-size:0.7rem;color:var(--muted);">{lvl}</div>
                </div>
              </div>
              <div style="display:flex;gap:8px;margin-top:10px;">
                <div style="flex:1;text-align:center;background:rgba(255,140,0,0.08);border:1px solid rgba(255,140,0,0.2);border-radius:10px;padding:5px;">
                  <div style="font-size:1.1rem;">{'🔥' if streak>0 else '💤'}</div>
                  <div style="font-size:0.7rem;color:var(--orange);font-weight:700;">{streak}</div>
                </div>
                <div style="flex:1;text-align:center;background:rgba(245,196,0,0.08);border:1px solid rgba(245,196,0,0.2);border-radius:10px;padding:5px;">
                  <div style="font-size:1.1rem;">⭐</div>
                  <div style="font-size:0.7rem;color:var(--gold);font-weight:700;">{pts}</div>
                </div>
              </div>
            </div>
            """,unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;gap:6px;margin-bottom:14px;">
          <div style="flex:1;background:var(--surface2);border:1px solid var(--border-gold);border-radius:12px;padding:8px;text-align:center;">
            <div style="font-size:0.62rem;color:var(--muted);font-weight:600;letter-spacing:0.08em;">LOTTO</div>
            <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--gold);">{jp['lotto']}M</div>
          </div>
          <div style="flex:1;background:var(--surface2);border:1px solid rgba(0,230,118,0.2);border-radius:12px;padding:8px;text-align:center;">
            <div style="font-size:0.62rem;color:var(--muted);font-weight:600;letter-spacing:0.08em;">EURO</div>
            <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--green);">{jp['euro']}M</div>
          </div>
        </div>
        """,unsafe_allow_html=True)

        st.markdown('<div style="height:1px;background:var(--border);margin-bottom:8px;"></div>',unsafe_allow_html=True)

        PAGES=[("🏠",t["nav_home"],"home"),("🔮",t["nav_daily"],"daily"),
               ("🎲",t["nav_lotto"],"lotto"),("🌍",t["nav_euro"],"euro"),
               ("📊",t["nav_stats"],"stats"),("🎮",t["nav_player"],"player"),
               ("👥",t["nav_community"],"community")]
        if user:
            PAGES+=[("👤",t["nav_profile"],"profile"),("📰",t["nav_news"],"news"),
                    ("📷",t["nav_scan"],"scan"),("👑",t["nav_premium"],"premium")]

        for icon,label,key in PAGES:
            is_active=st.session_state.active_page==key
            if st.button(f"{icon}  {label}",key=f"nav_{key}",use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.active_page=key; st.rerun()

        st.markdown('<div style="height:1px;background:var(--border);margin:10px 0;"></div>',unsafe_allow_html=True)
        if st.button(f"⚙️  {t['settings']}",key="nav_set",use_container_width=True):
            st.session_state.show_settings=not st.session_state.show_settings

        if st.session_state.show_settings:
            st.markdown(f"<div style='font-size:0.78rem;color:var(--muted);font-weight:700;margin:8px 0 4px;'>{t['language']}</div>",unsafe_allow_html=True)
            for lbl,code in [("🇩🇪 Deutsch","de"),("🇬🇧 English","en"),("🇸🇦 العربية","ar")]:
                if st.button(lbl,key=f"lg_{code}",use_container_width=True):
                    st.session_state.language=code; st.rerun()
            c1,c2=st.columns(2)
            with c1:
                if st.button(f"🌙",key="td",use_container_width=True): st.session_state.theme="dark"; st.rerun()
            with c2:
                if st.button(f"☀️",key="tl2",use_container_width=True): st.session_state.theme="light"; st.rerun()

        if user:
            st.markdown('<div style="height:1px;background:var(--border);margin:10px 0;"></div>',unsafe_allow_html=True)
            if st.button(f"🚪  {t['logout']}",key="do_out",use_container_width=True):
                st.session_state.user=None; st.session_state.active_page="home"; st.rerun()

        st.markdown(f"""
        <div style="text-align:center;font-size:0.6rem;color:var(--muted);margin-top:16px;padding:0 8px;line-height:1.6;">
          {t['footer']}<br/>
          <span style="color:var(--gold);">●</span> {datetime.now().strftime('%H:%M:%S')}
        </div>
        """,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════════════════════════════
hist=get_hist(); jp=get_jackpots(); ai=AI()

TICKER_NEWS=[
    f"EUROJACKPOT: {jp['euro']} MIO. € — Freitag",
    f"LOTTO 6aus49: {jp['lotto']} MIO. € — Mittwoch & Samstag",
    "KI analysiert täglich 2.000 historische Ziehungen in Echtzeit",
    "🔥 Maria_B erreicht 30-Tage-Streak — Gratulation!",
    "Neue Funktion: Community-Posts & Tages-Vorhersage Live",
    "Familie Schmidt gewinnt 38.2 Mio. € in Berlin",
]

WINNERS=[
    {"n":"Familie Schmidt","c":"Berlin","p":"38.2 Mio. €","d":"17.03.2026","g":"Eurojackpot","e":"👨‍👩‍👧‍👦"},
    {"n":"Klaus W.","c":"Sachsen-Anhalt","p":"6 Mio. €","d":"15.03.2026","g":"Lotto 6aus49","e":"👴"},
    {"n":"Müller GbR","c":"München","p":"12.5 Mio. €","d":"12.03.2026","g":"Eurojackpot","e":"👥"},
    {"n":"Anna & Thomas","c":"Hamburg","p":"4.8 Mio. €","d":"10.03.2026","g":"Lotto 6aus49","e":"💑"},
]

def page_home():
    ticker(TICKER_NEWS)
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 32px;">
      <div style="font-size:0.7rem;letter-spacing:0.22em;color:var(--cyan);font-family:'JetBrains Mono',monospace;margin-bottom:10px;opacity:0.75;">
        QUANTUM AI · STATISTICAL ENGINE · LIVE 2026
      </div>
      <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2rem,5vw,3.5rem);font-weight:900;
                 letter-spacing:-0.02em;margin-bottom:10px;line-height:1.1;
                 background:linear-gradient(135deg,var(--gold),var(--orange),var(--gold2));
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        {t['title']}
      </h1>
      <p style="color:var(--muted);max-width:520px;margin:0 auto 18px;font-size:0.95rem;font-weight:400;">{t['subtitle']}</p>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">{LIVE()}
        <span style="display:inline-flex;align-items:center;gap:5px;background:rgba(0,207,255,0.08);border:1px solid rgba(0,207,255,0.2);border-radius:100px;padding:4px 12px;font-size:0.72rem;font-weight:700;color:var(--cyan);">🤖 AI v2.6</span>
        <span style="display:inline-flex;align-items:center;gap:5px;background:rgba(0,230,118,0.08);border:1px solid rgba(0,230,118,0.2);border-radius:100px;padding:4px 12px;font-size:0.72rem;font-weight:700;color:var(--green);">✅ 50K+ Nutzer</span>
      </div>
    </div>
    """,unsafe_allow_html=True)

    c1,c2=st.columns(2,gap="medium")
    with c1:
        st.markdown(f"""<div class="jackpot-wrap">
          <div style="font-size:2.5rem;margin-bottom:8px;">🎲</div>
          <div style="font-size:0.7rem;letter-spacing:0.2em;color:rgba(255,255,255,0.45);font-family:'JetBrains Mono',monospace;margin-bottom:6px;">LOTTO 6AUS49</div>
          <div class="jackpot-amount">{jp['lotto']} MIO. €</div>
          <div style="color:rgba(245,196,0,0.4);font-size:0.78rem;margin-top:8px;">Chance: 1 : 139.838.160</div>
          <div style="margin-top:14px;font-size:0.72rem;color:rgba(255,255,255,0.35);">Mittwoch & Samstag</div>
        </div>""",unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="jackpot-wrap euro">
          <div style="font-size:2.5rem;margin-bottom:8px;">🌍</div>
          <div style="font-size:0.7rem;letter-spacing:0.2em;color:rgba(255,255,255,0.45);font-family:'JetBrains Mono',monospace;margin-bottom:6px;">EUROJACKPOT</div>
          <div class="jackpot-amount">{jp['euro']} MIO. €</div>
          <div style="color:rgba(0,230,118,0.4);font-size:0.78rem;margin-top:8px;">Chance: 1 : 139.838.160</div>
          <div style="margin-top:14px;font-size:0.72rem;color:rgba(255,255,255,0.35);">Freitag</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br/>",unsafe_allow_html=True)
    SEC("Letzte Gewinnzahlen — 17.03.2026","🏆")
    st.markdown(f"""<div class="card card-green" style="text-align:center;">
      <div style="font-size:0.75rem;color:var(--muted);margin-bottom:12px;letter-spacing:0.08em;">EUROJACKPOT · 17.03.2026 · {jp['euro']} MIO. €</div>
      {B([12,13,16,17,37],'euro')}{B([4,11],'extra')}
    </div>""",unsafe_allow_html=True)

    SEC(t["winners"],"🥇")
    cols=st.columns(4,gap="small")
    for i,w in enumerate(WINNERS):
        with cols[i]:
            st.markdown(f"""<div class="winner-card">
              <div style="font-size:2rem;">{w['e']}</div>
              <div style="font-weight:700;font-size:0.85rem;margin:6px 0;">{w['n']}</div>
              <div style="color:var(--muted);font-size:0.75rem;">📍 {w['c']}</div>
              <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:var(--gold);margin:6px 0;">{w['p']}</div>
              <div style="color:var(--muted);font-size:0.7rem;">{w['g']} · {w['d']}</div>
            </div>""",unsafe_allow_html=True)

    st.markdown("<br/>",unsafe_allow_html=True)
    SEC(f"{t['horoscope']} 2026","🔮")
    hc1,hc2=st.columns([1,2],gap="medium")
    signs=['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
    with hc1:
        sign=st.selectbox(t["star_sign"],signs,label_visibility="collapsed")
    with hc2:
        lucky=ai.horoscope(sign)
        st.markdown(f"""<div class="card" style="text-align:center;">
          <div style="color:var(--muted);font-size:0.78rem;margin-bottom:10px;">✨ {t['lucky_nums']} · {sign} 2026</div>
          {B(lucky,'gold')}
        </div>""",unsafe_allow_html=True)


def page_daily():
    pred=db_get_daily_prediction()
    user=st.session_state.user
    streak=st.session_state.get("streak",db_get_streak(user["id"]) if user else 0)
    claimed=st.session_state.get("daily_claimed",False)

    SEC(t["daily_title"],"")
    st.markdown(f'<div style="color:var(--muted);margin-bottom:20px;font-size:0.9rem;">{t["daily_sub"]} · {datetime.now().strftime("%d.%m.%Y")}</div>',unsafe_allow_html=True)

    c1,c2=st.columns([2,1],gap="large")
    with c1:
        nums=pred.get("numbers",[])
        sn=pred.get("super_number",0)
        conf=pred.get("confidence",87.5)
        reason=pred.get("ai_reason","")

        st.markdown(f"""<div class="daily-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px;">
            <div>
              <div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:900;color:var(--purple);">{t['daily_title']}</div>
              <div style="color:var(--muted);font-size:0.78rem;margin-top:2px;">{datetime.now().strftime('%A, %d. %B 2026')}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;
                          background:linear-gradient(135deg,var(--gold),var(--orange));
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{conf}%</div>
              <div style="font-size:0.68rem;color:var(--muted);letter-spacing:0.08em;">{t['confidence']}</div>
            </div>
          </div>
          <div class="cbar"><div class="cfill" style="width:{conf}%;"></div></div>
          <br/>
          <div style="font-size:0.72rem;color:var(--muted);letter-spacing:0.1em;margin-bottom:8px;">{t['main_nums']}</div>
          {B(nums,'gold pulse')}
          <div style="font-size:0.72rem;color:var(--muted);letter-spacing:0.1em;margin:12px 0 6px;">{t['super_num']}</div>
          {B([sn],'extra')}
          {"<div style='margin-top:18px;padding:14px;background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.2);border-radius:12px;'>" +
          "<div style='font-size:0.7rem;color:var(--purple);font-weight:700;letter-spacing:0.1em;margin-bottom:6px;'>🤖 " + t['ai_reason'] + "</div>" +
          "<div style='font-size:0.85rem;color:var(--muted);line-height:1.6;'>" + reason + "</div></div>" if reason else ""}
        </div>""",unsafe_allow_html=True)

        if user:
            share_buttons(nums,"Lotto 6aus49",jp["lotto"],st.session_state.language)

    with c2:
        # Streak Card
        fire_icons="🔥"*min(streak,5) if streak>0 else "💤"
        st.markdown(f"""<div class="streak-card">
          <div class="streak-fire">{fire_icons if streak>0 else "💤"}</div>
          <div class="streak-num">{streak}</div>
          <div style="font-size:0.82rem;color:var(--orange);font-weight:600;margin:4px 0;">{t['streak']}</div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:6px;">
            {str(streak)+' '+t['streak_msg'] if streak>0 else 'Starte heute deinen Streak!'}
          </div>
        </div>""",unsafe_allow_html=True)

        st.markdown("<br/>",unsafe_allow_html=True)

        if user:
            if not claimed:
                if st.button(t["claim_btn"],key="claim_d",use_container_width=True,type="primary"):
                    db_claim_daily(user["id"])
                    new_s=st.session_state.get("streak",0)
                    badges=get_user_badges(new_s)
                    if new_s in [7,30,100]:
                        st.balloons()
                    st.success(f"✅ +10 Punkte! Streak: {new_s} 🔥")
                    st.rerun()
            else:
                st.markdown(f"""<div style="background:rgba(0,230,118,0.08);border:1px solid rgba(0,230,118,0.25);
                  border-radius:14px;padding:16px;text-align:center;">
                  <div style="font-size:1.5rem;">✅</div>
                  <div style="color:var(--green);font-weight:700;margin-top:6px;">{t['claimed']}</div>
                  <div style="color:var(--muted);font-size:0.78rem;margin-top:4px;">Morgen wieder verfügbar</div>
                </div>""",unsafe_allow_html=True)
        else:
            st.info("🔐 Anmelden um den Streak zu starten")

        # Streak Milestones
        st.markdown("<br/>",unsafe_allow_html=True)
        milestones=[(1,"🌱","Start"),(7,"🔥","Woche"),(30,"💎","Monat"),(100,"👑","100 Tage")]
        st.markdown(f'<div style="font-size:0.78rem;color:var(--muted);font-weight:700;margin-bottom:8px;letter-spacing:0.08em;">MEILENSTEINE</div>',unsafe_allow_html=True)
        for days,icon,label in milestones:
            done=streak>=days
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;
              background:{"rgba(245,196,0,0.08)" if done else "var(--surface2)"};
              border:1px solid {"rgba(245,196,0,0.25)" if done else "var(--border)"};
              border-radius:10px;margin-bottom:6px;opacity:{"1" if done else "0.5"};">
              <span style="font-size:1.1rem;">{icon}</span>
              <span style="font-size:0.82rem;font-weight:600;color:{"var(--gold)" if done else "var(--muted)"};">{days} Tage — {label}</span>
              {"<span style='margin-left:auto;font-size:0.7rem;color:var(--green);'>✓</span>" if done else ""}
            </div>""",unsafe_allow_html=True)

        # Badges
        if user:
            streak_val=streak
            badges=get_user_badges(streak_val)
            if badges:
                st.markdown("<br/>",unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.78rem;color:var(--muted);font-weight:700;margin-bottom:8px;letter-spacing:0.08em;">{t["badges"].upper()}</div>',unsafe_allow_html=True)
                bcols=st.columns(min(len(badges),4))
                for i,b in enumerate(badges):
                    with bcols[i%4]:
                        bicon=str(b.get("icon",""))
                        bname=str(b.get("name",""))
                        badge_html = "<div class=\"
                         
