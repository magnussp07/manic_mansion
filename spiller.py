from klasser import SpillObjekt
import pygame as pg
from pathlib import Path

class Spiller(SpillObjekt):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.fart = 6


        bildesti = Path(__file__).parent / "bilder" / "spiller.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 120))
        
        self.rect = self.image.get_rect()
        
        self.opp = False
        self.ned = False
        self.venstre = False
        self.hoyre = False

    def oppdater(self):
        if self.opp:
            self.rect.y -= self.fart
        if self.ned:
            self.rect.y += self.fart
        if self.hoyre:
            self.rect.x += self.fart
            
        if self.venstre:
            self.rect.x -= self.fart
            
    

    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)