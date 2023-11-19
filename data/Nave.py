import pygame 
import pygame.sprite
import os
from data.Tiros import Tiros

class Navinha(pygame.sprite.Sprite):
    def __init__(self, x, y, combustivel, tiros_group, limitex, limitey):
        pygame.sprite.Sprite.__init__(self)
        self.combustivel_maximo = self.combustivel_base = combustivel
        self.frame = 0
        self.combustivel_restante = 0
        self.animacao = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.limitex = limitex
        self.limitey = limitey
        self.tiros_group = tiros_group #Validar se precisa desse cara passando aqui        

        self.carregarImagens(x, y)
    
    def carregarImagens(self, x, y):
        frames = len(os.listdir(f'./assets/player'))
        templist = []
        for frame in range(frames):
            self.animacao.append(pygame.transform.scale(pygame.image.load(f"./assets/player/barco_principal_{frame+1}.png"), (120,120)))

        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        velocidade = 3
        frameskip = 160
        #tempo em ms para "recarga dos canhões"
        recarga = 500
        
        tecla = pygame.key.get_pressed()
        if (tecla[pygame.K_LEFT] or tecla[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= velocidade
        if (tecla[pygame.K_RIGHT] or tecla[pygame.K_d])and self.rect.right < self.limitey - 30:
            self.rect.x += velocidade
        if (tecla[pygame.K_DOWN] or tecla[pygame.K_s]) and self.rect.bottom <= self.limitex:
            self.rect.y += velocidade
        if (tecla[pygame.K_UP] or tecla[pygame.K_w])and self.rect.top >= 0:
            self.rect.y -= velocidade

        #pra nao deixar o combustivel ultrapassar o maximo
        if self.combustivel_restante > self.combustivel_maximo:
            self.combustivel_restante = self.combustivel_maximo  

        if pygame.time.get_ticks() - self.last_update > frameskip:
            self.last_update = pygame.time.get_ticks()
            self.frame += 1 if self.frame < len(self.animacao)-1 else self.frame*-1

        self.image = self.animacao[self.frame]