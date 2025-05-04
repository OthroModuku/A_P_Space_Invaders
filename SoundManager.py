import pygame

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.laser = pygame.mixer.Sound("Audio/Shoot.mp3")
        self.laser.set_volume(0.1)
        self.explosion = pygame.mixer.Sound("Audio/Hit.mp3")
        self.explosion.set_volume(0.4)

    def laser_sound(self):
        self.laser.play()

    def explosion_sound(self):
        self.explosion.play()
