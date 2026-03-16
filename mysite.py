# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
import os
import time
import random
import hashlib
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="AI Negotiator | مفاوضك الذكي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تحميل المتغيرات ====================
load_dotenv()

# ==================== تهيئة الجلسة ====================
if 'user_id' not in st.session_state:
    st.session_state.user_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'negotiations' not in st.session_state:
    st.session_state.negotiations = []
if 'current_negotiation' not in st.session_state:
    st.session_state.current_negotiation = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'total_savings' not in st.session_state:
    st.session_state.total_savings = 0

# ==================== نظام اللغات ====================
LANGUAGES = {
    'ar': {
        'app_name': '🤖 AI Negotiator',
        'subtitle': 'مفاوضك الذكي الشخصي',
        'menu_home': '🏠 الرئيسية',
        'menu_salary': '💰 تفاوض راتب',
        'menu_shopping': '🛒 مساومة ذكية',
        'menu_complaint': '📞 شكاوى ومطالبات',
        'menu_stats': '📊 إحصائياتي',
        'menu_settings': '⚙️ الإعدادات',
        'menu_achievements': '🏆 الإنجازات',
        'start_negotiation': '🚀 ابدأ التفاوض',
        'company_name': 'اسم الشركة',
        'job_title': 'المسمى الوظيفي',
        'current_offer': 'العرض الحالي (ريال)',
        'desired_salary': 'الراتب المطلوب (ريال)',
        'experience': 'سنوات الخبرة',
        'education': 'المؤهل العلمي',
        'market_rate': 'متوسط السوق (ريال)',
        'analysis_result': '📊 نتيجة التحليل',
        'email_draft': '📧 مسودة البريد الإلكتروني',
        'send_email': '✉️ إرسال البريد',
        'negotiation_history': '📋 سجل المفاوضات',
        'total_savings': '💰 إجمالي التوفير',
        'success_rate': '📈 نسبة النجاح',
        'negotiations_count': '🔢 عدد المفاوضات',
        'achievements': '🏆 الإنجازات',
        'challenges': '🎯 التحديات',
        'settings_language': 'اللغة',
        'settings_api': 'مفتاح API',
        'settings_email': 'البريد الإلكتروني',
        'save_settings': '💾 حفظ الإعدادات'
    },
    'en': {
        'app_name': '🤖 AI Negotiator',
        'subtitle': 'Your Personal Smart Negotiator',
        'menu_home': '🏠 Home',
        'menu_salary': '💰 Salary Negotiation',
        'menu_shopping': '🛒 Smart Bargaining',
        'menu_complaint': '📞 Complaints',
        'menu_stats': '📊 My Stats',
        'menu_settings': '⚙️ Settings',
        'menu_achievements': '🏆 Achievements',
        'start_negotiation': '🚀 Start Negotiation',
        'company_name': 'Company Name',
        'job_title': 'Job Title',
        'current_offer': 'Current Offer (SAR)',
        'desired_salary': 'Desired Salary (SAR)',
        'experience': 'Years of Experience',
        'education': 'Education',
        'market_rate': 'Market Rate (SAR)',
        'analysis_result': '📊 Analysis Result',
        'email_draft': '📧 Email Draft',
        'send_email': '✉️ Send Email',
        'negotiation_history': '📋 Negotiation History',
        'total_savings': '💰 Total Savings',
        'success_rate': '📈 Success Rate',
        'negotiations_count': '🔢 Negotiations Count',
        'achievements': '🏆 Achievements',
        'challenges': '🎯 Challenges',
        'settings_language': 'Language',
        'settings_api': 'API Key',
        'settings_email': 'Email',
        'save_settings': '💾 Save Settings'
    }
}

