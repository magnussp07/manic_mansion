import pygame as pg
from constants import *
from klasser2 import *
from spillbrett import Spillbrett

vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

spillbrett = Spillbrett()

while spillbrett.running:
    spillbrett.events()
    spillbrett.oppdater()
    spillbrett.tegn(vindu)
    spillbrett.tegntekst(vindu)


    pg.display.flip()
    clock.tick(FPS)

pg.quit()
