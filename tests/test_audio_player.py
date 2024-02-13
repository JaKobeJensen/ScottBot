import unittest

import numpy as np
from pygame.mixer import Sound

from managers import AudioPlayerManager


class TestAudioPlayerManager(unittest.TestCase):
    def __init__(self):
        self.audio_player_manager = AudioPlayerManager()

    def test_play_sound(self):
        print("Testing play sound")
        sample_rate = 44100
        duration = 2
        frequency = 440
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
        sound = Sound(buffer=waveform.astype(np.int16))
        self.assertIsNone(
            self.audio_player_manager.play_sound(sound, wait_for_sound=True)
        )

    def test_play_audio(self):
        print("Testing play audio")
        audio_data = None
        self.assertIsNone(
            self.audio_player_manager.play_audio(audio_data, wait_for_sound=True)
        )

    def test_play_audio_file(self):
        print("Testing play audio file")
        audio_file = "tests/audio/sample.wav"
        self.assertIsNone(
            self.audio_player_manager.play_audio_file(audio_file, wait_for_sound=True)
        )


if __name__ == "__main__":
    unittest.main
