import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, x, y):
        super().__init__()
        file_path = 'Pictures/' + alien_type + '.png'
        original_image = pygame.image.load(file_path).convert_alpha()
        scale_size = (60, 60)
        self.image= pygame.transform.scale(original_image, scale_size)
        self.rect = self.image.get_rect(topleft = (x, y))

        if alien_type == 'Enemy_3': self.value = 100
        elif alien_type == 'Enemy_2': self.value = 200
        else: self.value = 300

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        original_image = pygame.image.load('Pictures/Enemy_4.png').convert_alpha()
        scale_size = (38, 38)
        self.image = pygame.transform.scale(original_image, scale_size)
        
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
                x = -50
                self.speed = 3
            
        self.rect = self.image.get_rect(topleft = (x, 80))

    def update(self):
        self.rect.x += self.speed
