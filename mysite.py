
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
from PIL import Image # تصحيح: كان لديك pil، والصحيح هو PIL
import io
import base64

# إعداد الصفحة
st.set_page_config(
    page_title="طاهر | الطقس الذكي",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تثبيت التصميم الحديث (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'IBM Plex Sans Arabic', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
