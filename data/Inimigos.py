import pygame
from random import randint
from data.Tiros import Tiros

class Inimigos(pygame.sprite.Sprite):
    def __init__(self, x, y, limiteAltura, limiteLargura, tirosGroup, caminhoimagem, tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.carregarImagem(x, y, caminhoimagem, tamanho)
        self.movimento = 0
        self.direcao = 1
        self.ultimo_tiro = pygame.time.get_ticks()
        self.limiteAltura = limiteAltura-tamanho
        self.limiteLargura = limiteLargura-tamanho
        self.tirosGroup = tirosGroup
        self.targetX = randint(0, self.limiteAltura)
        self.targetY = randint(0, self.limiteLargura)

    def carregarImagem(self, x, y, caminhoimagem, tamanho):
        self.image = pygame.transform.scale(pygame.image.load(caminhoimagem), (tamanho,tamanho))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def caminho(self):
        self.targetX = randint(0, self.limiteAltura) if self.targetX == self.rect.x else self.targetX
        self.targetY = randint(0, self.limiteLargura) if self.targetY == self.rect.y else self.targetY
        self.rect.x += 2 if self.rect.x <= self.targetX else -1
        self.rect.y += 2 if self.rect.y <= self.targetY else -1
        

    def update(self):
        self.caminho()
        recarga = 500
        if pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.bottom, False, self.limiteLargura+self.rect.centerx, self.limiteAltura+self.rect.centery)
            self.tirosGroup.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()

        for tiro in self.tirosGroup:
            if (0 > tiro.rect.x or tiro.rect.x >= self.limiteLargura) or (0 > tiro.rect.y or tiro.rect.y >= self.limiteAltura):
                self.tirosGroup.remove(tiro)
