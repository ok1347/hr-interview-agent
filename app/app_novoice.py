#this app was for just text input with no voice interaction. no whisper or audio recording.
import streamlit as st
import os
from utils import extract_text_from_pdf
from agent import agent_rh_respond
from voice import synthesize_speech

# === 1. Define paths ===
cv_dir = "/home/yaya/rhagent/data/cvs"
offer_dir = "/home/yaya/rhagent/data/jobs"
os.makedirs(cv_dir, exist_ok=True)
os.makedirs(offer_dir, exist_ok=True)

# === 2. Session State Initialization ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === 3. Sidebar File Upload ===
with st.sidebar:
    st.title("📄 Upload Candidate & Offer")

    cv_file = st.file_uploader("Upload candidate CV", type="pdf")
    offer_file = st.file_uploader("Upload job offer", type="pdf")

    if cv_file and offer_file:
        cv_path = os.path.join(cv_dir, cv_file.name)
        offer_path = os.path.join(offer_dir, offer_file.name)

        with open(cv_path, "wb") as f:
            f.write(cv_file.read())

        with open(offer_path, "wb") as f:
            f.write(offer_file.read())

        st.session_state.cv_text = extract_text_from_pdf(cv_path)
        st.session_state.offer_text = extract_text_from_pdf(offer_path)

        st.success("✅ Files uploaded and content loaded successfully.")

# === 4. Main Chat Interface ===
st.title("🧠 HR Interview Agent")

if "cv_text" in st.session_state and "offer_text" in st.session_state:
    user_input = st.chat_input("Ask or answer something...")
    if user_input:
        st.session_state.chat_history.append(f"Candidate: {user_input}")

        with st.spinner("🤖 Thinking..."):
            response = agent_rh_respond(
                cv_text=st.session_state.cv_text,
                offer_text=st.session_state.offer_text,
                chat_history=st.session_state.chat_history,
                user_input=user_input
            )
            audio_path = synthesize_speech(response)

        st.session_state.chat_history.append(response)

# === 5. Display Chat History ===
for msg in st.session_state.chat_history:
    if msg.startswith("Candidate:"):
        st.chat_message("user").write(msg.replace("Candidate: ", ""))
    else:
        st.chat_message("assistant").write(msg)
        audio_path = synthesize_speech(msg)
        st.audio(audio_path, format="audio/wav")
