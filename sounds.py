import pygame
import os
from config import *

class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'eat': pygame.mixer.Sound(os.path.join('sounds', 'eat.wav')) if os.path.exists(os.path.join('sounds', 'eat.wav')) else None,
            'death': pygame.mixer.Sound(os.path.join('sounds', 'death.wav')) if os.path.exists(os.path.join('sounds', 'death.wav')) else None
        }
        self.volume = 0.5
        self.set_volume(self.volume)

    def set_volume(self, volume):
        self.volume = volume
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)

    def play(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()