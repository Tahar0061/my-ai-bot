
import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration --- #
st.set_page_config(page_title="Syphax AI", page_icon="🤖", layout="wide")

# --- Custom CSS for Glassmorphism and Styling --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
        color: #E0E0E0;
    }

    /* Animated Background */
    body {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #1e293b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Main container styling */
    .stApp {
        background: rgba(0,0,0,0) !important;
    }

    /* Glassmorphism effect for main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3rem;
        margin-top: 2rem;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Chat input styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }

    /* Titles and text */
    h1 {
        color: #38bdf8 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

</style>
""", unsafe_allow_html=True)

# --- Configuration --- #
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
elif os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    st.error("GOOGLE_API_KEY not found. Please add it to secrets.")
    st.stop()

st.title("🤖 Syphax Intelligent Assistant")

# --- Sidebar --- #
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    assistant_type = st.selectbox("Assistant Persona", ["Helpful", "Professional", "Creative"])
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.info("Syphax is ready to help!")

# --- Chat Logic --- #
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Syphax anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Auto-select best model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
