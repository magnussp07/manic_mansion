from __future__ import annotations
from constants import *
import pygame as pg
from pathlib import Path
from random import randint
import math as math
     




class SpillObjekt:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y



class Spokelse(SpillObjekt):
    def __init__(self, x:int, y: int) -> None:
        super().__init__(x, y)
        self.vx = randint(1,4)      
        self.vy = randint(1,4) 

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
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.fart = 6
        self.status = False
        self.poeng = 0


        bildesti = Path(__file__).parent / "bilder" / "spiller.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 120))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x  #FORSKJELL
        self.rect.centery = y     #FORSKJELL
        
        self.opp = False
        self.ned = False
        self.venstre = False
        self.hoyre = False

    def sjekkKollisjonSauer(self, sauer):
        for sau in sauer:
          if self.rect.colliderect(sau.rect):
            if self.status == False:
                sau.hentet = True
                self.status = True
            else: 
                return True
            
    
    def sjekkKollisjonSpokelse(self, spokelser):
        for spokelse in spokelser:
          if self.rect.colliderect(spokelse.rect):
              return True

    def oppdater(self):
        if self.status == True:
            self.fart = 3
            if self.rect.right < GRENSE_V:
                self.status = False
        else: 
            self.fart = 5

        if self.opp and self.rect.top > 0:
            self.rect.y -= self.fart
        if self.ned and self.rect.bottom < VINDU_HOYDE:
            self.rect.y += self.fart
        if self.hoyre and self.rect.right <= VINDU_BREDDE:
            self.rect.x += self.fart
            
        if self.venstre and self.rect.left >= 0:
            self.rect.x -= self.fart
        

    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)



class Hindring(SpillObjekt):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)

        bildesti = Path(__file__).parent / "bilder" / "gravstein.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (90, 90))
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    
    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)



class Sau(SpillObjekt):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self.hentet = False

        bildesti = Path(__file__).parent / "bilder" / "sau2.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 100))
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    
    def sjekkPos(self):
        if self.rect.centerx < GRENSE_V:
            return True

    
    def oppdater(self, spiller:Spiller):
        if self.hentet == True:
            self.image = pg.transform.smoothscale(self.image, (40, 55))
            self.rect.centery = spiller.rect.bottom
            self.rect.left = spiller.rect.right + 10
        else:
            self.rect.x = self.x
            self.rect.y = self.y
        
    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)

pg.init()
# Angir hvilken skrifttype og tekststørrelse vi vil bruke på tekst
font = pg.font.SysFont("Tahoma", 24)

class Knapp:
  def __init__(self, xPosisjon, yPosisjon, tekst):
    self.xPosisjon = xPosisjon
    self.yPosisjon = yPosisjon
    self.bredde = len(tekst) * 20
    self.hoyde = 60
    self.tekst = tekst
    self.rect = pg.Rect(
      self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde
    )
    self.farge =  BLACK

  def tegn(self, vindu):
    pg.draw.rect(vindu, self.farge, self.rect, 4)
    tekst = font.render(self.tekst, True, BLACK)
    tekstRamme = tekst.get_rect(center=self.rect.center)
    vindu.blit(tekst, tekstRamme.topleft)