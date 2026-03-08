
import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration --- #
st.set_page_config(page_title="Syphax AI", page_icon="🤖")

# --- Configuration --- #
# Ensure GOOGLE_API_KEY is set in Streamlit secrets or environment variables
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
elif os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    st.error("GOOGLE_API_KEY not found. Please add it to Streamlit secrets or set it as an environment variable.")
    st.stop()

# --- Title Update --- #
st.title("🤖 Syphax Intelligent Assistant")

# --- Session State Initialization --- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Functions --- #
@st.cache_data(ttl=3600) # Cache for 1 hour to avoid frequent API calls
def get_available_models():
    """Lists available Gemini models that support generateContent."""
    try:
        all_models = genai.list_models()
        supported_models = []
        for m in all_models:
            if "generateContent" in m.supported_generation_methods:
                # Store the short name (e.g., 'gemini-1.5-flash')
                supported_models.append(m.name.split('/')[-1])
        return supported_models
    except Exception as e:
        st.error(f"Error listing models: {e}")
        return []

def select_model():
    """Selects the best available model, prioritizing gemini-1.5-flash."""
    available_models = get_available_models()
    
    if not available_models:
        st.error("No suitable Gemini models found. Please check your API key and regional access.")
        return None

    # Prioritize specific models
    preferred_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    for model_name in preferred_models:
        if model_name in available_models:
            return model_name

    # Fallback to any available model
    return available_models[0]

# --- Main Application Logic --- #

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask Syphax anything..."):
    # Add user message to chat history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Select model dynamically
    selected_model_name = select_model()
    if selected_model_name is None:
        st.stop()

    # Attempt to get a response from the AI model
    try:
        model = genai.GenerativeModel(selected_model_name)
        response = model.generate_content(prompt)
        
        # Display AI response and save to chat history
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"An error occurred: {e}")
