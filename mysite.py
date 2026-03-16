# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
import os
from dotenv import load_dotenv
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
import hashlib
import time
import random

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
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .ai-message {
        background: #f0f2f5;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    .negotiation-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .achievement-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .challenge-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
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
    
    .sidebar-content {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
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
        
        # جدول المستخدمين
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                api_key TEXT,
                created_at TIMESTAMP,
                language TEXT DEFAULT 'ar'
            )
        """)
        
        # جدول المفاوضات
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
        
        # جدول الرسائل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                negotiation_id INTEGER,
                sender TEXT,
                content TEXT,
                sentiment TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (negotiation_id) REFERENCES negotiations (id)
            )
        """)
        
        # جدول الإنجازات
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
    
    def save_message(self, negotiation_id, sender, content, sentiment):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (negotiation_id, sender, content, sentiment, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (negotiation_id, sender, content, sentiment, datetime.now()))
        self.conn.commit()
    
    def get_user_stats(self, user_id):
        cursor = self.conn.cursor()
        
        # عدد المفاوضات
        cursor.execute("SELECT COUNT(*) FROM negotiations WHERE user_id=?", (user_id,))
        total = cursor.fetchone()[0] or 0
        
        # مجموع التوفير
        cursor.execute("SELECT SUM(savings) FROM negotiations WHERE user_id=? AND savings IS NOT NULL", (user_id,))
        total_savings = cursor.fetchone()[0] or 0
        
        # نسبة النجاح
        cursor.execute("SELECT COUNT(*) FROM negotiations WHERE user_id=? AND status='completed'", (user_id,))
        completed = cursor.fetchone()[0] or 0
        
        success_rate = (completed / total * 100) if total > 0 else 0
        
        # آخر المفاوضات
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
    
    def earn_achievement(self, user_id, achievement_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO achievements (user_id, achievement_id, earned_at)
            VALUES (?, ?, ?)
        """, (user_id, achievement_id, datetime.now()))
        self.conn.commit()
    
    def get_achievements(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT achievement_id FROM achievements WHERE user_id=?", (user_id,))
        return [row[0] for row in cursor.fetchall()]

# ==================== AI Agent ====================
class AIAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        self.context = []
    
    def analyze_offer(self, offer_text, context_text):
        """تحليل العرض وتقديم استراتيجية"""
        if not self.api_key:
            return self.mock_analysis(offer_text, context_text)
        
        try:
            prompt = f"""
            أنت خبير تفاوض محترف. حلل هذا العرض بدقة:
            
            العرض: {offer_text}
            السياق: {context_text}
            
            قدم تحليلك في النقاط التالية:
            1. تقييم العرض (ضعيف/متوسط/ممتاز مع نسبة مئوية)
            2. نقاط القوة في العرض
            3. نقاط الضعف والثغرات
            4. استراتيجية التفاوض المقترحة (خطوات محددة)
            5. الكلمات المفتاحية التي يجب استخدامها
            6. الكلمات التي يجب تجنبها
            7. السعر/الراتب المستهدف المقترح
            8. البدائل والمزايا الإضافية التي يمكن طلبها
            
            كن دقيقاً ومهنياً واستخدم أسلوباً مقنعاً.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير تفاوض محترف مع 20 سنة خبرة."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self.mock_analysis(offer_text, context_text)
    
    def mock_analysis(self, offer_text, context_text):
        """تحليل تجريبي عند عدم وجود API"""
        import random
        
        # استخراج الأرقام من النص
        import re
        numbers = re.findall(r'\d+', offer_text)
        current_offer = int(numbers[0]) if numbers else 5000
        
        # توليد تحليل عشوائي لكن واقعي
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
        
        4. **استراتيجية المقترحة:**
           - ابدأ بشكرهم على العرض
           - قدم تحليلك لمتوسط السوق
           - اطلب زيادة {target-current_offer} ريال
           - تفاوض على بدلات إضافية
        
        5. **الراتب المستهدف:** {target} ريال
        
        6. **بدائل مقترحة:**
           - بدل سكن
           - تأمين صحي للعائلة
           - أيام إجازة إضافية
           - مرونة في العمل
        """
    
    def generate_response(self, message, strategy, role='user'):
        """توليد رد تفاوضي"""
        if not self.api_key:
            return self.mock_response(message, strategy)
        
        try:
            prompt = f"""
            أنت مفاوض محترف. استراتيجيتك: {strategy}
            
            رسالة الطرف الآخر: {message}
            
            اكتب رداً ذكياً:
            - مهنياً ومحترماً
            - مقنعاً ومنطقياً
            - يحقق أهداف التفاوض
            - يحافظ على العلاقة
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مفاوض محترف."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except:
            return self.mock_response(message, strategy)
    
    def mock_response(self, message, strategy):
        """رد تجريبي"""
        responses = [
            "شكراً لردكم. نقدر عرضكم ولكن نعتقد أن هناك مجالاً للتحسين.",
            "بناءً على خبراتنا ومؤهلاتنا، نتطلع إلى قيمة أعلى.",
            "هل يمكن مناقشة بعض المزايا الإضافية؟",
            "نقدر وقتكم ونتطلع للوصول لاتفاق يرضي الطرفين."
        ]
        return random.choice(responses)
    
    def analyze_sentiment(self, message):
        """تحليل المشاعر في النص"""
        positive_words = ['ممتاز', 'جيد', 'ممكن', 'نعم', 'أتفق', 'شكراً', 'تمام', 'رائع']
        negative_words = ['لا', 'مستحيل', 'صعب', 'رفض', 'سيء', 'للأسف', 'مرفوض']
        
        score = 0
        message = message.lower()
        
        for word in positive_words:
            if word in message:
                score += 1
        
        for word in negative_words:
            if word in message:
                score -= 1
        
        if score > 2:
            sentiment = 'إيجابي جداً'
            color = '#10b981'
        elif score > 0:
            sentiment = 'إيجابي'
            color = '#34d399'
        elif score == 0:
            sentiment = 'محايد'
            color = '#9ca3af'
        elif score > -2:
            sentiment = 'سلبي'
            color = '#f87171'
        else:
            sentiment = 'سلبي جداً'
            color = '#ef4444'
        
        return {
            'score': score,
            'sentiment': sentiment,
            'color': color
        }

# ==================== Email Bot ====================
class EmailBot:
    def __init__(self, email=None, password=None):
        self.email = email or os.getenv("EMAIL_ADDRESS")
        self.password = password or os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
    
    def send_email(self, to_email, subject, body):
        """إرسال بريد إلكتروني"""
        if not self.email or not self.password:
            return {"success": False, "message": "البريد الإلكتروني غير مضبوط"}
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return {"success": True, "message": "تم الإرسال بنجاح"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def draft_salary_email(self, company, position, current_offer, desired_salary, qualifications):
        """صياغة بريد تفاوض راتب"""
        return f"""
        الموضوع: بخصوص عرض العمل - {position}
        
        السادة المحترمون،
        {company}
        
        تحية طيبة وبعد،
        
        أشكركم جزيل الشكر على عرض العمل الكريم بمنصب {position}. أقدر كثيراً ثقتكم بي واهتمامكم بانضمامي لفريق العمل.
        
        بعد دراسة متأنية للعرض، أود مناقشة بند الراتب. العرض الحالي: {current_offer:,.0f} ريال
        
        بناءً على:
        • خبرتي المهنية: {qualifications.get('experience', '')} سنوات في المجال
        • مؤهلاتي العلمية: {qualifications.get('education', '')}
        • متوسط الرواتب في السوق لهذا المنصب: {qualifications.get('market_rate', 0):,.0f} ريال
        • إنجازاتي السابقة وإضافتي المتوقعة للشركة
        
        أتطلع إلى راتب يبلغ {desired_salary:,.0f} ريال. كما أنني منفتح لمناقشة مزايا إضافية مثل:
        • بدل سكن وتنقل
        • تأمين صحي شامل للعائلة
        • مكافآت أداء ربع سنوية
        • أيام إجازة إضافية
        • برامج تطوير مهني
        
        أثق أننا سنتوصل لاتفاق يرضي الطرفين ويعكس قيمة الدور والخبرات المطلوبة.
        
        أنا متاح لمناقشة هذه النقاط في أي وقت يناسبكم.
        
        مع جزيل الشكر والتقدير،
        {qualifications.get('name', '')}
        """
    
    def draft_complaint_email(self, company, service_type, issue, desired_compensation):
        """صياغة بريد شكوى"""
        return f"""
        الموضوع: شكوى بخصوص {service_type}
        
        السادة المحترمون،
        {company}
        
        تحية طيبة،
        
        أتواصل معكم اليوم بخصوص {issue} الذي واجهته مؤخراً مع خدمتكم.
        
        تفاصيل المشكلة:
        • تاريخ المشكلة: {datetime.now().strftime('%Y-%m-%d')}
        • نوع الخدمة: {service_type}
        • المشكلة بالتفصيل: {issue}
        
        هذا الموقف تسبب في {self.get_impact_text(service_type)}.
        
        أتطلع إلى:
        1. التحقيق في المشكلة
        2. إبلاغي بالنتائج
        3. تعويض مناسب: {desired_compensation}
        
        رقم حسابي/عميلي: [يرجى الإضافة]
        
        شاكراً لكم حسن تعاونكم،
        {st.session_state.user_id}
        """
    
    def get_impact_text(self, service_type):
        if service_type == 'اتصالات':
            return 'انقطاع الخدمة وتعطيل أعمالي'
        elif service_type == 'كهرباء':
            return 'تلف بعض الأجهزة المنزلية'
        elif service_type == 'مياه':
            return 'إزعاج كبير وتعطيل'
        else:
            return 'إزعاج كبير وتعطيل لأعمالي اليومية'

# ==================== Reward System ====================
class RewardSystem:
    def __init__(self):
        self.achievements = {
            'first_negotiation': {
                'name': '🤝 أول خطوة',
                'description': 'أول مفاوضة ناجحة',
                'icon': '🎯',
                'points': 100,
                'color': '#10b981'
            },
            'saver_1000': {
                'name': '💰 المدخر الصغير',
                'description': 'وفرت 1000 ريال',
                'icon': '💰',
                'points': 200,
                'color': '#3b82f6'
            },
            'saver_5000': {
                'name': '💎 المدخر المحترف',
                'description': 'وفرت 5000 ريال',
                'icon': '💎',
                'points': 500,
                'color': '#8b5cf6'
            },
            'saver_10000': {
                'name': '👑 أسطورة التوفير',
                'description': 'وفرت 10000 ريال',
                'icon': '👑',
                'points': 1000,
                'color': '#f59e0b'
            },
            'negotiator_5': {
                'name': '🔰 مفاوض مبتدئ',
                'description': '5 مفاوضات ناجحة',
                'icon': '🔰',
                'points': 150,
                'color': '#14b8a6'
            },
            'negotiator_20': {
                'name': '⚡ مفاوض محترف',
                'description': '20 مفاوضة ناجحة',
                'icon': '⚡',
                'points': 400,
                'color': '#ec4899'
            },
            'negotiator_50': {
                'name': '🏆 أيقونة التفاوض',
                'description': '50 مفاوضة ناجحة',
                'icon': '🏆',
                'points': 1000,
                'color': '#ef4444'
            },
            'challenge_complete': {
                'name': '🎮 بطل التحديات',
                'description': 'أكملت أول تحدي',
                'icon': '🎮',
                'points': 150,
                'color': '#f97316'
            }
        }
        
        self.challenges = [
            {
                'id': 'challenge_1',
                'name': '🎯 تحدي المبتدئين',
                'description': 'أكمل 3 مفاوضات في أسبوع',
                'reward': 200,
                'icon': '🎯',
                'days': 7,
                'requirement': 3
            },
            {
                'id': 'challenge_2',
                'name': '💰 تحدي التوفير',
                'description': 'وفر 2000 ريال في شهر',
                'reward': 500,
                'icon': '💰',
                'days': 30,
                'requirement': 2000
            },
            {
                'id': 'challenge_3',
                'name': '⚡ تحدي السرعة',
                'description': 'أنجز مفاوضة في أقل من ساعة',
                'reward': 150,
                'icon': '⚡',
                'requirement': 'speed'
            },
            {
                'id': 'challenge_4',
                'name': '🛡️ تحدي الصمود',
                'description': 'تفاوض لمدة 5 جولات دون استسلام',
                'reward': 300,
                'icon': '🛡️',
                'requirement': 5
            },
            {
                'id': 'challenge_5',
                'name': '🎪 تحدي التنوع',
                'description': 'جرب 3 أنواع مختلفة من المفاوضات',
                'reward': 400,
                'icon': '🎪',
                'requirement': 3
            }
        ]
    
    def check_achievements(self, user_stats, earned_achievements):
        """فحص الإنجازات المستحقة"""
        new_achievements = []
        
        # إنجاز أول مفاوضة
        if user_stats['total_negotiations'] >= 1 and 'first_negotiation' not in earned_achievements:
            new_achievements.append('first_negotiation')
        
        # إنجازات التوفير
        savings = user_stats['total_savings']
        if savings >= 10000 and 'saver_10000' not in earned_achievements:
            new_achievements.append('saver_10000')
        elif savings >= 5000 and 'saver_5000' not in earned_achievements:
            new_achievements.append('saver_5000')
        elif savings >= 1000 and 'saver_1000' not in earned_achievements:
            new_achievements.append('saver_1000')
        
        # إنجازات عدد المفاوضات
        total = user_stats['total_negotiations']
        if total >= 50 and 'negotiator_50' not in earned_achievements:
            new_achievements.append('negotiator_50')
        elif total >= 20 and 'negotiator_20' not in earned_achievements:
            new_achievements.append('negotiator_20')
        elif total >= 5 and 'negotiator_5' not in earned_achievements:
            new_achievements.append('negotiator_5')
        
        return new_achievements

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
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;">
                {LANGUAGES[st.session_state.language]['app_name']}
            </h1>
            <p style="color: #666;">{LANGUAGES[st.session_state.language]['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # اختيار اللغة
    lang_cols = st.columns(2)
    with lang_cols[0]:
        if st.button("🇸🇦 العربية", use_container_width=True):
            st.session_state.language = 'ar'
            st.rerun()
    with lang_cols[1]:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    st.markdown("---")
    
    # القائمة الرئيسية
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
    
    # إحصائيات سريعة
    stats = st.session_state.db.get_user_stats(st.session_state.user_id)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1rem; border-radius: 10px; color: white;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            LANGUAGES[st.session_state.language]['negotiations_count'],
            stats['total_negotiations']
        )
    with col2:
        st.metric(
            LANGUAGES[st.session_state.language]['success_rate'],
            f"{stats['success_rate']}%"
        )
    
    st.metric(
        LANGUAGES[st.session_state.language]['total_savings'],
        f"{stats['total_savings']:,.0f} ريال"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # آخر المفاوضات
    if stats['recent']:
        st.markdown("---")
        st.markdown("📋 **آخر المفاوضات**")
        for n in stats['recent'][:3]:
            st.markdown(f"""
                <div style="font-size: 0.9rem; padding: 0.3rem; 
                           border-bottom: 1px solid #eee;">
                    {n[1]}<br>
                    <span style="color: #667eea;">{n[3]:,.0f} ريال</span>
                </div>
            """, unsafe_allow_html=True)

# ==================== الصفحة الرئيسية ====================
if selected_menu == LANGUAGES[st.session_state.language]['menu_home']:
    st.markdown(f"""
        <div class="main-header">
            <h1>🤖 {LANGUAGES[st.session_state.language]['app_name']}</h1>
            <p style="font-size: 1.2rem;">{LANGUAGES[st.session_state.language]['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات رئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 3rem;">💰</div>
                <div class="metric-value">{stats['total_savings']:,.0f}</div>
                <div class="metric-label">{LANGUAGES[st.session_state.language]['total_savings']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 3rem;">📊</div>
                <div class="metric-value">{stats['success_rate']}%</div>
                <div class="metric-label">{LANGUAGES[st.session_state.language]['success_rate']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 3rem;">🔢</div>
                <div class="metric-value">{stats['total_negotiations']}</div>
                <div class="metric-label">{LANGUAGES[st.session_state.language]['negotiations_count']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 3rem;">🏆</div>
                <div class="metric-value">{len(st.session_state.db.get_achievements(st.session_state.user_id))}</div>
                <div class="metric-label">{LANGUAGES[st.session_state.language]['achievements']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # أنواع المفاوضات
    st.markdown("---")
    st.subheader("🎯 اختر نوع المفاوضة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stat-card" style="cursor: pointer;" onclick="alert('test')">
                <div style="font-size: 4rem;">💰</div>
                <h3>تفاوض الراتب</h3>
                <p>احصل على الراتب الذي تستحق</p>
                <div class="badge">متوسط الزيادة: 30%</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ابدأ", key="home_salary"):
            st.session_state.selected = LANGUAGES[st.session_state.language]['menu_salary']
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <div style="font-size: 4rem;">🛒</div>
                <h3>مساومة ذكية</h3>
                <p>وفر في مشترياتك</p>
                <div class="badge">متوسط التوفير: 25%</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ابدأ", key="home_shopping"):
            st.session_state.selected = LANGUAGES[st.session_state.language]['menu_shopping']
            st.rerun()
    
    with col3:
        st.markdown("""
            <div class="stat-card">
                <div style="font-size: 4rem;">📞</div>
                <h3>شكاوى ومطالبات</h3>
                <p>احصل على تعويضاتك</p>
                <div class="badge">متوسط التعويض: 500+</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ابدأ", key="home_complaint"):
            st.session_state.selected = LANGUAGES[st.session_state.language]['menu_complaint']
            st.rerun()
    
    # آخر النشاطات
    st.markdown("---")
    st.subheader("📋 آخر النشاطات")
    
    if stats['recent']:
        for n in stats['recent']:
            st.markdown(f"""
                <div class="negotiation-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span><b>{n[1]}</b> - {n[2]}</span>
                        <span class="badge">+{n[3]:,.0f} ريال</span>
                    </div>
                    <div style="color: #666; font-size: 0.9rem;">
                        {n[4][:10]}
