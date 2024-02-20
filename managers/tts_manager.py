import torch
from TTS.api import TTS


class TTSManager:
    def __init__(self, model_path: str | None = None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if model_path is not None:
            self.model_path = model_path
            self.tts = TTS(
                model_path=model_path,
                config_path=f"{model_path}/config.json",
                progress_bar=False,
            ).to(device)
        else:
            self.model_path = None
            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False,
            ).to(device)

    def text_to_speech(self, text: str) -> list[int]:
        if self.model_path is not None:
            return self.tts.tts(
                text=text, language="en", speaker_wav=f"{self.model_path}/sample.wav"
            )
        else:
            return self.tts.tts(text=text, language="en", speaker="Aaron Dreschner")

    def text_to_audio_file(
        self, text: str, output_file_name: str | None = None
    ) -> None:
        output_file_name = (
            "output.wav" if output_file_name is None else output_file_name
        )
        if self.model_path is not None:
            self.tts.tts_to_file(
                text=text,
                language="en",
                file_path=output_file_name,
                speaker_wav=f"{self.model_path}/sample.wav",
            )
        else:
            self.tts.tts_to_file(
                text=text,
                language="en",
                file_path=output_file_name,
                speaker="Aaron Dreschner",
            )
        return
