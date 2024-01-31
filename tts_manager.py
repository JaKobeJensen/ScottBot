from TTS.api import TTS
from scipy.io import wavfile
import torch


class TTSManager():
    
    def __init__(self, model_path: str | None = None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if model_path is not None:
            self.tts = TTS(model_path=model_path, config_path=f"{model_path}/config.json").to(device)
        else:
            self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        
    def text_to_speech(self, text: str):
        return self.tts.tts(text=text, language="en")
    
    def text_to_audio_file(self, text: str, output_file_name: str | None = None) -> None:
        output_file_name = "output.wav" if output_file_name is None else output_file_name
        self.tts.tts_to_file(text=text, language="en", file_path=output_file_name)
        return
    
    
if __name__ == "__main__":
    tts_manager = TTSManager()
    
    quit()

