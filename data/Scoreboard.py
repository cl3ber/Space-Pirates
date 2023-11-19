import pygame
from data.Sprites import SpriteSheet

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprites = SpriteSheet(pygame.image.load("./assets/screen/TreasureChest.png").convert_alpha())

        self.images = []
        for num in range(0, 3):
            img = sprites.carregarimagem(num, 64, 64, 2, (0, 0, 0))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        velocidade_explosao = 6
        self.counter += 1
        if self.index < len(self.images)-1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        # if self.index >= len(self.images) -1 and self.counter >= velocidade_explosao:
        #     self.kill()