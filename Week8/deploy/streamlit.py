import streamlit as st
import requests
import config

# Page config
st.set_page_config(page_title="Medical Assistant", page_icon="🏥")
st.title("🏥 Medical Assistant Chatbot")
st.caption("Powered by TinyLlama ChatDoctor — Week 8 Capstone")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar settings
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.1, 1.0, config.TEMPERATURE)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, config.MAX_TOKENS)
top_k = st.sidebar.slider("Top-K", 1, 100, config.TOP_K)
top_p = st.sidebar.slider("Top-P", 0.1, 1.0, config.TOP_P)

# Display chat history
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.write(turn["assistant"])

# Chat input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Call /chat API
    with st.spinner("Thinking..."):
        response = requests.post(
            f"http://{config.HOST}:{config.PORT}/chat",
            json={
                "message": user_input,
                "history": st.session_state.history,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_k": top_k,
                "top_p": top_p
            }
        )
        data = response.json()
        assistant_response = data["response"]
        st.session_state.history = data["history"]

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(assistant_response)