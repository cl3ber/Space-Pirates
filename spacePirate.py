import math
import random
from random import randint
from typing import Any
import pygame
from pygame.sprite import Group, AbstractGroup

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
        self.targetX = randint(0, LARGURA_TELA-120)
        self.targetY = randint(0, ALTURA_TELA-120)

    def update(self):
        self.targetX = randint(0, LARGURA_TELA-120) if self.targetX == self.rect.x else self.targetX
        self.targetY = randint(0, ALTURA_TELA-120) if self.targetY == self.rect.y else self.targetY

        self.rect.x += 1 if self.rect.x <= self.targetX else -1
        self.rect.y += 1 if self.rect.y <= self.targetY else -1
        
        recarga = 5000
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
        self.combustivel_restante = 0
        self.combustivel_maximo = 100
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        velocidade = 3

        #tempo em ms para "recarga dos canhões"
        recarga = 500
        
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if tecla[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA-30:
            self.rect.x += velocidade
        if tecla[pygame.K_DOWN] and self.rect.bottom <= ALTURA_TELA:
            self.rect.y += velocidade
        if tecla[pygame.K_UP] and self.rect.top >=0:
            self.rect.y -= velocidade


        if tecla[pygame.K_SPACE] and pygame.time.get_ticks() - self.ultimo_tiro > recarga:
            tiro = Tiros(self.rect.centerx, self.rect.top, True)
            tiros_group.add(tiro)
            self.ultimo_tiro = pygame.time.get_ticks()

        self.mask = pygame.mask.from_surface(self.image)
        pygame.draw.rect(tela, (255,0,0), (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.combustivel_restante > 0:
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.combustivel_restante / self.combustivel_base)), 15))
        #pra nao deixar o combustivel ultrapassar o maximo
        if self.combustivel_restante > self.combustivel_maximo:
            self.combustivel_restante = self.combustivel_maximo  

def paralax(scroll):
    #desenhando o fundo
    for i in range(0, tiles):
        tela.blit(fundo, (0, i * altura_fundo + scroll))

def criar_piratas(altura, largura):
        piratas_group.add(Piratas(altura, 100 + largura * 70))

def reset():
    navinha.combustivel_restante = 0
    piratas_group.empty()
    navinha.rect.center = [int(LARGURA_TELA/2), ALTURA_TELA-100]
    tiros_group.empty()
    explosao_group.empty()

class GameState():
    def __init__(self):
        self.state = 'main_menu'
        self.fase = 2
        self.selected_index = 0

    def main_menu(self):
        title = pygame.image.load("./assets/title.png").convert()
        info = pygame.image.load("./assets/menu_info.png").convert()
        tela.blit(title, (LARGURA_TELA/2-272, 250))
        tela.blit(info, (LARGURA_TELA/2-58, 500))
        pygame.display.update()
        if(pygame.key.get_pressed()[pygame.K_SPACE]):
            self.state = 'jogo'
    
    def jogo(self):
        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        pygame.display.update()

        #condições de vitória/derrota
        if navinha.combustivel_restante < 0:
            self.state = 'game_over'
        if pygame.key.get_pressed()[pygame.K_LSHIFT] and navinha.combustivel_restante == navinha.combustivel_maximo:
            self.state = 'win'

    def game_over(self):
        #Criando uma variavel que ira verificar se o usuario continuara jogando ou voltara pro menu
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.selected_index = 0
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.selected_index = 1
        
        #Desenhando imagem de game over + retry
        game_over = pygame.image.load("./assets/game_over.png").convert()
        retry = pygame.image.load("./assets/retry.png").convert()
        yes = pygame.image.load("./assets/yes.png").convert()
        no = pygame.image.load("./assets/no.png").convert()
        pick = pygame.image.load("./assets/pick.png").convert()
        tela.blit(game_over, (LARGURA_TELA/2-199, ALTURA_TELA/2-33))
        tela.blit(retry, (LARGURA_TELA/2-66, 600))
        tela.blit(yes, (150, 650))
        tela.blit(no, (350, 650))

        if self.selected_index == 0:
            tela.blit(pick, (120, 650))
        elif self.selected_index == 1:
            tela.blit(pick, (320, 650))

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if self.selected_index == 0:
                reset()
                self.state = 'jogo'
            else:
                reset()
                self.state = 'main_menu'

        pygame.display.update()

    def win(self):
        reset()
        self.state = 'main_menu'
        pygame.display.update()

    def state_manager(self):
        if self.state == 'main_menu':
            self.main_menu()
        if self.state == 'jogo':
            self.jogo()
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'win':
            self.win()
    


clock = pygame.time.Clock()
LARGURA_TELA = 1280
ALTURA_TELA = 800
game_state = GameState()

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
navinha = Navinha(60, ALTURA_TELA/2, 100)

naves_group.add(navinha)

rodando = True

delay_piratas = 2000
respawn = pygame.time.get_ticks()

while rodando:
    paralax(scroll_tela)

    scroll_tela = 0 if abs(scroll_tela) > altura_fundo else scroll_tela-1

    #Mudei essa parte do codigo pros piratas so spawnarem quando o jogo estiver rodando
    if pygame.time.get_ticks() - respawn > delay_piratas and len(piratas_group.sprites()) < 5 and game_state.state == 'jogo':
            criar_piratas(random.randint(60, LARGURA_TELA-60), random.randint(1, 6))
            respawn = pygame.time.get_ticks()

    #Esse for captura todos os eventos que o pygame está executando, inclusive inputs
    for event in pygame.event.get():
        rodando = event.type != pygame.QUIT

    #Toda a parte de troca de telas/fases acontece nesse metodo
    game_state.state_manager()

    if pygame.key.get_pressed()[pygame.K_ESCAPE] and game_state.state == 'main_menu':
        rodando = False

    clock.tick(120)

pygame.quit()