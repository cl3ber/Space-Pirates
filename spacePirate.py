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
from data.Marinha import Marinha
from data.Capitao import Capitao
from data.Almirante import Almirante
from data.Explosao import Explosao
from data.Scoreboard import ScoreBoard

pygame.init()

class GameState():
    def __init__(self):
        self.state = 'main_menu'
        self.fase = 2   
        self.selected_index = 0
        self.respawn = pygame.time.get_ticks()

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

        self.estagios()
        #condições de vitória/derrota
        if navinha.combustivel_restante < 0:
            self.state = 'game_over'
        if navinha.combustivel_restante == navinha.combustivel_maximo:
            self.state = 'win'

        if pygame.key.get_pressed()[pygame.K_SPACE] and pygame.time.get_ticks() - navinha.ultimo_tiro > RECARGA:
            tiros_group.add(Tiros(navinha.rect.centerx, navinha.rect.top, True, LARGURA_TELA+navinha.rect.centerx, ALTURA_TELA+navinha.rect.centery))
            navinha.ultimo_tiro = pygame.time.get_ticks()

        colisoes_jogador = pygame.sprite.groupcollide(tiros_group, piratas_group, True, True, pygame.sprite.collide_mask)
        for pirata, tiro in colisoes_jogador.items():
            navinha.combustivel_restante+=5
            explosao_group.add(Explosao(pirata.rect.centerx, pirata.rect.centery))

        colisaoJogadorChefe = pygame.sprite.groupcollide(chefes_group, tiros_group, False, True, pygame.sprite.collide_mask)
        for pirata, tiro in colisaoJogadorChefe.items():
            pirata.combustivel_restante-=5
            navinha.combustivel_restante+=5
            if pirata.combustivel_restante <= 0:
                pirata.kill()
                explosao_group.add(Explosao(pirata.rect.centerx, pirata.rect.centery))

        colisaoChefeJogador = pygame.sprite.groupcollide(tiros_chefe_group, naves_group, True, False, pygame.sprite.collide_mask)
        for nave, tiro in colisaoChefeJogador.items():
            navinha.combustivel_restante-=5
            for chefe in chefes_group:
                chefe.combustivel_restante+=5

        colisoes_piratas = pygame.sprite.groupcollide(tiros_piratas_group, naves_group, True, False, pygame.sprite.collide_mask)
        for nave, tiro in colisoes_piratas.items():
            navinha.combustivel_restante-=2*ACTUAL_LEVEL

        pygame.draw.rect(tela, (255,0,0), (0, (ALTURA_TELA - 10), LARGURA_TELA, 15))
        if navinha.combustivel_restante > 0:
            pygame.draw.rect(tela, (0,255,0), (0, (ALTURA_TELA  - 10), int(LARGURA_TELA * (navinha.combustivel_restante / navinha.combustivel_base)), 15))

        for tiro in tiros_group:
            if (tiro.rect.x < 0 or tiro.rect.x >= LARGURA_TELA) or (tiro.rect.y < 0 or tiro.rect.y >= ALTURA_TELA):
                tiros_group.remove(tiro)

        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()
        tiros_piratas_group.update()
        scoreBoard_group.update()
        chefes_group.update()
        tiros_chefe_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        tiros_piratas_group.draw(tela)
        scoreBoard_group.draw(tela)
        chefes_group.draw(tela)
        tiros_chefe_group.draw(tela)

        pygame.display.update()

    def estagios(self):
        match ACTUAL_LEVEL:
            case 1:
                if pygame.time.get_ticks() - self.respawn > RESPAWN_DELAY and len(piratas_group.sprites()) < 5 and game_state.state == 'jogo':
                    piratas_group.add(Piratas(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_piratas_group))
                    self.respawn = pygame.time.get_ticks()
            case 2:
                if pygame.time.get_ticks() - self.respawn > RESPAWN_DELAY and len(piratas_group.sprites()) < 5 and game_state.state == 'jogo':
                    piratas_group.add(Marinha(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_piratas_group))
                    self.respawn = pygame.time.get_ticks()
            case 3:
                if pygame.time.get_ticks() - self.respawn > RESPAWN_DELAY and len(chefes_group.sprites()) < 1 and game_state.state == 'jogo' and navinha.combustivel_restante < navinha.combustivel_maximo:
                    chefes_group.add(Capitao(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_chefe_group, tela))
                    self.respawn = pygame.time.get_ticks()
            case 4:
                if pygame.time.get_ticks() - self.respawn > RESPAWN_DELAY and len(piratas_group.sprites()) < 6 and game_state.state == 'jogo':
                    if random.randint(1,2) % 2 == 0:
                        piratas_group.add(Marinha(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_piratas_group))
                    else:
                        piratas_group.add(Piratas(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_piratas_group))
                    self.respawn = pygame.time.get_ticks()
            case 5:
                if pygame.time.get_ticks() - self.respawn > RESPAWN_DELAY and len(chefes_group.sprites()) < 1 and game_state.state == 'jogo' and navinha.combustivel_restante < navinha.combustivel_maximo:
                    chefes_group.add(Almirante(LARGURA_TELA, 100 + random.randint(1,2) * 70, LARGURA_TELA, ALTURA_TELA, tiros_chefe_group, tela))
                    self.respawn = pygame.time.get_ticks()
            case _:
                self.state = 'credits'
                self.credits()

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
        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()
        tiros_piratas_group.update()
        scoreBoard_group.update()
        chefes_group.update()
        tiros_chefe_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        tiros_piratas_group.draw(tela)
        scoreBoard_group.draw(tela)
        chefes_group.draw(tela)
        tiros_chefe_group.draw(tela)
        pygame.display.update()

    def change_level(self, level):
        tela.fill((0,0,0))
        if ACTUAL_LEVEL < 6:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Level {level}", True, (255,255,255))
            tela.blit(text, (LARGURA_TELA // 2 - text.get_width() // 2, ALTURA_TELA // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(1500)  # Aguarda 2 segundos (ajuste conforme necessário)
            pygame.display.flip()
            self.state = 'jogo'
            navinha.combustivel_restante = 0
        else:
            self.state = 'credits'

    def animacao(self):
        piratas_group.empty()
        tiros_group.empty()
        explosao_group.empty()
        tiros_piratas_group.empty()
        tiros_chefe_group.empty()
        chefes_group.empty()
        naves_group.update()
        tiros_group.update()
        explosao_group.update()
        piratas_group.update()
        tiros_piratas_group.update()
        scoreBoard_group.update()
        tiros_chefe_group.update()
        chefes_group.update()

        naves_group.draw(tela)
        tiros_group.draw(tela)
        piratas_group.draw(tela)
        explosao_group.draw(tela)
        tiros_piratas_group.draw(tela)
        scoreBoard_group.draw(tela)
        tiros_chefe_group.draw(tela)
        chefes_group.draw(tela)

        pygame.display.update()

    def credits(self):
        creditos = ["SPACE PIRATES - Pensado e criado por:",
                    " ",
                    "Organização do time, documentação e controle", 
                    "Arielson Alves de Santana",
                    " ",
                    "Conceitos, Artes e Animações",
                    "Rafael Oliveira da Silva",
                    "Arthur de Oliveira Albiol Maróstica", 
                    " ",
                    "Desenvolvimento,  padrões de código e testes",
                    "Gustavo Henrique de Souza Sales",
                    "Cleber de Jesus Silva", 
                    "", 
                    "",
                    "",
                    "",
                    "Obrigado por jogar"]
        textos = []
        font = pygame.font.SysFont("Arial", 40)

        for indice, linha in enumerate(creditos):
            superfice = font.render(linha, 1, (255, 255, 255))
            rect = superfice.get_rect(centerx=tela.get_rect().centerx, y=tela.get_rect().bottom + indice * 45)
            textos.append((rect, superfice))
        
        
        while self.state == 'credits':
            for e in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    None

            tela.blit(fundo, (0, 0))
            pirataimage = pygame.image.load("./assets/GameLogo2.png").convert_alpha()
            tela.blit(pirataimage, (LARGURA_TELA-415, 225))
            for r, s in textos:
                r.move_ip(0, -1)
                tela.blit(s, r)

            if not tela.get_rect().collidelistall([r for (r, _) in textos]):
                tela.fill((0,0,0))
                self.state = 'main_menu'

            pygame.display.flip()
            clock.tick(120)
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
            self.change_level(ACTUAL_LEVEL)
        if self.state == 'credits':
            self.credits()

def paralax(scroll):
    #desenhando o fundo
    for i in range(0, tiles):
        tela.blit(fundo, (i * largura_fundo + scroll, 0))

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

ACTUAL_LEVEL = 1
RODANDO = True
RESPAWN_DELAY = 2000
CUTSCENCE_TIMER = 0
SCROLL_TELA = 0
RESPAWN = pygame.time.get_ticks()
game_state = GameState()

#criando a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
fundo = pygame.image.load("./assets/background2.png").convert()
altura_fundo = fundo.get_height()
largura_fundo = fundo.get_width()
limite_fundo = fundo.get_rect()

#Variáveis do jogo
tiles = math.ceil(ALTURA_TELA / altura_fundo) + 1


#Criando um grupo de sprites pra facilitar a inclusão deles na tela
scoreBoard_group = pygame.sprite.Group()
naves_group = pygame.sprite.Group()
tiros_group = pygame.sprite.Group()
piratas_group = pygame.sprite.Group()
tiros_piratas_group = pygame.sprite.Group()
tiros_chefe_group = pygame.sprite.Group()
explosao_group = pygame.sprite.Group()
chefes_group = pygame.sprite.Group()

#navinha
navinha = Navinha(60, ALTURA_TELA/2, 100, tiros_group, ALTURA_TELA, LARGURA_TELA)

naves_group.add(navinha)



while RODANDO:
    paralax(SCROLL_TELA)
    
    SCROLL_TELA = 0 if abs(SCROLL_TELA) > largura_fundo else SCROLL_TELA-1
    #Esse for captura todos os eventos que o pygame está executando, inclusive inputs
    for event in pygame.event.get():
        RODANDO = event.type != pygame.QUIT

    #Toda a parte de troca de telas/fases acontece nesse metodo
    game_state.state_manager()

    if pygame.key.get_pressed()[pygame.K_ESCAPE] and game_state.state == 'main_menu':
        RODANDO = False

    if game_state.state == 'win':
        CUTSCENCE_TIMER = pygame.time.get_ticks() if CUTSCENCE_TIMER == 0 else CUTSCENCE_TIMER
        if game_state.state == 'win' and pygame.time.get_ticks() - CUTSCENCE_TIMER > 2000:
            CUTSCENCE_TIMER = pygame.time.get_ticks()
            game_state.state = 'animacao'
            ACTUAL_LEVEL += 1

    if game_state.state == 'animacao' and pygame.time.get_ticks() - CUTSCENCE_TIMER > 5000:
        game_state.state = 'change_level'
        CUTSCENCE_TIMER = 0
    elif game_state.state == 'animacao':
        SCROLL_TELA -= (pygame.time.get_ticks() - CUTSCENCE_TIMER) / 200

    clock.tick(120)

pygame.quit()