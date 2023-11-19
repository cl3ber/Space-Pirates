from data.Inimigos import Inimigos

class Piratas(Inimigos):
    def __init__(self, x, y, limiteAltura, limiteLargura, tirosGroup):
        super().__init__(x, y, limiteAltura, limiteLargura, tirosGroup, "./assets/barco_boss.png", 120)
