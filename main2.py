import pygame as pg
from constants import *
from klasser import *

pg.init()
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

spillbrett = Spillbrett()
while spillbrett.running:
    spillbrett.events()
    spillbrett.oppdater()
    spillbrett.tegn(vindu)


    pg.display.flip()
    clock.tick(FPS)

pg.quit()
