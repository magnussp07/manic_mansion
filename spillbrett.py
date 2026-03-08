from __future__ import annotations
from constants import *
import pygame as pg
from random import randint
import math as math
from klasser2 import *

class Spillbrett:
    def __init__(self) -> None:
        self.running = True
        self.levende = True
        
        self.genererKordinater()
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))
        self.knapp = Knapp(VINDU_BREDDE/2 - 70, VINDU_HOYDE/2 + 100, "Restart")

    def genererKordinater(self):
        
        self.spokelser = [self.nyttSpokelse()]
        self.hindringer = [self.nyHindring()]
        self.sauer = [self.nySau()]

        for _ in range(2):
            self.hindringer.append(self.leggTilNyttObjekt(self.hindringer, Hindring))
            self.sauer.append(self.leggTilNyttObjekt(self.sauer, Sau))

        return self.sauer, self.hindringer, self.spokelser
    
    def nyttSpokelse(self):
        return Spokelse(randint(GRENSE_V, GRENSE_H-80), randint(0, VINDU_HOYDE-120))
    
    def nyHindring(self):
        return Hindring(randint(GRENSE_V, GRENSE_H-60), randint(0, VINDU_HOYDE-60))
    
    def nySau(self):
        return Sau(randint(GRENSE_H, VINDU_BREDDE-80), randint(0, VINDU_HOYDE-100))
    
    #lager nytt objekt som ikke kolliderer med noen av de tidligere objektene i lista
    def leggTilNyttObjekt(self, gamle:list[SpillObjekt], type: type[SpillObjekt]):
        while True:
            if type == Sau:
                ny = type(randint(GRENSE_H, VINDU_BREDDE-80), randint(0, VINDU_HOYDE-100))
            elif type == Hindring:
                ny = self.nyHindring()
            elif type == Spokelse:
                ny = self.nyttSpokelse()


            kollisjon = False

            for obj in gamle:
                if ny.rect.colliderect(obj.rect):
                    kollisjon = True
                    break

            if kollisjon == False:
                return ny
    
    def restart(self): 
        self.levende = True
        self.genererKordinater()
        self.spiller = Spiller(50, int(VINDU_HOYDE/2))

    def oppdater(self):
        if self.levende:
            self.spiller.oppdater(self.hindringer)
            
            # Sjekker om spillet er ferdig
            if self.spiller.sjekkKollisjonSauer(self.sauer) or self.spiller.sjekkKollisjonSpokelse(self.spokelser):
                self.levende = False

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

                    #x, y = self.tilfeldig_sau()
                    #self.nySau = Sau(x, y)
                    #self.sauer.append(self.nySau)

                    self.spokelser.append(self.leggTilNyttObjekt(self.spokelser, Spokelse))
                    self.hindringer.append(self.leggTilNyttObjekt(self.hindringer, Hindring))
                    self.sauer.append(self.leggTilNyttObjekt(self.sauer, Sau))

    
    def tegn(self, vindu:pg.Surface):
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

    def tegntekst(self, vindu:pg.Surface): 
        font = pg.font.SysFont("Tahoma", FONT_SIZE)
        if self.levende:
            text_surface = font.render("Score: " + str(self.spiller.poeng), True, BLACK)
            vindu.blit(text_surface, (600, 80))
        else:
            font = pg.font.SysFont("Tahoma", FONT_SIZE+20)
            text_surface = font.render("Din poengscore ble: " + str(self.spiller.poeng), True, BLACK, WHITE)
            vindu.blit(text_surface, (195, VINDU_HOYDE/2-70))