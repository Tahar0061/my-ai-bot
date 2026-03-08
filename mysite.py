import streamlit as st
import google.generativeai as genai
import os
import datetime

# --- Page Configuration --- #
st.set_page_config(page_title="Syphax AI Pro", page_icon="✨", layout="wide")

# --- Custom CSS for Advanced Glassmorphism & Futuristic UI --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }

    /* Animated Dark Background */
    .stApp {
        background: linear-gradient(225deg, #0a0a0a, #1a1a1a, #2a2a2a, #1a1a1a);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        background-attachment: fixed;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Advanced Glassmorphism Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 3.5rem;
        margin-top: 2.5rem;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Futuristic Title */
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #0ea5e9 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(14, 165, 233, 0.6);
    }

    /* Chat Bubbles Styling */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Status Bar Footer */
    .footer-status {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0,0,0,0.8);
        padding: 10px 20px;
        color: #0ea5e9;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8em;
        display: flex;
        justify-content: space-between;
        z-index: 1000;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- API Configuration --- #
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
elif os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    st.error("API Key missing.")
    st.stop()

st.title("✨ Syphax AI Pro")

# --- Sidebar Widgets --- #
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Weather Widget (Simulated)
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.1);">
        <h4 style="color: #0ea5e9; margin:0;"><i class="fas fa-cloud-sun"></i> Weather</h4>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <span style="font-size: 2em;">24°C</span>
            <span>Sunny</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    language = st.selectbox("🌐 Language", ["English", "العربية", "Français"])
    persona = st.selectbox("👤 Persona", ["Assistant", "Creative", "Technical"])
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Chat History --- #
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input & Response --- #
if prompt := st.chat_input("Message Syphax Pro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

# --- Footer Status Bar --- #
st.markdown(f"""
<div class="footer-status">
    <span><i class="fas fa-microchip"></i> System: Online</span>
    <span><i class="fas fa-clock"></i> {datetime.datetime.now().strftime("%H:%M:%S")} UTC</span>
    <span><i class="fas fa-network-wired"></i> Secure Connection</span>
</div>
""", unsafe_allow_html=True)




