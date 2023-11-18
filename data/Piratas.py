import pygame
from random import randint
from data.Tiros import Tiros

class Piratas(pygame.sprite.Sprite):
    def __init__(self, x, y, limiteAltura, limiteLargura, tirosGroup):
        pygame.sprite.Sprite.__init__(self)
        IMG_SIZE = self.carregarImagem(x, y)
        self.movimento = 0
        self.direcao = 1
        self.ultimo_tiro = pygame.time.get_ticks()
        self.limiteAltura = limiteAltura-IMG_SIZE
        self.limiteLargura = limiteLargura-IMG_SIZE
        self.tirosGroup = tirosGroup
        self.targetX = randint(0, self.limiteAltura)
        self.targetY = randint(0, self.limiteLargura)

    def carregarImagem(self, x, y):
        IMG_SIZE = 120

        self.image = pygame.transform.scale(pygame.image.load("./assets/barco_boss_mercenario.png"), (120,120)) if randint(0, 2) == randint(0,2) else pygame.transform.scale(pygame.image.load("./assets/boss_barco_marinha.png"), (IMG_SIZE,IMG_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        return IMG_SIZE

    def caminho(self):
        self.targetX = randint(0, self.limiteAltura) if self.targetX == self.rect.x else self.targetX
        self.targetY = randint(0, self.limiteLargura) if self.targetY == self.rect.y else self.targetY
        self.rect.x += 2 if self.rect.x <= self.targetX else -1
        self.rect.y += 2 if self.rect.y <= self.targetY else -1
        

    def update(self):
        self.caminho()
        recarga = 500
        if pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.bottom, False, self.limiteAltura, self.limiteLargura)
            self.tirosGroup.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()
