import pygame
from data.Sprites import SpriteSheet
from data.Inimigos import Inimigos
from random import randint
from data.Tiros import Tiros

class Capitao(Inimigos):
    def __init__(self, x, y, limiteAltura, limiteLargura, tirosGroup, tela):
        super().__init__(x, y, limiteAltura, limiteLargura, tirosGroup, "./assets/barco_boss.png", 480)
        self.combustivel_maximo = self.combustivel_base = 100
        self.combustivel_restante = 100
        self.tela = tela

    def healtBar(self, tela):
        pygame.draw.rect(tela, (255,0,0), (self.rect.x, (self.rect.bottom-100), self.rect.width, 15))
        if self.combustivel_restante > 0:
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, (self.rect.bottom-100), int(self.rect.width * (self.combustivel_restante / self.combustivel_base)), 15))

    def update(self):
        #tempo em ms para "recarga dos canhões"
        recarga = 500
        self.healtBar(self.tela)

        #pra nao deixar o combustivel ultrapassar o maximo
        if self.combustivel_restante > self.combustivel_maximo:
            self.combustivel_restante = self.combustivel_maximo  

        self.caminho()
        recarga = 500
        if pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.bottom, False, self.limiteLargura+self.rect.centerx, self.limiteAltura+self.rect.centery)
            self.tirosGroup.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()