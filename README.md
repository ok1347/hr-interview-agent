# HR Interview Agent with Voice 

This project is an intelligent HR agent that conducts job interviews with candidates, combining GPT-4o, Whisper (speech-to-text), and MeloTTS (text-to-speech) in a Streamlit interface.
Whisper may sometimes not pick up the best words from the audio, so it is better to talk clear into the mic, and also in english if possible XD.
We used MeloTTS fo text-to-speech because it is light and gives a bit more natural voice to the HR agent. You can read about the model in this hugging face page : https://huggingface.co/myshell-ai/MeloTTS-English
We also decided to use Whisper with api key, because Whisper local didn't give us the best results, but if you have a good gpu you can always download the model. But since we are already using gpt-4o as our LLM, we figured it is better to use Whisper model for ASR (Automatic Speech Recognition) as an api
We also provided an alternative for whisper, you can write down what you want to say to our HR agent and continue with the process.

## Project Lifecycle :

Here is the architecture of our project : 

Upload CV + Job Offer  
     │  
     ▼  
Start Interview Session  
     │  
     ▼  
Candidate Asks a Question (voice input or text) 
     │  
     ├──► Whisper (if voice input)  
     │           │  
     │           ▼  
     └──────► Transcribed Text  
                 │  
                 ▼  
GPT-4o (Uses CV + Offer as context)  
     │  
     ▼  
MeloTTS (Text-to-Speech synthesis)  
     │  
     ▼  
Audio Answer Played to Candidate


## Features

- Upload and process candidate CV and job offer PDFs
- HR agent powered by GPT-4o and LangChain
- Candidate can **type or speak**
- Uses **Whisper API** to transcribe speech
- Agent responds in English, with voice using **MeloTTS** (It's the only one we could integrate with our small gpus :C)
- Fully local + OpenAI integration

---

## Project Structure

```
rhagent/
├── MeloTTS/             ← Local TTS model (https://github.com/myshell-ai/MeloTTS)
├── data/
│   ├── cvs/             ← Uploaded candidate CVs
│   └── jobs/            ← Uploaded job offers
├── app/
│   ├── app.py           ← Main Streamlit interface
│   ├── agent.py         ← Prompt + LangChain logic
│   ├── utils.py         ← PDF extraction (PyMuPDF + OCR fallback (if the pdf is extracted from an image))
│   ├── voice.py         ← Text-to-speech using MeloTTS
│   └── .env             ← Your OpenAI API key (sorry couldn't include mine -no credits left- haha)
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## How to Run:

### 1. Install dependencies

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Set your OpenAI key

Create a `.env` file inside `app/`:

```env
OPENAI_API_KEY=sk-xxx... #your_openai_key
```

### 3. Run the app


```bash
source hr_env/bin/activate
streamlit run test_app_novoice/app.py
```


We provided you with a cv and an offer to test in the file cv_offer_to_test_with

## Notes

- Whisper transcription supports French, Arabic, English, etc.
- Agent always responds in **English** because MeloTTS for now we tested it on only english
- Voice output = MeloTTS (CPU-friendly, fast)
- Code handles real-time chat with memory
- Audio files are generated temporarily (`.wav`)
- We used WSL for this project (since we know you like working with Linux)

---

## Authors

- **Name:** Yahya KROMBI,  Ghaya_El_Mouna BEDOUI, Wijdane EL MOUHTADI, Adil OUSSIDI
- **Project:** MSBDE AI Project — Multimodal HR Agent  
- **Professor:** PRILLARD Martin

---

## Enjoy the demo!
