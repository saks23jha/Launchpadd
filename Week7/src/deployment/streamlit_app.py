import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------------
# 1️⃣ Load environment variables FIRST (CRITICAL)
# -------------------------------------------------
load_dotenv()

# Safety check (fail fast if key missing)
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

# -------------------------------------------------
# 2️⃣ Add project root to Python path
#    (Week7/src)
# -------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

# -------------------------------------------------
# 3️⃣ Import app logic AFTER env + path setup
# -------------------------------------------------
from src.deployment.ask import ask_text
from src.deployment.ask_sql import ask_sql
from src.deployment.ask_image import ask_image

# -------------------------------------------------
# 4️⃣ Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="RAG Capstone – Day 5")

st.title(" Multimodal RAG Capstone")

mode = st.selectbox("Choose mode", ["Text", "SQL", "Image"])
query = st.text_input("Enter your query")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        if mode == "Text":
            result = ask_text(query)
            st.json(result)

        elif mode == "SQL":
            result = ask_sql(query)
            st.json(result)

        elif mode == "Image":
            result = ask_image(query)
            st.json(result)
