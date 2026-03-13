import streamlit as st
import requests
import config

# Page configuration
st.set_page_config(page_title="Medical Assistant", page_icon="🏥")

# Hide Streamlit menu/footer for cleaner UI
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🏥 Medical Assistant Chatbot")
st.caption("Powered by TinyLlama ChatDoctor — Week 8 Capstone")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn["assistant"])

# Chat input
user_input = st.chat_input("Ask a medical question...")

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Call FastAPI /chat endpoint
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"http://{config.HOST}:{config.PORT}/chat",
                json={
                    "message": user_input,
                    "history": st.session_state.history,
                    "temperature": config.TEMPERATURE,
                    "max_tokens": config.MAX_TOKENS,
                    "top_k": config.TOP_K,
                    "top_p": config.TOP_P
                }
            )

            data = response.json()
            assistant_response = data["response"]
            st.session_state.history = data["history"]

        except Exception as e:
            assistant_response = f"Error contacting API: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)