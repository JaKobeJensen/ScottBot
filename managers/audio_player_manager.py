import pygame
from pygame.mixer import Sound

pygame.init()


class AudioPlayerManager:
    SAMPLE_RATE = 44100
    BITS_PER_SAMPLE = 16
    CHANNELS = 1

    def __init__(self):
        pygame.mixer.init(self.SAMPLE_RATE, self.BITS_PER_SAMPLE, self.CHANNELS)

    def play_audio(self, audio_data, wait_for_sound: bool = False) -> None:
        self.play_sound(pygame.sndarray.make_sound(audio_data), wait_for_sound)
        return

    def play_audio_file(self, audio_file: str, wait_for_sound: bool = False) -> None:
        self.play_sound(pygame.mixer.Sound(audio_file), wait_for_sound)
        return

    def play_sound(self, sound: Sound, wait_for_sound: bool = False) -> None:
        sound.play()
        if wait_for_sound:
            pygame.time.wait(int(sound.get_length() * 1000))
        return
