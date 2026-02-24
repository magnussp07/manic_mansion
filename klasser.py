from constants import *
import pygame as pg
from pathlib import Path

class SpillObjekt:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Spokelse(SpillObjekt):
    def __init__(self, x:int, y: int) -> None:
        super().__init__(x, y)
        self.vx = 2              # evt sende med tilfeldig fart x- og y-retning 
        self.vy = 2

        bildesti = Path(__file__).parent / "bilder" / "spokelse.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 120))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def oppdater(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    
        if self.rect.right > GRENSE_H or self.rect.left < GRENSE_V:
            self.vx *= -1        
        if self.rect.bottom > VINDU_HOYDE or self.rect.top < 0:
            self.vy *= -1
    
    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)
        

class Spiller(SpillObjekt):
    pass

class Hindring(SpillObjekt):
    pass

class Sau(SpillObjekt):
    pass