from constants import *
import pygame as pg
from pathlib import Path
from random import randint


class Spillbrett:
    def __init__(self) -> None:
        self.running = True
        
        # Må legge inn tilfeldige posisjoner som ikke overlapper 
        self.spokelser = [Spokelse(200, 300), Spokelse(400, 100)]
        self.sauer = [Sau(800, 50), Sau(800, 200), Sau(800, 350)]
        self.hindringer = [Hindring(180, 150), Hindring(580, 280), Hindring(420, 400)]
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))


    def oppdater(self):
        self.spiller.oppdater()
        
        # Sjekker om spillet er ferdig
       # if self.spiller.sjekkKollisjonSauer(self.sauer) or self.spiller.sjekkKollisjonSpokelse(self.spokelser):
        #    self.running = False

        # Sjekker kollisjon med sauer, hvis bonde ikke har hentet sau enda
        if self.spiller.status == False:
            self.spiller.sjekkKollisjonSauer(self.sauer)
        
        # Oppdaterer spøkelser
        for s in self.spokelser:
            s.oppdater()

        # Oppdaterer sau, sjekker om hentet sau har kommet over til målområde
        for a in self.sauer:
            a.oppdater(self.spiller)
            if a.sjekkPos() == True:
                self.sauer.remove(a)
                self.spiller.poeng +=1
                self.spiller.status = False
                self.sauer.append(Sau(800, 50))
    
    def tegn(self, vindu):

        # Tegner bakgrunn
        vindu.fill(WHITE)
        pg.draw.rect(vindu, LIGHT_GREEN, pg.Rect(0, 0, GRENSE_V, VINDU_HOYDE))
        pg.draw.rect(vindu, LIGHT_GREEN, pg.Rect(VINDU_BREDDE-GRENSE_V, 0, GRENSE_V, VINDU_HOYDE))
        
        # Tegner spiller, sauer, spøkelse og hindringer
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



class Spokelse(SpillObjekt):
    def tilfeldigFartSpøkelse(self):
        return randint(1,4)
    
    def __init__(self, x:int, y: int) -> None:
        super().__init__(x, y)
        self.vx = self.tilfeldigFartSpøkelse()       #evt dele på 2, eller bare sette lik fast tall
        self.vy = self.tilfeldigFartSpøkelse() 

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