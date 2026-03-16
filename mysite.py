# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
from dotenv import load_dotenv
import sqlite3
import hashlib
import time
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="AI Negotiator",
    page_icon="🤖",
    layout="wide"
)

# ==================== تهيئة الجلسة ====================
if 'user_id' not in st.session_state:
    st.session_state.user_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
if 'language' not in st.session_state:
    st.session_state.language = 'ar'

# ==================== نظام اللغات ====================
LANGUAGES = {
    'ar': {
        'app_name': '🤖 AI Negotiator',
        'subtitle': 'مفاوضك الذكي الشخصي',
        'menu_home': '🏠 الرئيسية',
        'menu_salary': '💰 تفاوض راتب',
        'total_savings': '💰 إجمالي التوفير',
        'start': '🚀 ابدأ'
    },
    'en': {
        'app_name': '🤖 AI Negotiator',
        'subtitle': 'Your Personal Smart Negotiator',
        'menu_home': '🏠 Home',
        'menu_salary': '💰 Salary Negotiation',
        'total_savings': '💰 Total Savings',
        'start': '🚀 Start'
    }
}

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.title("🤖 AI Negotiator")
    
    lang = st.radio("Language", ["ar", "en"], 
                    format_func=lambda x: "🇸🇦 عربي" if x=="ar" else "🇬🇧 English")
    st.session_state.language = lang
    
    menu = st.radio("", [
        LANGUAGES[lang]['menu_home'],
        LANGUAGES[lang]['menu_salary']
    ])

# ==================== الصفحة الرئيسية ====================
_ = LANGUAGES[st.session_state.language]

if menu == _['menu_home']:
    st.title(_['app_name'])
    st.markdown(f"### {_['subtitle']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("المفاوضات", "0")
    col2.metric(_['total_savings'], "0 ريال")
    col3.metric("نسبة النجاح", "0%")

elif menu == _['menu_salary']:
    st.header(_['menu_salary'])
    
    with st.form("salary_form"):
        company = st.text_input("اسم الشركة")
        current_offer = st.number_input("العرض الحالي", min_value=0)
        desired = st.number_input("الراتب المطلوب", min_value=0)
        
        if st.form_submit_button(_['start']):
            st.success("تم! شاهد بريدك الإلكتروني للتقييم")
