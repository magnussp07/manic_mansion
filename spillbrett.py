from __future__ import annotations
from constants import *
import pygame as pg
from pathlib import Path
from random import randint
import math as math
from klasser2 import *

class Spillbrett:
    def __init__(self) -> None:
        self.running = True
        self.levende = True
        
        # Må legge inn tilfeldige posisjoner som ikke overlapper 
        self.genererKordinater()
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))
        self.knapp = Knapp(VINDU_BREDDE/2 - 70, VINDU_HOYDE/2 + 100, "Restart")

    def sjekkAvstand(self, x1:int, y1:int, x2:int, y2:int):
        return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)


    def genererKordinater(self):
        
        def lag_pos(antall:int, min_x:int, max_x:int, min_y:int, max_y:int, bredde:int, hoyde:int):
            posisjoner:list[list[int]] = []

            while len(posisjoner) < antall:
                nyx = randint(min_x, max_x - bredde)
                nyy = randint(min_y, max_y - hoyde)

                ok = True

                for (x, y) in posisjoner:
                    if self.sjekkAvstand(x, y, nyx, nyy) < 120:
                        ok = False
                        break

                if ok:
                    posisjoner.append([nyx, nyy])

            return posisjoner

        h_pos = lag_pos(3, GRENSE_V, GRENSE_H, 0, VINDU_HOYDE, 90, 120)
        sau_pos = lag_pos(3, GRENSE_H, VINDU_BREDDE, 0, VINDU_HOYDE, 80, 100)
    

        self.spokelser = [self.nyttSpokelse()]
        self.hindringer = [Hindring(h_pos[0][0], h_pos[0][1]), Hindring(h_pos[1][0], h_pos[1][1]), Hindring(h_pos[2][0], h_pos[2][1])]
        self.sauer = [Sau(sau_pos[0][0], sau_pos[0][1]), Sau(sau_pos[1][0], sau_pos[1][1]), Sau(sau_pos[2][0], sau_pos[2][1])]

        return self.sauer, self.hindringer, self.spokelser
    
    def nyttSpokelse(self):
        return Spokelse(randint(GRENSE_V, GRENSE_H-80), randint(0, VINDU_HOYDE))
    
    def restart(self): #FORSKJELL
        """Restarter spillet"""
        self.levende = True
        self.genererKordinater()
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))

    def oppdater(self):
        if self.levende:
            self.spiller.oppdater()
            
            # Sjekker om spillet er ferdig
            if self.spiller.sjekkKollisjonSauer(self.sauer) or self.spiller.sjekkKollisjonSpokelse(self.spokelser):
                self.levende = False

            # Sjekker kollisjon med sauer, hvis bonde ikke har hentet sau enda
            if self.spiller.status == False:
                self.spiller.sjekkKollisjonSauer(self.sauer)

            if self.spiller.sjekkKollisjonHinder(self.hindringer):
                pass
            
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
    
    def tegn(self, vindu:pg.Surface):
# Tegner bakgrunn
        vindu.fill(WHITE)

        if self.levende:
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
        else: self.knapp.tegn(vindu)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.spiller.opp = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.spiller.ned = True
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.spiller.venstre = True
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.spiller.hoyre = True
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.spiller.opp = False
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.spiller.ned = False
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.spiller.venstre = False
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.spiller.hoyre = False
            
            elif event.type == pg.MOUSEBUTTONDOWN: #forskjell
                x_pos, y_pos = event.pos
                if self.knapp.rect.collidepoint( (x_pos, y_pos) ):
                    print(f"Klikket på: {self.knapp.tekst}")
                    self.restart()

    def tegntekst(self, vindu:pg.Surface): #FORSKJELL
        font = pg.font.SysFont("Tahoma", FONT_SIZE)
        if self.levende:
            text_surface = font.render("Score: " + str(self.spiller.poeng), True, BLACK)
            vindu.blit(text_surface, (600, 80))
        else:
            font = pg.font.SysFont("Tahoma", FONT_SIZE+20)
            text_surface = font.render("Din poengscore ble: " + str(self.spiller.poeng), True, BLACK, WHITE)
            vindu.blit(text_surface, (195, VINDU_HOYDE/2-70))