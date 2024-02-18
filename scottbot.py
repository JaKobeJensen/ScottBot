from rich import print

from managers import (
    AudioPlayerManager,
    ChatGPTManager,
    SpeechRecognitionManager,
    TTSManager,
)


class ScottBot:
    FIRST_SYSTEM_PROMT = "For now on you are a college computer science professor, named ScottBot, and loves to answer students questions. Make sure you follow these rules at all times: 1. make responses only one paragraph long, 2. never generate code, use words instead"

    def __init__(self):
        print("[yellow]ScottBot booting up...")

        self.chatgpt_manager = ChatGPTManager(
            model="gpt-3.5-turbo", first_system_prompt=self.FIRST_SYSTEM_PROMT
        )
        self.speech_recognition_manager = SpeechRecognitionManager(whisper_model="base")
        self.tts_manager = TTSManager(model_path="managers/tts_model")
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

        print(f"[yellow]Forming an answer to your question...\n")
        response = self.chatgpt_manager.chat_with_history(question)
        print(f"[green]{response}\n")

        audio = self.tts_manager.text_to_speech(response)

        return {"text": response, "audio": audio}

    def ask_question(self) -> dict | None:
        response = self.answer_question(self.listen())
        self.speak(response["audio"])
        return response

    def speak(self, audio: list[int]) -> None:
        self.audio_player_manager.play_audio(audio)
        return
