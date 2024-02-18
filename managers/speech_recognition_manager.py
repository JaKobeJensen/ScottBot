from rich import print
from speech_recognition import (
    AudioFile,
    Microphone,
    Recognizer,
    UnknownValueError,
    WaitTimeoutError,
)


class SpeechRecognitionManager:
    def __init__(self, whisper_model: str = "base"):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.model = whisper_model

    def get_microphone_input(self, duration: float | int | None = None) -> list[int]:
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.listen(source=source, timeout=duration)
            return audio_data
        except UnknownValueError:
            print("[bright_red]Unable to recognize microphone audio\n")
            return None
        except WaitTimeoutError:
            print("[bright_red]Timeout\n")
            return None

    def audio_to_text(self, audio_data: list[int]) -> str:
        return self.recognizer.recognize_whisper(audio_data, model=self.model)

    def audio_file_to_text(self, audio_file: str) -> str:
        with AudioFile(audio_file) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = self.recognizer.record(source)
        return self.audio_to_text(audio_data)

    def speech_to_text(self, duration: float | int | None = None) -> str | None:
        audio_data = self.get_microphone_input(duration)
        if audio_data is None:
            return None
        return self.audio_to_text(audio_data)
