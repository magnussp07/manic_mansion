import pygame as pg
from constants import *

pg.init()
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

running = True

while running:
    
    vindu.fill(WHITE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
   
    pg.display.flip()
    clock.tick(FPS)

pg.quit()