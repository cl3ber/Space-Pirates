import math
import random
from random import randint
from typing import Any
import pygame
from pygame.sprite import Group, AbstractGroup
import os
from data.Nave import Navinha
from data.Tiros import Tiros
from data.Piratas import Piratas
from data.Explosao import Explosao
from data.Scoreboard import ScoreBoard

pygame.init()

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
        RECARGA = 500
        #condições de vitória/derrota
        if navinha.combustivel_restante < 0:
            self.state = 'game_over'
        if pygame.key.get_pressed()[pygame.K_LSHIFT] and navinha.combustivel_restante == navinha.combustivel_maximo:
            self.state = 'win'

        if pygame.key.get_pressed()[pygame.K_SPACE] and pygame.time.get_ticks() - navinha.ultimo_tiro > RECARGA:
            tiros_group.add(Tiros(navinha.rect.centerx, navinha.rect.top, True, ALTURA_TELA, LARGURA_TELA))
            navinha.ultimo_tiro = pygame.time.get_ticks()

        colisoes_jogador = pygame.sprite.groupcollide(tiros_group, piratas_group, True, True)
        for pirata, tiro in colisoes_jogador.items():
            navinha.combustivel_restante+=100
            explosao_group.add(Explosao(pirata.rect.centerx, pirata.rect.centery))

        colisoes_piratas = pygame.sprite.groupcollide(tiros_piratas_group, naves_group, True, False)
        for nave, tiro in colisoes_piratas.items():
            navinha.combustivel_restante-=10

        pygame.draw.rect(tela, (255,0,0), (0, (ALTURA_TELA - 10), LARGURA_TELA, 15))
        if navinha.combustivel_restante > 0:
            pygame.draw.rect(tela, (0,255,0), (0, (ALTURA_TELA  - 10), int(LARGURA_TELA * (navinha.combustivel_restante / navinha.combustivel_base)), 15))

        scoreBoard_group.add(ScoreBoard(ALTURA_TELA - 100, LARGURA_TELA - 100))

        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()
        tiros_piratas_group.update()
        scoreBoard_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        tiros_piratas_group.draw(tela)
        scoreBoard_group.draw(tela)

        pygame.display.update()

    def game_over(self):

        #Criando uma variavel que ira verificar se o usuario continuara jogando ou voltara pro menu
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.selected_index = 0
        elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.selected_index = 1
        
        #Desenhando imagem de game over + retry
        game_over = pygame.image.load("./assets/game_over.png").convert()
        retry = pygame.image.load("./assets/retry.png").convert()
        yes = pygame.image.load("./assets/yes.png").convert()
        no = pygame.image.load("./assets/no.png").convert()
        pick = pygame.image.load("./assets/pick.png").convert()
        tela.blit(game_over, (LARGURA_TELA/2-199, ALTURA_TELA/2-33))
        tela.blit(retry, (LARGURA_TELA/2-66, 600))
        tela.blit(yes, (LARGURA_TELA/2-120, 650))
        tela.blit(no, (LARGURA_TELA/2+60, 650))

        if self.selected_index == 0:
            tela.blit(pick, (LARGURA_TELA/2-150, 650))
        elif self.selected_index == 1:
            tela.blit(pick, (LARGURA_TELA/2+30, 650))

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if self.selected_index == 0:
                reset()
                self.state = 'jogo'
            else:
                reset()
                self.state = 'main_menu'

        pygame.display.update()

    def win(self):
        pygame.display.update()

    def change_level(self, level):
        tela.fill((0,0,0))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level {level}", True, (255,255,255))
        tela.blit(text, (LARGURA_TELA // 2 - text.get_width() // 2, ALTURA_TELA // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1500)  # Aguarda 2 segundos (ajuste conforme necessário)
        pygame.display.flip()
        self.state = 'jogo'

    def animacao(self):
        piratas_group.empty()
        tiros_group.empty()
        explosao_group.empty()
        tiros_piratas_group.empty()
        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()
        tiros_piratas_group.update()
        scoreBoard_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        tiros_piratas_group.draw(tela)
        scoreBoard_group.draw(tela)

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
        if self.state == 'animacao':
            self.animacao()
        if self.state == 'change_level':
            self.change_level(0)


def paralax(scroll):
    #desenhando o fundo
    for i in range(0, tiles):
        tela.blit(fundo, (i * largura_fundo + scroll, 0))

def criar_piratas(altura, largura):
        piratas_group.add(Piratas(altura, 100 + largura * 70, ALTURA_TELA, LARGURA_TELA, tiros_piratas_group))

def reset():
    navinha.combustivel_restante = 0
    piratas_group.empty()
    tiros_group.empty()
    explosao_group.empty()
    tiros_piratas_group.empty()
    scoreBoard_group.empty()
    navinha.rect.center = [60, ALTURA_TELA/2]

clock = pygame.time.Clock()
LARGURA_TELA = 1280
ALTURA_TELA = 800
game_state = GameState()

#criando a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
fundo = pygame.image.load("./assets/background2.png").convert()
altura_fundo = fundo.get_height()
largura_fundo = fundo.get_width()
limite_fundo = fundo.get_rect()

#Variáveis do jogo
tiles = math.ceil(ALTURA_TELA / altura_fundo) + 1
scroll_tela = 0

#Criando um grupo de sprites pra facilitar a inclusão deles na tela
scoreBoard_group = pygame.sprite.Group()
naves_group = pygame.sprite.Group()
tiros_group = pygame.sprite.Group()
piratas_group = pygame.sprite.Group()
tiros_piratas_group = pygame.sprite.Group()
explosao_group = pygame.sprite.Group()

#navinha
navinha = Navinha(60, ALTURA_TELA/2, 100, tiros_group, ALTURA_TELA, LARGURA_TELA)

naves_group.add(navinha)

rodando = True

delay_piratas = 2000
respawn = pygame.time.get_ticks()
animacao_fim = 0

while rodando:
    paralax(scroll_tela)
    
    scroll_tela = 0 if abs(scroll_tela) > largura_fundo else scroll_tela-1

    #Mudei essa parte do codigo pros piratas so spawnarem quando o jogo estiver rodando
    if pygame.time.get_ticks() - respawn > delay_piratas and len(piratas_group.sprites()) < 5 and game_state.state == 'jogo':
            criar_piratas(LARGURA_TELA, random.randint(1,6))
            respawn = pygame.time.get_ticks()

    #Esse for captura todos os eventos que o pygame está executando, inclusive inputs
    for event in pygame.event.get():
        rodando = event.type != pygame.QUIT

    #Toda a parte de troca de telas/fases acontece nesse metodo
    game_state.state_manager()

    if pygame.key.get_pressed()[pygame.K_ESCAPE] and game_state.state == 'main_menu':
        rodando = False

    if game_state.state == 'win':
        animacao_fim = pygame.time.get_ticks()
        game_state.state = 'animacao'

    if game_state.state == 'animacao' and pygame.time.get_ticks() - animacao_fim > 5000:
        game_state.state = 'change_level'
    elif game_state.state == 'animacao':
        scroll_tela -= (pygame.time.get_ticks() - animacao_fim) / 200

    clock.tick(120)

pygame.quit()