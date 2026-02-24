import pygame as pg

from constants import *
from klasser import *


pg.init()
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

running = True


spokelser = [Spokelse(200, 300), Spokelse(400, 100)]

while running:
    
    vindu.fill(WHITE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for s in spokelser:
        s.oppdater()
        s.tegn()
        
   
    pg.display.flip()
    clock.tick(FPS)

pg.quit()