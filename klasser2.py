from constants import *
import pygame as pg
from pathlib import Path
from random import randint


class Spillbrett:
    def __init__(self) -> None:
        self.running = True

        self.spokelser = [Spokelse(200, 300), Spokelse(400, 100)]
        self.sauer = [Sau(800, 50), Sau(800, 200), Sau(800, 350)]
        self.hindringer = [Hindring(180, 150), Hindring(580, 280), Hindring(420, 400)]
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))

    def oppdater(self):
        if self.spiller.status:
            pass
        self.spiller.oppdater()
        self.spiller.sjekkKollisjonSauer(self.sauer)

        for s in self.spokelser:
            s.oppdater()

        for a in self.sauer:
            a.oppdater(self.spiller)
    
    def tegn(self, vindu):
        vindu.fill(WHITE)
        pg.draw.rect(vindu, LIGHT_GREEN, pg.Rect(0, 0, GRENSE_V, VINDU_HOYDE))
        pg.draw.rect(vindu, LIGHT_GREEN, pg.Rect(VINDU_BREDDE-GRENSE_V, 0, GRENSE_V, VINDU_HOYDE))
        self.spiller.tegn(vindu)

        

        for a in self.sauer:
            a.tegn(vindu)
        
        for h in self.hindringer:
            h.tegn(vindu)

        for s in self.spokelser:
            s.tegn(vindu)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.spiller.opp = True
                if event.key == pg.K_s:
                    self.spiller.ned = True
                if event.key == pg.K_a:
                    self.spiller.venstre = True
                if event.key == pg.K_d:
                    self.spiller.hoyre = True
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.spiller.opp = False
                if event.key == pg.K_s:
                    self.spiller.ned = False
                if event.key == pg.K_a:
                    self.spiller.venstre = False
                if event.key == pg.K_d:
                    self.spiller.hoyre = False
                    




class SpillObjekt:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y


def tilfeldigFartSpøkelse():
    return randint(1,4)

class Spokelse(SpillObjekt):
    def __init__(self, x:int, y: int) -> None:
        super().__init__(x, y)
        self.vx = tilfeldigFartSpøkelse()       #evt dele på 2, eller bare sette lik fast tall
        self.vy = tilfeldigFartSpøkelse() 

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


        bildesti = Path(__file__).parent / "bilder" / "spiller.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (80, 120))
        
        self.rect = self.image.get_rect()
        
        self.opp = False
        self.ned = False
        self.venstre = False
        self.hoyre = False

    def sjekkKollisjonSauer(self, sauer):
        for sau in sauer:
          if self.rect.colliderect(sau.rect):
            sau.hentet = True
            self.status = True

    def oppdater(self):
        if self.status == True:
            self.fart = 3
            if self.rect.right < GRENSE_V:
                self.status = False

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

class Hindring(SpillObjekt):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)

        bildesti = Path(__file__).parent / "bilder" / "gravstein.png"
        self.image = pg.image.load(bildesti).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (70, 70))
        
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

    
    def oppdater(self, spiller:Spiller):
        if self.hentet == True:
            self.rect.bottomleft = spiller.rect.bottomright
            self.image = pg.transform.smoothscale(self.image, (40, 55))
        else:
            self.rect.x = self.x
            self.rect.y = self.y
        
    def tegn(self, vindu:pg.Surface):
        vindu.blit(self.image, self.rect)