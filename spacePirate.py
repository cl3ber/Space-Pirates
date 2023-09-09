import math
import random
from typing import Any
import pygame
from pygame.sprite import AbstractGroup

pygame.init()

class Tiros(pygame.sprite.Sprite):
    def __init__(self, x, y, sobe):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/tiro.png"), (20,20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.sobe = sobe

    def update(self):
        self.rect.y = self.rect.y - 5 if self.sobe else self.rect.y + 5
        #Se o tiro sair da tela, remover ele do grupo de tiros e do jogo
        if (self.sobe and self.rect.bottom < 0) or (not self.sobe and self.rect.top > ALTURA_TELA):
            self.kill()

        if self.sobe and pygame.sprite.spritecollide(self, piratas_group, True):
            navinha.combustivel_restante += 10
            self.kill()
            explosao = Explosao(self.rect.centerx, self.rect.centery)
            explosao_group.add(explosao)

        if not self.sobe and pygame.sprite.spritecollide(self, naves_group, False, pygame.sprite.collide_mask):
            navinha.combustivel_restante -= 10
            self.kill()

class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprites = SpriteSheet(pygame.image.load("./assets/boom2.png").convert_alpha())
        
        self.images = []
        for num in range(0, 6):
            tam = 145 if num in (2,3) else 155 if num in (6,4) else 160 if num == 5 else 135 if num == 1 else 130
            img = sprites.carregarimagem(num, tam, 155, 2, (0, 0, 0))
            self.images.append(img)
        
        print(self.images)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        velocidade_explosao = 6
        self.counter += 1
        if self.counter >= velocidade_explosao and self.index < len(self.images)-1:
            print(self.index)
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) -1 and self.counter >= velocidade_explosao:
            self.kill()

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def carregarimagem(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width, height))
        image.set_colorkey(color)

        return image

class Piratas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/pirata.png"), (120,120))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.movimento = 0
        self.direcao = 1
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.direcao
        self.movimento += 1
        recarga = 1000
        if abs(self.movimento) > 75:
            self.direcao *= -1
            self.movimento *= self.direcao
        
        if pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.bottom, False)
            tiros_group.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()

class Navinha(pygame.sprite.Sprite):
    def __init__(self, x, y, combustivel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/boat.png"), (120,120))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.combustivel_base = combustivel
        self.combustivel_restante = combustivel
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        velocidade = 4

        #tempo em ms para "recarga dos canhões"
        recarga = 500

        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if tecla[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA:
            self.rect.x += velocidade
        if tecla[pygame.K_DOWN] and self.rect.bottom > 0:
            self.rect.y += velocidade
        if tecla[pygame.K_UP] and self.rect.top < altura_fundo:
            self.rect.y -= velocidade


        if tecla[pygame.K_SPACE] and pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.top, True)
            tiros_group.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()

        self.mask = pygame.mask.from_surface(self.image)
        pygame.draw.rect(tela, (255,0,0), (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.combustivel_restante > 0:
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.combustivel_restante / self.combustivel_base)), 15))


clock = pygame.time.Clock()
LARGURA_TELA = 600
ALTURA_TELA = 1000

#criando a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

fundo = pygame.image.load("./assets/space.jpg").convert()
altura_fundo = fundo.get_height()
limite_fundo = fundo.get_rect()

#Variáveis do jogo
tiles = math.ceil(ALTURA_TELA / altura_fundo) + 1
scroll_tela = 0


#Criando um grupo de sprites pra facilitar a inclusão deles na tela
naves_group = pygame.sprite.Group()
tiros_group = pygame.sprite.Group()
piratas_group = pygame.sprite.Group()
explosao_group = pygame.sprite.Group()

#navinha
navinha = Navinha(int(LARGURA_TELA/2), altura_fundo-100, 100)

naves_group.add(navinha)

rodando = True

delay_piratas = 2500
respawn = pygame.time.get_ticks()

def paralax(scroll):
    #desenhando o fundo
    for i in range(0, tiles):
        tela.blit(fundo, (0, i * altura_fundo + scroll))

def criar_piratas(altura, largura):
        piratas_group.add(Piratas(altura, 100 + largura * 70))

while rodando:
    clock.tick(120)

    paralax(scroll_tela)

    scroll_tela = 0 if abs(scroll_tela) > altura_fundo else scroll_tela-1

    if pygame.time.get_ticks() - respawn > delay_piratas and len(piratas_group.sprites()) < 5:
        criar_piratas(random.randint(1, LARGURA_TELA), random.randint(1, 6))
        respawn = pygame.time.get_ticks()

    #Esse for captura todos os eventos que o pygame está executando, inclusive inputs
    for event in pygame.event.get():
        rodando = event.type != pygame.QUIT

    naves_group.update()
    tiros_group.update()
    piratas_group.update()
    explosao_group.update()

    naves_group.draw(tela)
    tiros_group.draw(tela)
    piratas_group.draw(tela)
    explosao_group.draw(tela)
    pygame.display.update()

pygame.quit()