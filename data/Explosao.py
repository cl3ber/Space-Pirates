import pygame
from data.Sprites import SpriteSheet

class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprites = SpriteSheet(pygame.image.load("./assets/boom2.png").convert_alpha())
        
        self.images = []
        for num in range(0, 6):
            tam = 145 if num in (2,3) else 155 if num in (6,4) else 160 if num == 5 else 135 if num == 1 else 130
            img = sprites.carregarimagem(num, tam, 155, 2, (0, 0, 0))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        velocidade_explosao = 6
        self.counter += 1
        if self.counter >= velocidade_explosao and self.index < len(self.images)-1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) -1 and self.counter >= velocidade_explosao:
            self.kill()
