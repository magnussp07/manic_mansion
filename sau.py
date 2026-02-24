from klasser import SpillObjekt
from spiller import Spiller
import pygame as pg
from pathlib import Path

class Sau(SpillObjekt):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)

        bildesti = Path(__file__).parent / "bilder" / "sau.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 120))
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.hentet = False
    
    def oppdater(self, spiller:Spiller):
        if self.hentet == True:
            self.rect.bottomleft = spiller.rect.bottomright
        else:
            self.rect.x = self.x
            self.rect.y = self.y
        
    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)


# Helt enkel funksjon som kan legges inn hos spiller, funker at spiller tar med seg sau
"""def sjekkKollisjonSauer(self, sauer):
        for sau in sauer:
          if self.rect.colliderect(sau.rect):
            sau.hentet = True"""