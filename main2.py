import pygame as pg
from constants import *
from klasser2 import *

pg.init()
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

font_path = 'fonts/Pixeltype.ttf'
font = pg.font.SysFont(font_path, FONT_SIZE)

spillbrett = Spillbrett()
while spillbrett.running:
    spillbrett.events()
    spillbrett.oppdater()
    spillbrett.tegn(vindu)

    text_surface = font.render("Score: " + str(spillbrett.spiller.poeng), True, BLACK)
    vindu.blit(text_surface, (600, 80))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
