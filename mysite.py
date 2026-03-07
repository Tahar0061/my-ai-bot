import streamlit as st
import requests
import json

st.title("🤖 مساعدي الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("اسألني أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        full_res = ""
        placeholder = st.empty()
        try:
            url = "http://localhost:11434/api/generate"
            payload = {"model": "llama3", "prompt": prompt, "stream": True}
            r = requests.post(url, json=payload, stream=True)
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    full_res += chunk.get("response", "")
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except:
            st.error("تأكد أن Ollama يعمل!")