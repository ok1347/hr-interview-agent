#this module is used to synthesize speech using MeloTTS.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "MeloTTS")))
from melo.api import TTS 
import tempfile
import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.data.path.append("/home/yaya/nltk_data")





# Load MeloTTS once (English voice)
tts_model = TTS(language='EN')  # we can use 'FR' for French or 'ES' for Spanish, etc.

def synthesize_speech(text: str, speaker: int = 0, output_path: str = None) -> str:
    """
    Synthesizes speech using MeloTTS and returns the path to the audio file.
    """
    if output_path is None:
        output_path = tempfile.mktemp(suffix=".wav")
    
    tts_model.tts_to_file(text, speaker_id=speaker, output_path=output_path)
    return output_path
