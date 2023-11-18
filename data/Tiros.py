import pygame
import Explosao

class Tiros(pygame.sprite.Sprite):
    def __init__(self, x, y, jogador, limitex, limitey):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/tiro.png"), (20,20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.jogador = jogador
        self.limitey = limitey
        self.limitex = limitex

    def update(self):
        self.rect.x = self.rect.x + 5 if self.jogador else self.rect.x - 5

        #Se o tiro sair da tela, remover ele do grupo de tiros e do jogo
        # if (0 < self.rect.x > self.limitex) or (0 < self.rect.y > self.limitey):
        #     self.kill()

        # if self.jogador and pygame.sprite.spritecollide(self, self.piratas_group, True):
        #     self.nave.combustivel_restante += 10
        #     self.kill()
        #     explosao = Explosao(self.rect.centerx, self.rect.centery)
        #     self.explosao_group.add(explosao)

        # if not self.jogador and pygame.sprite.spritecollide(self, self.naves_group, False, pygame.sprite.collide_mask):
        #     self.nave.combustivel_restante -= 10
        #     self.kill()