from speech_recognition import Recognizer, Microphone, AudioFile, UnknownValueError


class SpeechRecognitionManager:
    
    def __init__(self, whisper_model: str = "small"):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.model = whisper_model
    
    def get_microphone_input(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.listen(source)
            return audio_data
        except UnknownValueError:
            print("Unable to recognize microphone audio")
            return None
        
    def audio_to_text(self, audio_data = None, audio_file: str | None = None) -> str:
        if audio_file is not None:
            with AudioFile(audio_file) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
        elif audio_data is None:
            exit("audio_data and audio_file are not set")
        return self.recognizer.recognize_whisper(audio_data, model=self.model)
            
    def speech_to_text(self) -> str | None:
        audio_data = self.get_microphone_input()
        if audio_data is None:
            return None
        return self.audio_to_text(audio_data)
    
    
if __name__ == "__main__":
    speech_recognize_manager = SpeechRecognitionManager(whisper_model="small")
    # text = speech_recognize_manager.speech_to_text()
    text = speech_recognize_manager.audio_to_text(audio_file="sample.wav")
    print(text)
    quit()
    