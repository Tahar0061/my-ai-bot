import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration --- #
st.set_page_config(page_title="Syphax AI", page_icon="🤖", layout="wide")

# --- Optimized CSS for Performance --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    /* Optimized Static Gradient Background (Faster than Animation) */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        background-attachment: fixed;
    }

    /* Light Glassmorphism (Optimized Blur) */
    .main .block-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        backdrop-filter: blur(8px); /* Reduced blur for speed */
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin-top: 1rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Chat Bubbles Optimization */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 8px !important;
    }

    h1 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Hide unnecessary Streamlit elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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

st.title("🤖 Syphax AI")

# --- Sidebar --- #
with st.sidebar:
    st.header("⚙️ Syphax Panel")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("v2.0 | Optimized for Speed")

# --- Chat History --- #
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input & Response --- #
if prompt := st.chat_input("Message Syphax..."):
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

