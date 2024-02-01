from managers import ChatGPTManager, SpeechRecognitionManager, TTSManager


class ScottBotOnline:
    FIRST_SYSTEM_PROMT = ""

    def __init__(self):
        self.chatgpt_manager = ChatGPTManager(
            model="gpt-3.5-turbo", first_system_prompt=self.FIRST_SYSTEM_PROMT
        )
        self.speech_recognition_manager = SpeechRecognitionManager(whisper_model="base")
        self.tts_manager = TTSManager(model_path="./managers/tts_model")
