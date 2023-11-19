import pygame
from data.Sprites import SpriteSheet
from data.Inimigos import Inimigos

class Marinha(Inimigos):
    def __init__(self, x, y, limiteAltura, limiteLargura, tirosGroup):
        super().__init__(x, y, limiteAltura, limiteLargura, tirosGroup, "./assets/boss_barco_marinha.png", 120)