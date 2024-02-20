from rich import print
import numpy as np

from managers import (
    AudioPlayerManager,
    ChatGPTManager,
    SpeechRecognitionManager,
    TTSManager,
)


class ScottBot:
    FIRST_SYSTEM_PROMT = "For now on you are a college computer science professor, named ScottBot, and loves to answer students questions. Make sure you follow these rules at all times: 1. make responses only one paragraph long, 2. never generate code, use words instead"
    MODEL_PATH = "managers/tts_model/jacob"

    def __init__(self):
        print("\n[yellow]ScottBot booting up...")

        self.chatgpt_manager = ChatGPTManager(
            model="gpt-3.5-turbo", first_system_prompt=self.FIRST_SYSTEM_PROMT
        )
        self.speech_recognition_manager = SpeechRecognitionManager(whisper_model="base")
        self.tts_manager = TTSManager(model_path=self.MODEL_PATH)
        self.audio_player_manager = AudioPlayerManager()
        self.current_question = None

        print("[green]ScottBot is ready to go!\n")

    def listen(self, duration: int | None = None) -> str | None:
        print("[yellow]I'm currently listening!")

        self.current_question = self.speech_recognition_manager.speech_to_text(duration)

        if self.current_question is None:
            print("[red]Sorry I couldn't hear you.\n")
            return self.current_question

        print("[green]Okay I got what you said!\n")
        print(f"[bright_blue]This is what you said:\n{self.current_question}\n")

        return self.current_question

    def answer_question(self, question: str | None = None) -> dict | None:
        if question is None and self.current_question is not None:
            question = self.current_question
            self.current_question = None
        elif question is None and self.current_question is None:
            exit("[red]Question was not given.\n")

        print(f"[yellow]Forming an answer to your question...")
        response = self.chatgpt_manager.chat_with_history(question)
        print(f"[green]Response:\n{response}\n")

        print("[yellow]Generating audio from response...")
        # audio = self.tts_manager.text_to_speech(response)
        self.tts_manager.text_to_audio_file(response, "temp/audio.wav")
        print("[green]Finished generating audio")

        # return {"text": response, "audio": np.array(audio)}
        return response

    def ask_question(self) -> dict | None:
        response = self.answer_question(self.listen())
        # self.speak_from_audio_data(response["audio"])
        self.speak_from_audio_file("temp/audio.wav")
        return response

    def speak_from_audio_data(self, audio: list[int]) -> None:
        print("[yellow]Speaking...")
        self.audio_player_manager.play_audio(audio)
        print("[green]Finish Speaking\n")
        return
    
    def speak_from_audio_file(self, audio_file_path: str) -> None:
        print("[yellow]Speaking...")
        self.audio_player_manager.play_audio_file(audio_file_path, wait_for_sound=True)
        print("[green]Finish Speaking\n")
        return
