import unittest

from managers import AudioPlayerManager, TTSManager


class TestTTSManager(unittest.TestCase):
    AUDIO_FILE_CUSTOM = "audio/test_custom.wav"
    AUDIO_FILE_DEFAULT = "audio/test_defualt.wav"
    TEXT = "The quick brown fox jumps over the lazy dog."
    MODEL_PATH = "managers/jacob/tts_model"

    def __init__(self):
        self.custom_tts_manager = TTSManager(model_path=self.MODEL_PATH)
        self.defualt_tts_manager = TTSManager()
        self.audio_player = AudioPlayerManager()

    def test_text_to_speech_custom(self):
        print("Testing text to speech with custom model")
        audio = self.custom_tts_manager.text_to_speech(self.TEXT)
        self.assertEqual(type(audio), list)
        self.assertEqual(type(audio[0], int))
        self.audio_player.play_audio(audio, wait_for_sound=True)

    def test_text_to_audio_file_custom(self):
        print("Testing text to audio file with custom model")
        self.assertIsNone(
            self.custom_tts_manager.text_to_audio_file(
                self.TEXT, self.AUDIO_FILE_CUSTOM
            )
        )
        self.audio_player.play_audio_file(self.AUDIO_FILE_CUSTOM, wait_for_sound=True)

    def test_text_to_speech_default(self):
        print("Testing text to speech with default model")
        audio = self.custom_tts_manager.text_to_speech(self.TEXT)
        self.assertEqual(type(audio), list)
        self.assertEqual(type(audio[0], int))
        self.audio_player.play_audio(audio, wait_for_sound=True)

    def test_text_to_audio_file_default(self):
        print("Testing text to audio file with default model")
        self.assertIsNone(
            self.custom_tts_manager.text_to_audio_file(
                self.TEXT, self.AUDIO_FILE_DEFAULT
            )
        )
        self.audio_player.play_audio_file(self.AUDIO_FILE_DEFAULT, wait_for_sound=True)


if __name__ == "__main__":
    unittest.main