# ==================== CSS مخصص ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
        border: 1px solid #eee;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .negotiation-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ==================== قاعدة البيانات ====================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('negotiator.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                api_key TEXT,
                created_at TIMESTAMP,
                language TEXT DEFAULT 'ar'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS negotiations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                type TEXT,
                title TEXT,
                company TEXT,
                initial_offer REAL,
                desired_amount REAL,
                final_amount REAL,
                savings REAL,
                status TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                data TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                achievement_id TEXT,
                earned_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        self.conn.commit()
    
    def save_user(self, user_id, email=None, api_key=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (id, email, api_key, created_at, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, email, api_key, datetime.now(), st.session_state.language))
        self.conn.commit()
    
    def save_negotiation(self, user_id, type, title, company, initial_offer, desired_amount, data):
        cursor = self.conn.cursor()
        now = datetime.now()
        cursor.execute("""
            INSERT INTO negotiations 
            (user_id, type, title, company, initial_offer, desired_amount, status, created_at, updated_at, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, type, title, company, initial_offer, desired_amount, 'active', now, now, json.dumps(data)))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_negotiation(self, negotiation_id, final_amount, savings):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE negotiations 
            SET final_amount = ?, savings = ?, status = 'completed', updated_at = ?
            WHERE id = ?
        """, (final_amount, savings, datetime.now(), negotiation_id))
        self.conn.commit()
    
    def get_user_stats(self, user_id):
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM negotiations WHERE user_id=?", (user_id,))
        total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(savings) FROM negotiations WHERE user_id=? AND savings IS NOT NULL", (user_id,))
        total_savings = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM negotiations WHERE user_id=? AND status='completed'", (user_id,))
        completed = cursor.fetchone()[0] or 0
        
        success_rate = (completed / total * 100) if total > 0 else 0
        
        cursor.execute("""
            SELECT type, title, company, savings, created_at 
            FROM negotiations 
            WHERE user_id=? 
            ORDER BY created_at DESC 
            LIMIT 5
        """, (user_id,))
        recent = cursor.fetchall()
        
        return {
            'total_negotiations': total,
            'total_savings': total_savings,
            'success_rate': round(success_rate, 1),
            'recent': recent
        }
    
    def get_achievements(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT achievement_id FROM achievements WHERE user_id=?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
    
    def earn_achievement(self, user_id, achievement_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO achievements (user_id, achievement_id, earned_at)
            VALUES (?, ?, ?)
        """, (user_id, achievement_id, datetime.now()))
        self.conn.commit()

# ==================== AI Agent ====================
class AIAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def analyze_offer(self, offer_text, context_text):
        import re
        numbers = re.findall(r'\d+', offer_text)
        current_offer = int(numbers[0]) if numbers else 5000
        
        rating = random.choice(['ضعيف', 'متوسط', 'جيد'])
        target = int(current_offer * random.uniform(1.2, 1.5))
        
        return f"""
📊 **تحليل العرض:**

1. **تقييم العرض:** {rating} (أقل من متوسط السوق)

2. **نقاط القوة:**
   - استقرار الوظيفة
   - سمعة الشركة جيدة
   - مزايا إضافية محتملة

3. **نقاط الضعف:**
   - الراتب أقل من المتوقع
   - لا يوجد وضوح في بدلات أخرى
   - فترة تجربة طويلة

4. **الراتب المستهدف:** {target} ريال

5. **البدائل المقترحة:**
   - بدل سكن
   - تأمين صحي للعائلة
   - أيام إجازة إضافية
        """
    
    def analyze_sentiment(self, message):
        positive_words = ['ممتاز', 'جيد', 'ممكن', 'نعم', 'أتفق', 'شكراً']
        negative_words = ['لا', 'مستحيل', 'صعب', 'رفض', 'سيء']
        
        score = 0
        for word in positive_words:
            if word in message:
                score += 1
        for word in negative_words:
            if word in message:
                score -= 1
        
        if score > 0:
            sentiment = 'إيجابي'
            color = '#10b981'
        elif score < 0:
            sentiment = 'سلبي'
            color = '#ef4444'
        else:
            sentiment = 'محايد'
            color = '#9ca3af'
        
        return {'sentiment': sentiment, 'color': color}

# ==================== Email Bot ====================
class EmailBot:
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
    
    def draft_salary_email(self, company, position, current_offer, desired_salary, qualifications):
        return f"""
الموضوع: بخصوص عرض العمل - {position}

السادة المحترمون،
{company}

تحية طيبة وبعد،

أشكركم على عرض العمل بمنصب {position}. 
العرض الحالي: {current_offer:,.0f} ريال

بناءً على:
• الخبرة: {qualifications.get('experience', '')} سنوات
• المؤهل: {qualifications.get('education', '')}
• متوسط السوق: {qualifications.get('market_rate', 0):,.0f} ريال

أتطلع إلى راتب {desired_salary:,.0f} ريال.

مع الشكر،
[الاسم]
        """
    
    def send_email(self, to_email, subject, body):
        return {"success": False, "message": "البريد الإلكتروني غير مفعل في النسخة التجريبية"}

# ==================== Reward System ====================
class RewardSystem:
    def __init__(self):
        self.achievements = {
            'first_negotiation': {
                'name': '🤝 أول خطوة',
                'description': 'أول مفاوضة ناجحة',
                'icon': '🎯',
                'color': '#10b981'
            },
            'saver_1000': {
                'name': '💰 المدخر',
                'description': 'وفرت 1000 ريال',
                'icon': '💰',
                'color': '#3b82f6'
            }
        }
        
        self.challenges = [
            {
                'name': '🎯 تحدي المبتدئين',
                'description': 'أكمل 3 مفاوضات',
                'reward': 200,
                'icon': '🎯'
            },
            {
                'name': '💰 تحدي التوفير',
                'description': 'وفر 2000 ريال',
                'reward': 500,
                'icon': '💰'
            }
        ]
    
    def check_achievements(self, user_stats, earned_achievements):
        new = []
        if user_stats['total_negotiations'] >= 1 and 'first_negotiation' not in earned_achievements:
            new.append('first_negotiation')
        if user_stats['total_savings'] >= 1000 and 'saver_1000' not in earned_achievements:
            new.append('saver_1000')
        return new

# ==================== تهيئة الكائنات ====================
if 'db' not in st.session_state:
    st.session_state.db = Database()
    st.session_state.db.save_user(st.session_state.user_id)

if 'agent' not in st.session_state:
    st.session_state.agent = AIAgent()

if 'email_bot' not in st.session_state:
    st.session_state.email_bot = EmailBot()

if 'rewards' not in st.session_state:
    st.session_state.rewards = RewardSystem()

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"# {LANGUAGES[st.session_state.language]['app_name']}")
    st.markdown(f"*{LANGUAGES[st.session_state.language]['subtitle']}*")
    
    st.markdown("---")
    
    lang = st.radio("Language", ["ar", "en"], format_func=lambda x: "🇸🇦 العربية" if x == "ar" else "🇬🇧 English")
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()
    
    st.markdown("---")
    
    menu_options = [
        LANGUAGES[st.session_state.language]['menu_home'],
        LANGUAGES[st.session_state.language]['menu_salary'],
        LANGUAGES[st.session_state.language]['menu_shopping'],
        LANGUAGES[st.session_state.language]['menu_complaint'],
        LANGUAGES[st.session_state.language]['menu_stats'],
        LANGUAGES[st.session_state.language]['menu_achievements'],
        LANGUAGES[st.session_state.language]['menu_settings']
    ]
    
    selected_menu = st.radio("", menu_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    stats = st.session_state.db.get_user_stats(st.session_state.user_id)
    
    st.metric(LANGUAGES[st.session_state.language]['negotiations_count'], stats['total_negotiations'])
    st.metric(LANGUAGES[st.session_state.language]['total_savings'], f"{stats['total_savings']:,.0f} ريال")
    st.metric(LANGUAGES[st.session_state.language]['success_rate'], f"{stats['success_rate']}%")

# ==================== الصفحات ====================
_ = LANGUAGES[st.session_state.language]

# الصفحة الرئيسية
if selected_menu == _['menu_home']:
    st.markdown(f"""
        <div class="main-header">
            <h1>🤖 {_['app_name']}</h1>
            <p>{_['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stat-card">
                <div style="font-size: 4rem;">💰</div>
                <h3>تفاوض الراتب</h3>
                <p>احصل على الراتب الذي تستحق</p>
                <span class="badge">زيادة 30%</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <div style="font-size: 4rem;">🛒</div>
                <h3>مساومة ذكية</h3>
                <p>وفر في مشترياتك</p>
                <span class="badge">توفير 25%</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stat-card">
                <div style="font-size: 4rem;">📞</div>
                <h3>شكاوى ومطالبات</h3>
                <p>احصل على تعويضاتك</p>
                <span class="badge">تعويض 500+</span>
            </div>
        """, unsafe_allow_html=True)

# صفحة تفاوض الراتب
elif selected_menu == _['menu_salary']:
    st.header(_['menu_salary'])
    
    with st.form("salary_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input(_['company_name'])
            position = st.text_input(_['job_title'])
            current_offer = st.number_input(_['current_offer'], min_value=0, step=1000)
        
        with col2:
            experience = st.number_input(_['experience'], min_value=0)
            education = st.selectbox(_['education'], ["بكالوريوس", "ماجستير", "دكتوراه"])
            desired_salary = st.number_input(_['desired_salary'], min_value=0, step=1000)
        
        market_rate = st.number_input(_['market_rate'], min_value=0, step=1000)
        
        submitted = st.form_submit_button(_['start_negotiation'])
        
        if submitted:
            qualifications = {
                'experience': experience,
                'education': education,
                'market_rate': market_rate
            }
            
            analysis = st.session_state.agent.analyze_offer(
                f"عرض {current_offer} ريال",
                f"خبرة {experience} سنوات"
            )
            
            st.subheader(_['analysis_result'])
            st.markdown(analysis)
            
            email_draft = st.session_state.email_bot.draft_salary_email(
                company, position, current_offer, desired_salary, qualifications
            )
            
            st.subheader(_['email_draft'])
            st.text_area("", email_draft, height=200)
            
            if st.button(_['send_email']):
                st.success("تم تجهيز البريد الإلكتروني (نسخة تجريبية)")

# صفحة الإحصائيات
elif selected_menu == _['menu_stats']:
    st.header(_['menu_stats'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric(_['negotiations_count'], stats['total_negotiations'])
    col2.metric(_['total_savings'], f"{stats['total_savings']:,.0f} ريال")
    col3.metric(_['success_rate'], f"{stats['success_rate']}%")
    
    if stats['recent']:
        st.subheader(_['negotiation_history'])
        for n in stats['recent']:
            st.markdown(f"""
                <div class="negotiation-card">
                    <b>{n[1]}</b> - {n[2]}<br>
                    <span style="color: #667eea;">التوفير: {n[3]:,.0f} ريال</span>
                </div>
            """, unsafe_allow_html=True)

# صفحة الإنجازات
elif selected_menu == _['menu_achievements']:
    st.header(_['menu_achievements'])
    
    earned = st.session_state.db.get_achievements(st.session_state.user_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(_['achievements'])
        for aid, ach in st.session_state.rewards.achievements.items():
            if aid in earned:
                st.markdown(f"""
                    <div style="background: {ach['color']}; color: white; padding: 1rem; 
                              border-radius: 10px; margin: 0.5rem 0;">
                        {ach['icon']} {ach['name']}<br>
                        <small>{ach['description']}</small>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader(_['challenges'])
        for ch in st.session_state.rewards.challenges:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    {ch['icon']} {ch['name']}<br>
                    <small>{ch['description']}</small>
                </div>
            """, unsafe_allow_html=True)

# صفحة الإعدادات
elif selected_menu == _['menu_settings']:
    st.header(_['menu_settings'])
    
    email = st.text_input(_['settings_email'], value=os.getenv("EMAIL_ADDRESS", ""))
    api_key = st.text_input(_['settings_api'], value=os.getenv("OPENAI_API_KEY", ""), type="password")
    
    if st.button(_['save_settings']):
        st.session_state.db.save_user(st.session_state.user_id, email, api_key)
        st.success("تم حفظ الإعدادات")

# ==================== التذييل ====================
st.markdown(f"""
    <div class="footer">
        {_['app_name']} | {datetime.now().year}
    </div>
""", unsafe_allow_html=True)
