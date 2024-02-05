import torch
from TTS.api import TTS


class TTSManager:
    def __init__(self, model_path: str | None = None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if model_path is not None:
            self.tts = TTS(
                model_path=model_path,
                config_path=f"{model_path}/config.json",
                progress_bar=False,
            ).to(device)
            self.custom_model = True
        else:
            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False,
            ).to(device)
            self.custom_model = False

    def text_to_speech(self, text: str) -> list[int]:
        if self.custom_model:
            return self.tts.tts(
                text=text, language="en", speaker_wav="managers/audio/sample.wav"
            )
        else:
            return self.tts.tts(text=text, language="en", speaker="Aaron Dreschner")

    def text_to_audio_file(
        self, text: str, output_file_name: str | None = None
    ) -> None:
        output_file_name = (
            "output.wav" if output_file_name is None else output_file_name
        )
        if self.custom_model:
            self.tts.tts_to_file(
                text=text,
                language="en",
                file_path=output_file_name,
                speaker_wav="managers/audio/sample.wav",
            )
        else:
            self.tts.tts_to_file(
                text=text,
                language="en",
                file_path=output_file_name,
                speaker="Aaron Dreschner",
            )
        return


if __name__ == "__main__":
    tts_manager = TTSManager(model_path="managers/tts_model")
    # tts_manager = TTSManager()
    text = "Hello my name is Jacob Jensen. This is a test for the text to speech to see how good it is."
    tts_manager.text_to_audio_file(
        text=text, output_file_name="managers/audio/jacob_output.wav"
    )
    audio = tts_manager.text_to_speech(text=text)
    print(type(audio))
    quit()
