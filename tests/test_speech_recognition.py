import unittest

from managers import SpeechRecognitionManager


class TestSpeechRecognitionManager(unittest.TestCase):
    SENTENCE = "The brown dog jumped over the red fox"

    def __init__(self):
        self.speech_recognition_manager = SpeechRecognitionManager(whisper_model="base")

    def test_speech_to_text(self):
        print("Testing microphone input")
        print(f"Read this setence: '{self.SENTENCE}'\n")
        text = self.speech_recognition_manager.speech_to_text()

        self.assertEqual(
            text,
            self.SENTENCE,
            f"\nSpeech to text: '{text}'\nActually sentence: '{self.SENTENCE}'",
        )

    def test_microphone_duration_timeout(self):
        print("Testing microphone duration timeout\n")
        text = self.speech_recognition_manager.get_microphone_input(duration=0.01)
        self.assertIsNone(text, f"Output from microphone ({text}) is not None")

    def test_audio_file_to_text(self):
        print("Testing audio file to text\n")
        audio_file = "test/audio/sample.wav"
        text = self.speech_recognition_manager.audio_file_to_text(audio_file)
        self.assertEqual(
            text,
            self.SENTENCE,
            f"\naudio file to text: '{text}'\nActually sentence: '{self.SENTENCE}'",
        )

    def test_audio_to_text(self):
        print("Testing audio to text\n")
        audio_data = ""
        text = self.speech_recognition_manager.audio_to_text(audio_data)
        self.assertEqual(
            text,
            self.SENTENCE,
            f"\naudio to text: '{text}'\nActually sentence: '{self.SENTENCE}'",
        )


if __name__ == "__main__":
    unittest.main()
