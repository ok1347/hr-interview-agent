#this is the main file for the HR agent app
import streamlit as st
import os
from utils import extract_text_from_pdf
from agent import agent_rh_respond
from voice import synthesize_speech
from audiorecorder import audiorecorder
from dotenv import load_dotenv
import openai
from openai import OpenAI
import nltk

nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)



client = OpenAI()

# === Init API Key ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Paths ===
cv_dir = "/home/yaya/rhagent/data/cvs"
offer_dir = "/home/yaya/rhagent/data/jobs"
os.makedirs(cv_dir, exist_ok=True)
os.makedirs(offer_dir, exist_ok=True)

# === Session state ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Upload PDFs ===
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

        st.success("Files uploaded and content loaded successfully.")

# === Main Chat ===
st.title("🧑‍💼 HR Interview Agent")

if "cv_text" in st.session_state and "offer_text" in st.session_state:

    st.subheader("🎙️ Your Turn: Speak or Type")

    audio = audiorecorder("🎤 Click to record", "⏹️ Stop recording")
    typed_input = st.chat_input("...or type your question/answer")

    user_input = None

    # === Handle audio
    if audio:
    #    st.audio(audio.raw_data, format="audio/wav")

        with st.spinner("Transcribing with Whisper..."):
            audio.export("user_voice.wav", format="wav")

            with open("user_voice.wav", "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

            user_input = transcript  # text only
            st.success(f"You said: {user_input}")

    elif typed_input:
        user_input = typed_input

    # === Run agent
    if user_input:
        st.session_state.chat_history.append(f"Candidate: {user_input}")

        with st.spinner("🤖 Thinking..."):
            # Call the agent with CV, offer, chat history, and user input
            response = agent_rh_respond(
                cv_text=st.session_state.cv_text,
                offer_text=st.session_state.offer_text,
                chat_history=st.session_state.chat_history,
                user_input=user_input
            )
            audio_path = synthesize_speech(response)

        st.session_state.chat_history.append(response)

# === Chat Display ===
for msg in st.session_state.chat_history:
    if msg.startswith("Candidate:"):
        st.chat_message("user").write(msg.replace("Candidate: ", ""))
    else:
        st.chat_message("assistant").write(msg)
        audio_path = synthesize_speech(msg)
        st.audio(audio_path, format="audio/wav")
